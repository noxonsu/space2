<!DOCTYPE html>
<html lang="ru">
  <head>
<style>
body {
  background-image: url('vista.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
  background-attachment: fixed;
  background-color: #00008B;
  height: 100vh;
  margin: 0;
  padding:0%;
}
</style>
</head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Vibecoding: Быстрая разработка CRM, ИИ, Telegram, API и дашбордов с использованием нейросетей."
    />
    <link rel="icon" href="/favicon.ico" />
    <link rel="apple-touch-icon" href="/logo192.png" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet" />
    <title>Vibecoding - Разработка быстрее и дешевле</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
      :root {
        --text-color: #ffffff;
        --glass-bg: rgba(255,255,255,0.15);
        --glass-border: 1px solid rgba(255,255,255,0.8);
        --glass-shadow: 0 8px 32px rgba(31,38,135,0.2), inset 0 4px 20px rgba(255,255,255,0.3);
        --glass-radius: 2rem;
        --glass-shine-bg: rgba(255,255,255,0.1);
        --glass-shine-shadow: inset -10px -8px 0px -11px rgba(255,255,255,1), inset 0px -9px 0px -8px rgba(255,255,255,1);
      }

      body {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        min-height: 100vh;
        color: #ffffff;
        transition: all 0.3s ease;
      }

      .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
      }

      header, section, footer {
        position: relative;
        background: var(--glass-bg);
        border: var(--glass-border);
        border-radius: var(--glass-radius);
        box-shadow: var(--glass-shadow);
        backdrop-filter: blur(2px) saturate(180%);
        -webkit-backdrop-filter: blur(2px) saturate(180%);
        overflow: hidden;
      }

      header {
        text-align: center;
        padding: 60px 20px;
        color: white;
        margin-bottom: 20px;
        animation: fadeIn 1s ease-out;
      }

      header h1 {
        margin: 0;
        font-size: 3em;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0,0,0,0.25);
      }

      header p {
        font-size: 1.2em;
        opacity: 0.9;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2);
      }

      section {
        margin: 30px 0;
        padding: 30px;
        animation: slideUp 0.8s ease-out;
      }

      footer {
        text-align: center;
        padding: 20px;
        color: white;
        margin-top: 40px;
        border-radius: var(--glass-radius) var(--glass-radius) 0 0;
      }

      header::after, section::after, footer::after {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: var(--glass-shine-bg);
        border-radius: inherit;
        backdrop-filter: blur(1px);
        box-shadow: var(--glass-shine-shadow);
        opacity: 0.6;
        z-index: -1;
        filter: blur(1px) drop-shadow(10px 4px 6px black) brightness(115%);
        pointer-events: none;
      }

      h2 {
        color: #ffffff;
        font-size: 2em;
        font-weight: 600;
        margin-bottom: 20px;
      }

      .tariffs ul {
        list-style: none;
        padding: 0;
      }

      .tariffs li {
        margin: 15px 0;
        font-size: 1.1em;
      }

      .tariffs li p {
        margin: 5px 0;
        font-size: 0.95em;
        opacity: 0.8;
      }

      .contact a {
        color: #ffffff;
        text-decoration: none;
        font-weight: 600;
      }

      .contact a:hover {
        text-decoration: underline;
      }

      .telegram-button, .username-button {
        display: inline-block;
        background: #007bff;
        color: #ffffff;
        padding: 18px 40px;
        font-size: 1.3em;
        font-weight: 600;
        border-radius: 1.2rem;
        text-align: center;
        border: none;
        cursor: pointer;
        margin-top: 25px;
        margin-right: 10px;
        transition: background 0.3s ease, transform 0.2s ease;
        box-shadow: 0 2px 8px rgba(31,38,135,0.08);
      }

      .telegram-button:hover, .username-button:hover {
        background: #0056b3;
        transform: translateY(-3px);
      }

      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }

      @media (max-width: 600px) {
        header h1 { font-size: 2em; }
        header p { font-size: 1em; }
        .telegram-button, .username-button { padding: 14px 30px; font-size: 1.1em; }
        section { padding: 20px; }
      }
    </style>
  </head>
  <body>
    <header>
      <h1>Vibecoding: Быстрая веб-разработка с нейросетями</h1>
      <p>Интеграция CRM, ИИ, Telegram, API и дашбордов быстрее и дешевле!</p>
    </header>
    <div class="container">
      <section class="about">
        <h2>О моих услугах</h2>
        <p>
          Привет! Я веб-разработчик, использующий нейросети для кода поэтому делаю быстрее. Это позволяет создавать решения быстрее и дешевле традиционных методов. Моя цель — 100 аутсорс-проектов до конца года. Готовы обсудить вашу задачу? Первая демка за 24 часа!
        </p>
        <p>
          Также привожу траф с Telegram Ads для телеграм-ботов — настраиваю рекламные кампании, чтобы трафик шел на ваш бот и приносил деньги или продажи.
        </p>
        <p>
          Посмотрите примеры кейсов в канале: <a href="https://t.me/aideaxondemos">@aideaxondemos</a>
        </p>
      </section>
      <section class="tariffs">
        <h2>Тарифы</h2>
        <ul>
          <li>
            <strong>1 час: 2 500 рублей</strong><br />
            Подходит для быстрых задач или консультаций.
            <p>Смотрите работы в канале, я там указываю количество часов. Обычно первая версия не дороже 20 тыс. рублей.</p>
          </li>
          <li>
            <strong>1 день: 20 000 рублей</strong><br />
            Подходит для небольших задач (например, интеграция с API, создание простого бота).
          </li>
          <li>
            <strong>1 неделя: 100 000 рублей</strong><br />
            Для сложных проектов (например, CRM-интеграция, дашборды с аналитикой).
          </li>
        </ul>
      </section>
      <section class="contact">
        <h2>Свяжитесь со мной</h2>
        <p>
          Пишите в Telegram: <a href="https://t.me/sashanoxon">@sashanoxon</a><br />
          Читайте отзывы и смотрите мои ранние работы: <a href="https://www.fl.ru/users/158484/portfolio/">Профиль на FL.ru</a><br />
          Профиль разработчика на GitHub: <a href="https://github.com/noxonsu">github.com/noxonsu</a>
        </p>
        <button class="telegram-button" onclick="window.open('https://t.me/sashanoxon', '_blank')">Написать в Telegram</button>
      </section>
    </div>
    <footer>
      <p>Я сам использую нейросети для кода поэтому делаю быстрее, что сокращает затраты времени</p>
    </footer>
    <script>
      function showUsername() {
        const user = window.Telegram.WebApp.initDataUnsafe.user;
        const username = user && user.username ? `@${user.username}` : 'Имя пользователя не задано';
        alert(`Ваше имя пользователя: ${username}`);
      }

      // Send username and UTM parameters from URL to endpoint on page load
      window.onload = function() {
        const user = window.Telegram.WebApp.initDataUnsafe.user;
        const username = user && user.username ? `@${user.username}` : '@unknown';
        const urlParams = new URLSearchParams(window.location.search);
        const utmSource = urlParams.get('utm_source') || 'telegram';
        const utmMedium = urlParams.get('utm_medium') || 'webapp';
        const utmCampaign = urlParams.get('utm_campaign') || 'vibecoding_2025';
        const utmParams = `utm_source=${encodeURIComponent(utmSource)}&utm_medium=${encodeURIComponent(utmMedium)}&utm_campaign=${encodeURIComponent(utmCampaign)}`;
        const message = encodeURIComponent(`открыли https://t.me/sashanoxonbot/webdev пользователь ${username}&${utmParams}`);
        const url = `https://noxon.wpmix.net/counter.php?tome=1&msg=${message}`;

        fetch(url, { method: 'GET' })
          .catch(error => console.error('Error sending username:', error));
      };
    </script>
  </body>
</html>
