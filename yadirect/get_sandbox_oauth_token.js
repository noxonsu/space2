const axios = require('axios');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '.env') });

console.log('🧪 Получение OAuth токена для песочницы Яндекс.Директ');
console.log('====================================================');

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

// Генерируем URL для авторизации для песочницы
// Для песочницы добавляем параметр device_name=sandbox
const authUrl = `https://oauth.yandex.ru/authorize?response_type=token&client_id=${clientId}&device_name=sandbox`;

console.log('🌐 Для получения OAuth токена для ПЕСОЧНИЦЫ выполните следующие шаги:');
console.log('');
console.log('1. Откройте эту ссылку в браузере (СПЕЦИАЛЬНО для песочницы):');
console.log(`   ${authUrl}`);
console.log('');
console.log('2. Войдите в Яндекс и разрешите доступ приложению');
console.log('');
console.log('3. После редиректа скопируйте access_token из URL');
console.log('   (часть после #access_token=...)');
console.log('');
console.log('4. Добавьте YANDEX_SANDBOX_OAUTH_TOKEN в файл .env');
console.log('');

// Функция для тестирования OAuth токена песочницы
async function testSandboxOAuthToken(token) {
  try {
    console.log('🔍 Тестирование OAuth токена для песочницы...');
    
    // Проверяем токен через API информации о пользователе
    const userInfoResponse = await axios.get('https://login.yandex.ru/info', {
      headers: {
        'Authorization': `OAuth ${token}`
      }
    });
    
    console.log('✅ OAuth токен действителен!');
    console.log('👤 Информация о пользователе:');
    console.log(`   Login: ${userInfoResponse.data.login}`);
    console.log(`   Display Name: ${userInfoResponse.data.display_name}`);
    console.log(`   Email: ${userInfoResponse.data.default_email || 'не указан'}`);
    console.log('');
    
    // Тестируем доступ к песочнице Яндекс.Директ
    console.log('🧪 Проверяем доступ к песочнице Яндекс.Директ...');
    
    // Для песочницы используется специальный URL api-sandbox
    const directResponse = await axios.post('https://api-sandbox.direct.yandex.com/json/v5/campaigns', {
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
      console.log(`✅ Доступ к песочнице Яндекс.Директ получен! Найдено кампаний: ${campaigns.length}`);
      
      if (campaigns.length > 0) {
        console.log('📊 Тестовые кампании в песочнице:');
        campaigns.forEach((campaign, index) => {
          console.log(`   ${index + 1}. ID: ${campaign.Id}, Название: "${campaign.Name}", Статус: ${campaign.Status}`);
        });
      } else {
        console.log('📝 В песочнице пока нет тестовых кампаний');
        console.log('💡 Вы можете создать тестовые кампании через API или в интерфейсе');
      }
    } else {
      console.log('⚠️  Получен неожиданный ответ от песочницы Яндекс.Директ:');
      console.log(JSON.stringify(directResponse.data, null, 2));
    }
    
  } catch (error) {
    console.error('❌ Ошибка при тестировании OAuth токена песочницы:');
    if (error.response) {
      console.error(`   HTTP ${error.response.status}: ${error.response.statusText}`);
      console.error(`   Ответ: ${JSON.stringify(error.response.data, null, 2)}`);
      
      // Специальная обработка ошибок
      if (error.response.data && error.response.data.error) {
        const errorCode = error.response.data.error.error_code;
        const errorDetail = error.response.data.error.error_detail;
        
        console.log('');
        console.log('💡 Рекомендации:');
        
        if (errorCode === 53) {
          console.log('   - Недействительный OAuth-токен');
          console.log('   - Получите новый OAuth токен по ссылке выше');
          console.log('   - Убедитесь, что используете device_name=sandbox при авторизации');
        } else if (errorCode === 58) {
          console.log('   - Незавершенная регистрация приложения');
          console.log('   - Убедитесь, что приложение зарегистрировано для работы с песочницей');
        } else {
          console.log(`   - Код ошибки: ${errorCode}`);
          console.log(`   - Описание: ${errorDetail}`);
        }
      }
    } else {
      console.error(`   ${error.message}`);
    }
  }
}

// Если есть токен песочницы в .env, тестируем его
const currentSandboxToken = process.env.YANDEX_SANDBOX_OAUTH_TOKEN;
if (currentSandboxToken && currentSandboxToken !== '') {
  console.log('🔄 Тестируем текущий OAuth токен песочницы из .env...');
  testSandboxOAuthToken(currentSandboxToken);
} else {
  console.log('⚠️  OAuth токен для песочницы отсутствует в .env');
  console.log('   Получите новый токен по инструкции выше и добавьте как YANDEX_SANDBOX_OAUTH_TOKEN');
}

// Экспортируем функцию тестирования для использования с новым токеном
module.exports = { testSandboxOAuthToken };
