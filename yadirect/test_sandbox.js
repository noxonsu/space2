const axios = require('axios');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '.env') });

console.log('🧪 Тестирование песочницы Яндекс.Директ');
console.log('========================================');


// Проверяем переменные окружения
const sandboxOAuthToken = process.env.YANDEX_SANDBOX_OAUTH_TOKEN;

if (!sandboxOAuthToken) {
  console.error('❌ Отсутствует YANDEX_SANDBOX_OAUTH_TOKEN в .env');
  console.error('   Пожалуйста, получите его, запустив `node get_sandbox_oauth_token.js` и следуя инструкциям.');
  process.exit(1);
}

console.log('📋 Данные песочницы:');
console.log(`   Sandbox OAuth Token: ${sandboxOAuthToken.substring(0, 8)}...`); // Mask token for display
console.log('');

// Функция для тестирования песочницы
async function testSandbox() {
  try {
    console.log('🔍 Тестирование доступа к песочнице...');
    
    // Тестируем доступ к песочнице Яндекс.Директ
    const directResponse = await axios.post('https://api-sandbox.direct.yandex.com/json/v5/campaigns', {
      method: 'get',
      params: {
        SelectionCriteria: {},
        FieldNames: ['Id', 'Name', 'Status', 'StatusPayment', 'StatusClarification']
      }
    }, {
      headers: {
        'Authorization': `Bearer ${sandboxOAuthToken}`,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Language': 'ru'
      }
    });
    
    console.log('✅ Успешное подключение к песочнице!');
    
    if (directResponse.data.result && directResponse.data.result.Campaigns) {
      const campaigns = directResponse.data.result.Campaigns;
      console.log(`📊 Найдено кампаний в песочнице: ${campaigns.length}`);
      
      if (campaigns.length > 0) {
        console.log('📋 Тестовые кампании:');
        campaigns.forEach((campaign, index) => {
          console.log(`   ${index + 1}. ID: ${campaign.Id}, Название: "${campaign.Name}", Статус: ${campaign.Status}`);
        });
      } else {
        console.log('📝 В песочнице пока нет тестовых кампаний');
        console.log('💡 Создайте тестовые кампании в интерфейсе песочницы');
      }
    } else {
      console.log('⚠️  Получен неожиданный ответ от песочницы:');
      console.log(JSON.stringify(directResponse.data, null, 2));
    }
    
  } catch (error) {
    console.error('❌ Ошибка при работе с песочницей:');
    if (error.response) {
      console.error(`   HTTP ${error.response.status}: ${error.response.statusText}`);
      console.error(`   Ответ: ${JSON.stringify(error.response.data, null, 2)}`);
    } else {
      console.error(`   ${error.message}`);
    }
  }
}

// Запускаем тест
testSandbox();
