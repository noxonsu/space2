#!/usr/bin/env node

/**
 * Тестовый скрипт для демонстрации работы блэклиста
 * Запуск: node test_blacklist_demo.js
 */

const {
  loadBlacklist,
  saveBlacklist,
  addToBlacklist,
  isInBlacklist
} = require('./space2_newsalert');

console.log('🔧 Демонстрация работы блэклиста обработанных URL\n');

// Загружаем текущий блэклист
console.log('1. Загружаем существующий блэклист...');
const blacklist = loadBlacklist();
console.log(`   Текущий размер блэклиста: ${blacklist.size} URL\n`);

// Симулируем обработку новостей
const mockNewsUrls = [
  'https://fastmarkets.com/news/antimony-trioxide-prices-surge',
  'https://chemweek.com/sb2o3-supply-shortage-china',
  'https://reuters.com/antimony-market-update-2025',
  'https://fastmarkets.com/news/antimony-trioxide-prices-surge', // Дубликат
  'https://bloomberg.com/chemical-markets-sb2o3'
];

console.log('2. Симулируем обработку новостных URL...');
let processedCount = 0;
let skippedCount = 0;

mockNewsUrls.forEach((url, index) => {
  console.log(`\n   URL ${index + 1}: ${url}`);
  
  if (isInBlacklist(url, blacklist)) {
    console.log(`   ❌ ПРОПУЩЕН - уже обработан ранее`);
    skippedCount++;
  } else {
    console.log(`   ✅ НОВЫЙ - добавляем в обработку`);
    addToBlacklist(url, blacklist);
    processedCount++;
    // Здесь бы происходила обработка через OpenAI
    console.log(`   🤖 [Симуляция] Отправляем в OpenAI для анализа...`);
  }
});

console.log(`\n3. Результаты обработки:`);
console.log(`   📊 Обработано новых: ${processedCount}`);
console.log(`   🚫 Пропущено (дубликаты): ${skippedCount}`);
console.log(`   📝 Общий размер блэклиста: ${blacklist.size}`);

// Сохраняем обновленный блэклист
console.log(`\n4. Сохраняем обновленный блэклист...`);
saveBlacklist(blacklist);

// Демонстрируем что блэклист работает при повторном запуске
console.log(`\n5. Демонстрируем работу при повторном запуске...`);
const reloadedBlacklist = loadBlacklist();
console.log(`   Загружен блэклист с ${reloadedBlacklist.size} URL`);

const testUrl = 'https://fastmarkets.com/news/antimony-trioxide-prices-surge';
console.log(`\n   Проверяем URL: ${testUrl}`);
if (isInBlacklist(testUrl, reloadedBlacklist)) {
  console.log(`   ✅ Правильно! URL найден в блэклисте - повторная обработка будет пропущена`);
} else {
  console.log(`   ❌ Ошибка! URL не найден в блэклисте`);
}

console.log(`\n🎉 Демонстрация завершена!\n`);
console.log(`💡 Преимущества блэклиста:`);
console.log(`   • Экономия токенов OpenAI (не анализируем повторно)`);
console.log(`   • Ускорение обработки (пропускаем известные URL)`);
console.log(`   • Предотвращение спама в Telegram (не дублируем сообщения)`);
console.log(`   • Персистентность между перезапусками`);
