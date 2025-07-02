#!/usr/bin/env node

/**
 * Тестовый скрипт для проверки работы с Яндекс.Директ API
 */

require('dotenv').config();
const YandexDirectService = require('./src/services/yandexDirectService');
const logger = require('./src/utils/logger');

async function testYandexDirectAPI() {
  console.log('🧪 Тестирование Яндекс.Директ API...\n');

  // Проверяем переменные окружения
  if (!process.env.YANDEX_CLIENT_ID || !process.env.YANDEX_CLIENT_SECRET) {
    console.error('❌ Не найдены данные OAuth в .env файле');
    return;
  }

  console.log('✅ OAuth данные найдены:');
  console.log(`   Client ID: ${process.env.YANDEX_CLIENT_ID}`);
  console.log(`   Client Secret: ${process.env.YANDEX_CLIENT_SECRET.substring(0, 8)}...`);
  console.log(`   Redirect URI: ${process.env.YANDEX_REDIRECT_URI}\n`);

  // Получаем токен из аргументов командной строки
  const token = process.argv[2];
  if (!token) {
    console.log('💡 Для тестирования API передайте токен доступа как аргумент:');
    console.log('   node test_api.js YOUR_ACCESS_TOKEN\n');
    
    console.log('📝 Для получения токена:');
    console.log('1. Запустите сервер: npm start');
    console.log('2. Перейдите на: http://localhost:3000/auth/yandex/url');
    console.log('3. Скопируйте токен из результата авторизации\n');
    return;
  }

  try {
    const yandexService = new YandexDirectService(token);
    
    console.log('🔍 Проверка токена...');
    try {
      await yandexService.validateToken();
      console.log('✅ Токен действителен!\n');
    } catch (error) {
      console.error('❌ Ошибка валидации токена:', error.message);
      return;
    }

    console.log('📋 Получение списка кампаний...');
    try {
      const campaigns = await yandexService.getCampaigns();
      console.log(`✅ Найдено кампаний: ${campaigns.Campaigns?.length || 0}`);
      
      if (campaigns.Campaigns && campaigns.Campaigns.length > 0) {
        console.log('\n📊 Первые 3 кампании:');
        campaigns.Campaigns.slice(0, 3).forEach((campaign, index) => {
          console.log(`   ${index + 1}. ID: ${campaign.Id}, Название: ${campaign.Name}, Статус: ${campaign.Status}`);
        });
      }
      console.log('');
    } catch (error) {
      console.error('❌ Ошибка получения кампаний:', error.message);
    }

    // Тест создания объявлений с помощью OpenAI
    if (process.env.OPENAI_API_KEY) {
      console.log('🤖 Тестирование генерации объявлений...');
      try {
        const OpenAIService = require('./src/services/openaiService');
        const openaiService = new OpenAIService();
        
        const testData = {
          url: 'https://habab.ru/brachnogo-dogovora',
          title: 'Проверка брачного договора онлайн',
          meta_description: 'Быстрая и качественная проверка брачного договора',
          meta_keywords: ['брачный договор', 'проверка договора'],
          main_keyword: 'брачный договор'
        };

        const ads = await openaiService.generateAds(testData);
        console.log(`✅ Сгенерировано объявлений: ${ads.length}`);
        
        if (ads.length > 0) {
          console.log('\n📝 Первое объявление:');
          console.log(`   Заголовок: ${ads[0].title}`);
          console.log(`   Описание: ${ads[0].description}`);
          console.log(`   URL: ${ads[0].url}`);
        }
        console.log('');
      } catch (error) {
        console.error('❌ Ошибка генерации объявлений:', error.message);
      }
    } else {
      console.log('⚠️  OpenAI API ключ не настроен, пропускаем тест генерации объявлений\n');
    }

    console.log('🎉 Тестирование завершено!');

  } catch (error) {
    console.error('💥 Критическая ошибка:', error.message);
    logger.error('Критическая ошибка в тесте:', error);
  }
}

// Обработка сигналов для корректного завершения
process.on('SIGINT', () => {
  console.log('\n👋 Тестирование прервано пользователем');
  process.exit(0);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Необработанная ошибка Promise:', reason);
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Запускаем тест
testYandexDirectAPI().catch(error => {
  console.error('Фатальная ошибка:', error);
  process.exit(1);
});
