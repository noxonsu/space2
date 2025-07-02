# Стратегии показа  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/objects/campaign-strategies

**Дата скачивания:** 2025-07-01 12:36:12

---

# Стратегии показа

### Была ли статья полезна?

# Стратегии показа

### Была ли статья полезна?

Стратегии показа делятся на две категории:

Ручные стратегии — рекламодатель или агентство самостоятельно назначает ставки на условия показа: ключевые фразы, условия нацеливания на аудиторию, условия нацеливания для динамических объявлений.

Примечание

Назначенная вручную ставка за клик может автоматически снижаться или повышаться в зависимости от вероятности конверсии (см. раздел  Автоматическая корректировка ставок  помощи Директа).

Автоматические стратегии — ставки устанавливаются автоматически в соответствии с параметрами стратегии. Рекламодатель или агентство может указать приоритеты условий показа.

Подробная информация о стратегиях показа приведена в разделе  Какую стратегию показов выбрать  помощи Директа.

В API версии 5 стратегия показа настраивается раздельно на поиске и в сетях (Рекламной сети Яндекса и внешних сетях).

Совместимость стратегий представлена в таблицах ниже:

Внимание

Для подключения стратегий WB_MAXIMUM_CONVERSION_RATE, WB_MAXIMUM_APP_INSTALLS, AVERAGE_CPA, AVERAGE_CPA_MULTIPLE_GOALS, AVERAGE_CPI, AVERAGE_ROI, AVERAGE_CRR, PAY_FOR_CONVERSION, PAY_FOR_CONVERSION_MULTIPLE_GOALS, PAY_FOR_CONVERSION_PER_CAMPAIGN, PAY_FOR_INSTALL, WB_AVERAGE_CPV, CP_AVERAGE_CPV, AVERAGE_CRR и PAY_FOR_CONVERSION_CRR необходимо выполнение ряда условий, см. описание соответствующих стратегий в помощи Директа.

Ручные стратегии

Стратегия на поиске

Допустимые стратегии в сетях

Типы кампаний, для которых доступна стратегия

HIGHEST_POSITION

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

MAXIMUM_COVERAGE

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

SERVING_OFF

MAXIMUM_COVERAGE

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

MANUAL_CPM

CPM_BANNER_CAMPAIGN

Автоматические стратегии

Стратегия на поиске

Допустимые стратегии в сетях

Типы кампаний, для которых доступна стратегия

AVERAGE_CPA

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPA_MULTIPLE_GOALS

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPA_PER_CAMP

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

AVERAGE_CPA_PER_FILTER

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

AVERAGE_CPC

NETWORK_DEFAULT

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPC_PER_CAMP

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

AVERAGE_CPC_PER_FILTER

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

AVERAGE_CPI

NETWORK_DEFAULT

MOBILE_APP_CAMPAIGN

SERVING_OFF

MOBILE_APP_CAMPAIGN

AVERAGE_ROI

NETWORK_DEFAULT

TEXT_CAMPAIGN, SMART_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN

AVERAGE_CRR

NETWORK_DEFAULT

TEXT_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_CRR

NETWORK_DEFAULT

TEXT_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_MULTIPLE_GOALS

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_PER_CAMPAIGN

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

PAY_FOR_CONVERSION_PER_FILTER

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

PAY_FOR_INSTALL

NETWORK_DEFAULT

MOBILE_APP_CAMPAIGN

SERVING_OFF

MOBILE_APP_CAMPAIGN

WB_MAXIMUM_APP_INSTALLS

NETWORK_DEFAULT

MOBILE_APP_CAMPAIGN

SERVING_OFF

MOBILE_APP_CAMPAIGN

WB_MAXIMUM_CLICKS

NETWORK_DEFAULT

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

WB_MAXIMUM_CONVERSION_RATE

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

WEEKLY_CLICK_PACKAGE

Внимание

Опция устарела и больше не поддерживается.

NETWORK_DEFAULT

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

SERVING_OFF

AVERAGE_CPA

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPA_PER_CAMP

SMART_CAMPAIGN

AVERAGE_CPA_PER_FILTER

SMART_CAMPAIGN

AVERAGE_CPC

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPC_PER_CAMP

SMART_CAMPAIGN

AVERAGE_CPC_PER_FILTER

SMART_CAMPAIGN

AVERAGE_CPI

MOBILE_APP_CAMPAIGN

AVERAGE_ROI

TEXT_CAMPAIGN, SMART_CAMPAIGN

AVERAGE_CRR

TEXT_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN

WB_MAXIMUM_APP_INSTALLS

MOBILE_APP_CAMPAIGN

WB_MAXIMUM_CLICKS

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

WB_MAXIMUM_CONVERSION_RATE

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

WEEKLY_CLICK_PACKAGE

Внимание

Опция устарела и больше не поддерживается.

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

CP_DECREASED_PRICE_FOR_REPEATED_IMPRESSIONS

CPM_BANNER_CAMPAIGN

CP_MAXIMUM_IMPRESSIONS

CPM_BANNER_CAMPAIGN

WB_DECREASED_PRICE_FOR_REPEATED_IMPRESSIONS

CPM_BANNER_CAMPAIGN

WB_MAXIMUM_IMPRESSIONS

CPM_BANNER_CAMPAIGN

PAY_FOR_CONVERSION

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_CRR

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_PER_CAMPAIGN

SMART_CAMPAIGN

PAY_FOR_CONVERSION_PER_FILTER

SMART_CAMPAIGN

WB_AVERAGE_CPV

CPM_BANNER_CAMPAIGN

CP_AVERAGE_CPV

CPM_BANNER_CAMPAIGN

PAY_FOR_INSTALL

MOBILE_APP_CAMPAIGN

«Ручное управление ставками с оптимизацией», включено раздельное управление ставками на поиске и в сетях.

См.  описание  в помощи Директа.

«Оптимизация конверсий», удерживать среднюю цену конверсии.

См.  описание  в помощи Директа.

«Максимум конверсий» с оплатой за клики, удерживать среднюю цену конверсии по нескольким целям.

См.  описание  в помощи Директа.

«Оптимизация количества конверсий», CPA на всю кампанию.

См.  описание  в помощи Директа.

«Оптимизация количества конверсий», CPA на каждый фильтр.

См.  описание  в помощи Директа.

«Оптимизация кликов», ограничивать по средней цене клика.

См.  описание  в помощи Директа.

«Оптимизация количества кликов», CPC на всю кампанию.

См.  описание  в помощи Директа.

«Оптимизация количества кликов», CPC на каждый фильтр.

См.  описание  в помощи Директа.

«Оптимизация количества установок приложения», удерживать среднюю цену установки.

См.  описание  в помощи Директа.

«Оптимизация доли рекламных расходов».

См.  описание  в помощи Директа.

«Оптимизация рентабельности».

См.  описание  в помощи Директа.

«Максимум просмотров видео», за период.

См.  описание  в помощи Директа.

«Снижение цены повторных показов», за период.

См.  описание  в помощи Директа.

«Максимум показов по минимальной цене», за период.

См.  описание  в помощи Директа.

«Ручное управление ставками с оптимизацией».

См.  описание  в помощи Директа.

«Ручное управление ставками» (для медийных кампаний).

См.  описание  в помощи Директа.

Настройки показов в сетях в зависимости от настроек на поиске.

«Оптимизация конверсий», оплата за конверсии (для кампаний с типом «Текстово-графические объявления», «Динамические объявления»).

См.  описание  в помощи Директа.

«Оптимизация доли рекламных расходов», оплата за конверсии.

См.  описание  в помощи Директа.

«Максимум конверсий» с оплатой за конверсии по каждой из указанных целей.

См.  описание  в помощи Директа.

«Оптимизация количества конверсий», оплата за конверсии (для кампаний с типом «Смарт-баннеры»).

См.  описание  в помощи Директа.

«Оптимизация количества конверсий», оплата за конверсии на каждый фильтр (для кампаний с типом «Смарт-баннеры»).

См.  описание  в помощи Директа.

«Оптимизация конверсий», оплата за установки.

См.  описание  в помощи Директа.

Показы отключены.

«Максимум просмотров видео», еженедельно.

См.  описание  в помощи Директа.

«Снижение цены повторных показов», еженедельно.

См.  описание  в помощи Директа.

«Оптимизация количества установок приложения», без указания средней цены установки.

См.  описание  в помощи Директа.

«Оптимизация кликов», ограничивать по недельному бюджету.

См.  описание  в помощи Директа.

«Оптимизация конверсий», без указания средней цены конверсии.

См.  описание  в помощи Директа.

«Максимум показов по минимальной цене», еженедельно.

См.  описание  в помощи Директа.

«Оптимизация кликов», ограничивать по пакету кликов.

См.  описание  в помощи Директа.

Внимание

Параметр устарел и больше не поддерживается.

Стратегии показа делятся на две категории:

Ручные стратегии — рекламодатель или агентство самостоятельно назначает ставки на условия показа: ключевые фразы, условия нацеливания на аудиторию, условия нацеливания для динамических объявлений.

Примечание

Назначенная вручную ставка за клик может автоматически снижаться или повышаться в зависимости от вероятности конверсии (см. раздел  Автоматическая корректировка ставок  помощи Директа).

Автоматические стратегии — ставки устанавливаются автоматически в соответствии с параметрами стратегии. Рекламодатель или агентство может указать приоритеты условий показа.

Подробная информация о стратегиях показа приведена в разделе  Какую стратегию показов выбрать  помощи Директа.

В API версии 5 стратегия показа настраивается раздельно на поиске и в сетях (Рекламной сети Яндекса и внешних сетях).

Совместимость стратегий представлена в таблицах ниже:

Внимание

Для подключения стратегий WB_MAXIMUM_CONVERSION_RATE, WB_MAXIMUM_APP_INSTALLS, AVERAGE_CPA, AVERAGE_CPA_MULTIPLE_GOALS, AVERAGE_CPI, AVERAGE_ROI, AVERAGE_CRR, PAY_FOR_CONVERSION, PAY_FOR_CONVERSION_MULTIPLE_GOALS, PAY_FOR_CONVERSION_PER_CAMPAIGN, PAY_FOR_INSTALL, WB_AVERAGE_CPV, CP_AVERAGE_CPV, AVERAGE_CRR и PAY_FOR_CONVERSION_CRR необходимо выполнение ряда условий, см. описание соответствующих стратегий в помощи Директа.

Ручные стратегии

Стратегия на поиске

Допустимые стратегии в сетях

Типы кампаний, для которых доступна стратегия

HIGHEST_POSITION

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

MAXIMUM_COVERAGE

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

SERVING_OFF

MAXIMUM_COVERAGE

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

MANUAL_CPM

CPM_BANNER_CAMPAIGN

Автоматические стратегии

Стратегия на поиске

Допустимые стратегии в сетях

Типы кампаний, для которых доступна стратегия

AVERAGE_CPA

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPA_MULTIPLE_GOALS

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPA_PER_CAMP

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

AVERAGE_CPA_PER_FILTER

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

AVERAGE_CPC

NETWORK_DEFAULT

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPC_PER_CAMP

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

AVERAGE_CPC_PER_FILTER

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

AVERAGE_CPI

NETWORK_DEFAULT

MOBILE_APP_CAMPAIGN

SERVING_OFF

MOBILE_APP_CAMPAIGN

AVERAGE_ROI

NETWORK_DEFAULT

TEXT_CAMPAIGN, SMART_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN

AVERAGE_CRR

NETWORK_DEFAULT

TEXT_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_CRR

NETWORK_DEFAULT

TEXT_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_MULTIPLE_GOALS

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_PER_CAMPAIGN

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

PAY_FOR_CONVERSION_PER_FILTER

NETWORK_DEFAULT

SMART_CAMPAIGN

SERVING_OFF

SMART_CAMPAIGN

PAY_FOR_INSTALL

NETWORK_DEFAULT

MOBILE_APP_CAMPAIGN

SERVING_OFF

MOBILE_APP_CAMPAIGN

WB_MAXIMUM_APP_INSTALLS

NETWORK_DEFAULT

MOBILE_APP_CAMPAIGN

SERVING_OFF

MOBILE_APP_CAMPAIGN

WB_MAXIMUM_CLICKS

NETWORK_DEFAULT

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

WB_MAXIMUM_CONVERSION_RATE

NETWORK_DEFAULT

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

WEEKLY_CLICK_PACKAGE

Внимание

Опция устарела и больше не поддерживается.

NETWORK_DEFAULT

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

SERVING_OFF

TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

SERVING_OFF

AVERAGE_CPA

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPA_PER_CAMP

SMART_CAMPAIGN

AVERAGE_CPA_PER_FILTER

SMART_CAMPAIGN

AVERAGE_CPC

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

AVERAGE_CPC_PER_CAMP

SMART_CAMPAIGN

AVERAGE_CPC_PER_FILTER

SMART_CAMPAIGN

AVERAGE_CPI

MOBILE_APP_CAMPAIGN

AVERAGE_ROI

TEXT_CAMPAIGN, SMART_CAMPAIGN

AVERAGE_CRR

TEXT_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN

WB_MAXIMUM_APP_INSTALLS

MOBILE_APP_CAMPAIGN

WB_MAXIMUM_CLICKS

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN

WB_MAXIMUM_CONVERSION_RATE

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

WEEKLY_CLICK_PACKAGE

Внимание

Опция устарела и больше не поддерживается.

TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN

CP_DECREASED_PRICE_FOR_REPEATED_IMPRESSIONS

CPM_BANNER_CAMPAIGN

CP_MAXIMUM_IMPRESSIONS

CPM_BANNER_CAMPAIGN

WB_DECREASED_PRICE_FOR_REPEATED_IMPRESSIONS

CPM_BANNER_CAMPAIGN

WB_MAXIMUM_IMPRESSIONS

CPM_BANNER_CAMPAIGN

PAY_FOR_CONVERSION

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_CRR

TEXT_CAMPAIGN, UNIFIED_CAMPAIGN

PAY_FOR_CONVERSION_PER_CAMPAIGN

SMART_CAMPAIGN

PAY_FOR_CONVERSION_PER_FILTER

SMART_CAMPAIGN

WB_AVERAGE_CPV

CPM_BANNER_CAMPAIGN

CP_AVERAGE_CPV

CPM_BANNER_CAMPAIGN

PAY_FOR_INSTALL

MOBILE_APP_CAMPAIGN

«Ручное управление ставками с оптимизацией», включено раздельное управление ставками на поиске и в сетях.

См.  описание  в помощи Директа.

«Оптимизация конверсий», удерживать среднюю цену конверсии.

См.  описание  в помощи Директа.

«Максимум конверсий» с оплатой за клики, удерживать среднюю цену конверсии по нескольким целям.

См.  описание  в помощи Директа.

«Оптимизация количества конверсий», CPA на всю кампанию.

См.  описание  в помощи Директа.

«Оптимизация количества конверсий», CPA на каждый фильтр.

См.  описание  в помощи Директа.

«Оптимизация кликов», ограничивать по средней цене клика.

См.  описание  в помощи Директа.

«Оптимизация количества кликов», CPC на всю кампанию.

См.  описание  в помощи Директа.

«Оптимизация количества кликов», CPC на каждый фильтр.

См.  описание  в помощи Директа.

«Оптимизация количества установок приложения», удерживать среднюю цену установки.

См.  описание  в помощи Директа.

«Оптимизация доли рекламных расходов».

См.  описание  в помощи Директа.

«Оптимизация рентабельности».

См.  описание  в помощи Директа.

«Максимум просмотров видео», за период.

См.  описание  в помощи Директа.

«Снижение цены повторных показов», за период.

См.  описание  в помощи Директа.

«Максимум показов по минимальной цене», за период.

См.  описание  в помощи Директа.

«Ручное управление ставками с оптимизацией».

См.  описание  в помощи Директа.

«Ручное управление ставками» (для медийных кампаний).

См.  описание  в помощи Директа.

Настройки показов в сетях в зависимости от настроек на поиске.

«Оптимизация конверсий», оплата за конверсии (для кампаний с типом «Текстово-графические объявления», «Динамические объявления»).

См.  описание  в помощи Директа.

«Оптимизация доли рекламных расходов», оплата за конверсии.

См.  описание  в помощи Директа.

«Максимум конверсий» с оплатой за конверсии по каждой из указанных целей.

См.  описание  в помощи Директа.

«Оптимизация количества конверсий», оплата за конверсии (для кампаний с типом «Смарт-баннеры»).

См.  описание  в помощи Директа.

«Оптимизация количества конверсий», оплата за конверсии на каждый фильтр (для кампаний с типом «Смарт-баннеры»).

См.  описание  в помощи Директа.

«Оптимизация конверсий», оплата за установки.

См.  описание  в помощи Директа.

Показы отключены.

«Максимум просмотров видео», еженедельно.

См.  описание  в помощи Директа.

«Снижение цены повторных показов», еженедельно.

См.  описание  в помощи Директа.

«Оптимизация количества установок приложения», без указания средней цены установки.

См.  описание  в помощи Директа.

«Оптимизация кликов», ограничивать по недельному бюджету.

См.  описание  в помощи Директа.

«Оптимизация конверсий», без указания средней цены конверсии.

См.  описание  в помощи Директа.

«Максимум показов по минимальной цене», еженедельно.

См.  описание  в помощи Директа.

«Оптимизация кликов», ограничивать по пакету кликов.

См.  описание  в помощи Директа.

Внимание

Параметр устарел и больше не поддерживается.

- Как начать работу с API
- Руководство разработчика   О руководстве   Обзор API Директа версии 5   Варианты использования   Быстрый старт   Основные объекты   Кампания (Campaign)   Стратегии показа   Параметры кампаний   Группа объявлений (AdGroup)   Объявление (Ad)   Набор быстрых ссылок (SitelinksSet)   Изображение (AdImage)   Видео (AdVideo)   Креатив (Creative)   Расширение (AdExtension)   Турбо-страница (TurboPage)   Ключевая фраза (Keyword)   Ставка (KeywordBid)   Корректировки (BidModifier)   Пакетная стратегия (Strategy)   Условие нацеливания на аудиторию (AudienceTarget)   Условие ретаргетинга и подбора аудитории (RetargetingList)   Фид (Feed)   Фильтр — условие нацеливания для смарт-баннеров (SmartAdTarget)   Условие нацеливания для динамических объявлений (DynamicFeedAdTarget)   Условие нацеливания для динамических объявлений (DynamicTextAdTarget — Webpage)   Клиент (Client)   Общий счет (SharedAccount)   Доступ и авторизация   Формат взаимодействия   Ограничения, баллы   Общие свойства методов API версии 5   Практика использования   Песочница   Список терминов
- О руководстве
- Обзор API Директа версии 5
- Варианты использования
- Быстрый старт
- Основные объекты   Кампания (Campaign)   Стратегии показа   Параметры кампаний   Группа объявлений (AdGroup)   Объявление (Ad)   Набор быстрых ссылок (SitelinksSet)   Изображение (AdImage)   Видео (AdVideo)   Креатив (Creative)   Расширение (AdExtension)   Турбо-страница (TurboPage)   Ключевая фраза (Keyword)   Ставка (KeywordBid)   Корректировки (BidModifier)   Пакетная стратегия (Strategy)   Условие нацеливания на аудиторию (AudienceTarget)   Условие ретаргетинга и подбора аудитории (RetargetingList)   Фид (Feed)   Фильтр — условие нацеливания для смарт-баннеров (SmartAdTarget)   Условие нацеливания для динамических объявлений (DynamicFeedAdTarget)   Условие нацеливания для динамических объявлений (DynamicTextAdTarget — Webpage)   Клиент (Client)   Общий счет (SharedAccount)
- Кампания (Campaign)   Стратегии показа   Параметры кампаний
- Стратегии показа
- Параметры кампаний
- Группа объявлений (AdGroup)
- Объявление (Ad)
- Набор быстрых ссылок (SitelinksSet)
- Изображение (AdImage)
- Видео (AdVideo)
- Креатив (Creative)
- Расширение (AdExtension)
- Турбо-страница (TurboPage)
- Ключевая фраза (Keyword)
- Ставка (KeywordBid)
- Корректировки (BidModifier)
- Пакетная стратегия (Strategy)
- Условие нацеливания на аудиторию (AudienceTarget)
- Условие ретаргетинга и подбора аудитории (RetargetingList)
- Фид (Feed)
- Фильтр — условие нацеливания для смарт-баннеров (SmartAdTarget)
- Условие нацеливания для динамических объявлений (DynamicFeedAdTarget)
- Условие нацеливания для динамических объявлений (DynamicTextAdTarget — Webpage)
- Клиент (Client)
- Общий счет (SharedAccount)
- Доступ и авторизация
- Формат взаимодействия
- Ограничения, баллы
- Общие свойства методов API версии 5
- Практика использования
- Песочница
- Список терминов
- Справочник API
- Статистика
- Примеры
- Руководство по переходу с версии 4
- Служба поддержки
- История изменений
- Обновление до Единой перфоманс-кампании

- О руководстве
- Обзор API Директа версии 5
- Варианты использования
- Быстрый старт
- Основные объекты   Кампания (Campaign)   Стратегии показа   Параметры кампаний   Группа объявлений (AdGroup)   Объявление (Ad)   Набор быстрых ссылок (SitelinksSet)   Изображение (AdImage)   Видео (AdVideo)   Креатив (Creative)   Расширение (AdExtension)   Турбо-страница (TurboPage)   Ключевая фраза (Keyword)   Ставка (KeywordBid)   Корректировки (BidModifier)   Пакетная стратегия (Strategy)   Условие нацеливания на аудиторию (AudienceTarget)   Условие ретаргетинга и подбора аудитории (RetargetingList)   Фид (Feed)   Фильтр — условие нацеливания для смарт-баннеров (SmartAdTarget)   Условие нацеливания для динамических объявлений (DynamicFeedAdTarget)   Условие нацеливания для динамических объявлений (DynamicTextAdTarget — Webpage)   Клиент (Client)   Общий счет (SharedAccount)
- Кампания (Campaign)   Стратегии показа   Параметры кампаний
- Стратегии показа
- Параметры кампаний
- Группа объявлений (AdGroup)
- Объявление (Ad)
- Набор быстрых ссылок (SitelinksSet)
- Изображение (AdImage)
- Видео (AdVideo)
- Креатив (Creative)
- Расширение (AdExtension)
- Турбо-страница (TurboPage)
- Ключевая фраза (Keyword)
- Ставка (KeywordBid)
- Корректировки (BidModifier)
- Пакетная стратегия (Strategy)
- Условие нацеливания на аудиторию (AudienceTarget)
- Условие ретаргетинга и подбора аудитории (RetargetingList)
- Фид (Feed)
- Фильтр — условие нацеливания для смарт-баннеров (SmartAdTarget)
- Условие нацеливания для динамических объявлений (DynamicFeedAdTarget)
- Условие нацеливания для динамических объявлений (DynamicTextAdTarget — Webpage)
- Клиент (Client)
- Общий счет (SharedAccount)
- Доступ и авторизация
- Формат взаимодействия
- Ограничения, баллы
- Общие свойства методов API версии 5
- Практика использования
- Песочница
- Список терминов

- Кампания (Campaign)   Стратегии показа   Параметры кампаний
- Стратегии показа
- Параметры кампаний
- Группа объявлений (AdGroup)
- Объявление (Ad)
- Набор быстрых ссылок (SitelinksSet)
- Изображение (AdImage)
- Видео (AdVideo)
- Креатив (Creative)
- Расширение (AdExtension)
- Турбо-страница (TurboPage)
- Ключевая фраза (Keyword)
- Ставка (KeywordBid)
- Корректировки (BidModifier)
- Пакетная стратегия (Strategy)
- Условие нацеливания на аудиторию (AudienceTarget)
- Условие ретаргетинга и подбора аудитории (RetargetingList)
- Фид (Feed)
- Фильтр — условие нацеливания для смарт-баннеров (SmartAdTarget)
- Условие нацеливания для динамических объявлений (DynamicFeedAdTarget)
- Условие нацеливания для динамических объявлений (DynamicTextAdTarget — Webpage)
- Клиент (Client)
- Общий счет (SharedAccount)

- Стратегии показа
- Параметры кампаний

- Ручные стратегии — рекламодатель или агентство самостоятельно назначает ставки на условия показа: ключевые фразы, условия нацеливания на аудиторию, условия нацеливания для динамических объявлений. 
 Примечание 
 Назначенная вручную ставка за клик может автоматически снижаться или повышаться в зависимости от вероятности конверсии (см. раздел  Автоматическая корректировка ставок  помощи Директа).
- Автоматические стратегии — ставки устанавливаются автоматически в соответствии с параметрами стратегии. Рекламодатель или агентство может указать приоритеты условий показа.

- Ручные стратегии
- Автоматические стратегии

- Ручные стратегии — рекламодатель или агентство самостоятельно назначает ставки на условия показа: ключевые фразы, условия нацеливания на аудиторию, условия нацеливания для динамических объявлений. 
 Примечание 
 Назначенная вручную ставка за клик может автоматически снижаться или повышаться в зависимости от вероятности конверсии (см. раздел  Автоматическая корректировка ставок  помощи Директа).
- Автоматические стратегии — ставки устанавливаются автоматически в соответствии с параметрами стратегии. Рекламодатель или агентство может указать приоритеты условий показа.

- Ручные стратегии
- Автоматические стратегии


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Стратегия на поиске | Допустимые стратегии в сетях |
| HIGHEST_POSITION | SERVING_OFF |
| MAXIMUM_COVERAGE | TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN |
| SERVING_OFF | MAXIMUM_COVERAGE |
| MANUAL_CPM | CPM_BANNER_CAMPAIGN |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Стратегия на поиске | Допустимые стратегии в сетях |
| AVERAGE_CPA | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| AVERAGE_CPA_MULTIPLE_GOALS | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| AVERAGE_CPA_PER_CAMP | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| AVERAGE_CPA_PER_FILTER | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| AVERAGE_CPC | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN |
| AVERAGE_CPC_PER_CAMP | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| AVERAGE_CPC_PER_FILTER | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| AVERAGE_CPI | NETWORK_DEFAULT |
| SERVING_OFF | MOBILE_APP_CAMPAIGN |
| AVERAGE_ROI | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN |
| AVERAGE_CRR | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_CRR | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_MULTIPLE_GOALS | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_PER_CAMPAIGN | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| PAY_FOR_CONVERSION_PER_FILTER | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| PAY_FOR_INSTALL | NETWORK_DEFAULT |
| SERVING_OFF | MOBILE_APP_CAMPAIGN |
| WB_MAXIMUM_APP_INSTALLS | NETWORK_DEFAULT |
| SERVING_OFF | MOBILE_APP_CAMPAIGN |
| WB_MAXIMUM_CLICKS | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN |
| WB_MAXIMUM_CONVERSION_RATE | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| WEEKLY_CLICK_PACKAGE 
 Внимание 
 Опция устарела и больше не поддерживается. | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN |
| SERVING_OFF | AVERAGE_CPA |
| AVERAGE_CPA_PER_CAMP | SMART_CAMPAIGN |
| AVERAGE_CPA_PER_FILTER | SMART_CAMPAIGN |
| AVERAGE_CPC | TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN |
| AVERAGE_CPC_PER_CAMP | SMART_CAMPAIGN |
| AVERAGE_CPC_PER_FILTER | SMART_CAMPAIGN |
| AVERAGE_CPI | MOBILE_APP_CAMPAIGN |
| AVERAGE_ROI | TEXT_CAMPAIGN, SMART_CAMPAIGN |
| AVERAGE_CRR | TEXT_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN |
| WB_MAXIMUM_APP_INSTALLS | MOBILE_APP_CAMPAIGN |
| WB_MAXIMUM_CLICKS | TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN |
| WB_MAXIMUM_CONVERSION_RATE | TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| WEEKLY_CLICK_PACKAGE 
 Внимание 
 Опция устарела и больше не поддерживается. | TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN |
| CP_DECREASED_PRICE_FOR_REPEATED_IMPRESSIONS | CPM_BANNER_CAMPAIGN |
| CP_MAXIMUM_IMPRESSIONS | CPM_BANNER_CAMPAIGN |
| WB_DECREASED_PRICE_FOR_REPEATED_IMPRESSIONS | CPM_BANNER_CAMPAIGN |
| WB_MAXIMUM_IMPRESSIONS | CPM_BANNER_CAMPAIGN |
| PAY_FOR_CONVERSION | TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_CRR | TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_PER_CAMPAIGN | SMART_CAMPAIGN |
| PAY_FOR_CONVERSION_PER_FILTER | SMART_CAMPAIGN |
| WB_AVERAGE_CPV | CPM_BANNER_CAMPAIGN |
| CP_AVERAGE_CPV | CPM_BANNER_CAMPAIGN |
| PAY_FOR_INSTALL | MOBILE_APP_CAMPAIGN |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Стратегия на поиске | Допустимые стратегии в сетях |
| HIGHEST_POSITION | SERVING_OFF |
| MAXIMUM_COVERAGE | TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN |
| SERVING_OFF | MAXIMUM_COVERAGE |
| MANUAL_CPM | CPM_BANNER_CAMPAIGN |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Стратегия на поиске | Допустимые стратегии в сетях |
| AVERAGE_CPA | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| AVERAGE_CPA_MULTIPLE_GOALS | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| AVERAGE_CPA_PER_CAMP | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| AVERAGE_CPA_PER_FILTER | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| AVERAGE_CPC | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN |
| AVERAGE_CPC_PER_CAMP | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| AVERAGE_CPC_PER_FILTER | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| AVERAGE_CPI | NETWORK_DEFAULT |
| SERVING_OFF | MOBILE_APP_CAMPAIGN |
| AVERAGE_ROI | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN |
| AVERAGE_CRR | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_CRR | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, SMART_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_MULTIPLE_GOALS | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_PER_CAMPAIGN | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| PAY_FOR_CONVERSION_PER_FILTER | NETWORK_DEFAULT |
| SERVING_OFF | SMART_CAMPAIGN |
| PAY_FOR_INSTALL | NETWORK_DEFAULT |
| SERVING_OFF | MOBILE_APP_CAMPAIGN |
| WB_MAXIMUM_APP_INSTALLS | NETWORK_DEFAULT |
| SERVING_OFF | MOBILE_APP_CAMPAIGN |
| WB_MAXIMUM_CLICKS | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN |
| WB_MAXIMUM_CONVERSION_RATE | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| WEEKLY_CLICK_PACKAGE 
 Внимание 
 Опция устарела и больше не поддерживается. | NETWORK_DEFAULT |
| SERVING_OFF | TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN |
| SERVING_OFF | AVERAGE_CPA |
| AVERAGE_CPA_PER_CAMP | SMART_CAMPAIGN |
| AVERAGE_CPA_PER_FILTER | SMART_CAMPAIGN |
| AVERAGE_CPC | TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN |
| AVERAGE_CPC_PER_CAMP | SMART_CAMPAIGN |
| AVERAGE_CPC_PER_FILTER | SMART_CAMPAIGN |
| AVERAGE_CPI | MOBILE_APP_CAMPAIGN |
| AVERAGE_ROI | TEXT_CAMPAIGN, SMART_CAMPAIGN |
| AVERAGE_CRR | TEXT_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN |
| WB_MAXIMUM_APP_INSTALLS | MOBILE_APP_CAMPAIGN |
| WB_MAXIMUM_CLICKS | TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, UNIFIED_CAMPAIGN |
| WB_MAXIMUM_CONVERSION_RATE | TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| WEEKLY_CLICK_PACKAGE 
 Внимание 
 Опция устарела и больше не поддерживается. | TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN |
| CP_DECREASED_PRICE_FOR_REPEATED_IMPRESSIONS | CPM_BANNER_CAMPAIGN |
| CP_MAXIMUM_IMPRESSIONS | CPM_BANNER_CAMPAIGN |
| WB_DECREASED_PRICE_FOR_REPEATED_IMPRESSIONS | CPM_BANNER_CAMPAIGN |
| WB_MAXIMUM_IMPRESSIONS | CPM_BANNER_CAMPAIGN |
| PAY_FOR_CONVERSION | TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_CRR | TEXT_CAMPAIGN, UNIFIED_CAMPAIGN |
| PAY_FOR_CONVERSION_PER_CAMPAIGN | SMART_CAMPAIGN |
| PAY_FOR_CONVERSION_PER_FILTER | SMART_CAMPAIGN |
| WB_AVERAGE_CPV | CPM_BANNER_CAMPAIGN |
| CP_AVERAGE_CPV | CPM_BANNER_CAMPAIGN |
| PAY_FOR_INSTALL | MOBILE_APP_CAMPAIGN |

