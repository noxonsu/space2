const axios = require('axios');
require('dotenv').config();

console.log('🔑 Получение токена Яндекс.Директ');
console.log('=====================================');

// Проверяем переменные окружения
const clientId = process.env.YANDEX_CLIENT_ID;
const clientSecret = process.env.YANDEX_CLIENT_SECRET;
const redirectUri = process.env.YANDEX_REDIRECT_URI;

if (!clientId || !clientSecret) {
  console.error('❌ Отсутствуют необходимые переменные окружения:');
  console.error('   YANDEX_CLIENT_ID или YANDEX_CLIENT_SECRET');
  process.exit(1);
}

console.log('📋 Данные приложения:');
console.log(`   Client ID: ${clientId}`);
console.log(`   Redirect URI: ${redirectUri}`);
console.log('');

// Генерируем URL для авторизации
const authUrl = `https://oauth.yandex.ru/authorize?response_type=token&client_id=${clientId}`;

console.log('🌐 Для получения токена выполните следующие шаги:');
console.log('');
console.log('1. Откройте эту ссылку в браузере:');
console.log(`   ${authUrl}`);
console.log('');
console.log('2. Войдите в Яндекс и разрешите доступ приложению');
console.log('');
console.log('3. После редиректа скопируйте access_token из URL');
console.log('   (часть после #access_token=...)');
console.log('');
console.log('4. Обновите YANDEX_DIRECT_TOKEN в файле .env');
console.log('');

// Функция для тестирования токена
async function testToken(token) {
  try {
    console.log('🔍 Тестирование токена...');
    
    // Проверяем токен через API информации о пользователе
    const userInfoResponse = await axios.get('https://login.yandex.ru/info', {
      headers: {
        'Authorization': `OAuth ${token}`
      }
    });
    
    console.log('✅ Токен действителен!');
    console.log('👤 Информация о пользователе:');
    console.log(`   Login: ${userInfoResponse.data.login}`);
    console.log(`   Display Name: ${userInfoResponse.data.display_name}`);
    console.log(`   Email: ${userInfoResponse.data.default_email || 'не указан'}`);
    console.log('');
    
    // Тестируем доступ к Яндекс.Директ
    console.log('🎯 Проверяем доступ к Яндекс.Директ...');
    
    const directResponse = await axios.post('https://api.direct.yandex.com/json/v5/campaigns', {
      method: 'get',
      params: {
        SelectionCriteria: {},
        FieldNames: ['Id', 'Name', 'Status', 'StatusPayment', 'StatusClarification']
      }
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Language': 'ru'
      }
    });
    
    if (directResponse.data.result && directResponse.data.result.Campaigns) {
      const campaigns = directResponse.data.result.Campaigns;
      console.log(`✅ Доступ к Яндекс.Директ получен! Найдено кампаний: ${campaigns.length}`);
      
      if (campaigns.length > 0) {
        console.log('📊 Ваши кампании:');
        campaigns.forEach((campaign, index) => {
          console.log(`   ${index + 1}. ID: ${campaign.Id}, Название: "${campaign.Name}", Статус: ${campaign.Status}`);
        });
      } else {
        console.log('📝 У вас пока нет кампаний в Яндекс.Директ');
      }
    } else {
      console.log('⚠️  Получен неожиданный ответ от Яндекс.Директ:');
      console.log(JSON.stringify(directResponse.data, null, 2));
    }
    
  } catch (error) {
    console.error('❌ Ошибка при тестировании токена:');
    if (error.response) {
      console.error(`   HTTP ${error.response.status}: ${error.response.statusText}`);
      console.error(`   Ответ: ${JSON.stringify(error.response.data, null, 2)}`);
    } else {
      console.error(`   ${error.message}`);
    }
  }
}

// Если токен уже есть в .env, тестируем его
const currentToken = process.env.YANDEX_DIRECT_TOKEN;
if (currentToken && currentToken !== 'l55qon6u2gjnr2wl') {
  console.log('🔄 Тестируем текущий токен из .env...');
  testToken(currentToken);
} else {
  console.log('⚠️  Токен в .env отсутствует или недействителен');
  console.log('   Получите новый токен по инструкции выше');
}

// Экспортируем функцию тестирования для использования с новым токеном
module.exports = { testToken };
