
import streamlit as st
import requests
import pandas as pd
import os

# URL вашего локального Flask API
# Автоматически определяем URL для Codespaces
if os.getenv("CODESPACES") == "true":
    codespace_name = os.getenv("CODESPACE_NAME")
    forwarding_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    API_URL = f"https://{codespace_name}-5000.{forwarding_domain}"
else:
    # Для локального запуска или других сред
    API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")

st.set_page_config(layout="wide")

st.title("Аналитическая панель 'Vagon'")

# --- Функция для получения данных из API ---
def get_api_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = f"Ошибка при подключении к API: {e}"
        if e.response is not None:
            try:
                error_details = e.response.json().get('error', e.response.text)
                error_message = f"Ошибка при подключении к API: {error_details}"
            except ValueError:
                error_message = f"Ошибка при подключении к API: Не удалось декодировать JSON. Ответ: {e.response.text}"
        st.error(error_message)
        return None

# --- Отображение статистики по таблицам ---
st.header("Статистика по таблицам в базе данных")
stats_data = get_api_data("api/stats")

if stats_data:
    df_stats = pd.DataFrame(stats_data)
    st.dataframe(df_stats)
else:
    st.warning("Не удалось загрузить статистику по таблицам.")

# --- Генерация и выполнение SQL-запросов ---
st.header("Конструктор SQL-запросов с помощью LLM")

user_request = st.text_area("Введите ваш запрос на естественном языке:", height=100, placeholder="например, 'покажи 5 самых тяжелых грузов'")

if st.button("Сгенерировать SQL"):
    if user_request:
        with st.spinner("Генерация SQL-запроса..."):
            try:
                response = requests.post(f"{API_URL}/api/generate-sql", json={"query": user_request})
                response.raise_for_status()
                sql_query = response.json().get("sql_query")
                st.session_state.sql_query = sql_query # Сохраняем в состояние сессии
                st.code(sql_query, language="sql")
            except requests.exceptions.RequestException as e:
                st.error(f"Ошибка при генерации SQL: {e.response.json().get('error', e)}")
    else:
        st.warning("Пожалуйста, введите запрос.")

# --- Выполнение SQL и отображение результата ---
if 'sql_query' in st.session_state and st.session_state.sql_query:
    st.subheader("Результат выполнения запроса")
    with st.spinner("Выполнение запроса к базе данных..."):
        try:
            response = requests.post(f"{API_URL}/api/execute-sql", json={"query": st.session_state.sql_query})
            response.raise_for_status()
            data = response.json()
            if data:
                df_results = pd.DataFrame(data)
                st.dataframe(df_results)
            else:
                st.info("Запрос не вернул данных.")
        except requests.exceptions.RequestException as e:
            st.error(f"Ошибка при выполнении SQL: {e.response.json().get('error', e)}")
