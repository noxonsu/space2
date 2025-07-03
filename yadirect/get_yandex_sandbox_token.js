const axios = require('axios');
require('dotenv').config();

console.log('🧪 Тестирование Яндекс.Директ Песочница');
console.log('==========================================');

// Проверяем переменные окружения
const clientId = process.env.YANDEX_CLIENT_ID;
const clientSecret = process.env.YANDEX_CLIENT_SECRET;
const redirectUri = process.env.YANDEX_REDIRECT_URI;
const sandboxToken = process.env.YANDEX_SANDBOX_TOKEN;

if (!clientId || !clientSecret) {
  console.error('❌ Отсутствуют необходимые переменные окружения:');
  console.error('   YANDEX_CLIENT_ID или YANDEX_CLIENT_SECRET');
  process.exit(1);
}

if (!sandboxToken) {
  console.error('❌ Отсутствует мастер-токен песочницы:');
  console.error('   YANDEX_SANDBOX_TOKEN');
  process.exit(1);
}

console.log('📋 Данные приложения:');
console.log(`   Client ID: ${clientId}`);
console.log(`   Redirect URI: ${redirectUri}`);
console.log(`   Sandbox Token: ${sandboxToken}`);
console.log('');

// Функция для тестирования токена песочницы
async function testSandboxToken(token) {
  try {
    console.log('🔍 Тестирование мастер-токена песочницы...');
    
    // Проверяем токен через API информации о пользователе
    const userInfoResponse = await axios.get('https://login.yandex.ru/info', {
      headers: {
        'Authorization': `OAuth ${token}`
      }
    });
    
    console.log('✅ Мастер-токен действителен!');
    console.log('👤 Информация о пользователе:');
    console.log(`   Login: ${userInfoResponse.data.login}`);
    console.log(`   Display Name: ${userInfoResponse.data.display_name}`);
    console.log(`   Email: ${userInfoResponse.data.default_email || 'не указан'}`);
    console.log('');
    
    // Тестируем доступ к песочнице Яндекс.Директ
    console.log('🧪 Проверяем доступ к песочнице Яндекс.Директ...');
    
    // Для песочницы используется тот же URL, но другой токен
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
      console.log(`✅ Доступ к песочнице Яндекс.Директ получен! Найдено кампаний: ${campaigns.length}`);
      
      if (campaigns.length > 0) {
        console.log('📊 Тестовые кампании в песочнице:');
        campaigns.forEach((campaign, index) => {
          console.log(`   ${index + 1}. ID: ${campaign.Id}, Название: "${campaign.Name}", Статус: ${campaign.Status}`);
        });
      } else {
        console.log('📝 В песочнице пока нет тестовых кампаний');
        console.log('💡 Создайте тестовые кампании в интерфейсе песочницы Яндекс.Директ');
      }
    } else {
      console.log('⚠️  Получен неожиданный ответ от песочницы Яндекс.Директ:');
      console.log(JSON.stringify(directResponse.data, null, 2));
    }
    
    return true;
    
  } catch (error) {
    console.error('❌ Ошибка при тестировании мастер-токена песочницы:');
    if (error.response) {
      console.error(`   HTTP ${error.response.status}: ${error.response.statusText}`);
      console.error(`   Ответ: ${JSON.stringify(error.response.data, null, 2)}`);
      
      // Специальная обработка ошибок песочницы
      if (error.response.data && error.response.data.error) {
        const errorCode = error.response.data.error.error_code;
        const errorDetail = error.response.data.error.error_detail;
        
        console.log('');
        console.log('💡 Рекомендации по устранению ошибки:');
        
        if (errorCode === 58) {
          console.log('   - Это ошибка незавершенной регистрации для боевого API');
          console.log('   - В песочнице используйте YANDEX_SANDBOX_TOKEN вместо YANDEX_DIRECT_TOKEN');
          console.log('   - Убедитесь, что мастер-токен песочницы актуален');
        } else if (errorCode === 54) {
          console.log('   - Превышен лимит запросов к API');
          console.log('   - Подождите некоторое время перед следующим запросом');
        } else {
          console.log(`   - Код ошибки: ${errorCode}`);
          console.log(`   - Описание: ${errorDetail}`);
        }
      }
    } else {
      console.error(`   ${error.message}`);
    }
    
    return false;
  }
}

// Функция для создания тестовых кампаний в песочнице
async function createTestCampaigns(token) {
  try {
    console.log('');
    console.log('🏗️  Создание тестовой кампании в песочнице...');
    
    const campaignData = {
      method: 'add',
      params: {
        Campaigns: [
          {
            Name: 'Тестовая кампания API',
            StartDate: new Date().toISOString().split('T')[0],
            Type: 'TEXT_CAMPAIGN',
            TextCampaign: {
              BiddingStrategy: {
                Search: {
                  BiddingStrategyType: 'HIGHEST_POSITION'
                },
                Network: {
                  BiddingStrategyType: 'SERVING_OFF'
                }
              },
              Settings: []
            }
          }
        ]
      }
    };
    
    const response = await axios.post('https://api.direct.yandex.com/json/v5/campaigns', campaignData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Language': 'ru'
      }
    });
    
    if (response.data.result && response.data.result.AddResults) {
      const campaignId = response.data.result.AddResults[0].Id;
      console.log(`✅ Тестовая кампания создана! ID: ${campaignId}`);
    } else {
      console.log('⚠️  Неожиданный ответ при создании кампании:');
      console.log(JSON.stringify(response.data, null, 2));
    }
    
  } catch (error) {
    console.error('❌ Ошибка при создании тестовой кампании:');
    if (error.response) {
      console.error(`   HTTP ${error.response.status}: ${error.response.statusText}`);
      console.error(`   Ответ: ${JSON.stringify(error.response.data, null, 2)}`);
    } else {
      console.error(`   ${error.message}`);
    }
  }
}

// Основная функция
async function main() {
  console.log('🧪 === РЕЖИМ ПЕСОЧНИЦЫ ===');
  console.log('');
  console.log('ℹ️  Песочница Яндекс.Директ - это тестовая среда для отладки приложений');
  console.log('   Здесь можно безопасно тестировать API без влияния на реальные кампании');
  console.log('');
  
  const success = await testSandboxToken(sandboxToken);
  
  if (success) {
    console.log('');
    console.log('🎉 Песочница готова к использованию!');
    console.log('');
    console.log('📚 Полезные команды для работы с песочницей:');
    console.log('   - Создать тестовые кампании в интерфейсе: https://direct.yandex.ru/registered?cmd=manageAPIData');
    console.log('   - Очистить песочницу от тестовых данных');
    console.log('   - Сбросить счетчик финансовых операций');
    console.log('');
    
    // Можно добавить создание тестовой кампании
    const args = process.argv.slice(2);
    if (args.includes('--create-test-campaign')) {
      await createTestCampaigns(sandboxToken);
    }
  }
}

// Запуск основной функции
main().catch(console.error);

// Экспортируем функции для использования в других модулях
module.exports = { 
  testSandboxToken,
  createTestCampaigns
};
