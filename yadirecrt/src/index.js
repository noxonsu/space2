const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const multer = require('multer');
const path = require('path');

// Загружаем переменные окружения
dotenv.config();

// Импортируем наши модули
const logger = require('./utils/logger');
const YandexDirectService = require('./services/yandexDirectService');
const OpenAIService = require('./services/openaiService');
const FileProcessor = require('./services/fileProcessor');
const authRoutes = require('./routes/auth');
const campaignRoutes = require('./routes/campaigns');

const app = express();
const PORT = process.env.PORT || 3000;

// Настройка middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Настройка multer для загрузки файлов
const upload = multer({ 
  dest: 'uploads/',
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['.yaml', '.yml', '.txt', '.md'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowedTypes.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Неподдерживаемый тип файла'), false);
    }
  }
});

// Статические файлы
app.use(express.static('public'));

// Роуты
app.use('/auth', authRoutes);
app.use('/api/campaigns', campaignRoutes);

// Основной эндпоинт для обработки файлов
app.post('/api/process-file', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'Файл не загружен' });
    }

    const { accessToken } = req.body;
    if (!accessToken) {
      return res.status(400).json({ error: 'Токен доступа не предоставлен' });
    }

    logger.info(`Обработка файла: ${req.file.originalname}`);

    // Обрабатываем файл
    const fileProcessor = new FileProcessor();
    const parsedData = await fileProcessor.processFile(req.file.path);

    // Инициализируем сервисы
    const yandexService = new YandexDirectService(accessToken);
    const openaiService = new OpenAIService();

    // Генерируем объявления
    const generatedAds = await openaiService.generateAds(parsedData);

    // Создаем кампанию в Яндекс.Директ
    const campaignResult = await yandexService.createCampaign(parsedData, generatedAds);

    res.json({
      success: true,
      data: {
        parsedData,
        generatedAds,
        campaignResult
      }
    });

  } catch (error) {
    logger.error('Ошибка при обработке файла:', error);
    res.status(500).json({ 
      error: 'Произошла ошибка при обработке файла',
      details: error.message 
    });
  }
});

// Эндпоинт для проверки статуса
app.get('/api/status', (req, res) => {
  res.json({ 
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// Обработка ошибок
app.use((error, req, res, next) => {
  logger.error('Необработанная ошибка:', error);
  res.status(500).json({ 
    error: 'Внутренняя ошибка сервера',
    details: process.env.NODE_ENV === 'development' ? error.message : undefined
  });
});

// 404 обработчик
app.use((req, res) => {
  res.status(404).json({ error: 'Эндпоинт не найден' });
});

// Запуск сервера только если не в тестовой среде
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    logger.info(`🚀 Сервер запущен на порту ${PORT}`);
    logger.info(`🌍 Среда: ${process.env.NODE_ENV}`);
  });
}

module.exports = app;
