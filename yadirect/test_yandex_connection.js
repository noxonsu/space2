#!/usr/bin/env node

const axios = require('axios');
require('dotenv').config();

/**
 * Тест подключения к Яндекс.Директ API
 * Проверяем доступность API и получаем список кампаний
 */
async function testYandexDirectConnection() {
  console.log('🔍 Тестируем подключение к Яндекс.Директ API...\n');

  // Проверяем переменные окружения
  console.log('📋 Проверка переменных окружения:');
  console.log(`YANDEX_DIRECT_API_URL: ${process.env.YANDEX_DIRECT_API_URL}`);
  console.log(`YANDEX_DIRECT_TOKEN: ${process.env.YANDEX_DIRECT_TOKEN ? '✓ Установлен' : '❌ Не установлен'}`);
  console.log(`YANDEX_OAUTH_URL: ${process.env.YANDEX_OAUTH_URL}`);
  console.log(`YANDEX_CLIENT_ID: ${process.env.YANDEX_CLIENT_ID ? '✓ Установлен' : '❌ Не установлен'}\n`);

  if (!process.env.YANDEX_DIRECT_TOKEN) {
    console.log('❌ Токен Яндекс.Директ не установлен!');
    console.log('Для получения токена:');
    console.log('1. Перейдите по ссылке: https://oauth.yandex.ru/authorize?response_type=code&client_id=9ba5833fea41491ab3ea12fb37044691&redirect_uri=https://habab.ru/redirect&scope=direct:api');
    console.log('2. Авторизуйтесь и получите код');
    console.log('3. Обменяйте код на токен через POST запрос');
    return;
  }

  try {
    console.log('🚀 Запрос к Яндекс.Директ API для получения кампаний...');

    const requestData = {
      method: 'get',
      params: {
        SelectionCriteria: {},
        FieldNames: ['Id', 'Name', 'Status', 'StatusPayment', 'StatusClarification', 'SourceId', 'Statistics']
      }
    };

    console.log('📤 Отправляемые данные:', JSON.stringify(requestData, null, 2));

    const response = await axios.post(
      `${process.env.YANDEX_DIRECT_API_URL}/campaigns`,
      requestData,
      {
        headers: {
          'Authorization': `Bearer ${process.env.YANDEX_DIRECT_TOKEN}`,
          'Content-Type': 'application/json; charset=utf-8',
          'Accept-Language': 'ru',
          'Client-Login': process.env.YANDEX_CLIENT_LOGIN || '',
          'Use-Operator-Units': 'false'
        }
      }
    );

    console.log('✅ Успешный ответ от API!');
    console.log(`📊 Статус ответа: ${response.status}`);
    console.log('📋 Заголовки ответа:', response.headers);
    console.log('\n📁 Данные кампаний:');
    
    if (response.data && response.data.result && response.data.result.Campaigns) {
      const campaigns = response.data.result.Campaigns;
      console.log(`Найдено кампаний: ${campaigns.length}`);
      
      campaigns.forEach((campaign, index) => {
        console.log(`\n${index + 1}. Кампания ID: ${campaign.Id}`);
        console.log(`   Название: ${campaign.Name}`);
        console.log(`   Статус: ${campaign.Status}`);
        console.log(`   Статус оплаты: ${campaign.StatusPayment}`);
        if (campaign.Statistics) {
          console.log(`   Статистика: показы=${campaign.Statistics.Impressions}, клики=${campaign.Statistics.Clicks}`);
        }
      });
    } else {
      console.log('❌ Неожиданный формат ответа:', JSON.stringify(response.data, null, 2));
    }

  } catch (error) {
    console.log('❌ Ошибка при запросе к API:');
    console.log(`Статус: ${error.response?.status}`);
    console.log(`Сообщение: ${error.message}`);
    
    if (error.response?.data) {
      console.log('Детали ошибки:', JSON.stringify(error.response.data, null, 2));
    }

    // Проверяем различные типы ошибок
    if (error.response?.status === 401) {
      console.log('\n🔑 Возможные причины ошибки авторизации:');
      console.log('1. Неверный или истекший токен');
      console.log('2. Неправильные заголовки запроса');
      console.log('3. Токен не имеет необходимых разрешений');
    } else if (error.response?.status === 400) {
      console.log('\n📝 Возможные причины ошибки запроса:');
      console.log('1. Неверный формат запроса');
      console.log('2. Отсутствуют обязательные параметры');
      console.log('3. Неправильная структура данных');
    }
  }
}

/**
 * Тест валидации токена
 */
async function testTokenValidation() {
  console.log('\n🔐 Проверяем валидность токена...');
  
  try {
    const response = await axios.get(
      `https://login.yandex.ru/info?format=json`,
      {
        headers: {
          'Authorization': `OAuth ${process.env.YANDEX_DIRECT_TOKEN}`
        }
      }
    );

    console.log('✅ Токен валиден!');
    console.log('👤 Информация о пользователе:', {
      login: response.data.login,
      id: response.data.id,
      display_name: response.data.display_name
    });

  } catch (error) {
    console.log('❌ Токен невалиден или ошибка при проверке:', error.message);
    if (error.response?.data) {
      console.log('Детали:', error.response.data);
    }
  }
}

// Запускаем тесты
async function runTests() {
  await testTokenValidation();
  await testYandexDirectConnection();
}

runTests().catch(console.error);
