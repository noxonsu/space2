#!/usr/bin/env node

/**
 * Скрипт для тестирования структуры запросов к Яндекс.Директ API
 */

const axios = require('axios');

// Тестируем правильность структуры запросов
async function testAPIStructure() {
  console.log('🔬 Тестирование структуры запросов к Яндекс.Директ API\n');

  const token = process.argv[2];
  if (!token) {
    console.log('Использование: node test_structure.js YOUR_ACCESS_TOKEN');
    return;
  }

  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
    'Accept-Language': 'ru'
  };

  // Тест 1: Минимальный запрос к campaigns
  console.log('1️⃣ Тест минимального запроса к /campaigns...');
  try {
    const response = await axios.post('https://api.direct.yandex.com/json/v5/campaigns', {
      method: 'get',
      params: {
        SelectionCriteria: {},
        FieldNames: ['Id']
      }
    }, { headers });

    console.log('✅ Запрос успешен');
    console.log(`   Статус: ${response.status}`);
    console.log(`   Кампаний найдено: ${response.data.result.Campaigns?.length || 0}`);
    
    if (response.headers.requestid) {
      console.log(`   Request ID: ${response.headers.requestid}`);
    }
    if (response.headers.units) {
      console.log(`   Units: ${response.headers.units}`);
    }
  } catch (error) {
    console.error('❌ Ошибка:', error.response?.status, error.response?.statusText);
    if (error.response?.data) {
      console.error('   Детали:', JSON.stringify(error.response.data, null, 2));
    }
  }
  console.log('');

  // Тест 2: Запрос с дополнительными полями
  console.log('2️⃣ Тест запроса с дополнительными полями...');
  try {
    const response = await axios.post('https://api.direct.yandex.com/json/v5/campaigns', {
      method: 'get',
      params: {
        SelectionCriteria: {},
        FieldNames: ['Id', 'Name', 'Status', 'State', 'Type'],
        Page: {
          Limit: 5,
          Offset: 0
        }
      }
    }, { headers });

    console.log('✅ Расширенный запрос успешен');
    console.log(`   Кампаний получено: ${response.data.result.Campaigns?.length || 0}`);
    
    if (response.data.result.Campaigns && response.data.result.Campaigns.length > 0) {
      const campaign = response.data.result.Campaigns[0];
      console.log(`   Первая кампания: ID=${campaign.Id}, Name="${campaign.Name}", Status=${campaign.Status}`);
    }
  } catch (error) {
    console.error('❌ Ошибка в расширенном запросе:', error.response?.status);
    if (error.response?.data) {
      console.error('   Детали:', JSON.stringify(error.response.data, null, 2));
    }
  }
  console.log('');

  // Тест 3: Проверка справочников
  console.log('3️⃣ Тест получения справочников...');
  try {
    const response = await axios.post('https://api.direct.yandex.com/json/v5/dictionaries', {
      method: 'get',
      params: {
        DictionaryNames: ['Currencies', 'TimeZones']
      }
    }, { headers });

    console.log('✅ Справочники получены успешно');
    const dictionaries = response.data.result;
    if (dictionaries.Currencies) {
      console.log(`   Валют: ${dictionaries.Currencies.length}`);
    }
    if (dictionaries.TimeZones) {
      console.log(`   Часовых поясов: ${dictionaries.TimeZones.length}`);
    }
  } catch (error) {
    console.error('❌ Ошибка получения справочников:', error.response?.status);
    if (error.response?.data) {
      console.error('   Детали:', JSON.stringify(error.response.data, null, 2));
    }
  }
  console.log('');

  // Тест 4: Проверка заголовков ответа
  console.log('4️⃣ Анализ заголовков ответа...');
  try {
    const response = await axios.post('https://api.direct.yandex.com/json/v5/campaigns', {
      method: 'get',
      params: {
        SelectionCriteria: {},
        FieldNames: ['Id']
      }
    }, { headers });

    console.log('✅ Заголовки получены:');
    
    const importantHeaders = ['requestid', 'units', 'units-used-login'];
    importantHeaders.forEach(header => {
      if (response.headers[header]) {
        console.log(`   ${header}: ${response.headers[header]}`);
      }
    });
  } catch (error) {
    console.error('❌ Ошибка анализа заголовков:', error.response?.status);
  }
  console.log('');

  console.log('🏁 Тестирование структуры завершено!');
}

testAPIStructure().catch(error => {
  console.error('Фатальная ошибка:', error.message);
  process.exit(1);
});
