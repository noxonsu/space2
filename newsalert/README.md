# Space2 News Alert

Система мониторинга новостей с уведомлениями в Telegram.

## Установка

```bash
npm install pm2 -g
cd /workspaces/space2/newsalert
mkdir logs
```

## Управление через PM2

```bash
# Запуск
pm2 start ecosystem.config.js

# Остановка
pm2 stop space2-newsalert

# Перезапуск
pm2 restart space2-newsalert

# Просмотр логов
pm2 logs space2-newsalert

# Мониторинг
pm2 monit

# Статус
pm2 status

# Удаление из PM2
pm2 delete space2-newsalert
```

## Настройка переменных окружения

Создайте файл `.env`:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Создайте файл `.env_keys` с ключевыми словами (по одному на строку).

## Доступ к админ-панели

http://localhost:3656

## Автозапуск при перезагрузке

```bash
pm2 startup
pm2 save
```