# get  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/agencyclients/get

**Дата скачивания:** 2025-07-01 12:37:39

---

## В этой статье :

# get

## Узнайте больше

## Запрос

## Ответ

### Была ли статья полезна?

# get

## Узнайте больше

## Запрос

## Ответ

### Была ли статья полезна?

Возвращает список рекламодателей — клиентов агентства, их параметры и настройки главных представителей рекламодателя.

Примечание

В запросе к сервису  AgencyClients :

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / GetRequest (для SOAP)

SelectionCriteria

AgencyClientsSelectionCriteria

Критерии отбора клиентов.

Чтобы получить параметры всех клиентов агентства, необходимо указать пустую структуру  SelectionCriteria .

Да

FieldNames

array of AgencyClientFieldEnum

Имена параметров, которые требуется получить.

Да

TinInfoFieldNames

array of TinInfoFieldEnum

Имена параметров с налоговыми данными о конечном рекламодателе, которые требуется получить.

Нет

OrganizationFieldNames

array of OrganizationFieldEnum

Имена параметров с информацией об организации конечного рекламодателя, которые требуется получить.

Нет

ContractFieldNames

array of ContractFieldEnum

Имена параметров с информацией о договоре клиента-контрагента с конечным рекламодателем, которые требуется получить.

Нет

ContragentFieldNames

array of ContragentFieldEnum

Имена параметров с информацией о контрагенте, которые требуется получить.

Нет

ContragentTinInfoFieldNames

array of TinInfoFieldEnum

Имена параметров с налоговыми данными о контрагенте, которые требуется получить.

Нет

Page

LimitOffset

Структура, задающая страницу при  постраничной выборке  данных.

Нет

Структура AgencyClientsSelectionCriteria

Logins

array of string

Отбирать клиентов с указанными логинами представителей. Не более 10 000 элементов в массиве.

Нет

Archived

YesNoEnum

Отбирать клиентов по признаку нахождения в архиве: YES — архивные клиенты, NO — активные клиенты.

Нет

Примечание

Параметры  Login ,  ClientInfo ,  CreatedAt ,  Notification ,  Phone  относятся к главному представителю рекламодателя (см. раздел  Роли и доступы пользователей Директа ). Остальные параметры относятся к рекламодателю.

Если в запросе в параметре  Logins  указан логин представителя рекламодателя, который не является главным представителем, то ответ будет содержать логин главного представителя, отличающийся от логина в запросе.

Если в запросе в параметре  Logins  указано несколько логинов представителей одного рекламодателя, рекламодатель (и его главный представитель) будет присутствовать в ответе только один раз.

Список всех представителей рекламодателя представлен в параметре ответа  Representatives .

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / GetResponse (для SOAP)

Clients

array of ClientGetItem

Рекламодатели — клиенты агентства и их главные представители.

LimitedBy

long

Порядковый номер последнего возвращенного объекта. Передается в случае, если количество объектов в ответе было ограничено лимитом. См. раздел  Постраничная выборка .

Структура ClientGetItem

AccountQuality

decimal, nillable

Показатель качества аккаунта.

Archived

YesNoEnum

Признак того, что рекламодатель помещен в архив (не активен).

ClientId

long

Идентификатор рекламодателя.

ClientInfo

string

Название клиента (до 255 символов).

CountryId

int

Идентификатор страны рекламодателя из справочника регионов.

Справочник регионов можно получить с помощью метода  Dictionaries . get .

CreatedAt

string

Дата регистрации пользователя в Директе, в формате YYYY-MM-DD.

Currency

CurrencyEnum

Валюта рекламодателя.

Справочник валют можно получить с помощью метода  Dictionaries . get .

Grants

array of GrantGetItem

Полномочия рекламодателя по управлению кампаниями.

Bonuses

BonusesGet

Бонус, ожидающий начисления. Параметр актуален только для валюты RUB.

Login

string

Логин пользователя Директа.

Notification

NotificationGet

Настройки SMS- и email-уведомлений пользователя Директа.

OverdraftSumAvailable

long

Лимит овердрафта, которым рекламодатель может воспользоваться в текущий момент времени (см. раздел  Отсрочка платежа  помощи Директа).

Возвращается в виде целого числа, которое представляет собой лимит овердрафта в валюте рекламодателя, умноженный на 1 000 000.

Phone

string

Номер телефона пользователя Директа (до 50 символов, содержит только цифры и должен начинаться с кода страны).

Representatives

array of Representative

Представители рекламодателя.

См.  Роли и доступы пользователей Директа .

Restrictions

array of ClientRestrictionItem

Количественные ограничения на объекты рекламодателя.

Settings

array of ClientSettingGetItem

Настройки рекламодателя, допускающие только значения YES или NO.

Type

string

Тип клиента: SUBCLIENT.

VatRate

decimal, nillable

Ставка НДС агентства.

ForbiddenPlatform

ForbiddenPlatformEnum

Запрещенные площадки:

AvailableCampaignTypes

AvailableCampaignTypesEnum

Типы кампаний, которые доступны логину:

TinInfo

TinInfoGet

Налоговые данные конечного рекламодателя.

ErirAttributes

ErirAttributesGet

Дополнительные данные рекламодателя для маркировки рекламы.

Структура GrantGetItem

Privilege

PrivilegeEnum

Имя полномочия:

EDIT_CAMPAIGNS — редактирование кампаний.

IMPORT_XLS — управление кампаниями с помощью файлов (см. разделы  Управление кампаниями с помощью файлов формата XLS и XLSX  и  Загрузка кампаний из CSV-файлов  помощи Директа).

TRANSFER_MONEY — перенос средств между кампаниями (см. раздел  Перенос средств между кампаниями ).

Value

YesNoEnum

Есть ли у клиента данное полномочие.

Agency

string

Название рекламного агентства, если полномочие предоставлено агентством.

Структура BonusesGet

AwaitingBonus

long

Размер бонуса с НДС, который ожидает начисления. Возвращается в виде целого числа, умноженного на 1 000 000.

AwaitingBonusWithoutNds

long

Размер бонуса без НДС, который ожидает начисления. Возвращается в виде целого числа, умноженного на 1 000 000.

Структура NotificationGet

Lang

LangEnum

Язык уведомлений.

SmsPhoneNumber

string

Телефонный номер для отправки SMS-уведомлений из профиля пользователя на Яндексе (см. раздел  Мои телефоны  помощи Яндекс Паспорта).

Email

string

Адрес электронной почты для отправки уведомлений, связанных с аккаунтом (до 255 символов).

EmailSubscriptions

array of EmailSubscriptionItem

Типы уведомлений, отправляемых по электронной почте.

Структура EmailSubscriptionItem

Option

EmailSubscriptionEnum

Тип уведомления:

RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.

TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.

TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

Value

YesNoEnum

Отправлять ли уведомления данного типа.

Структура Representative

Login

string

Логин пользователя.

Email

string

Адрес электронной почты для отправки уведомлений.

Role

RepresentativeRoleEnum

Роль пользователя:

См.  Роли и доступы пользователей Директа .

Структура ClientRestrictionItem

Element

ClientRestrictionEnum

Имя ограничения:

CAMPAIGNS_TOTAL_PER_CLIENT — максимальное количество кампаний у рекламодателя.

CAMPAIGNS_UNARCHIVED_PER_CLIENT — максимальное количество кампаний, не находящихся в архиве.

ADGROUPS_TOTAL_PER_CAMPAIGN — максимальное количество групп в кампании.

ADS_TOTAL_PER_ADGROUP — максимальное количество объявлений в группе.

KEYWORDS_TOTAL_PER_ADGROUP — максимальное количество ключевых фраз в группе.

AD_EXTENSIONS_TOTAL — максимальное количество расширений к объявлениям у рекламодателя.

STAT_REPORTS_TOTAL_IN_QUEUE — максимальное количество одновременно формируемых статистических отчетов.

FORECAST_REPORTS_TOTAL_IN_QUEUE — максимальное количество хранимых на сервере отчетов о прогнозируемом бюджете, количестве показов и кликов.

WORDSTAT_REPORTS_TOTAL_IN_QUEUE — максимальное количество хранимых на сервере отчетов о статистике поисковых запросов.

API_POINTS — суточный лимит баллов.

GENERAL_DOMAIN_BLACKLIST_SIZE — максимальное количество площадок, на которых запрещены показы объявлений.

VIDEO_DOMAIN_BLACKLIST_SIZE — максимальное количество площадок, на которых запрещены показы видеообъявлений.

Value

int

Значение ограничения.

Структура ClientSettingGetItem

Option

ClientSettingGetEnum

Имя настройки:

CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.

DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).

SHARED_ACCOUNT_ENABLED — подключен общий счет.

Value

YesNoEnum

Значение настройки.

Структура TinInfoGet

TinType

TinTypeEnum

Тип организации:

Tin

string

Номер налогоплательщика либо его аналог в стране регистрации.

Структура ErirAttributesGet

Organization

OrganizationGet

Информация об организации конечного рекламодателя.

Contract

ContractGet

Информация о договоре клиента-контрагента с конечным рекламодателем.

Contragent

ContragentGet

Информация о контрагенте конечного рекламодателя.

Структура OrganizationGet

Name

string

Наименование организации (до 255 символов).

EpayNumber

string

Номер электронного средства платежа (до 255 символов).

RegNumber

string

Регистрационный номер либо его аналог (до 255 символов).

OksmNumber

string

Код страны регистрации юрлица в соответствии с ОКСМ (до 3 символов, содержит только цифры).

OkvedCode

string

Код вида деятельности по ОКВЭД.

Структура ContractGet

Number

string

Номер договора (до 255 символов).

Date

string

Дата договора в формате YYYY-MM-DD (не раньше 01.01.1991).

Type

ContractTypeEnum

Тип договора:

ActionType

ContractActionTypeEnum

Тип осуществляемых посредником-представителем действий:

SubjectType

ContractSubjectTypeEnum

Предмет договора:

Price

ContractPrice

Цена договора (не более двух знаков после разделителя).

Структура ContractPrice

Amount

decimal

Стоимость договора.

IncludingVat

YesNoEnum

Включен ли в стоимость НДС.

Структура ContragentGet

Name

string

Наименование (до 255 символов).

Phone

string

Номер телефона (до 50 символов, содержит только цифры и должен начинаться с кода страны).

EpayNumber

string

Номер электронного средства платежа (до 255 символов).

RegNumber

string

Регистрационный номер либо его аналог (до 255 символов).

OksmNumber

string

Код страны регистрации юрлица в соответствии с ОКСМ (до 3 символов, содержит только цифры).

TinInfo

TinInfoGet

Налоговые данные контрагента.

Возвращает список рекламодателей — клиентов агентства, их параметры и настройки главных представителей рекламодателя.

Примечание

В запросе к сервису  AgencyClients :

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / GetRequest (для SOAP)

SelectionCriteria

AgencyClientsSelectionCriteria

Критерии отбора клиентов.

Чтобы получить параметры всех клиентов агентства, необходимо указать пустую структуру  SelectionCriteria .

Да

FieldNames

array of AgencyClientFieldEnum

Имена параметров, которые требуется получить.

Да

TinInfoFieldNames

array of TinInfoFieldEnum

Имена параметров с налоговыми данными о конечном рекламодателе, которые требуется получить.

Нет

OrganizationFieldNames

array of OrganizationFieldEnum

Имена параметров с информацией об организации конечного рекламодателя, которые требуется получить.

Нет

ContractFieldNames

array of ContractFieldEnum

Имена параметров с информацией о договоре клиента-контрагента с конечным рекламодателем, которые требуется получить.

Нет

ContragentFieldNames

array of ContragentFieldEnum

Имена параметров с информацией о контрагенте, которые требуется получить.

Нет

ContragentTinInfoFieldNames

array of TinInfoFieldEnum

Имена параметров с налоговыми данными о контрагенте, которые требуется получить.

Нет

Page

LimitOffset

Структура, задающая страницу при  постраничной выборке  данных.

Нет

Структура AgencyClientsSelectionCriteria

Logins

array of string

Отбирать клиентов с указанными логинами представителей. Не более 10 000 элементов в массиве.

Нет

Archived

YesNoEnum

Отбирать клиентов по признаку нахождения в архиве: YES — архивные клиенты, NO — активные клиенты.

Нет

Примечание

Параметры  Login ,  ClientInfo ,  CreatedAt ,  Notification ,  Phone  относятся к главному представителю рекламодателя (см. раздел  Роли и доступы пользователей Директа ). Остальные параметры относятся к рекламодателю.

Если в запросе в параметре  Logins  указан логин представителя рекламодателя, который не является главным представителем, то ответ будет содержать логин главного представителя, отличающийся от логина в запросе.

Если в запросе в параметре  Logins  указано несколько логинов представителей одного рекламодателя, рекламодатель (и его главный представитель) будет присутствовать в ответе только один раз.

Список всех представителей рекламодателя представлен в параметре ответа  Representatives .

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / GetResponse (для SOAP)

Clients

array of ClientGetItem

Рекламодатели — клиенты агентства и их главные представители.

LimitedBy

long

Порядковый номер последнего возвращенного объекта. Передается в случае, если количество объектов в ответе было ограничено лимитом. См. раздел  Постраничная выборка .

Структура ClientGetItem

AccountQuality

decimal, nillable

Показатель качества аккаунта.

Archived

YesNoEnum

Признак того, что рекламодатель помещен в архив (не активен).

ClientId

long

Идентификатор рекламодателя.

ClientInfo

string

Название клиента (до 255 символов).

CountryId

int

Идентификатор страны рекламодателя из справочника регионов.

Справочник регионов можно получить с помощью метода  Dictionaries . get .

CreatedAt

string

Дата регистрации пользователя в Директе, в формате YYYY-MM-DD.

Currency

CurrencyEnum

Валюта рекламодателя.

Справочник валют можно получить с помощью метода  Dictionaries . get .

Grants

array of GrantGetItem

Полномочия рекламодателя по управлению кампаниями.

Bonuses

BonusesGet

Бонус, ожидающий начисления. Параметр актуален только для валюты RUB.

Login

string

Логин пользователя Директа.

Notification

NotificationGet

Настройки SMS- и email-уведомлений пользователя Директа.

OverdraftSumAvailable

long

Лимит овердрафта, которым рекламодатель может воспользоваться в текущий момент времени (см. раздел  Отсрочка платежа  помощи Директа).

Возвращается в виде целого числа, которое представляет собой лимит овердрафта в валюте рекламодателя, умноженный на 1 000 000.

Phone

string

Номер телефона пользователя Директа (до 50 символов, содержит только цифры и должен начинаться с кода страны).

Representatives

array of Representative

Представители рекламодателя.

См.  Роли и доступы пользователей Директа .

Restrictions

array of ClientRestrictionItem

Количественные ограничения на объекты рекламодателя.

Settings

array of ClientSettingGetItem

Настройки рекламодателя, допускающие только значения YES или NO.

Type

string

Тип клиента: SUBCLIENT.

VatRate

decimal, nillable

Ставка НДС агентства.

ForbiddenPlatform

ForbiddenPlatformEnum

Запрещенные площадки:

AvailableCampaignTypes

AvailableCampaignTypesEnum

Типы кампаний, которые доступны логину:

TinInfo

TinInfoGet

Налоговые данные конечного рекламодателя.

ErirAttributes

ErirAttributesGet

Дополнительные данные рекламодателя для маркировки рекламы.

Структура GrantGetItem

Privilege

PrivilegeEnum

Имя полномочия:

EDIT_CAMPAIGNS — редактирование кампаний.

IMPORT_XLS — управление кампаниями с помощью файлов (см. разделы  Управление кампаниями с помощью файлов формата XLS и XLSX  и  Загрузка кампаний из CSV-файлов  помощи Директа).

TRANSFER_MONEY — перенос средств между кампаниями (см. раздел  Перенос средств между кампаниями ).

Value

YesNoEnum

Есть ли у клиента данное полномочие.

Agency

string

Название рекламного агентства, если полномочие предоставлено агентством.

Структура BonusesGet

AwaitingBonus

long

Размер бонуса с НДС, который ожидает начисления. Возвращается в виде целого числа, умноженного на 1 000 000.

AwaitingBonusWithoutNds

long

Размер бонуса без НДС, который ожидает начисления. Возвращается в виде целого числа, умноженного на 1 000 000.

Структура NotificationGet

Lang

LangEnum

Язык уведомлений.

SmsPhoneNumber

string

Телефонный номер для отправки SMS-уведомлений из профиля пользователя на Яндексе (см. раздел  Мои телефоны  помощи Яндекс Паспорта).

Email

string

Адрес электронной почты для отправки уведомлений, связанных с аккаунтом (до 255 символов).

EmailSubscriptions

array of EmailSubscriptionItem

Типы уведомлений, отправляемых по электронной почте.

Структура EmailSubscriptionItem

Option

EmailSubscriptionEnum

Тип уведомления:

RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.

TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.

TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

Value

YesNoEnum

Отправлять ли уведомления данного типа.

Структура Representative

Login

string

Логин пользователя.

Email

string

Адрес электронной почты для отправки уведомлений.

Role

RepresentativeRoleEnum

Роль пользователя:

См.  Роли и доступы пользователей Директа .

Структура ClientRestrictionItem

Element

ClientRestrictionEnum

Имя ограничения:

CAMPAIGNS_TOTAL_PER_CLIENT — максимальное количество кампаний у рекламодателя.

CAMPAIGNS_UNARCHIVED_PER_CLIENT — максимальное количество кампаний, не находящихся в архиве.

ADGROUPS_TOTAL_PER_CAMPAIGN — максимальное количество групп в кампании.

ADS_TOTAL_PER_ADGROUP — максимальное количество объявлений в группе.

KEYWORDS_TOTAL_PER_ADGROUP — максимальное количество ключевых фраз в группе.

AD_EXTENSIONS_TOTAL — максимальное количество расширений к объявлениям у рекламодателя.

STAT_REPORTS_TOTAL_IN_QUEUE — максимальное количество одновременно формируемых статистических отчетов.

FORECAST_REPORTS_TOTAL_IN_QUEUE — максимальное количество хранимых на сервере отчетов о прогнозируемом бюджете, количестве показов и кликов.

WORDSTAT_REPORTS_TOTAL_IN_QUEUE — максимальное количество хранимых на сервере отчетов о статистике поисковых запросов.

API_POINTS — суточный лимит баллов.

GENERAL_DOMAIN_BLACKLIST_SIZE — максимальное количество площадок, на которых запрещены показы объявлений.

VIDEO_DOMAIN_BLACKLIST_SIZE — максимальное количество площадок, на которых запрещены показы видеообъявлений.

Value

int

Значение ограничения.

Структура ClientSettingGetItem

Option

ClientSettingGetEnum

Имя настройки:

CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.

DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).

SHARED_ACCOUNT_ENABLED — подключен общий счет.

Value

YesNoEnum

Значение настройки.

Структура TinInfoGet

TinType

TinTypeEnum

Тип организации:

Tin

string

Номер налогоплательщика либо его аналог в стране регистрации.

Структура ErirAttributesGet

Organization

OrganizationGet

Информация об организации конечного рекламодателя.

Contract

ContractGet

Информация о договоре клиента-контрагента с конечным рекламодателем.

Contragent

ContragentGet

Информация о контрагенте конечного рекламодателя.

Структура OrganizationGet

Name

string

Наименование организации (до 255 символов).

EpayNumber

string

Номер электронного средства платежа (до 255 символов).

RegNumber

string

Регистрационный номер либо его аналог (до 255 символов).

OksmNumber

string

Код страны регистрации юрлица в соответствии с ОКСМ (до 3 символов, содержит только цифры).

OkvedCode

string

Код вида деятельности по ОКВЭД.

Структура ContractGet

Number

string

Номер договора (до 255 символов).

Date

string

Дата договора в формате YYYY-MM-DD (не раньше 01.01.1991).

Type

ContractTypeEnum

Тип договора:

ActionType

ContractActionTypeEnum

Тип осуществляемых посредником-представителем действий:

SubjectType

ContractSubjectTypeEnum

Предмет договора:

Price

ContractPrice

Цена договора (не более двух знаков после разделителя).

Структура ContractPrice

Amount

decimal

Стоимость договора.

IncludingVat

YesNoEnum

Включен ли в стоимость НДС.

Структура ContragentGet

Name

string

Наименование (до 255 символов).

Phone

string

Номер телефона (до 50 символов, содержит только цифры и должен начинаться с кода страны).

EpayNumber

string

Номер электронного средства платежа (до 255 символов).

RegNumber

string

Регистрационный номер либо его аналог (до 255 символов).

OksmNumber

string

Код страны регистрации юрлица в соответствии с ОКСМ (до 3 символов, содержит только цифры).

TinInfo

TinInfoGet

Налоговые данные контрагента.

- Как начать работу с API
- Руководство разработчика
- Справочник API   О справочнике   AdExtensions: операции с расширениями объявлений   AdGroups: операции с группами объявлений   AdImages: операции с изображениями   Ads: операции с объявлениями   AdVideos: операции с видео   AgencyClients: управление клиентами агентства   add   addPassportOrganization   addPassportOrganizationMember   get   update   AudienceTargets: управление условиями нацеливания на аудиторию   Bids: управление ставками   Businesses: получение профилей организаций   BidModifiers: управление корректировками ставок   Campaigns: управление кампаниями   Changes: проверка наличия изменений   Clients: управление параметрами рекламодателя и настройками пользователя   Creatives: получение креативов   Dictionaries: получение справочных данных   Feeds: операции с фидами   KeywordBids: управление ставками   Keywords: управление ключевыми фразами и автотаргетингами   KeywordsResearch: предобработка ключевых фраз   Leads: получение данных из форм на Турбо-страницах   NegativeKeywordSharedSets: управление наборами минус-фраз   RetargetingLists: управление условиями ретаргетинга и подбора аудитории   Sitelinks: операции с быстрыми ссылками   Strategies: операции с пакетными стратегиями   TurboPages: получение параметров Турбо-страниц   Ошибки и предупреждения   Справочные данные
- О справочнике
- AdExtensions: операции с расширениями объявлений
- AdGroups: операции с группами объявлений
- AdImages: операции с изображениями
- Ads: операции с объявлениями
- AdVideos: операции с видео
- AgencyClients: управление клиентами агентства   add   addPassportOrganization   addPassportOrganizationMember   get   update
- add
- addPassportOrganization
- addPassportOrganizationMember
- get
- update
- AudienceTargets: управление условиями нацеливания на аудиторию
- Bids: управление ставками
- Businesses: получение профилей организаций
- BidModifiers: управление корректировками ставок
- Campaigns: управление кампаниями
- Changes: проверка наличия изменений
- Clients: управление параметрами рекламодателя и настройками пользователя
- Creatives: получение креативов
- Dictionaries: получение справочных данных
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
- AgencyClients: управление клиентами агентства   add   addPassportOrganization   addPassportOrganizationMember   get   update
- add
- addPassportOrganization
- addPassportOrganizationMember
- get
- update
- AudienceTargets: управление условиями нацеливания на аудиторию
- Bids: управление ставками
- Businesses: получение профилей организаций
- BidModifiers: управление корректировками ставок
- Campaigns: управление кампаниями
- Changes: проверка наличия изменений
- Clients: управление параметрами рекламодателя и настройками пользователя
- Creatives: получение креативов
- Dictionaries: получение справочных данных
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

- add
- addPassportOrganization
- addPassportOrganizationMember
- get
- update

- Узнайте больше
- Запрос
- Ответ

- Узнайте больше
- Запрос
- Ответ

- В HTTP-заголовке  Authorization  укажите токен, полученный для представителя агентства.
- HTTP-заголовок  Client-Login  не указывайте.

- Клиент (Client)
- Роли и доступы пользователей Директа
- Как работает метод get

- Параметры  Login ,  ClientInfo ,  CreatedAt ,  Notification ,  Phone  относятся к главному представителю рекламодателя (см. раздел  Роли и доступы пользователей Директа ). Остальные параметры относятся к рекламодателю.
- Если в запросе в параметре  Logins  указан логин представителя рекламодателя, который не является главным представителем, то ответ будет содержать логин главного представителя, отличающийся от логина в запросе.
- Если в запросе в параметре  Logins  указано несколько логинов представителей одного рекламодателя, рекламодатель (и его главный представитель) будет присутствовать в ответе только один раз.
- Список всех представителей рекламодателя представлен в параметре ответа  Representatives .

- SEARCH.
- NETWORK.
- NONE.

- TEXT_CAMPAIGN.
- MOBILE_APP_CAMAIGN.
- DYNAMIC_TEXT_CAMPAIGN.
- CPM_BANNER_CAMPAIGN.
- SMART_CAMPAIGN.
- CONTENT_PROMOTION.
- BILLING_AGGREGATE.
- UNIFIED_CAMPAIGN.

- EDIT_CAMPAIGNS — редактирование кампаний.
- IMPORT_XLS — управление кампаниями с помощью файлов (см. разделы  Управление кампаниями с помощью файлов формата XLS и XLSX  и  Загрузка кампаний из CSV-файлов  помощи Директа).
- TRANSFER_MONEY — перенос средств между кампаниями (см. раздел  Перенос средств между кампаниями ).

- RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.
- TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.
- TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

- CHIEF — главный представитель рекламодателя.
- DELEGATE — представитель рекламодателя с полным доступом.
- READONLY — представитель с доступом “Только чтение”.
- UNKNOWN — роль не поддерживается в данной версии API.

- CAMPAIGNS_TOTAL_PER_CLIENT — максимальное количество кампаний у рекламодателя.
- CAMPAIGNS_UNARCHIVED_PER_CLIENT — максимальное количество кампаний, не находящихся в архиве.
- ADGROUPS_TOTAL_PER_CAMPAIGN — максимальное количество групп в кампании.
- ADS_TOTAL_PER_ADGROUP — максимальное количество объявлений в группе.
- KEYWORDS_TOTAL_PER_ADGROUP — максимальное количество ключевых фраз в группе.
- AD_EXTENSIONS_TOTAL — максимальное количество расширений к объявлениям у рекламодателя.
- STAT_REPORTS_TOTAL_IN_QUEUE — максимальное количество одновременно формируемых статистических отчетов.
- FORECAST_REPORTS_TOTAL_IN_QUEUE — максимальное количество хранимых на сервере отчетов о прогнозируемом бюджете, количестве показов и кликов.
- WORDSTAT_REPORTS_TOTAL_IN_QUEUE — максимальное количество хранимых на сервере отчетов о статистике поисковых запросов.
- API_POINTS — суточный лимит баллов.
- GENERAL_DOMAIN_BLACKLIST_SIZE — максимальное количество площадок, на которых запрещены показы объявлений.
- VIDEO_DOMAIN_BLACKLIST_SIZE — максимальное количество площадок, на которых запрещены показы видеообъявлений.

- CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.
- DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).
- SHARED_ACCOUNT_ENABLED — подключен общий счет.

- LEGAL — юридическое лицо;
- PHYSICAL — физическое лицо;
- INDIVIDUAL — индивидуальный предприниматель;
- FOREIGN_LEGAL — иностранное юридическое лицо;
- FOREIGN_PHYSICAL — иностранное физическое лицо.

- CONTRACT — договор оказания услуг;
- INTERMEDIARY_CONTRACT — посреднический договор;
- ADDITIONAL_AGREEMENT — дополнительное соглашение.

- COMMERCIAL — коммерческое представительство;
- DISTRIBUTION — действия в целях распространения рекламы;
- CONCLUDE — заключение договоров;
- OTHER — иное.

- REPRESENTATION — представительство;
- MEDIATION — посредничество;
- DISTRIBUTION — договор на распространение рекламы;
- ORG_DISTRIBUTION — договор на организацию распространения рекламы;
- OTHER — иное.

- Узнайте больше
- Запрос
- Ответ

- В HTTP-заголовке  Authorization  укажите токен, полученный для представителя агентства.
- HTTP-заголовок  Client-Login  не указывайте.

- Клиент (Client)
- Роли и доступы пользователей Директа
- Как работает метод get

- Параметры  Login ,  ClientInfo ,  CreatedAt ,  Notification ,  Phone  относятся к главному представителю рекламодателя (см. раздел  Роли и доступы пользователей Директа ). Остальные параметры относятся к рекламодателю.
- Если в запросе в параметре  Logins  указан логин представителя рекламодателя, который не является главным представителем, то ответ будет содержать логин главного представителя, отличающийся от логина в запросе.
- Если в запросе в параметре  Logins  указано несколько логинов представителей одного рекламодателя, рекламодатель (и его главный представитель) будет присутствовать в ответе только один раз.
- Список всех представителей рекламодателя представлен в параметре ответа  Representatives .

- SEARCH.
- NETWORK.
- NONE.

- TEXT_CAMPAIGN.
- MOBILE_APP_CAMAIGN.
- DYNAMIC_TEXT_CAMPAIGN.
- CPM_BANNER_CAMPAIGN.
- SMART_CAMPAIGN.
- CONTENT_PROMOTION.
- BILLING_AGGREGATE.
- UNIFIED_CAMPAIGN.

- EDIT_CAMPAIGNS — редактирование кампаний.
- IMPORT_XLS — управление кампаниями с помощью файлов (см. разделы  Управление кампаниями с помощью файлов формата XLS и XLSX  и  Загрузка кампаний из CSV-файлов  помощи Директа).
- TRANSFER_MONEY — перенос средств между кампаниями (см. раздел  Перенос средств между кампаниями ).

- RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.
- TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.
- TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

- CHIEF — главный представитель рекламодателя.
- DELEGATE — представитель рекламодателя с полным доступом.
- READONLY — представитель с доступом “Только чтение”.
- UNKNOWN — роль не поддерживается в данной версии API.

- CAMPAIGNS_TOTAL_PER_CLIENT — максимальное количество кампаний у рекламодателя.
- CAMPAIGNS_UNARCHIVED_PER_CLIENT — максимальное количество кампаний, не находящихся в архиве.
- ADGROUPS_TOTAL_PER_CAMPAIGN — максимальное количество групп в кампании.
- ADS_TOTAL_PER_ADGROUP — максимальное количество объявлений в группе.
- KEYWORDS_TOTAL_PER_ADGROUP — максимальное количество ключевых фраз в группе.
- AD_EXTENSIONS_TOTAL — максимальное количество расширений к объявлениям у рекламодателя.
- STAT_REPORTS_TOTAL_IN_QUEUE — максимальное количество одновременно формируемых статистических отчетов.
- FORECAST_REPORTS_TOTAL_IN_QUEUE — максимальное количество хранимых на сервере отчетов о прогнозируемом бюджете, количестве показов и кликов.
- WORDSTAT_REPORTS_TOTAL_IN_QUEUE — максимальное количество хранимых на сервере отчетов о статистике поисковых запросов.
- API_POINTS — суточный лимит баллов.
- GENERAL_DOMAIN_BLACKLIST_SIZE — максимальное количество площадок, на которых запрещены показы объявлений.
- VIDEO_DOMAIN_BLACKLIST_SIZE — максимальное количество площадок, на которых запрещены показы видеообъявлений.

- CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.
- DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).
- SHARED_ACCOUNT_ENABLED — подключен общий счет.

- LEGAL — юридическое лицо;
- PHYSICAL — физическое лицо;
- INDIVIDUAL — индивидуальный предприниматель;
- FOREIGN_LEGAL — иностранное юридическое лицо;
- FOREIGN_PHYSICAL — иностранное физическое лицо.

- CONTRACT — договор оказания услуг;
- INTERMEDIARY_CONTRACT — посреднический договор;
- ADDITIONAL_AGREEMENT — дополнительное соглашение.

- COMMERCIAL — коммерческое представительство;
- DISTRIBUTION — действия в целях распространения рекламы;
- CONCLUDE — заключение договоров;
- OTHER — иное.

- REPRESENTATION — представительство;
- MEDIATION — посредничество;
- DISTRIBUTION — договор на распространение рекламы;
- ORG_DISTRIBUTION — договор на организацию распространения рекламы;
- OTHER — иное.

`AgencyClients`

`Authorization`

`Client-Login`

```
{
   "method" :  "get" ,
   "params" : {  /* params */ 
     "SelectionCriteria" : {   /* AgencyClientsSelectionCriteria */ 
       "Logins" : [(string), ... ],
       "Archived" : (  "YES"  |  "NO"  )
    },  /* required */ 
     "FieldNames" : [(  "AccountQuality"  |  "Archived"  |  "ClientId"  |  "ClientInfo"  |  "CountryId"  |  "CreatedAt"  |  "Currency"  |  "Grants"  |  "Bonuses"  |  "Login"  |  "Notification"  |  "OverdraftSumAvailable"  |  "Phone"  |  "Representatives"  |  "Restrictions"  |  "Settings"  |  "Type"  |  "VatRate"  |  "ForbiddenPlatform"  |  "AvailableCampaignTypes"  ), ... ],  /* required */ 
     "TinInfoFieldNames"  : [(  "TinType"  |  "Tin" ), ... ],
     "OrganizationFieldNames" : [(  "Name"  |  "EpayNumber"  |  "RegNumber"  |  "OksmNumber"  |  "OkvedCode"  ), ... ],
     "ContractFieldNames" : [(  "Number"  |  "Date"  |  "Price"  |  "Type"  |  "ActionType"  |  "SubjectType"  ), ... ],
     "ContragentFieldNames" : [(  "Name"  |  "Phone"  |  "EpayNumber"  |  "RegNumber"  |  "OksmNumber"  ), ... ],
     "ContragentTinInfoFieldNames" : [(  "TinType"  |  "Tin"  ), ... ],
     "Page" : {   /* LimitOffset */ 
       "Limit" : (long),
       "Offset" : (long)
    }
  }
}
```

```
{
   "method" :  "get" ,
   "params" : {  /* params */ 
     "SelectionCriteria" : {   /* AgencyClientsSelectionCriteria */ 
       "Logins" : [(string), ... ],
       "Archived" : (  "YES"  |  "NO"  )
    },  /* required */ 
     "FieldNames" : [(  "AccountQuality"  |  "Archived"  |  "ClientId"  |  "ClientInfo"  |  "CountryId"  |  "CreatedAt"  |  "Currency"  |  "Grants"  |  "Bonuses"  |  "Login"  |  "Notification"  |  "OverdraftSumAvailable"  |  "Phone"  |  "Representatives"  |  "Restrictions"  |  "Settings"  |  "Type"  |  "VatRate"  |  "ForbiddenPlatform"  |  "AvailableCampaignTypes"  ), ... ],  /* required */ 
     "TinInfoFieldNames"  : [(  "TinType"  |  "Tin" ), ... ],
     "OrganizationFieldNames" : [(  "Name"  |  "EpayNumber"  |  "RegNumber"  |  "OksmNumber"  |  "OkvedCode"  ), ... ],
     "ContractFieldNames" : [(  "Number"  |  "Date"  |  "Price"  |  "Type"  |  "ActionType"  |  "SubjectType"  ), ... ],
     "ContragentFieldNames" : [(  "Name"  |  "Phone"  |  "EpayNumber"  |  "RegNumber"  |  "OksmNumber"  ), ... ],
     "ContragentTinInfoFieldNames" : [(  "TinType"  |  "Tin"  ), ... ],
     "Page" : {   /* LimitOffset */ 
       "Limit" : (long),
       "Offset" : (long)
    }
  }
}
```

`SelectionCriteria`

`SelectionCriteria`

`FieldNames`

`TinInfoFieldNames`

`OrganizationFieldNames`

`ContractFieldNames`

`ContragentFieldNames`

`ContragentTinInfoFieldNames`

`Page`

`Logins`

`Archived`

`Login`

`ClientInfo`

`CreatedAt`

`Notification`

`Phone`

`Logins`

`Logins`

`Representatives`

```
{
   "result" : {  /* result */ 
     "Clients" : [{   /* ClientGetItem */ 
       "AccountQuality" : (decimal),  /* nillable */ 
       "Archived" : (  "YES"  |  "NO"  ),
       "ClientId" : (long),
       "ClientInfo" : (string),
       "CountryId" : (int),
       "CreatedAt" : (string),
       "Currency" : (  "RUB"  |  "BYN"  |  "CHF"  |  "EUR"  |  "KZT"  |  "TRY"  |  "UAH"  |  "USD"  ),
       "Grants" : [{   /* GrantGetItem */ 
         "Privilege" : (  "EDIT_CAMPAIGNS"  |  "IMPORT_XLS"  |  "TRANSFER_MONEY"  ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  ),  /* required */ 
         "Agency" : (string)
      }, ... ],
       "Bonuses"  : {   /* BonusesGet */ 
         "AwaitingBonus"  : (long)  /* required */ ,
         "AwaitingBonusWithoutNds"  : (long)  /* required */ 
      },
       "Login" : (string),
       "Notification" : {   /* NotificationGet */ 
         "Lang" : (  "RU"  |  "UK"  |  "EN"  |  "TR"  ),  /* required */ 
         "SmsPhoneNumber" : (string),  /* required */ 
         "Email" : (string),  /* required */ 
         "EmailSubscriptions" : [{   /* EmailSubscriptionItem */ 
           "Option" : (  "RECEIVE_RECOMMENDATIONS"  |  "TRACK_MANAGED_CAMPAIGNS"  |  "TRACK_POSITION_CHANGES"  ),  /* required */ 
           "Value" : (  "YES"  |  "NO"  )  /* required */ 
        }, ... ]  /* required */ 
      },
       "OverdraftSumAvailable" : (long),
       "Phone" : (string),
       "Representatives" : [{   /* Representative */ 
         "Login" : (string),  /* required */ 
         "Email" : (string),  /* required */ 
         "Role" : (  "CHIEF"  |  "DELEGATE"  |  "READONLY"  |  "UNKNOWN"  )  /* required */ 
      }, ... ],
       "Restrictions" : [{   /* ClientRestrictionItem */ 
         "Element" : (  "CAMPAIGNS_TOTAL_PER_CLIENT"  |  "CAMPAIGNS_UNARCHIVED_PER_CLIENT"  |  "ADGROUPS_TOTAL_PER_CAMPAIGN"  |  "ADS_TOTAL_PER_ADGROUP"  |  "KEYWORDS_TOTAL_PER_ADGROUP"  |  "AD_EXTENSIONS_TOTAL"  |  "STAT_REPORTS_TOTAL_IN_QUEUE"  |  "FORECAST_REPORTS_TOTAL_IN_QUEUE"  |  "WORDSTAT_REPORTS_TOTAL_IN_QUEUE"  |  "API_POINTS"  |  "GENERAL_DOMAIN_BLACKLIST_SIZE"  |  "VIDEO_DOMAIN_BLACKLIST_SIZE"  ),  /* required */ 
         "Value" : (int)  /* required */ 
      }, ... ],
       "Settings" : [{   /* ClientSettingGetItem */ 
         "Option" : (  "CORRECT_TYPOS_AUTOMATICALLY"  |  "DISPLAY_STORE_RATING"  |  "SHARED_ACCOUNT_ENABLED"   ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  )  /* required */ 
      }, ... ],
       "Type" : (string),
       "VatRate" : (decimal),  /* nillable */ 
       "ForbiddenPlatform" : ( "SEARCH"  |  "NETWORK"  |  "NONE" ),
       "AvailableCampaignTypes" : ( "TEXT_CAMPAIGN"  |  "MOBILE_APP_CAMPAIGN"  |  "DYNAMIC_TEXT_CAMPAIGN"  |  "CPM_BANNER_CAMPAIGN"  |  "SMART_CAMPAIGN"  |  "CONTENT_PROMOTION"  |  "BILLING_AGGREGATE"  |  "UNIFIED_CAMPAIGN"  ),
       "TinInfo" : {  /* TinInfoGet */ 
         "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
         "Tin" : (string)  /* nillable */ 
      },
       "ErirAttributes" : {  /* ErirAttributesGet */ 
         "Organization" : {  /* OrganizationGet */ 
           "Name" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "OkvedCode" : (string)  /* nillable */ 
        },
         "Contract" : {  /* ContractGet */ 
           "Number" : (string),  /* nillable */ 
           "Date" : (string),  /* nillable */ 
           "Type" : (  "CONTRACT"  |  "INTERMEDIARY_CONTRACT"  |  "ADDITIONAL_AGREEMENT"  ),  /* nillable */ 
           "ActionType" : (  "COMMERCIAL"  |  "DISTRIBUTION"  |  "CONCLUDE"  |  "OTHER"  ),  /* nillable */ 
           "SubjectType" : (  "REPRESENTATION"  |  "MEDIATION"  |  "DISTRIBUTION"  |  "ORG_DISTRIBUTION"  |  "OTHER"  ),  /* nillable */ 
           "Price" : {  /* PriceGet */ 
             "Amount" : (decimal),  /* required */ 
             "IncludingVat" : (  "YES"  |  "NO"  )  /* required */ 
          }
        },
         "Contragent" : {  /* ContragentGet */ 
           "Name" : (string),  /* nillable */ 
           "Phone" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "TinInfo" : {  /* TinInfoGet */ 
             "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
             "Tin" : (string)  /* nillable */ 
          }
        }
      }
    }, ... ],
     "LimitedBy" : (long)
  }
}
```

```
{
   "result" : {  /* result */ 
     "Clients" : [{   /* ClientGetItem */ 
       "AccountQuality" : (decimal),  /* nillable */ 
       "Archived" : (  "YES"  |  "NO"  ),
       "ClientId" : (long),
       "ClientInfo" : (string),
       "CountryId" : (int),
       "CreatedAt" : (string),
       "Currency" : (  "RUB"  |  "BYN"  |  "CHF"  |  "EUR"  |  "KZT"  |  "TRY"  |  "UAH"  |  "USD"  ),
       "Grants" : [{   /* GrantGetItem */ 
         "Privilege" : (  "EDIT_CAMPAIGNS"  |  "IMPORT_XLS"  |  "TRANSFER_MONEY"  ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  ),  /* required */ 
         "Agency" : (string)
      }, ... ],
       "Bonuses"  : {   /* BonusesGet */ 
         "AwaitingBonus"  : (long)  /* required */ ,
         "AwaitingBonusWithoutNds"  : (long)  /* required */ 
      },
       "Login" : (string),
       "Notification" : {   /* NotificationGet */ 
         "Lang" : (  "RU"  |  "UK"  |  "EN"  |  "TR"  ),  /* required */ 
         "SmsPhoneNumber" : (string),  /* required */ 
         "Email" : (string),  /* required */ 
         "EmailSubscriptions" : [{   /* EmailSubscriptionItem */ 
           "Option" : (  "RECEIVE_RECOMMENDATIONS"  |  "TRACK_MANAGED_CAMPAIGNS"  |  "TRACK_POSITION_CHANGES"  ),  /* required */ 
           "Value" : (  "YES"  |  "NO"  )  /* required */ 
        }, ... ]  /* required */ 
      },
       "OverdraftSumAvailable" : (long),
       "Phone" : (string),
       "Representatives" : [{   /* Representative */ 
         "Login" : (string),  /* required */ 
         "Email" : (string),  /* required */ 
         "Role" : (  "CHIEF"  |  "DELEGATE"  |  "READONLY"  |  "UNKNOWN"  )  /* required */ 
      }, ... ],
       "Restrictions" : [{   /* ClientRestrictionItem */ 
         "Element" : (  "CAMPAIGNS_TOTAL_PER_CLIENT"  |  "CAMPAIGNS_UNARCHIVED_PER_CLIENT"  |  "ADGROUPS_TOTAL_PER_CAMPAIGN"  |  "ADS_TOTAL_PER_ADGROUP"  |  "KEYWORDS_TOTAL_PER_ADGROUP"  |  "AD_EXTENSIONS_TOTAL"  |  "STAT_REPORTS_TOTAL_IN_QUEUE"  |  "FORECAST_REPORTS_TOTAL_IN_QUEUE"  |  "WORDSTAT_REPORTS_TOTAL_IN_QUEUE"  |  "API_POINTS"  |  "GENERAL_DOMAIN_BLACKLIST_SIZE"  |  "VIDEO_DOMAIN_BLACKLIST_SIZE"  ),  /* required */ 
         "Value" : (int)  /* required */ 
      }, ... ],
       "Settings" : [{   /* ClientSettingGetItem */ 
         "Option" : (  "CORRECT_TYPOS_AUTOMATICALLY"  |  "DISPLAY_STORE_RATING"  |  "SHARED_ACCOUNT_ENABLED"   ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  )  /* required */ 
      }, ... ],
       "Type" : (string),
       "VatRate" : (decimal),  /* nillable */ 
       "ForbiddenPlatform" : ( "SEARCH"  |  "NETWORK"  |  "NONE" ),
       "AvailableCampaignTypes" : ( "TEXT_CAMPAIGN"  |  "MOBILE_APP_CAMPAIGN"  |  "DYNAMIC_TEXT_CAMPAIGN"  |  "CPM_BANNER_CAMPAIGN"  |  "SMART_CAMPAIGN"  |  "CONTENT_PROMOTION"  |  "BILLING_AGGREGATE"  |  "UNIFIED_CAMPAIGN"  ),
       "TinInfo" : {  /* TinInfoGet */ 
         "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
         "Tin" : (string)  /* nillable */ 
      },
       "ErirAttributes" : {  /* ErirAttributesGet */ 
         "Organization" : {  /* OrganizationGet */ 
           "Name" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "OkvedCode" : (string)  /* nillable */ 
        },
         "Contract" : {  /* ContractGet */ 
           "Number" : (string),  /* nillable */ 
           "Date" : (string),  /* nillable */ 
           "Type" : (  "CONTRACT"  |  "INTERMEDIARY_CONTRACT"  |  "ADDITIONAL_AGREEMENT"  ),  /* nillable */ 
           "ActionType" : (  "COMMERCIAL"  |  "DISTRIBUTION"  |  "CONCLUDE"  |  "OTHER"  ),  /* nillable */ 
           "SubjectType" : (  "REPRESENTATION"  |  "MEDIATION"  |  "DISTRIBUTION"  |  "ORG_DISTRIBUTION"  |  "OTHER"  ),  /* nillable */ 
           "Price" : {  /* PriceGet */ 
             "Amount" : (decimal),  /* required */ 
             "IncludingVat" : (  "YES"  |  "NO"  )  /* required */ 
          }
        },
         "Contragent" : {  /* ContragentGet */ 
           "Name" : (string),  /* nillable */ 
           "Phone" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "TinInfo" : {  /* TinInfoGet */ 
             "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
             "Tin" : (string)  /* nillable */ 
          }
        }
      }
    }, ... ],
     "LimitedBy" : (long)
  }
}
```

`Clients`

`LimitedBy`

`AccountQuality`

`Archived`

`ClientId`

`ClientInfo`

`CountryId`

`CreatedAt`

`Currency`

`Grants`

`Bonuses`

`Login`

`Notification`

`OverdraftSumAvailable`

`Phone`

`Representatives`

`Restrictions`

`Settings`

`Type`

`VatRate`

`ForbiddenPlatform`

`AvailableCampaignTypes`

`TinInfo`

`ErirAttributes`

`Privilege`

`Value`

`Agency`

`AwaitingBonus`

`AwaitingBonusWithoutNds`

`Lang`

`SmsPhoneNumber`

`Email`

`EmailSubscriptions`

`Option`

`Value`

`Login`

`Email`

`Role`

`Element`

`Value`

`Option`

`Value`

`TinType`

`Tin`

`Organization`

`Contract`

`Contragent`

`Name`

`EpayNumber`

`RegNumber`

`OksmNumber`

`OkvedCode`

`Number`

`Date`

`Type`

`ActionType`

`SubjectType`

`Price`

`Amount`

`IncludingVat`

`Name`

`Phone`

`EpayNumber`

`RegNumber`

`OksmNumber`

`TinInfo`

`AgencyClients`

`Authorization`

`Client-Login`

```
{
   "method" :  "get" ,
   "params" : {  /* params */ 
     "SelectionCriteria" : {   /* AgencyClientsSelectionCriteria */ 
       "Logins" : [(string), ... ],
       "Archived" : (  "YES"  |  "NO"  )
    },  /* required */ 
     "FieldNames" : [(  "AccountQuality"  |  "Archived"  |  "ClientId"  |  "ClientInfo"  |  "CountryId"  |  "CreatedAt"  |  "Currency"  |  "Grants"  |  "Bonuses"  |  "Login"  |  "Notification"  |  "OverdraftSumAvailable"  |  "Phone"  |  "Representatives"  |  "Restrictions"  |  "Settings"  |  "Type"  |  "VatRate"  |  "ForbiddenPlatform"  |  "AvailableCampaignTypes"  ), ... ],  /* required */ 
     "TinInfoFieldNames"  : [(  "TinType"  |  "Tin" ), ... ],
     "OrganizationFieldNames" : [(  "Name"  |  "EpayNumber"  |  "RegNumber"  |  "OksmNumber"  |  "OkvedCode"  ), ... ],
     "ContractFieldNames" : [(  "Number"  |  "Date"  |  "Price"  |  "Type"  |  "ActionType"  |  "SubjectType"  ), ... ],
     "ContragentFieldNames" : [(  "Name"  |  "Phone"  |  "EpayNumber"  |  "RegNumber"  |  "OksmNumber"  ), ... ],
     "ContragentTinInfoFieldNames" : [(  "TinType"  |  "Tin"  ), ... ],
     "Page" : {   /* LimitOffset */ 
       "Limit" : (long),
       "Offset" : (long)
    }
  }
}
```

```
{
   "method" :  "get" ,
   "params" : {  /* params */ 
     "SelectionCriteria" : {   /* AgencyClientsSelectionCriteria */ 
       "Logins" : [(string), ... ],
       "Archived" : (  "YES"  |  "NO"  )
    },  /* required */ 
     "FieldNames" : [(  "AccountQuality"  |  "Archived"  |  "ClientId"  |  "ClientInfo"  |  "CountryId"  |  "CreatedAt"  |  "Currency"  |  "Grants"  |  "Bonuses"  |  "Login"  |  "Notification"  |  "OverdraftSumAvailable"  |  "Phone"  |  "Representatives"  |  "Restrictions"  |  "Settings"  |  "Type"  |  "VatRate"  |  "ForbiddenPlatform"  |  "AvailableCampaignTypes"  ), ... ],  /* required */ 
     "TinInfoFieldNames"  : [(  "TinType"  |  "Tin" ), ... ],
     "OrganizationFieldNames" : [(  "Name"  |  "EpayNumber"  |  "RegNumber"  |  "OksmNumber"  |  "OkvedCode"  ), ... ],
     "ContractFieldNames" : [(  "Number"  |  "Date"  |  "Price"  |  "Type"  |  "ActionType"  |  "SubjectType"  ), ... ],
     "ContragentFieldNames" : [(  "Name"  |  "Phone"  |  "EpayNumber"  |  "RegNumber"  |  "OksmNumber"  ), ... ],
     "ContragentTinInfoFieldNames" : [(  "TinType"  |  "Tin"  ), ... ],
     "Page" : {   /* LimitOffset */ 
       "Limit" : (long),
       "Offset" : (long)
    }
  }
}
```

`SelectionCriteria`

`SelectionCriteria`

`FieldNames`

`TinInfoFieldNames`

`OrganizationFieldNames`

`ContractFieldNames`

`ContragentFieldNames`

`ContragentTinInfoFieldNames`

`Page`

`Logins`

`Archived`

`Login`

`ClientInfo`

`CreatedAt`

`Notification`

`Phone`

`Logins`

`Logins`

`Representatives`

```
{
   "result" : {  /* result */ 
     "Clients" : [{   /* ClientGetItem */ 
       "AccountQuality" : (decimal),  /* nillable */ 
       "Archived" : (  "YES"  |  "NO"  ),
       "ClientId" : (long),
       "ClientInfo" : (string),
       "CountryId" : (int),
       "CreatedAt" : (string),
       "Currency" : (  "RUB"  |  "BYN"  |  "CHF"  |  "EUR"  |  "KZT"  |  "TRY"  |  "UAH"  |  "USD"  ),
       "Grants" : [{   /* GrantGetItem */ 
         "Privilege" : (  "EDIT_CAMPAIGNS"  |  "IMPORT_XLS"  |  "TRANSFER_MONEY"  ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  ),  /* required */ 
         "Agency" : (string)
      }, ... ],
       "Bonuses"  : {   /* BonusesGet */ 
         "AwaitingBonus"  : (long)  /* required */ ,
         "AwaitingBonusWithoutNds"  : (long)  /* required */ 
      },
       "Login" : (string),
       "Notification" : {   /* NotificationGet */ 
         "Lang" : (  "RU"  |  "UK"  |  "EN"  |  "TR"  ),  /* required */ 
         "SmsPhoneNumber" : (string),  /* required */ 
         "Email" : (string),  /* required */ 
         "EmailSubscriptions" : [{   /* EmailSubscriptionItem */ 
           "Option" : (  "RECEIVE_RECOMMENDATIONS"  |  "TRACK_MANAGED_CAMPAIGNS"  |  "TRACK_POSITION_CHANGES"  ),  /* required */ 
           "Value" : (  "YES"  |  "NO"  )  /* required */ 
        }, ... ]  /* required */ 
      },
       "OverdraftSumAvailable" : (long),
       "Phone" : (string),
       "Representatives" : [{   /* Representative */ 
         "Login" : (string),  /* required */ 
         "Email" : (string),  /* required */ 
         "Role" : (  "CHIEF"  |  "DELEGATE"  |  "READONLY"  |  "UNKNOWN"  )  /* required */ 
      }, ... ],
       "Restrictions" : [{   /* ClientRestrictionItem */ 
         "Element" : (  "CAMPAIGNS_TOTAL_PER_CLIENT"  |  "CAMPAIGNS_UNARCHIVED_PER_CLIENT"  |  "ADGROUPS_TOTAL_PER_CAMPAIGN"  |  "ADS_TOTAL_PER_ADGROUP"  |  "KEYWORDS_TOTAL_PER_ADGROUP"  |  "AD_EXTENSIONS_TOTAL"  |  "STAT_REPORTS_TOTAL_IN_QUEUE"  |  "FORECAST_REPORTS_TOTAL_IN_QUEUE"  |  "WORDSTAT_REPORTS_TOTAL_IN_QUEUE"  |  "API_POINTS"  |  "GENERAL_DOMAIN_BLACKLIST_SIZE"  |  "VIDEO_DOMAIN_BLACKLIST_SIZE"  ),  /* required */ 
         "Value" : (int)  /* required */ 
      }, ... ],
       "Settings" : [{   /* ClientSettingGetItem */ 
         "Option" : (  "CORRECT_TYPOS_AUTOMATICALLY"  |  "DISPLAY_STORE_RATING"  |  "SHARED_ACCOUNT_ENABLED"   ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  )  /* required */ 
      }, ... ],
       "Type" : (string),
       "VatRate" : (decimal),  /* nillable */ 
       "ForbiddenPlatform" : ( "SEARCH"  |  "NETWORK"  |  "NONE" ),
       "AvailableCampaignTypes" : ( "TEXT_CAMPAIGN"  |  "MOBILE_APP_CAMPAIGN"  |  "DYNAMIC_TEXT_CAMPAIGN"  |  "CPM_BANNER_CAMPAIGN"  |  "SMART_CAMPAIGN"  |  "CONTENT_PROMOTION"  |  "BILLING_AGGREGATE"  |  "UNIFIED_CAMPAIGN"  ),
       "TinInfo" : {  /* TinInfoGet */ 
         "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
         "Tin" : (string)  /* nillable */ 
      },
       "ErirAttributes" : {  /* ErirAttributesGet */ 
         "Organization" : {  /* OrganizationGet */ 
           "Name" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "OkvedCode" : (string)  /* nillable */ 
        },
         "Contract" : {  /* ContractGet */ 
           "Number" : (string),  /* nillable */ 
           "Date" : (string),  /* nillable */ 
           "Type" : (  "CONTRACT"  |  "INTERMEDIARY_CONTRACT"  |  "ADDITIONAL_AGREEMENT"  ),  /* nillable */ 
           "ActionType" : (  "COMMERCIAL"  |  "DISTRIBUTION"  |  "CONCLUDE"  |  "OTHER"  ),  /* nillable */ 
           "SubjectType" : (  "REPRESENTATION"  |  "MEDIATION"  |  "DISTRIBUTION"  |  "ORG_DISTRIBUTION"  |  "OTHER"  ),  /* nillable */ 
           "Price" : {  /* PriceGet */ 
             "Amount" : (decimal),  /* required */ 
             "IncludingVat" : (  "YES"  |  "NO"  )  /* required */ 
          }
        },
         "Contragent" : {  /* ContragentGet */ 
           "Name" : (string),  /* nillable */ 
           "Phone" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "TinInfo" : {  /* TinInfoGet */ 
             "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
             "Tin" : (string)  /* nillable */ 
          }
        }
      }
    }, ... ],
     "LimitedBy" : (long)
  }
}
```

```
{
   "result" : {  /* result */ 
     "Clients" : [{   /* ClientGetItem */ 
       "AccountQuality" : (decimal),  /* nillable */ 
       "Archived" : (  "YES"  |  "NO"  ),
       "ClientId" : (long),
       "ClientInfo" : (string),
       "CountryId" : (int),
       "CreatedAt" : (string),
       "Currency" : (  "RUB"  |  "BYN"  |  "CHF"  |  "EUR"  |  "KZT"  |  "TRY"  |  "UAH"  |  "USD"  ),
       "Grants" : [{   /* GrantGetItem */ 
         "Privilege" : (  "EDIT_CAMPAIGNS"  |  "IMPORT_XLS"  |  "TRANSFER_MONEY"  ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  ),  /* required */ 
         "Agency" : (string)
      }, ... ],
       "Bonuses"  : {   /* BonusesGet */ 
         "AwaitingBonus"  : (long)  /* required */ ,
         "AwaitingBonusWithoutNds"  : (long)  /* required */ 
      },
       "Login" : (string),
       "Notification" : {   /* NotificationGet */ 
         "Lang" : (  "RU"  |  "UK"  |  "EN"  |  "TR"  ),  /* required */ 
         "SmsPhoneNumber" : (string),  /* required */ 
         "Email" : (string),  /* required */ 
         "EmailSubscriptions" : [{   /* EmailSubscriptionItem */ 
           "Option" : (  "RECEIVE_RECOMMENDATIONS"  |  "TRACK_MANAGED_CAMPAIGNS"  |  "TRACK_POSITION_CHANGES"  ),  /* required */ 
           "Value" : (  "YES"  |  "NO"  )  /* required */ 
        }, ... ]  /* required */ 
      },
       "OverdraftSumAvailable" : (long),
       "Phone" : (string),
       "Representatives" : [{   /* Representative */ 
         "Login" : (string),  /* required */ 
         "Email" : (string),  /* required */ 
         "Role" : (  "CHIEF"  |  "DELEGATE"  |  "READONLY"  |  "UNKNOWN"  )  /* required */ 
      }, ... ],
       "Restrictions" : [{   /* ClientRestrictionItem */ 
         "Element" : (  "CAMPAIGNS_TOTAL_PER_CLIENT"  |  "CAMPAIGNS_UNARCHIVED_PER_CLIENT"  |  "ADGROUPS_TOTAL_PER_CAMPAIGN"  |  "ADS_TOTAL_PER_ADGROUP"  |  "KEYWORDS_TOTAL_PER_ADGROUP"  |  "AD_EXTENSIONS_TOTAL"  |  "STAT_REPORTS_TOTAL_IN_QUEUE"  |  "FORECAST_REPORTS_TOTAL_IN_QUEUE"  |  "WORDSTAT_REPORTS_TOTAL_IN_QUEUE"  |  "API_POINTS"  |  "GENERAL_DOMAIN_BLACKLIST_SIZE"  |  "VIDEO_DOMAIN_BLACKLIST_SIZE"  ),  /* required */ 
         "Value" : (int)  /* required */ 
      }, ... ],
       "Settings" : [{   /* ClientSettingGetItem */ 
         "Option" : (  "CORRECT_TYPOS_AUTOMATICALLY"  |  "DISPLAY_STORE_RATING"  |  "SHARED_ACCOUNT_ENABLED"   ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  )  /* required */ 
      }, ... ],
       "Type" : (string),
       "VatRate" : (decimal),  /* nillable */ 
       "ForbiddenPlatform" : ( "SEARCH"  |  "NETWORK"  |  "NONE" ),
       "AvailableCampaignTypes" : ( "TEXT_CAMPAIGN"  |  "MOBILE_APP_CAMPAIGN"  |  "DYNAMIC_TEXT_CAMPAIGN"  |  "CPM_BANNER_CAMPAIGN"  |  "SMART_CAMPAIGN"  |  "CONTENT_PROMOTION"  |  "BILLING_AGGREGATE"  |  "UNIFIED_CAMPAIGN"  ),
       "TinInfo" : {  /* TinInfoGet */ 
         "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
         "Tin" : (string)  /* nillable */ 
      },
       "ErirAttributes" : {  /* ErirAttributesGet */ 
         "Organization" : {  /* OrganizationGet */ 
           "Name" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "OkvedCode" : (string)  /* nillable */ 
        },
         "Contract" : {  /* ContractGet */ 
           "Number" : (string),  /* nillable */ 
           "Date" : (string),  /* nillable */ 
           "Type" : (  "CONTRACT"  |  "INTERMEDIARY_CONTRACT"  |  "ADDITIONAL_AGREEMENT"  ),  /* nillable */ 
           "ActionType" : (  "COMMERCIAL"  |  "DISTRIBUTION"  |  "CONCLUDE"  |  "OTHER"  ),  /* nillable */ 
           "SubjectType" : (  "REPRESENTATION"  |  "MEDIATION"  |  "DISTRIBUTION"  |  "ORG_DISTRIBUTION"  |  "OTHER"  ),  /* nillable */ 
           "Price" : {  /* PriceGet */ 
             "Amount" : (decimal),  /* required */ 
             "IncludingVat" : (  "YES"  |  "NO"  )  /* required */ 
          }
        },
         "Contragent" : {  /* ContragentGet */ 
           "Name" : (string),  /* nillable */ 
           "Phone" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "TinInfo" : {  /* TinInfoGet */ 
             "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
             "Tin" : (string)  /* nillable */ 
          }
        }
      }
    }, ... ],
     "LimitedBy" : (long)
  }
}
```

`Clients`

`LimitedBy`

`AccountQuality`

`Archived`

`ClientId`

`ClientInfo`

`CountryId`

`CreatedAt`

`Currency`

`Grants`

`Bonuses`

`Login`

`Notification`

`OverdraftSumAvailable`

`Phone`

`Representatives`

`Restrictions`

`Settings`

`Type`

`VatRate`

`ForbiddenPlatform`

`AvailableCampaignTypes`

`TinInfo`

`ErirAttributes`

`Privilege`

`Value`

`Agency`

`AwaitingBonus`

`AwaitingBonusWithoutNds`

`Lang`

`SmsPhoneNumber`

`Email`

`EmailSubscriptions`

`Option`

`Value`

`Login`

`Email`

`Role`

`Element`

`Value`

`Option`

`Value`

`TinType`

`Tin`

`Organization`

`Contract`

`Contragent`

`Name`

`EpayNumber`

`RegNumber`

`OksmNumber`

`OkvedCode`

`Number`

`Date`

`Type`

`ActionType`

`SubjectType`

`Price`

`Amount`

`IncludingVat`

`Name`

`Phone`

`EpayNumber`

`RegNumber`

`OksmNumber`

`TinInfo`


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Структура params (для JSON) / GetRequest (для SOAP) |  |
| SelectionCriteria | AgencyClientsSelectionCriteria |
| FieldNames | array of AgencyClientFieldEnum |
| TinInfoFieldNames | array of TinInfoFieldEnum |
| OrganizationFieldNames | array of OrganizationFieldEnum |
| ContractFieldNames | array of ContractFieldEnum |
| ContragentFieldNames | array of ContragentFieldEnum |
| ContragentTinInfoFieldNames | array of TinInfoFieldEnum |
| Page | LimitOffset |
| Структура AgencyClientsSelectionCriteria |  |
| Logins | array of string |
| Archived | YesNoEnum |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Clients | array of ClientGetItem |
| LimitedBy | long |
| AccountQuality | decimal, nillable |
| Archived | YesNoEnum |
| ClientId | long |
| ClientInfo | string |
| CountryId | int |
| CreatedAt | string |
| Currency | CurrencyEnum |
| Grants | array of GrantGetItem |
| Bonuses | BonusesGet |
| Login | string |
| Notification | NotificationGet |
| OverdraftSumAvailable | long |
| Phone | string |
| Representatives | array of Representative |
| Restrictions | array of ClientRestrictionItem |
| Settings | array of ClientSettingGetItem |
| Type | string |
| VatRate | decimal, nillable |
| ForbiddenPlatform | ForbiddenPlatformEnum |
| AvailableCampaignTypes | AvailableCampaignTypesEnum |
| TinInfo | TinInfoGet |
| ErirAttributes | ErirAttributesGet |
| Privilege | PrivilegeEnum |
| Value | YesNoEnum |
| Agency | string |
| AwaitingBonus | long |
| AwaitingBonusWithoutNds | long |
| Lang | LangEnum |
| SmsPhoneNumber | string |
| Email | string |
| EmailSubscriptions | array of EmailSubscriptionItem |
| Option | EmailSubscriptionEnum |
| Value | YesNoEnum |
| Login | string |
| Email | string |
| Role | RepresentativeRoleEnum |
| Element | ClientRestrictionEnum |
| Value | int |
| Option | ClientSettingGetEnum |
| Value | YesNoEnum |
| TinType | TinTypeEnum |
| Tin | string |
| Organization | OrganizationGet |
| Contract | ContractGet |
| Contragent | ContragentGet |
| Name | string |
| EpayNumber | string |
| RegNumber | string |
| OksmNumber | string |
| OkvedCode | string |
| Number | string |
| Date | string |
| Type | ContractTypeEnum |
| ActionType | ContractActionTypeEnum |
| SubjectType | ContractSubjectTypeEnum |
| Price | ContractPrice |
| Amount | decimal |
| IncludingVat | YesNoEnum |
| Name | string |
| Phone | string |
| EpayNumber | string |
| RegNumber | string |
| OksmNumber | string |
| TinInfo | TinInfoGet |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Структура params (для JSON) / GetRequest (для SOAP) |  |
| SelectionCriteria | AgencyClientsSelectionCriteria |
| FieldNames | array of AgencyClientFieldEnum |
| TinInfoFieldNames | array of TinInfoFieldEnum |
| OrganizationFieldNames | array of OrganizationFieldEnum |
| ContractFieldNames | array of ContractFieldEnum |
| ContragentFieldNames | array of ContragentFieldEnum |
| ContragentTinInfoFieldNames | array of TinInfoFieldEnum |
| Page | LimitOffset |
| Структура AgencyClientsSelectionCriteria |  |
| Logins | array of string |
| Archived | YesNoEnum |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Clients | array of ClientGetItem |
| LimitedBy | long |
| AccountQuality | decimal, nillable |
| Archived | YesNoEnum |
| ClientId | long |
| ClientInfo | string |
| CountryId | int |
| CreatedAt | string |
| Currency | CurrencyEnum |
| Grants | array of GrantGetItem |
| Bonuses | BonusesGet |
| Login | string |
| Notification | NotificationGet |
| OverdraftSumAvailable | long |
| Phone | string |
| Representatives | array of Representative |
| Restrictions | array of ClientRestrictionItem |
| Settings | array of ClientSettingGetItem |
| Type | string |
| VatRate | decimal, nillable |
| ForbiddenPlatform | ForbiddenPlatformEnum |
| AvailableCampaignTypes | AvailableCampaignTypesEnum |
| TinInfo | TinInfoGet |
| ErirAttributes | ErirAttributesGet |
| Privilege | PrivilegeEnum |
| Value | YesNoEnum |
| Agency | string |
| AwaitingBonus | long |
| AwaitingBonusWithoutNds | long |
| Lang | LangEnum |
| SmsPhoneNumber | string |
| Email | string |
| EmailSubscriptions | array of EmailSubscriptionItem |
| Option | EmailSubscriptionEnum |
| Value | YesNoEnum |
| Login | string |
| Email | string |
| Role | RepresentativeRoleEnum |
| Element | ClientRestrictionEnum |
| Value | int |
| Option | ClientSettingGetEnum |
| Value | YesNoEnum |
| TinType | TinTypeEnum |
| Tin | string |
| Organization | OrganizationGet |
| Contract | ContractGet |
| Contragent | ContragentGet |
| Name | string |
| EpayNumber | string |
| RegNumber | string |
| OksmNumber | string |
| OkvedCode | string |
| Number | string |
| Date | string |
| Type | ContractTypeEnum |
| ActionType | ContractActionTypeEnum |
| SubjectType | ContractSubjectTypeEnum |
| Price | ContractPrice |
| Amount | decimal |
| IncludingVat | YesNoEnum |
| Name | string |
| Phone | string |
| EpayNumber | string |
| RegNumber | string |
| OksmNumber | string |
| TinInfo | TinInfoGet |

