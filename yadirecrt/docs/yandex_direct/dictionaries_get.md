# get  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/dictionaries/get

**Дата скачивания:** 2025-07-01 12:35:53

---

## В этой статье :

# get

## Запрос

## Ответ

## Примеры

### Была ли статья полезна?

# get

## Запрос

## Ответ

## Примеры

### Была ли статья полезна?

Возвращает справочные данные: регионы, часовые пояса, курсы валют, список станций метрополитена, ограничения на значения параметров, внешние сети (SSP), сегменты Крипты для нацеливания по профилю пользователя и др.

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / GetRequest (для SOAP)

DictionaryNames

array of DictionaryNameEnum

Имена справочников, которые требуется получить.

Да

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / GetResponse (для SOAP)

AdCategories

array of AdCategoriesItem

Особые категории рекламируемых товаров и услуг.

См. раздел  Особая категория .

Constants

array of ConstantsItem

Ограничения на значения параметров.

Currencies

array of CurrenciesItem

Курсы валют, валютные параметры и ограничения.

GeoRegions

array of GeoRegionsItem

Регионы, доступные для таргетинга.

GeoRegionNames

array of GeoRegionNamesItem

Справочник названий регионов.

MetroStations

array of MetroStationsItem

Станции метрополитена (только для Москвы, Санкт-Петербурга и Киева).

OperationSystemVersions

array of OperationSystemVersionsItem

Версии операционных систем для рекламы мобильных приложений.

ProductivityAssertions

array of ProductivityAssertionsItem

Параметр утратил актуальность и не возвращается.

TimeZones

array of TimeZonesItem

Часовые пояса.

SupplySidePlatforms

array of SupplySidePlatformsItem

Внешние сети (SSP).

Interests

array of InterestsItem

Интересы к категориям мобильных приложений.

AudienceCriteriaTypes

array of AudienceCriteriaTypesItem

Социально-демографические характеристики и поведенческие признаки.

AudienceDemographicProfiles

array of AudienceDemographicProfilesItem

Сегменты по социально-демографическим характеристикам и поведенческим признакам для таргетинга по профилю пользователя.

AudienceInterests

array of AudienceInterestsItem

Сегменты по интересам пользователя для таргетинга по профилю пользователя.

FilterSchemas

array of FilterSchemasItem

Названия схем для создания фильтров.

Структура AdCategoriesItem

AdCategory

string

Обозначение особой категории (параметр объявления AdCategories).

Description

string

Краткое описание особой категории на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Message

string

Текст предупреждения, автоматически добавляемого в объявление, на языке, указанном в запросе в HTTP-заголовке  Accept-Language  (см. раздел  Предупреждения и возрастные ограничения в объявлениях  помощи Директа).

Структура ConstantsItem (для ограничений на значения параметров)

Name

string

Наименование ограничения:

MaximumAdTextLength — устарело, рекомендуем использовать MaximumTextAdTextLength.

MaximumAdTextWordLength — максимальное количество символов в каждом слове в тексте объявления.

MaximumAdTitleLength — устарело, рекомендуем использовать MaximumTextAdTitleLength.

MaximumAdTitleWordLength — максимальное количество символов в каждом слове в заголовке объявления.

MaximumDynamicTextAdTextLength — максимальное количество символов в тексте динамического объявления без учета «узких».

MaximumMobileAppAdTextLength — максимальное количество символов в тексте объявления для рекламы мобильных приложений.

MaximumMobileAppAdTitleLength — максимальное количество символов в заголовке объявления для рекламы мобильных приложений.

MaximumNumberOfNarrowCharacters — максимальное количество «узких» символов в заголовке или в тексте объявления.

MaximumSitelinkDescriptionLength — максимальное количество символов в описании быстрой ссылки.

MaximumSitelinksLength — максимальное суммарное количество символов в текстах всех быстрых ссылок в наборе.

MaximumSitelinksNumber — максимальное количество быстрых ссылок в наборе.

MaximumSitelinkTextLength — максимальное количество символов в тексте быстрой ссылки.

MaximumTextAdTextLength — максимальное количество символов в тексте текстово-графического объявления без учета «узких».

MaximumTextAdTitleLength — максимальное количество символов в заголовке 1 текстово-графического объявления без учета «узких».

MaximumTextAdTitle2Length — максимальное количество символов в заголовке 2 текстово-графического объявления без учета «узких».

Value

string

Значение ограничения.

Структура CurrenciesItem

Currency

string

Обозначение валюты (параметр кампании Currency).

Properties

array of ConstantsItem

Наименование и значение валютного параметра.

Структура ConstantsItem (для валютных параметров)

Name

string

Наименование валютного параметра:

См.  примеры  ниже.

Value

string

Значение валютного параметра.

Внимание

Все возвращаемые денежные значения представляют собой целые числа — результат умножения ставки или цены на 1 000 000.

Структура GeoRegionsItem

GeoRegionId

long

Идентификатор региона.

GeoRegionName

string

Название региона на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

GeoRegionType

string

Тип региона: World, Continent, Region, Country, Administrative area, District, City, City district, Village.

ParentId

long, nillable

Идентификатор вышестоящего региона.

Структура GeoRegionNamesItem

GeoRegionId

long

Идентификатор региона.

GeoRegionName

string

Название региона на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

GeoRegionType

string

Тип региона: World, Continent, Region, Country, Administrative area, District, City, City district, Village.

Структура MetroStationsItem

GeoRegionId

long

Идентификатор региона.

MetroStationId

long

Идентификатор станции метрополитена (параметр виртуальной визитки MetroStationId).

MetroStationName

string

Название станции (на русском языке).

Структура OperationSystemVersionsItem

OsName

string

Название операционной системы.

OsVersion

string

Версия операционной системы.

Структура TimeZonesItem

TimeZone

string

Обозначение часового пояса (параметр кампании TimeZone).

TimeZoneName

string

Описание часового пояса на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

UtcOffset

int

Смещение от UTC в секундах.

Структура SupplySidePlatformsItem

Title

string

Наименование внешней сети.

Структура InterestsItem

InterestId

long

Идентификатор интереса к категории мобильных приложений.

ParentId

long, nillable

Идентификатор вышестоящего интереса.

Name

string

Название интереса на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

IsTargetable

YesNoEnum

Признак того, что идентификатор интереса можно указывать в условии нацеливания на аудиторию.

Структура AudienceCriteriaTypesItem

Type

string

Идентификатор социально-демографической характеристики или поведенческого признака.

BlockElement

string

Группа характеристик, к которой относится характеристика:

Name

string

Название характеристики или признака на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Description

string

Описание характеристики или признака на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

CanSelect

CanSelectEnum

Допустимо ли указать в правиле отбора пользователей все сегменты по данной характеристике или признаку (например, указать все возрастные группы нельзя, а все профессии можно).

Структура AudienceDemographicProfilesItem

Id

long

Идентификатор сегмента по социально-демографической характеристике или поведенческому признаку.

Type

string

Идентификатор социально-демографической характеристики или поведенческого признака (параметр Type структуры  AudienceCriteriaTypes ).

Name

string

Название сегмента на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Description

string

Описание сегмента на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Структура AudienceInterestsItem

InterestKey

long

Идентификатор интереса пользователя.

Id

long

Идентификатор сегмента по интересам пользователя.

Идентификатор сегмента состоит из префикса, обозначающего тип интереса, и идентификатора интереса. Например,  InterestKey  равен 2499001182 (авиабилеты), а  Id  равен 102499001182 (краткосрочный интерес к авиабилетам).

ParentId

long

Идентификатор вышестоящего сегмента.

Name

string

Название сегмента на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Description

string

Описание сегмента на языке, указанном в запросе в HTTP-заголовке  Accept-Language

InterestType

InterestTypeEnum

Тип интереса: краткосрочный, долгосрочный или за любой период.

Структура FilterSchemasItem

Name

string

Название схемы для создания фильтров.

Fields

array of FilterSchemaItemFields

Параметры схемы.

Структура FilterSchemasItemFields (для параметров схемы создания фильтров)

Name

string

Название параметра.

Type

FieldTypeEnum

Тип параметра: Enum, Number, String.

EnumProps

EnumFieldStructure

Структура параметра типа Enum.

NumberProps

NumberFieldStructure

Структура параметра типа Number.

StringProps

StringFieldStructure

Структура параметра типа String.

Operators

array of OperatorStructure

Операторы.

Структура EnumFieldStructure (для структуры параметра типа Enum)

Values

EnumFieldStructureItem

Структура значений параметра типа Enum.

Структура EnumFieldStructureItem (для значений параметра типа Enum)

Items

array of strings

Массив значений.

Структура NumberFieldStructure (для структуры параметра типа Number)

Min

decimal

Минимальное значение.

Max

decimal

Максимальное значение.

Precision

integer

Точность.

Структура StringFieldStructure (для структуры параметра типа String)

MaxLength

integer

Максимальная длина возвращаемой строки.

MinLength

integer

Минимальная длина возвращаемой строки.

Структура OperatorStructure (для структуры оператора)

MaxItems

integer

Максимальное число элементов.

Type

OperatorEnum

Оператор: CONTAINS_ANY, EQUALS_ANY, EXISTS, GREATER_THAN, IN_RANGE, LESS_THAN, NOT_CONTAINS_ALL.

Пример запроса: получение справочника валют

Пример ответа

Возвращает справочные данные: регионы, часовые пояса, курсы валют, список станций метрополитена, ограничения на значения параметров, внешние сети (SSP), сегменты Крипты для нацеливания по профилю пользователя и др.

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / GetRequest (для SOAP)

DictionaryNames

array of DictionaryNameEnum

Имена справочников, которые требуется получить.

Да

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / GetResponse (для SOAP)

AdCategories

array of AdCategoriesItem

Особые категории рекламируемых товаров и услуг.

См. раздел  Особая категория .

Constants

array of ConstantsItem

Ограничения на значения параметров.

Currencies

array of CurrenciesItem

Курсы валют, валютные параметры и ограничения.

GeoRegions

array of GeoRegionsItem

Регионы, доступные для таргетинга.

GeoRegionNames

array of GeoRegionNamesItem

Справочник названий регионов.

MetroStations

array of MetroStationsItem

Станции метрополитена (только для Москвы, Санкт-Петербурга и Киева).

OperationSystemVersions

array of OperationSystemVersionsItem

Версии операционных систем для рекламы мобильных приложений.

ProductivityAssertions

array of ProductivityAssertionsItem

Параметр утратил актуальность и не возвращается.

TimeZones

array of TimeZonesItem

Часовые пояса.

SupplySidePlatforms

array of SupplySidePlatformsItem

Внешние сети (SSP).

Interests

array of InterestsItem

Интересы к категориям мобильных приложений.

AudienceCriteriaTypes

array of AudienceCriteriaTypesItem

Социально-демографические характеристики и поведенческие признаки.

AudienceDemographicProfiles

array of AudienceDemographicProfilesItem

Сегменты по социально-демографическим характеристикам и поведенческим признакам для таргетинга по профилю пользователя.

AudienceInterests

array of AudienceInterestsItem

Сегменты по интересам пользователя для таргетинга по профилю пользователя.

FilterSchemas

array of FilterSchemasItem

Названия схем для создания фильтров.

Структура AdCategoriesItem

AdCategory

string

Обозначение особой категории (параметр объявления AdCategories).

Description

string

Краткое описание особой категории на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Message

string

Текст предупреждения, автоматически добавляемого в объявление, на языке, указанном в запросе в HTTP-заголовке  Accept-Language  (см. раздел  Предупреждения и возрастные ограничения в объявлениях  помощи Директа).

Структура ConstantsItem (для ограничений на значения параметров)

Name

string

Наименование ограничения:

MaximumAdTextLength — устарело, рекомендуем использовать MaximumTextAdTextLength.

MaximumAdTextWordLength — максимальное количество символов в каждом слове в тексте объявления.

MaximumAdTitleLength — устарело, рекомендуем использовать MaximumTextAdTitleLength.

MaximumAdTitleWordLength — максимальное количество символов в каждом слове в заголовке объявления.

MaximumDynamicTextAdTextLength — максимальное количество символов в тексте динамического объявления без учета «узких».

MaximumMobileAppAdTextLength — максимальное количество символов в тексте объявления для рекламы мобильных приложений.

MaximumMobileAppAdTitleLength — максимальное количество символов в заголовке объявления для рекламы мобильных приложений.

MaximumNumberOfNarrowCharacters — максимальное количество «узких» символов в заголовке или в тексте объявления.

MaximumSitelinkDescriptionLength — максимальное количество символов в описании быстрой ссылки.

MaximumSitelinksLength — максимальное суммарное количество символов в текстах всех быстрых ссылок в наборе.

MaximumSitelinksNumber — максимальное количество быстрых ссылок в наборе.

MaximumSitelinkTextLength — максимальное количество символов в тексте быстрой ссылки.

MaximumTextAdTextLength — максимальное количество символов в тексте текстово-графического объявления без учета «узких».

MaximumTextAdTitleLength — максимальное количество символов в заголовке 1 текстово-графического объявления без учета «узких».

MaximumTextAdTitle2Length — максимальное количество символов в заголовке 2 текстово-графического объявления без учета «узких».

Value

string

Значение ограничения.

Структура CurrenciesItem

Currency

string

Обозначение валюты (параметр кампании Currency).

Properties

array of ConstantsItem

Наименование и значение валютного параметра.

Структура ConstantsItem (для валютных параметров)

Name

string

Наименование валютного параметра:

См.  примеры  ниже.

Value

string

Значение валютного параметра.

Внимание

Все возвращаемые денежные значения представляют собой целые числа — результат умножения ставки или цены на 1 000 000.

Структура GeoRegionsItem

GeoRegionId

long

Идентификатор региона.

GeoRegionName

string

Название региона на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

GeoRegionType

string

Тип региона: World, Continent, Region, Country, Administrative area, District, City, City district, Village.

ParentId

long, nillable

Идентификатор вышестоящего региона.

Структура GeoRegionNamesItem

GeoRegionId

long

Идентификатор региона.

GeoRegionName

string

Название региона на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

GeoRegionType

string

Тип региона: World, Continent, Region, Country, Administrative area, District, City, City district, Village.

Структура MetroStationsItem

GeoRegionId

long

Идентификатор региона.

MetroStationId

long

Идентификатор станции метрополитена (параметр виртуальной визитки MetroStationId).

MetroStationName

string

Название станции (на русском языке).

Структура OperationSystemVersionsItem

OsName

string

Название операционной системы.

OsVersion

string

Версия операционной системы.

Структура TimeZonesItem

TimeZone

string

Обозначение часового пояса (параметр кампании TimeZone).

TimeZoneName

string

Описание часового пояса на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

UtcOffset

int

Смещение от UTC в секундах.

Структура SupplySidePlatformsItem

Title

string

Наименование внешней сети.

Структура InterestsItem

InterestId

long

Идентификатор интереса к категории мобильных приложений.

ParentId

long, nillable

Идентификатор вышестоящего интереса.

Name

string

Название интереса на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

IsTargetable

YesNoEnum

Признак того, что идентификатор интереса можно указывать в условии нацеливания на аудиторию.

Структура AudienceCriteriaTypesItem

Type

string

Идентификатор социально-демографической характеристики или поведенческого признака.

BlockElement

string

Группа характеристик, к которой относится характеристика:

Name

string

Название характеристики или признака на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Description

string

Описание характеристики или признака на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

CanSelect

CanSelectEnum

Допустимо ли указать в правиле отбора пользователей все сегменты по данной характеристике или признаку (например, указать все возрастные группы нельзя, а все профессии можно).

Структура AudienceDemographicProfilesItem

Id

long

Идентификатор сегмента по социально-демографической характеристике или поведенческому признаку.

Type

string

Идентификатор социально-демографической характеристики или поведенческого признака (параметр Type структуры  AudienceCriteriaTypes ).

Name

string

Название сегмента на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Description

string

Описание сегмента на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Структура AudienceInterestsItem

InterestKey

long

Идентификатор интереса пользователя.

Id

long

Идентификатор сегмента по интересам пользователя.

Идентификатор сегмента состоит из префикса, обозначающего тип интереса, и идентификатора интереса. Например,  InterestKey  равен 2499001182 (авиабилеты), а  Id  равен 102499001182 (краткосрочный интерес к авиабилетам).

ParentId

long

Идентификатор вышестоящего сегмента.

Name

string

Название сегмента на языке, указанном в запросе в HTTP-заголовке  Accept-Language .

Description

string

Описание сегмента на языке, указанном в запросе в HTTP-заголовке  Accept-Language

InterestType

InterestTypeEnum

Тип интереса: краткосрочный, долгосрочный или за любой период.

Структура FilterSchemasItem

Name

string

Название схемы для создания фильтров.

Fields

array of FilterSchemaItemFields

Параметры схемы.

Структура FilterSchemasItemFields (для параметров схемы создания фильтров)

Name

string

Название параметра.

Type

FieldTypeEnum

Тип параметра: Enum, Number, String.

EnumProps

EnumFieldStructure

Структура параметра типа Enum.

NumberProps

NumberFieldStructure

Структура параметра типа Number.

StringProps

StringFieldStructure

Структура параметра типа String.

Operators

array of OperatorStructure

Операторы.

Структура EnumFieldStructure (для структуры параметра типа Enum)

Values

EnumFieldStructureItem

Структура значений параметра типа Enum.

Структура EnumFieldStructureItem (для значений параметра типа Enum)

Items

array of strings

Массив значений.

Структура NumberFieldStructure (для структуры параметра типа Number)

Min

decimal

Минимальное значение.

Max

decimal

Максимальное значение.

Precision

integer

Точность.

Структура StringFieldStructure (для структуры параметра типа String)

MaxLength

integer

Максимальная длина возвращаемой строки.

MinLength

integer

Минимальная длина возвращаемой строки.

Структура OperatorStructure (для структуры оператора)

MaxItems

integer

Максимальное число элементов.

Type

OperatorEnum

Оператор: CONTAINS_ANY, EQUALS_ANY, EXISTS, GREATER_THAN, IN_RANGE, LESS_THAN, NOT_CONTAINS_ALL.

Пример запроса: получение справочника валют

Пример ответа

- Как начать работу с API
- Руководство разработчика
- Справочник API   О справочнике   AdExtensions: операции с расширениями объявлений   AdGroups: операции с группами объявлений   AdImages: операции с изображениями   Ads: операции с объявлениями   AdVideos: операции с видео   AgencyClients: управление клиентами агентства   AudienceTargets: управление условиями нацеливания на аудиторию   Bids: управление ставками   Businesses: получение профилей организаций   BidModifiers: управление корректировками ставок   Campaigns: управление кампаниями   Changes: проверка наличия изменений   Clients: управление параметрами рекламодателя и настройками пользователя   Creatives: получение креативов   Dictionaries: получение справочных данных   get   getGeoRegions   Feeds: операции с фидами   KeywordBids: управление ставками   Keywords: управление ключевыми фразами и автотаргетингами   KeywordsResearch: предобработка ключевых фраз   Leads: получение данных из форм на Турбо-страницах   NegativeKeywordSharedSets: управление наборами минус-фраз   RetargetingLists: управление условиями ретаргетинга и подбора аудитории   Sitelinks: операции с быстрыми ссылками   Strategies: операции с пакетными стратегиями   TurboPages: получение параметров Турбо-страниц   Ошибки и предупреждения   Справочные данные
- О справочнике
- AdExtensions: операции с расширениями объявлений
- AdGroups: операции с группами объявлений
- AdImages: операции с изображениями
- Ads: операции с объявлениями
- AdVideos: операции с видео
- AgencyClients: управление клиентами агентства
- AudienceTargets: управление условиями нацеливания на аудиторию
- Bids: управление ставками
- Businesses: получение профилей организаций
- BidModifiers: управление корректировками ставок
- Campaigns: управление кампаниями
- Changes: проверка наличия изменений
- Clients: управление параметрами рекламодателя и настройками пользователя
- Creatives: получение креативов
- Dictionaries: получение справочных данных   get   getGeoRegions
- get
- getGeoRegions
- Feeds: операции с фидами
- KeywordBids: управление ставками
- Keywords: управление ключевыми фразами и автотаргетингами
- KeywordsResearch: предобработка ключевых фраз
- Leads: получение данных из форм на Турбо-страницах
- NegativeKeywordSharedSets: управление наборами минус-фраз
- RetargetingLists: управление условиями ретаргетинга и подбора аудитории
- Sitelinks: операции с быстрыми ссылками
- Strategies: операции с пакетными стратегиями
- TurboPages: получение параметров Турбо-страниц
- Ошибки и предупреждения
- Справочные данные
- Статистика
- Примеры
- Руководство по переходу с версии 4
- Служба поддержки
- История изменений
- Обновление до Единой перфоманс-кампании

- О справочнике
- AdExtensions: операции с расширениями объявлений
- AdGroups: операции с группами объявлений
- AdImages: операции с изображениями
- Ads: операции с объявлениями
- AdVideos: операции с видео
- AgencyClients: управление клиентами агентства
- AudienceTargets: управление условиями нацеливания на аудиторию
- Bids: управление ставками
- Businesses: получение профилей организаций
- BidModifiers: управление корректировками ставок
- Campaigns: управление кампаниями
- Changes: проверка наличия изменений
- Clients: управление параметрами рекламодателя и настройками пользователя
- Creatives: получение креативов
- Dictionaries: получение справочных данных   get   getGeoRegions
- get
- getGeoRegions
- Feeds: операции с фидами
- KeywordBids: управление ставками
- Keywords: управление ключевыми фразами и автотаргетингами
- KeywordsResearch: предобработка ключевых фраз
- Leads: получение данных из форм на Турбо-страницах
- NegativeKeywordSharedSets: управление наборами минус-фраз
- RetargetingLists: управление условиями ретаргетинга и подбора аудитории
- Sitelinks: операции с быстрыми ссылками
- Strategies: операции с пакетными стратегиями
- TurboPages: получение параметров Турбо-страниц
- Ошибки и предупреждения
- Справочные данные

- get
- getGeoRegions

- Запрос
- Ответ
- Примеры

- Запрос
- Ответ
- Примеры

- MaximumAdTextLength — устарело, рекомендуем использовать MaximumTextAdTextLength.
- MaximumAdTextWordLength — максимальное количество символов в каждом слове в тексте объявления.
- MaximumAdTitleLength — устарело, рекомендуем использовать MaximumTextAdTitleLength.
- MaximumAdTitleWordLength — максимальное количество символов в каждом слове в заголовке объявления.
- MaximumDynamicTextAdTextLength — максимальное количество символов в тексте динамического объявления без учета «узких».
- MaximumMobileAppAdTextLength — максимальное количество символов в тексте объявления для рекламы мобильных приложений.
- MaximumMobileAppAdTitleLength — максимальное количество символов в заголовке объявления для рекламы мобильных приложений.
- MaximumNumberOfNarrowCharacters — максимальное количество «узких» символов в заголовке или в тексте объявления.
- MaximumSitelinkDescriptionLength — максимальное количество символов в описании быстрой ссылки.
- MaximumSitelinksLength — максимальное суммарное количество символов в текстах всех быстрых ссылок в наборе.
- MaximumSitelinksNumber — максимальное количество быстрых ссылок в наборе.
- MaximumSitelinkTextLength — максимальное количество символов в тексте быстрой ссылки.
- MaximumTextAdTextLength — максимальное количество символов в тексте текстово-графического объявления без учета «узких».
- MaximumTextAdTitleLength — максимальное количество символов в заголовке 1 текстово-графического объявления без учета «узких».
- MaximumTextAdTitle2Length — максимальное количество символов в заголовке 2 текстово-графического объявления без учета «узких».

- FullName — название валюты на языке, указанном в запросе в HTTP-заголовке  Accept-Language ;
- AutobudgetAvgCpaWarning — средняя цена конверсии;
- BidIncrement — шаг торгов;
- MaxAutobudget — максимальная сумма недельного автобюджета;
- MaximumAverageCPV — максимальная средняя цена за просмотр видео для стратегий CP_AVERAGE_CPV, WB_AVERAGE_CPV;
- MaximumBid — максимальная ставка за клик (техническое ограничение);
- MaximumCPM — максимальная ставка или цена за тысячу показов для медийной рекламы;
- MaxDailyBudgetForPeriod — максимальная сумма бюджета на фиксированный период;
- MaximumPayForConversionCPA — максимальное значение цены конверсии для стратегий PAY_FOR_CONVERSION, PAY_FOR_CONVERSION_PER_CAMPAIGN, PAY_FOR_INSTALL;
- MinimumAccountDailyBudget — минимальный дневной бюджет общего счета;
- MinimumAverageCPA — минимальное значение средней цены конверсии для стратегии AVERAGE_CPA, минимальное значение средней цены установки для стратегии AVERAGE_CPI, минимальное значение цены конверсии для стратегии PAY_FOR_CONVERSION;
- MinimumAverageCPC — минимальное значение средней цены клика для стратегий AVERAGE_CPC, WEEKLY_CLICK_PACKAGE;
- MinimumAverageCPV — минимальная средняя цена за просмотр видео для стратегий CP_AVERAGE_CPV, WB_AVERAGE_CPV;
- MinimumBid — минимальная ставка за клик;
- MinCpcCpaPerformance — минимальная цена CPC/CPA для смарт-баннеров;
- MinimumCPM — минимальная ставка или цена за тысячу показов для медийной рекламы;
- MinimumDailyBudget — минимальный дневной бюджет кампании;
- MinDailyBudgetForPeriod — минимальная сумма бюджета на фиксированный период;
- MinimumPayment — минимальный платеж (без учета НДС);
- MinimumPayForConversionCPA — минимальное значение цены конверсии для стратегий PAY_FOR_CONVERSION, PAY_FOR_CONVERSION_PER_CAMPAIGN, PAY_FOR_INSTALL;
- MinimumTransferAmount — минимальная сумма перевода между кампаниями;
- MinimumWeeklySpendLimit — минимальный недельный бюджет.

- SOCIAL — пол, возраст, доход.
- EXTENDED_SOCIAL — семейное положение, дети, профессия.
- BEHAVIORAL_INDICATORS — поведенческие признаки.

- Запрос
- Ответ
- Примеры

- MaximumAdTextLength — устарело, рекомендуем использовать MaximumTextAdTextLength.
- MaximumAdTextWordLength — максимальное количество символов в каждом слове в тексте объявления.
- MaximumAdTitleLength — устарело, рекомендуем использовать MaximumTextAdTitleLength.
- MaximumAdTitleWordLength — максимальное количество символов в каждом слове в заголовке объявления.
- MaximumDynamicTextAdTextLength — максимальное количество символов в тексте динамического объявления без учета «узких».
- MaximumMobileAppAdTextLength — максимальное количество символов в тексте объявления для рекламы мобильных приложений.
- MaximumMobileAppAdTitleLength — максимальное количество символов в заголовке объявления для рекламы мобильных приложений.
- MaximumNumberOfNarrowCharacters — максимальное количество «узких» символов в заголовке или в тексте объявления.
- MaximumSitelinkDescriptionLength — максимальное количество символов в описании быстрой ссылки.
- MaximumSitelinksLength — максимальное суммарное количество символов в текстах всех быстрых ссылок в наборе.
- MaximumSitelinksNumber — максимальное количество быстрых ссылок в наборе.
- MaximumSitelinkTextLength — максимальное количество символов в тексте быстрой ссылки.
- MaximumTextAdTextLength — максимальное количество символов в тексте текстово-графического объявления без учета «узких».
- MaximumTextAdTitleLength — максимальное количество символов в заголовке 1 текстово-графического объявления без учета «узких».
- MaximumTextAdTitle2Length — максимальное количество символов в заголовке 2 текстово-графического объявления без учета «узких».

- FullName — название валюты на языке, указанном в запросе в HTTP-заголовке  Accept-Language ;
- AutobudgetAvgCpaWarning — средняя цена конверсии;
- BidIncrement — шаг торгов;
- MaxAutobudget — максимальная сумма недельного автобюджета;
- MaximumAverageCPV — максимальная средняя цена за просмотр видео для стратегий CP_AVERAGE_CPV, WB_AVERAGE_CPV;
- MaximumBid — максимальная ставка за клик (техническое ограничение);
- MaximumCPM — максимальная ставка или цена за тысячу показов для медийной рекламы;
- MaxDailyBudgetForPeriod — максимальная сумма бюджета на фиксированный период;
- MaximumPayForConversionCPA — максимальное значение цены конверсии для стратегий PAY_FOR_CONVERSION, PAY_FOR_CONVERSION_PER_CAMPAIGN, PAY_FOR_INSTALL;
- MinimumAccountDailyBudget — минимальный дневной бюджет общего счета;
- MinimumAverageCPA — минимальное значение средней цены конверсии для стратегии AVERAGE_CPA, минимальное значение средней цены установки для стратегии AVERAGE_CPI, минимальное значение цены конверсии для стратегии PAY_FOR_CONVERSION;
- MinimumAverageCPC — минимальное значение средней цены клика для стратегий AVERAGE_CPC, WEEKLY_CLICK_PACKAGE;
- MinimumAverageCPV — минимальная средняя цена за просмотр видео для стратегий CP_AVERAGE_CPV, WB_AVERAGE_CPV;
- MinimumBid — минимальная ставка за клик;
- MinCpcCpaPerformance — минимальная цена CPC/CPA для смарт-баннеров;
- MinimumCPM — минимальная ставка или цена за тысячу показов для медийной рекламы;
- MinimumDailyBudget — минимальный дневной бюджет кампании;
- MinDailyBudgetForPeriod — минимальная сумма бюджета на фиксированный период;
- MinimumPayment — минимальный платеж (без учета НДС);
- MinimumPayForConversionCPA — минимальное значение цены конверсии для стратегий PAY_FOR_CONVERSION, PAY_FOR_CONVERSION_PER_CAMPAIGN, PAY_FOR_INSTALL;
- MinimumTransferAmount — минимальная сумма перевода между кампаниями;
- MinimumWeeklySpendLimit — минимальный недельный бюджет.

- SOCIAL — пол, возраст, доход.
- EXTENDED_SOCIAL — семейное положение, дети, профессия.
- BEHAVIORAL_INDICATORS — поведенческие признаки.

```
{
   "method" :  "get" ,
   "params" : {  /* params */ 
     "DictionaryNames" : [(  "Currencies" 
                        |  "MetroStations" 
                        |  "GeoRegions" 
                        |  "GeoRegionNames" 
                        |  "TimeZones" 
                        |  "Constants" 
                        |  "AdCategories" 
                        |  "OperationSystemVersions" 
                        |  "ProductivityAssertions" 
                        |  "SupplySidePlatforms" 
                        |  "Interests" 
                        |  "AudienceCriteriaTypes" 
                        |  "AudienceDemographicProfiles" 
                        |  "AudienceInterests" 
                        |  "FilterSchemas" ), ... ]  /* required */ 
  }
}
```

```
{
   "method" :  "get" ,
   "params" : {  /* params */ 
     "DictionaryNames" : [(  "Currencies" 
                        |  "MetroStations" 
                        |  "GeoRegions" 
                        |  "GeoRegionNames" 
                        |  "TimeZones" 
                        |  "Constants" 
                        |  "AdCategories" 
                        |  "OperationSystemVersions" 
                        |  "ProductivityAssertions" 
                        |  "SupplySidePlatforms" 
                        |  "Interests" 
                        |  "AudienceCriteriaTypes" 
                        |  "AudienceDemographicProfiles" 
                        |  "AudienceInterests" 
                        |  "FilterSchemas" ), ... ]  /* required */ 
  }
}
```

`DictionaryNames`

```
{
   "result" : {
     "Currencies" : [{   /* CurrenciesItem */ 
       "Currency" : (string),  /* required */ 
       "Properties" : [{   /* ConstantsItem */ 
         "Name" : (string),  /* required */ 
         "Value" : (string)  /* required */ 
      }, ... ]  /* required */ 
    }, ... ],
     "MetroStations" : [{   /* MetroStationsItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "MetroStationId" : (long),  /* required */ 
       "MetroStationName" : (string)  /* required */ 
    }, ... ],
     "GeoRegions" : [{   /* GeoRegionsItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "GeoRegionName" : (string),  /* required */ 
       "GeoRegionType" : (string),  /* required */ 
       "ParentId" : (long)  /* nillable */ 
    }, ... ],
     "GeoRegionNames" : [{   /* GeoRegionNamesItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "GeoRegionName" : (string),  /* required */ 
       "GeoRegionType" : (string),  /* required */ 
    }, ... ],
     "TimeZones" : [{   /* TimeZonesItem */ 
       "TimeZone" : (string),  /* required */ 
       "TimeZoneName" : (string),  /* required */ 
       "UtcOffset" : (int)  /* required */ 
    }, ... ],
     "Constants" : [{   /* ConstantsItem */ 
       "Name" : (string),  /* required */ 
       "Value" : (string)  /* required */ 
    }, ... ],
     "AdCategories" : [{   /* AdCategoriesItem */ 
       "AdCategory" : (string),  /* required */ 
       "Description" : (string),  /* required */ 
       "Message" : (string)  /* required */ 
    }, ... ],
     "OperationSystemVersions" : [{   /* OperationSystemVersionsItem */ 
       "OsName" : (string),  /* required */ 
       "OsVersion" : (string)  /* required */ 
    }, ... ],
     "SupplySidePlatforms" : [{   /* SupplySidePlatformsItem */ 
       "Title" : (string)  /* required */ 
    }, ... ],
     "Interests" : [{   /* InterestsItem */ 
       "InterestId" : (long),
       "ParentId" : (long),  /* nillable */ 
       "Name" : (string),
       "IsTargetable" : (  "YES"  |  "NO"  )
    }, ... ],
     "AudienceCriteriaTypes" : [{  /* AudienceCriteriaTypesItem */ 
       "Type" : (string),  /* required */ 
       "BlockElement" : (string),   /* required */ 
       "Name" : (string),   /* required */ 
       "Description" : (string),   /* required */ 
       "CanSelect" : (  "ALL"  |  "EXCEPT_ALL"  )  /* required */ 
    }, ... ],
     "AudienceDemographicProfiles" : [{  /* AudienceDemographicProfilesItem */ 
       "Id" : (long),  /* required */ 
       "Type" : (string),  /* required */ 
       "Name" : (string),  /* required */ 
       "Description" : (string)  /* required */ 
    }, ... ],
     "AudienceInterests" : [{  /* AudienceInterestsItem */ 
       "InterestKey" : (long),  /* required */ 
       "Id" : (long),  /* required */ 
       "ParentId" : (long),  /* required */ 
       "Name" : (string),  /* required */ 
       "Description" : (string),  /* required */ 
       "InterestType" : (  "SHORT_TERM"  |  "LONG_TERM"  |  "ANY"  )   /* required */ 
    }, ... ],
     "FilterSchemas" : [{  /* FilterSchemasItem */ 
       "Name" : (string),  /* required */ 
       "Fields" : [{  /* required */ 
         "Name" : (string),  /* required */ 
         "Type" : ( "Enum" ,  "Number" ,  "String" ),  /* required */ 
         "EnumProps" : {
           "Values" : {  /* required */ 
             "Items" : [(string)]  /* required */ 
          },
        },
         "NumberProps" : {
           "Min" : (decimal),  /* required */ 
           "Max" : (decimal),  /* required */ 
           "Precision" : (integer)  /* required */ 
        },
         "StringProps" : {
           "MaxLength" : (integer),  /* required */ 
           "MinLength" : (integer)  /* required */ 
        },
         "Operators" : [{  /* required */ 
           "MaxItems" : (integer),  /* required */ 
           "Type" : ( "CONTAINS_ANY"  |  "EQUALS_ANY"  |  "EXISTS"  |  "GREATER_THAN"  |  "IN_RANGE"  |  "LESS_THAN"  |  "NOT_CONTAINS_ALL" )  /* required */ 
        }, ...]
    }, ... ]
  }
}
```

```
{
   "result" : {
     "Currencies" : [{   /* CurrenciesItem */ 
       "Currency" : (string),  /* required */ 
       "Properties" : [{   /* ConstantsItem */ 
         "Name" : (string),  /* required */ 
         "Value" : (string)  /* required */ 
      }, ... ]  /* required */ 
    }, ... ],
     "MetroStations" : [{   /* MetroStationsItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "MetroStationId" : (long),  /* required */ 
       "MetroStationName" : (string)  /* required */ 
    }, ... ],
     "GeoRegions" : [{   /* GeoRegionsItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "GeoRegionName" : (string),  /* required */ 
       "GeoRegionType" : (string),  /* required */ 
       "ParentId" : (long)  /* nillable */ 
    }, ... ],
     "GeoRegionNames" : [{   /* GeoRegionNamesItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "GeoRegionName" : (string),  /* required */ 
       "GeoRegionType" : (string),  /* required */ 
    }, ... ],
     "TimeZones" : [{   /* TimeZonesItem */ 
       "TimeZone" : (string),  /* required */ 
       "TimeZoneName" : (string),  /* required */ 
       "UtcOffset" : (int)  /* required */ 
    }, ... ],
     "Constants" : [{   /* ConstantsItem */ 
       "Name" : (string),  /* required */ 
       "Value" : (string)  /* required */ 
    }, ... ],
     "AdCategories" : [{   /* AdCategoriesItem */ 
       "AdCategory" : (string),  /* required */ 
       "Description" : (string),  /* required */ 
       "Message" : (string)  /* required */ 
    }, ... ],
     "OperationSystemVersions" : [{   /* OperationSystemVersionsItem */ 
       "OsName" : (string),  /* required */ 
       "OsVersion" : (string)  /* required */ 
    }, ... ],
     "SupplySidePlatforms" : [{   /* SupplySidePlatformsItem */ 
       "Title" : (string)  /* required */ 
    }, ... ],
     "Interests" : [{   /* InterestsItem */ 
       "InterestId" : (long),
       "ParentId" : (long),  /* nillable */ 
       "Name" : (string),
       "IsTargetable" : (  "YES"  |  "NO"  )
    }, ... ],
     "AudienceCriteriaTypes" : [{  /* AudienceCriteriaTypesItem */ 
       "Type" : (string),  /* required */ 
       "BlockElement" : (string),   /* required */ 
       "Name" : (string),   /* required */ 
       "Description" : (string),   /* required */ 
       "CanSelect" : (  "ALL"  |  "EXCEPT_ALL"  )  /* required */ 
    }, ... ],
     "AudienceDemographicProfiles" : [{  /* AudienceDemographicProfilesItem */ 
       "Id" : (long),  /* required */ 
       "Type" : (string),  /* required */ 
       "Name" : (string),  /* required */ 
       "Description" : (string)  /* required */ 
    }, ... ],
     "AudienceInterests" : [{  /* AudienceInterestsItem */ 
       "InterestKey" : (long),  /* required */ 
       "Id" : (long),  /* required */ 
       "ParentId" : (long),  /* required */ 
       "Name" : (string),  /* required */ 
       "Description" : (string),  /* required */ 
       "InterestType" : (  "SHORT_TERM"  |  "LONG_TERM"  |  "ANY"  )   /* required */ 
    }, ... ],
     "FilterSchemas" : [{  /* FilterSchemasItem */ 
       "Name" : (string),  /* required */ 
       "Fields" : [{  /* required */ 
         "Name" : (string),  /* required */ 
         "Type" : ( "Enum" ,  "Number" ,  "String" ),  /* required */ 
         "EnumProps" : {
           "Values" : {  /* required */ 
             "Items" : [(string)]  /* required */ 
          },
        },
         "NumberProps" : {
           "Min" : (decimal),  /* required */ 
           "Max" : (decimal),  /* required */ 
           "Precision" : (integer)  /* required */ 
        },
         "StringProps" : {
           "MaxLength" : (integer),  /* required */ 
           "MinLength" : (integer)  /* required */ 
        },
         "Operators" : [{  /* required */ 
           "MaxItems" : (integer),  /* required */ 
           "Type" : ( "CONTAINS_ANY"  |  "EQUALS_ANY"  |  "EXISTS"  |  "GREATER_THAN"  |  "IN_RANGE"  |  "LESS_THAN"  |  "NOT_CONTAINS_ALL" )  /* required */ 
        }, ...]
    }, ... ]
  }
}
```

`AdCategories`

`Constants`

`Currencies`

`GeoRegions`

`GeoRegionNames`

`MetroStations`

`OperationSystemVersions`

`ProductivityAssertions`

`TimeZones`

`SupplySidePlatforms`

`Interests`

`AudienceCriteriaTypes`

`AudienceDemographicProfiles`

`AudienceInterests`

`AdCategory`

`Description`

`Message`

`Name`

`Value`

`Currency`

`Properties`

`Name`

`Value`

`GeoRegionId`

`GeoRegionName`

`GeoRegionType`

`ParentId`

`GeoRegionId`

`GeoRegionName`

`GeoRegionType`

`GeoRegionId`

`MetroStationId`

`MetroStationName`

`OsName`

`OsVersion`

`TimeZone`

`TimeZoneName`

`UtcOffset`

`Title`

`InterestId`

`ParentId`

`Name`

`IsTargetable`

`Type`

`BlockElement`

`Name`

`Description`

`CanSelect`

`Id`

`Type`

`AudienceCriteriaTypes`

`Name`

`Description`

`InterestKey`

`Id`

`InterestKey`

`Id`

`ParentId`

`Name`

`Description`

`InterestType`

`Name`

`Fields`

`Name`

`Type`

```
{
   "method" :  "get" ,
   "params" : {
     "DictionaryNames" : [  "Currencies"  ]
  }
}
```

```
{
   "method" :  "get" ,
   "params" : {
     "DictionaryNames" : [  "Currencies"  ]
  }
}
```

```
{
   "result" : {
     "Currencies" : [
      {
         "Currency" : "RUB" ,
         "Properties" : [
          {  "Name" :  "FullName" ,                    "Value" :  "российские рубли"  },
          {  "Name" :  "AutobudgetAvgCpaWarning" ,     "Value" :  "XXXX"  },
          {  "Name" :  "BidIncrement" ,                "Value" :  "100000"  },
          {  "Name" :  "MaxAutobudget" ,               "Value" :  "XXXX"  },
          {  "Name" :  "MaximumBid" ,                  "Value" :  "25000000000"  },
          {  "Name" :  "MaximumCPM" ,                  "Value" :  "3000000000"  },
          {  "Name" :  "MaxDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MaximumPayForConversionCPA" ,  "Value" :  "5000000000"  },
          {  "Name" :  "MinimumAverageCPA" ,           "Value" :  "900000"  },
          {  "Name" :  "MinimumAverageCPC" ,           "Value" :  "900000"  },
          {  "Name" :  "MinimumBid" ,                  "Value" :  "300000"  },
          {  "Name" :  "MinCpcCpaPerformance" ,        "Value" :  "XXXX"  },
          {  "Name" :  "MinimumCPM" ,                  "Value" :  "5000000"  },
          {  "Name" :  "MinimumDailyBudget" ,          "Value" :  "300000000"  },
          {  "Name" :  "MinDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MinimumPayment" ,              "Value" :  "300000000"  },
          {  "Name" :  "MinimumPayForConversionCPA" ,  "Value" :  "900000"  },
          {  "Name" :  "MinimumTransferAmount" ,       "Value" :  "1000000000"  },
          {  "Name" :  "MinimumWeeklySpendLimit" ,     "Value" :  "300000000"  }
        ]
      },
      ...
      {
         "Currency" :  "EUR" ,
         "Properties" : [
          {  "Name" :  "FullName" ,                    "Value" :  "евро"  },
          {  "Name" :  "AutobudgetAvgCpaWarning" ,     "Value" :  "XXXX"  },
          {  "Name" :  "BidIncrement" ,                "Value" :  "10000"  },
          {  "Name" :  "MaxAutobudget" ,               "Value" :  "XXXX"  },
          {  "Name" :  "MaximumBid" ,                  "Value" :  "500000000"  },
          {  "Name" :  "MaximumCPM" ,                  "Value" :  "44000000"  },
          {  "Name" :  "MaxDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MaximumPayForConversionCPA" ,  "Value" :  "170000000"  },
          {  "Name" :  "MinimumAverageCPA" ,           "Value" :  "30000"  },
          {  "Name" :  "MinimumAverageCPC" ,           "Value" :  "30000"  },
          {  "Name" :  "MinimumBid" ,                  "Value" :  "10000"  },
          {  "Name" :  "MinCpcCpaPerformance" ,        "Value" :  "XXXX"  },
          {  "Name" :  "MinimumCPM" ,                  "Value" :  "70000"  },
          {  "Name" :  "MinimumDailyBudget" ,          "Value" :  "10000000"  },
          {  "Name" :  "MinDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MinimumPayment" ,              "Value" :  "15000000"  },
          {  "Name" :  "MinimumPayForConversionCPA" ,  "Value" :  "30000"  },
          {  "Name" :  "MinimumTransferAmount" ,       "Value" :  "15000000"  },
          {  "Name" :  "MinimumWeeklySpendLimit" ,     "Value" :  "10000000"  }
        ]
      }
    ]
  }
}
```

```
{
   "result" : {
     "Currencies" : [
      {
         "Currency" : "RUB" ,
         "Properties" : [
          {  "Name" :  "FullName" ,                    "Value" :  "российские рубли"  },
          {  "Name" :  "AutobudgetAvgCpaWarning" ,     "Value" :  "XXXX"  },
          {  "Name" :  "BidIncrement" ,                "Value" :  "100000"  },
          {  "Name" :  "MaxAutobudget" ,               "Value" :  "XXXX"  },
          {  "Name" :  "MaximumBid" ,                  "Value" :  "25000000000"  },
          {  "Name" :  "MaximumCPM" ,                  "Value" :  "3000000000"  },
          {  "Name" :  "MaxDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MaximumPayForConversionCPA" ,  "Value" :  "5000000000"  },
          {  "Name" :  "MinimumAverageCPA" ,           "Value" :  "900000"  },
          {  "Name" :  "MinimumAverageCPC" ,           "Value" :  "900000"  },
          {  "Name" :  "MinimumBid" ,                  "Value" :  "300000"  },
          {  "Name" :  "MinCpcCpaPerformance" ,        "Value" :  "XXXX"  },
          {  "Name" :  "MinimumCPM" ,                  "Value" :  "5000000"  },
          {  "Name" :  "MinimumDailyBudget" ,          "Value" :  "300000000"  },
          {  "Name" :  "MinDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MinimumPayment" ,              "Value" :  "300000000"  },
          {  "Name" :  "MinimumPayForConversionCPA" ,  "Value" :  "900000"  },
          {  "Name" :  "MinimumTransferAmount" ,       "Value" :  "1000000000"  },
          {  "Name" :  "MinimumWeeklySpendLimit" ,     "Value" :  "300000000"  }
        ]
      },
      ...
      {
         "Currency" :  "EUR" ,
         "Properties" : [
          {  "Name" :  "FullName" ,                    "Value" :  "евро"  },
          {  "Name" :  "AutobudgetAvgCpaWarning" ,     "Value" :  "XXXX"  },
          {  "Name" :  "BidIncrement" ,                "Value" :  "10000"  },
          {  "Name" :  "MaxAutobudget" ,               "Value" :  "XXXX"  },
          {  "Name" :  "MaximumBid" ,                  "Value" :  "500000000"  },
          {  "Name" :  "MaximumCPM" ,                  "Value" :  "44000000"  },
          {  "Name" :  "MaxDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MaximumPayForConversionCPA" ,  "Value" :  "170000000"  },
          {  "Name" :  "MinimumAverageCPA" ,           "Value" :  "30000"  },
          {  "Name" :  "MinimumAverageCPC" ,           "Value" :  "30000"  },
          {  "Name" :  "MinimumBid" ,                  "Value" :  "10000"  },
          {  "Name" :  "MinCpcCpaPerformance" ,        "Value" :  "XXXX"  },
          {  "Name" :  "MinimumCPM" ,                  "Value" :  "70000"  },
          {  "Name" :  "MinimumDailyBudget" ,          "Value" :  "10000000"  },
          {  "Name" :  "MinDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MinimumPayment" ,              "Value" :  "15000000"  },
          {  "Name" :  "MinimumPayForConversionCPA" ,  "Value" :  "30000"  },
          {  "Name" :  "MinimumTransferAmount" ,       "Value" :  "15000000"  },
          {  "Name" :  "MinimumWeeklySpendLimit" ,     "Value" :  "10000000"  }
        ]
      }
    ]
  }
}
```

```
{
   "method" :  "get" ,
   "params" : {  /* params */ 
     "DictionaryNames" : [(  "Currencies" 
                        |  "MetroStations" 
                        |  "GeoRegions" 
                        |  "GeoRegionNames" 
                        |  "TimeZones" 
                        |  "Constants" 
                        |  "AdCategories" 
                        |  "OperationSystemVersions" 
                        |  "ProductivityAssertions" 
                        |  "SupplySidePlatforms" 
                        |  "Interests" 
                        |  "AudienceCriteriaTypes" 
                        |  "AudienceDemographicProfiles" 
                        |  "AudienceInterests" 
                        |  "FilterSchemas" ), ... ]  /* required */ 
  }
}
```

```
{
   "method" :  "get" ,
   "params" : {  /* params */ 
     "DictionaryNames" : [(  "Currencies" 
                        |  "MetroStations" 
                        |  "GeoRegions" 
                        |  "GeoRegionNames" 
                        |  "TimeZones" 
                        |  "Constants" 
                        |  "AdCategories" 
                        |  "OperationSystemVersions" 
                        |  "ProductivityAssertions" 
                        |  "SupplySidePlatforms" 
                        |  "Interests" 
                        |  "AudienceCriteriaTypes" 
                        |  "AudienceDemographicProfiles" 
                        |  "AudienceInterests" 
                        |  "FilterSchemas" ), ... ]  /* required */ 
  }
}
```

`DictionaryNames`

```
{
   "result" : {
     "Currencies" : [{   /* CurrenciesItem */ 
       "Currency" : (string),  /* required */ 
       "Properties" : [{   /* ConstantsItem */ 
         "Name" : (string),  /* required */ 
         "Value" : (string)  /* required */ 
      }, ... ]  /* required */ 
    }, ... ],
     "MetroStations" : [{   /* MetroStationsItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "MetroStationId" : (long),  /* required */ 
       "MetroStationName" : (string)  /* required */ 
    }, ... ],
     "GeoRegions" : [{   /* GeoRegionsItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "GeoRegionName" : (string),  /* required */ 
       "GeoRegionType" : (string),  /* required */ 
       "ParentId" : (long)  /* nillable */ 
    }, ... ],
     "GeoRegionNames" : [{   /* GeoRegionNamesItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "GeoRegionName" : (string),  /* required */ 
       "GeoRegionType" : (string),  /* required */ 
    }, ... ],
     "TimeZones" : [{   /* TimeZonesItem */ 
       "TimeZone" : (string),  /* required */ 
       "TimeZoneName" : (string),  /* required */ 
       "UtcOffset" : (int)  /* required */ 
    }, ... ],
     "Constants" : [{   /* ConstantsItem */ 
       "Name" : (string),  /* required */ 
       "Value" : (string)  /* required */ 
    }, ... ],
     "AdCategories" : [{   /* AdCategoriesItem */ 
       "AdCategory" : (string),  /* required */ 
       "Description" : (string),  /* required */ 
       "Message" : (string)  /* required */ 
    }, ... ],
     "OperationSystemVersions" : [{   /* OperationSystemVersionsItem */ 
       "OsName" : (string),  /* required */ 
       "OsVersion" : (string)  /* required */ 
    }, ... ],
     "SupplySidePlatforms" : [{   /* SupplySidePlatformsItem */ 
       "Title" : (string)  /* required */ 
    }, ... ],
     "Interests" : [{   /* InterestsItem */ 
       "InterestId" : (long),
       "ParentId" : (long),  /* nillable */ 
       "Name" : (string),
       "IsTargetable" : (  "YES"  |  "NO"  )
    }, ... ],
     "AudienceCriteriaTypes" : [{  /* AudienceCriteriaTypesItem */ 
       "Type" : (string),  /* required */ 
       "BlockElement" : (string),   /* required */ 
       "Name" : (string),   /* required */ 
       "Description" : (string),   /* required */ 
       "CanSelect" : (  "ALL"  |  "EXCEPT_ALL"  )  /* required */ 
    }, ... ],
     "AudienceDemographicProfiles" : [{  /* AudienceDemographicProfilesItem */ 
       "Id" : (long),  /* required */ 
       "Type" : (string),  /* required */ 
       "Name" : (string),  /* required */ 
       "Description" : (string)  /* required */ 
    }, ... ],
     "AudienceInterests" : [{  /* AudienceInterestsItem */ 
       "InterestKey" : (long),  /* required */ 
       "Id" : (long),  /* required */ 
       "ParentId" : (long),  /* required */ 
       "Name" : (string),  /* required */ 
       "Description" : (string),  /* required */ 
       "InterestType" : (  "SHORT_TERM"  |  "LONG_TERM"  |  "ANY"  )   /* required */ 
    }, ... ],
     "FilterSchemas" : [{  /* FilterSchemasItem */ 
       "Name" : (string),  /* required */ 
       "Fields" : [{  /* required */ 
         "Name" : (string),  /* required */ 
         "Type" : ( "Enum" ,  "Number" ,  "String" ),  /* required */ 
         "EnumProps" : {
           "Values" : {  /* required */ 
             "Items" : [(string)]  /* required */ 
          },
        },
         "NumberProps" : {
           "Min" : (decimal),  /* required */ 
           "Max" : (decimal),  /* required */ 
           "Precision" : (integer)  /* required */ 
        },
         "StringProps" : {
           "MaxLength" : (integer),  /* required */ 
           "MinLength" : (integer)  /* required */ 
        },
         "Operators" : [{  /* required */ 
           "MaxItems" : (integer),  /* required */ 
           "Type" : ( "CONTAINS_ANY"  |  "EQUALS_ANY"  |  "EXISTS"  |  "GREATER_THAN"  |  "IN_RANGE"  |  "LESS_THAN"  |  "NOT_CONTAINS_ALL" )  /* required */ 
        }, ...]
    }, ... ]
  }
}
```

```
{
   "result" : {
     "Currencies" : [{   /* CurrenciesItem */ 
       "Currency" : (string),  /* required */ 
       "Properties" : [{   /* ConstantsItem */ 
         "Name" : (string),  /* required */ 
         "Value" : (string)  /* required */ 
      }, ... ]  /* required */ 
    }, ... ],
     "MetroStations" : [{   /* MetroStationsItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "MetroStationId" : (long),  /* required */ 
       "MetroStationName" : (string)  /* required */ 
    }, ... ],
     "GeoRegions" : [{   /* GeoRegionsItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "GeoRegionName" : (string),  /* required */ 
       "GeoRegionType" : (string),  /* required */ 
       "ParentId" : (long)  /* nillable */ 
    }, ... ],
     "GeoRegionNames" : [{   /* GeoRegionNamesItem */ 
       "GeoRegionId" : (long),  /* required */ 
       "GeoRegionName" : (string),  /* required */ 
       "GeoRegionType" : (string),  /* required */ 
    }, ... ],
     "TimeZones" : [{   /* TimeZonesItem */ 
       "TimeZone" : (string),  /* required */ 
       "TimeZoneName" : (string),  /* required */ 
       "UtcOffset" : (int)  /* required */ 
    }, ... ],
     "Constants" : [{   /* ConstantsItem */ 
       "Name" : (string),  /* required */ 
       "Value" : (string)  /* required */ 
    }, ... ],
     "AdCategories" : [{   /* AdCategoriesItem */ 
       "AdCategory" : (string),  /* required */ 
       "Description" : (string),  /* required */ 
       "Message" : (string)  /* required */ 
    }, ... ],
     "OperationSystemVersions" : [{   /* OperationSystemVersionsItem */ 
       "OsName" : (string),  /* required */ 
       "OsVersion" : (string)  /* required */ 
    }, ... ],
     "SupplySidePlatforms" : [{   /* SupplySidePlatformsItem */ 
       "Title" : (string)  /* required */ 
    }, ... ],
     "Interests" : [{   /* InterestsItem */ 
       "InterestId" : (long),
       "ParentId" : (long),  /* nillable */ 
       "Name" : (string),
       "IsTargetable" : (  "YES"  |  "NO"  )
    }, ... ],
     "AudienceCriteriaTypes" : [{  /* AudienceCriteriaTypesItem */ 
       "Type" : (string),  /* required */ 
       "BlockElement" : (string),   /* required */ 
       "Name" : (string),   /* required */ 
       "Description" : (string),   /* required */ 
       "CanSelect" : (  "ALL"  |  "EXCEPT_ALL"  )  /* required */ 
    }, ... ],
     "AudienceDemographicProfiles" : [{  /* AudienceDemographicProfilesItem */ 
       "Id" : (long),  /* required */ 
       "Type" : (string),  /* required */ 
       "Name" : (string),  /* required */ 
       "Description" : (string)  /* required */ 
    }, ... ],
     "AudienceInterests" : [{  /* AudienceInterestsItem */ 
       "InterestKey" : (long),  /* required */ 
       "Id" : (long),  /* required */ 
       "ParentId" : (long),  /* required */ 
       "Name" : (string),  /* required */ 
       "Description" : (string),  /* required */ 
       "InterestType" : (  "SHORT_TERM"  |  "LONG_TERM"  |  "ANY"  )   /* required */ 
    }, ... ],
     "FilterSchemas" : [{  /* FilterSchemasItem */ 
       "Name" : (string),  /* required */ 
       "Fields" : [{  /* required */ 
         "Name" : (string),  /* required */ 
         "Type" : ( "Enum" ,  "Number" ,  "String" ),  /* required */ 
         "EnumProps" : {
           "Values" : {  /* required */ 
             "Items" : [(string)]  /* required */ 
          },
        },
         "NumberProps" : {
           "Min" : (decimal),  /* required */ 
           "Max" : (decimal),  /* required */ 
           "Precision" : (integer)  /* required */ 
        },
         "StringProps" : {
           "MaxLength" : (integer),  /* required */ 
           "MinLength" : (integer)  /* required */ 
        },
         "Operators" : [{  /* required */ 
           "MaxItems" : (integer),  /* required */ 
           "Type" : ( "CONTAINS_ANY"  |  "EQUALS_ANY"  |  "EXISTS"  |  "GREATER_THAN"  |  "IN_RANGE"  |  "LESS_THAN"  |  "NOT_CONTAINS_ALL" )  /* required */ 
        }, ...]
    }, ... ]
  }
}
```

`AdCategories`

`Constants`

`Currencies`

`GeoRegions`

`GeoRegionNames`

`MetroStations`

`OperationSystemVersions`

`ProductivityAssertions`

`TimeZones`

`SupplySidePlatforms`

`Interests`

`AudienceCriteriaTypes`

`AudienceDemographicProfiles`

`AudienceInterests`

`AdCategory`

`Description`

`Message`

`Name`

`Value`

`Currency`

`Properties`

`Name`

`Value`

`GeoRegionId`

`GeoRegionName`

`GeoRegionType`

`ParentId`

`GeoRegionId`

`GeoRegionName`

`GeoRegionType`

`GeoRegionId`

`MetroStationId`

`MetroStationName`

`OsName`

`OsVersion`

`TimeZone`

`TimeZoneName`

`UtcOffset`

`Title`

`InterestId`

`ParentId`

`Name`

`IsTargetable`

`Type`

`BlockElement`

`Name`

`Description`

`CanSelect`

`Id`

`Type`

`AudienceCriteriaTypes`

`Name`

`Description`

`InterestKey`

`Id`

`InterestKey`

`Id`

`ParentId`

`Name`

`Description`

`InterestType`

`Name`

`Fields`

`Name`

`Type`

```
{
   "method" :  "get" ,
   "params" : {
     "DictionaryNames" : [  "Currencies"  ]
  }
}
```

```
{
   "method" :  "get" ,
   "params" : {
     "DictionaryNames" : [  "Currencies"  ]
  }
}
```

```
{
   "result" : {
     "Currencies" : [
      {
         "Currency" : "RUB" ,
         "Properties" : [
          {  "Name" :  "FullName" ,                    "Value" :  "российские рубли"  },
          {  "Name" :  "AutobudgetAvgCpaWarning" ,     "Value" :  "XXXX"  },
          {  "Name" :  "BidIncrement" ,                "Value" :  "100000"  },
          {  "Name" :  "MaxAutobudget" ,               "Value" :  "XXXX"  },
          {  "Name" :  "MaximumBid" ,                  "Value" :  "25000000000"  },
          {  "Name" :  "MaximumCPM" ,                  "Value" :  "3000000000"  },
          {  "Name" :  "MaxDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MaximumPayForConversionCPA" ,  "Value" :  "5000000000"  },
          {  "Name" :  "MinimumAverageCPA" ,           "Value" :  "900000"  },
          {  "Name" :  "MinimumAverageCPC" ,           "Value" :  "900000"  },
          {  "Name" :  "MinimumBid" ,                  "Value" :  "300000"  },
          {  "Name" :  "MinCpcCpaPerformance" ,        "Value" :  "XXXX"  },
          {  "Name" :  "MinimumCPM" ,                  "Value" :  "5000000"  },
          {  "Name" :  "MinimumDailyBudget" ,          "Value" :  "300000000"  },
          {  "Name" :  "MinDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MinimumPayment" ,              "Value" :  "300000000"  },
          {  "Name" :  "MinimumPayForConversionCPA" ,  "Value" :  "900000"  },
          {  "Name" :  "MinimumTransferAmount" ,       "Value" :  "1000000000"  },
          {  "Name" :  "MinimumWeeklySpendLimit" ,     "Value" :  "300000000"  }
        ]
      },
      ...
      {
         "Currency" :  "EUR" ,
         "Properties" : [
          {  "Name" :  "FullName" ,                    "Value" :  "евро"  },
          {  "Name" :  "AutobudgetAvgCpaWarning" ,     "Value" :  "XXXX"  },
          {  "Name" :  "BidIncrement" ,                "Value" :  "10000"  },
          {  "Name" :  "MaxAutobudget" ,               "Value" :  "XXXX"  },
          {  "Name" :  "MaximumBid" ,                  "Value" :  "500000000"  },
          {  "Name" :  "MaximumCPM" ,                  "Value" :  "44000000"  },
          {  "Name" :  "MaxDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MaximumPayForConversionCPA" ,  "Value" :  "170000000"  },
          {  "Name" :  "MinimumAverageCPA" ,           "Value" :  "30000"  },
          {  "Name" :  "MinimumAverageCPC" ,           "Value" :  "30000"  },
          {  "Name" :  "MinimumBid" ,                  "Value" :  "10000"  },
          {  "Name" :  "MinCpcCpaPerformance" ,        "Value" :  "XXXX"  },
          {  "Name" :  "MinimumCPM" ,                  "Value" :  "70000"  },
          {  "Name" :  "MinimumDailyBudget" ,          "Value" :  "10000000"  },
          {  "Name" :  "MinDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MinimumPayment" ,              "Value" :  "15000000"  },
          {  "Name" :  "MinimumPayForConversionCPA" ,  "Value" :  "30000"  },
          {  "Name" :  "MinimumTransferAmount" ,       "Value" :  "15000000"  },
          {  "Name" :  "MinimumWeeklySpendLimit" ,     "Value" :  "10000000"  }
        ]
      }
    ]
  }
}
```

```
{
   "result" : {
     "Currencies" : [
      {
         "Currency" : "RUB" ,
         "Properties" : [
          {  "Name" :  "FullName" ,                    "Value" :  "российские рубли"  },
          {  "Name" :  "AutobudgetAvgCpaWarning" ,     "Value" :  "XXXX"  },
          {  "Name" :  "BidIncrement" ,                "Value" :  "100000"  },
          {  "Name" :  "MaxAutobudget" ,               "Value" :  "XXXX"  },
          {  "Name" :  "MaximumBid" ,                  "Value" :  "25000000000"  },
          {  "Name" :  "MaximumCPM" ,                  "Value" :  "3000000000"  },
          {  "Name" :  "MaxDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MaximumPayForConversionCPA" ,  "Value" :  "5000000000"  },
          {  "Name" :  "MinimumAverageCPA" ,           "Value" :  "900000"  },
          {  "Name" :  "MinimumAverageCPC" ,           "Value" :  "900000"  },
          {  "Name" :  "MinimumBid" ,                  "Value" :  "300000"  },
          {  "Name" :  "MinCpcCpaPerformance" ,        "Value" :  "XXXX"  },
          {  "Name" :  "MinimumCPM" ,                  "Value" :  "5000000"  },
          {  "Name" :  "MinimumDailyBudget" ,          "Value" :  "300000000"  },
          {  "Name" :  "MinDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MinimumPayment" ,              "Value" :  "300000000"  },
          {  "Name" :  "MinimumPayForConversionCPA" ,  "Value" :  "900000"  },
          {  "Name" :  "MinimumTransferAmount" ,       "Value" :  "1000000000"  },
          {  "Name" :  "MinimumWeeklySpendLimit" ,     "Value" :  "300000000"  }
        ]
      },
      ...
      {
         "Currency" :  "EUR" ,
         "Properties" : [
          {  "Name" :  "FullName" ,                    "Value" :  "евро"  },
          {  "Name" :  "AutobudgetAvgCpaWarning" ,     "Value" :  "XXXX"  },
          {  "Name" :  "BidIncrement" ,                "Value" :  "10000"  },
          {  "Name" :  "MaxAutobudget" ,               "Value" :  "XXXX"  },
          {  "Name" :  "MaximumBid" ,                  "Value" :  "500000000"  },
          {  "Name" :  "MaximumCPM" ,                  "Value" :  "44000000"  },
          {  "Name" :  "MaxDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MaximumPayForConversionCPA" ,  "Value" :  "170000000"  },
          {  "Name" :  "MinimumAverageCPA" ,           "Value" :  "30000"  },
          {  "Name" :  "MinimumAverageCPC" ,           "Value" :  "30000"  },
          {  "Name" :  "MinimumBid" ,                  "Value" :  "10000"  },
          {  "Name" :  "MinCpcCpaPerformance" ,        "Value" :  "XXXX"  },
          {  "Name" :  "MinimumCPM" ,                  "Value" :  "70000"  },
          {  "Name" :  "MinimumDailyBudget" ,          "Value" :  "10000000"  },
          {  "Name" :  "MinDailyBudgetForPeriod" ,     "Value" :  "XXXX"  },
          {  "Name" :  "MinimumPayment" ,              "Value" :  "15000000"  },
          {  "Name" :  "MinimumPayForConversionCPA" ,  "Value" :  "30000"  },
          {  "Name" :  "MinimumTransferAmount" ,       "Value" :  "15000000"  },
          {  "Name" :  "MinimumWeeklySpendLimit" ,     "Value" :  "10000000"  }
        ]
      }
    ]
  }
}
```


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| DictionaryNames | array of DictionaryNameEnum |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| AdCategories | array of AdCategoriesItem |
| Constants | array of ConstantsItem |
| Currencies | array of CurrenciesItem |
| GeoRegions | array of GeoRegionsItem |
| GeoRegionNames | array of GeoRegionNamesItem |
| MetroStations | array of MetroStationsItem |
| OperationSystemVersions | array of OperationSystemVersionsItem |
| ProductivityAssertions | array of ProductivityAssertionsItem |
| TimeZones | array of TimeZonesItem |
| SupplySidePlatforms | array of SupplySidePlatformsItem |
| Interests | array of InterestsItem |
| AudienceCriteriaTypes | array of AudienceCriteriaTypesItem |
| AudienceDemographicProfiles | array of AudienceDemographicProfilesItem |
| AudienceInterests | array of AudienceInterestsItem |
| FilterSchemas | array of FilterSchemasItem |
| AdCategory | string |
| Description | string |
| Message | string |
| Name | string |
| Value | string |
| Currency | string |
| Properties | array of ConstantsItem |
| Name | string |
| Value | string |
| GeoRegionId | long |
| GeoRegionName | string |
| GeoRegionType | string |
| ParentId | long, nillable |
| GeoRegionId | long |
| GeoRegionName | string |
| GeoRegionType | string |
| GeoRegionId | long |
| MetroStationId | long |
| MetroStationName | string |
| OsName | string |
| OsVersion | string |
| TimeZone | string |
| TimeZoneName | string |
| UtcOffset | int |
| Title | string |
| InterestId | long |
| ParentId | long, nillable |
| Name | string |
| IsTargetable | YesNoEnum |
| Type | string |
| BlockElement | string |
| Name | string |
| Description | string |
| CanSelect | CanSelectEnum |
| Id | long |
| Type | string |
| Name | string |
| Description | string |
| InterestKey | long |
| Id | long |
| ParentId | long |
| Name | string |
| Description | string |
| InterestType | InterestTypeEnum |
| Name | string |
| Fields | array of FilterSchemaItemFields |
| Name | string |
| Type | FieldTypeEnum |
| EnumProps | EnumFieldStructure |
| NumberProps | NumberFieldStructure |
| StringProps | StringFieldStructure |
| Operators | array of OperatorStructure |
| Values | EnumFieldStructureItem |
| Items | array of strings |
| Min | decimal |
| Max | decimal |
| Precision | integer |
| MaxLength | integer |
| MinLength | integer |
| MaxItems | integer |
| Type | OperatorEnum |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| DictionaryNames | array of DictionaryNameEnum |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| AdCategories | array of AdCategoriesItem |
| Constants | array of ConstantsItem |
| Currencies | array of CurrenciesItem |
| GeoRegions | array of GeoRegionsItem |
| GeoRegionNames | array of GeoRegionNamesItem |
| MetroStations | array of MetroStationsItem |
| OperationSystemVersions | array of OperationSystemVersionsItem |
| ProductivityAssertions | array of ProductivityAssertionsItem |
| TimeZones | array of TimeZonesItem |
| SupplySidePlatforms | array of SupplySidePlatformsItem |
| Interests | array of InterestsItem |
| AudienceCriteriaTypes | array of AudienceCriteriaTypesItem |
| AudienceDemographicProfiles | array of AudienceDemographicProfilesItem |
| AudienceInterests | array of AudienceInterestsItem |
| FilterSchemas | array of FilterSchemasItem |
| AdCategory | string |
| Description | string |
| Message | string |
| Name | string |
| Value | string |
| Currency | string |
| Properties | array of ConstantsItem |
| Name | string |
| Value | string |
| GeoRegionId | long |
| GeoRegionName | string |
| GeoRegionType | string |
| ParentId | long, nillable |
| GeoRegionId | long |
| GeoRegionName | string |
| GeoRegionType | string |
| GeoRegionId | long |
| MetroStationId | long |
| MetroStationName | string |
| OsName | string |
| OsVersion | string |
| TimeZone | string |
| TimeZoneName | string |
| UtcOffset | int |
| Title | string |
| InterestId | long |
| ParentId | long, nillable |
| Name | string |
| IsTargetable | YesNoEnum |
| Type | string |
| BlockElement | string |
| Name | string |
| Description | string |
| CanSelect | CanSelectEnum |
| Id | long |
| Type | string |
| Name | string |
| Description | string |
| InterestKey | long |
| Id | long |
| ParentId | long |
| Name | string |
| Description | string |
| InterestType | InterestTypeEnum |
| Name | string |
| Fields | array of FilterSchemaItemFields |
| Name | string |
| Type | FieldTypeEnum |
| EnumProps | EnumFieldStructure |
| NumberProps | NumberFieldStructure |
| StringProps | StringFieldStructure |
| Operators | array of OperatorStructure |
| Values | EnumFieldStructureItem |
| Items | array of strings |
| Min | decimal |
| Max | decimal |
| Precision | integer |
| MaxLength | integer |
| MinLength | integer |
| MaxItems | integer |
| Type | OperatorEnum |

