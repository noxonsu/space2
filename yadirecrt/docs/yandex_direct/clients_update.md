# update  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/clients/update

**Дата скачивания:** 2025-07-01 12:37:57

---

## В этой статье :

# update

## Узнайте больше

## Запрос

## Ответ

### Была ли статья полезна?

# update

## Узнайте больше

## Запрос

## Ответ

### Была ли статья полезна?

Изменяет параметры рекламодателя и настройки пользователя — представителя рекламодателя.

Любой представитель рекламодателя может редактировать параметры рекламодателя и собственные настройки.

Главный представитель рекламодателя может также редактировать настройки другого представителя: для этого необходимо передать логин представителя в HTTP-заголовке запроса  Client-Login .

Примечание

Параметры  ClientInfo ,  Notification ,  Phone  относятся к пользователю — представителю рекламодателя:

Параметр  Settings  относится к рекламодателю и не зависит от представителя.

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / UpdateRequest (для SOAP)

Clients

array of ClientUpdateItem

Параметры рекламодателя и настройки пользователя, которые требуется изменить.

Да

Структура ClientUpdateItem

ClientInfo

string

ФИО пользователя Директа (до 255 символов).

Нет

Notification

NotificationUpdate

Настройки SMS- и email-уведомлений пользователя Директа.

Нет

Phone

string

Номер телефона пользователя Директа (до 255 символов).

Нет

Settings

array of ClientSettingUpdateItem

Настройки рекламодателя, допускающие только значения YES или NO.

Нет

TinInfo

TinInfoUpdate

Налоговые данные конечного рекламодателя.

Нет

ErirAttributes

ErirAttributesUpdate

Дополнительные данные рекламодателя для маркировки рекламы.

Нет

Структура NotificationUpdate

Lang

LangEnum

Язык уведомлений.

Нет

Email

string

Адрес электронной почты для отправки уведомлений, связанных с аккаунтом (до 255 символов).

Нет

EmailSubscriptions

array of EmailSubscriptionItem

Типы уведомлений, отправляемых по электронной почте.

Нет

Структура EmailSubscriptionItem

Option

EmailSubscriptionEnum

Тип уведомления:

RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.

TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.

TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

Да

Value

YesNoEnum

Отправлять ли уведомления данного типа.

Да

Структура ClientSettingUpdateItem

Option

ClientSettingUpdateEnum

Имя настройки:

CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.

DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).

Да

Value

YesNoEnum

Значение настройки.

Да

Структура TinInfoUpdate

TinType

TinTypeEnum

Тип организации:

Нет

Tin

string

Номер налогоплательщика либо его аналог в стране регистрации.

Нет

Структура ErirAttributesUpdate

Organization

OrganizationUpdate

Информация об организации конечного рекламодателя.

Нет

Contract

ContractUpdate

Информация о договоре клиента-контрагента с конечным рекламодателем.

Нет

Contragent

ContragentUpdate

Информация о контрагенте конечного рекламодателя.

Нет

Структура OrganizationUpdate

Name

string

Наименование организации.

Нет

EpayNumber

string

Номер электронного средства платежа.

Нет

RegNumber

string

Регистрационный номер либо его аналог.

Нет

OksmNumber

string

Код страны регистрации юрлица в соответствии с ОКСМ.

Нет

OkvedCode

string

Код вида деятельности по ОКВЭД.

Нет

Структура ContractUpdate

Number

string

Номер договора.

Нет

Date

string

Дата договора в формате YYYY-MM-DD.

Нет

Type

ContractTypeEnum

Тип договора:

CONTRACT — договор оказания услуг;

INTERMEDIARY_CONTRACT — посреднический договор;

ADDITIONAL_AGREEMENT — дополнительное соглашение.

Внимание

Значение ADDITIONAL_AGREEMENT устарело, больше не принимается.

Нет

ActionType

ContractActionTypeEnum

Тип осуществляемых посредником-представителем действий:

Нет

SubjectType

ContractSubjectTypeEnum

Предмет договора:

Нет

Price

ContractPrice

Цена договора.

Нет

Структура ContractPrice

Amount

decimal

Стоимость договора.

Да

IncludingVat

YesNoEnum

Включен ли в стоимость НДС.

Да

Структура ContragentUpdate

Name

string

Наименование.

Нет

Phone

string

Номер телефона.

Нет

EpayNumber

string

Номер электронного средства платежа.

Нет

RegNumber

string

Регистрационный номер либо его аналог.

Нет

OksmNumber

string

Код страны регистрации юрлица в соответствии с ОКСМ.

Нет

TinInfo

TinInfoUpdate

Налоговые данные контрагента.

Нет

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / UpdateResponse (для SOAP)

UpdateResults

array of ClientsActionResult

Результат изменения параметров рекламодателя и настроек пользователя.

Структура ClientsActionResult

ClientId

long

Идентификатор рекламодателя. Возвращается в случае отсутствия ошибок, см. раздел  Операции над массивом объектов .

Warnings

array of ExceptionNotification

Предупреждения, возникшие при выполнении операции.

Errors

array of ExceptionNotification

Ошибки, возникшие при выполнении операции.

Изменяет параметры рекламодателя и настройки пользователя — представителя рекламодателя.

Любой представитель рекламодателя может редактировать параметры рекламодателя и собственные настройки.

Главный представитель рекламодателя может также редактировать настройки другого представителя: для этого необходимо передать логин представителя в HTTP-заголовке запроса  Client-Login .

Примечание

Параметры  ClientInfo ,  Notification ,  Phone  относятся к пользователю — представителю рекламодателя:

Параметр  Settings  относится к рекламодателю и не зависит от представителя.

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / UpdateRequest (для SOAP)

Clients

array of ClientUpdateItem

Параметры рекламодателя и настройки пользователя, которые требуется изменить.

Да

Структура ClientUpdateItem

ClientInfo

string

ФИО пользователя Директа (до 255 символов).

Нет

Notification

NotificationUpdate

Настройки SMS- и email-уведомлений пользователя Директа.

Нет

Phone

string

Номер телефона пользователя Директа (до 255 символов).

Нет

Settings

array of ClientSettingUpdateItem

Настройки рекламодателя, допускающие только значения YES или NO.

Нет

TinInfo

TinInfoUpdate

Налоговые данные конечного рекламодателя.

Нет

ErirAttributes

ErirAttributesUpdate

Дополнительные данные рекламодателя для маркировки рекламы.

Нет

Структура NotificationUpdate

Lang

LangEnum

Язык уведомлений.

Нет

Email

string

Адрес электронной почты для отправки уведомлений, связанных с аккаунтом (до 255 символов).

Нет

EmailSubscriptions

array of EmailSubscriptionItem

Типы уведомлений, отправляемых по электронной почте.

Нет

Структура EmailSubscriptionItem

Option

EmailSubscriptionEnum

Тип уведомления:

RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.

TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.

TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

Да

Value

YesNoEnum

Отправлять ли уведомления данного типа.

Да

Структура ClientSettingUpdateItem

Option

ClientSettingUpdateEnum

Имя настройки:

CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.

DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).

Да

Value

YesNoEnum

Значение настройки.

Да

Структура TinInfoUpdate

TinType

TinTypeEnum

Тип организации:

Нет

Tin

string

Номер налогоплательщика либо его аналог в стране регистрации.

Нет

Структура ErirAttributesUpdate

Organization

OrganizationUpdate

Информация об организации конечного рекламодателя.

Нет

Contract

ContractUpdate

Информация о договоре клиента-контрагента с конечным рекламодателем.

Нет

Contragent

ContragentUpdate

Информация о контрагенте конечного рекламодателя.

Нет

Структура OrganizationUpdate

Name

string

Наименование организации.

Нет

EpayNumber

string

Номер электронного средства платежа.

Нет

RegNumber

string

Регистрационный номер либо его аналог.

Нет

OksmNumber

string

Код страны регистрации юрлица в соответствии с ОКСМ.

Нет

OkvedCode

string

Код вида деятельности по ОКВЭД.

Нет

Структура ContractUpdate

Number

string

Номер договора.

Нет

Date

string

Дата договора в формате YYYY-MM-DD.

Нет

Type

ContractTypeEnum

Тип договора:

CONTRACT — договор оказания услуг;

INTERMEDIARY_CONTRACT — посреднический договор;

ADDITIONAL_AGREEMENT — дополнительное соглашение.

Внимание

Значение ADDITIONAL_AGREEMENT устарело, больше не принимается.

Нет

ActionType

ContractActionTypeEnum

Тип осуществляемых посредником-представителем действий:

Нет

SubjectType

ContractSubjectTypeEnum

Предмет договора:

Нет

Price

ContractPrice

Цена договора.

Нет

Структура ContractPrice

Amount

decimal

Стоимость договора.

Да

IncludingVat

YesNoEnum

Включен ли в стоимость НДС.

Да

Структура ContragentUpdate

Name

string

Наименование.

Нет

Phone

string

Номер телефона.

Нет

EpayNumber

string

Номер электронного средства платежа.

Нет

RegNumber

string

Регистрационный номер либо его аналог.

Нет

OksmNumber

string

Код страны регистрации юрлица в соответствии с ОКСМ.

Нет

TinInfo

TinInfoUpdate

Налоговые данные контрагента.

Нет

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / UpdateResponse (для SOAP)

UpdateResults

array of ClientsActionResult

Результат изменения параметров рекламодателя и настроек пользователя.

Структура ClientsActionResult

ClientId

long

Идентификатор рекламодателя. Возвращается в случае отсутствия ошибок, см. раздел  Операции над массивом объектов .

Warnings

array of ExceptionNotification

Предупреждения, возникшие при выполнении операции.

Errors

array of ExceptionNotification

Ошибки, возникшие при выполнении операции.

- Как начать работу с API
- Руководство разработчика
- Справочник API   О справочнике   AdExtensions: операции с расширениями объявлений   AdGroups: операции с группами объявлений   AdImages: операции с изображениями   Ads: операции с объявлениями   AdVideos: операции с видео   AgencyClients: управление клиентами агентства   AudienceTargets: управление условиями нацеливания на аудиторию   Bids: управление ставками   Businesses: получение профилей организаций   BidModifiers: управление корректировками ставок   Campaigns: управление кампаниями   Changes: проверка наличия изменений   Clients: управление параметрами рекламодателя и настройками пользователя   get   update   Creatives: получение креативов   Dictionaries: получение справочных данных   Feeds: операции с фидами   KeywordBids: управление ставками   Keywords: управление ключевыми фразами и автотаргетингами   KeywordsResearch: предобработка ключевых фраз   Leads: получение данных из форм на Турбо-страницах   NegativeKeywordSharedSets: управление наборами минус-фраз   RetargetingLists: управление условиями ретаргетинга и подбора аудитории   Sitelinks: операции с быстрыми ссылками   Strategies: операции с пакетными стратегиями   TurboPages: получение параметров Турбо-страниц   Ошибки и предупреждения   Справочные данные
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
- Clients: управление параметрами рекламодателя и настройками пользователя   get   update
- get
- update
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
- AgencyClients: управление клиентами агентства
- AudienceTargets: управление условиями нацеливания на аудиторию
- Bids: управление ставками
- Businesses: получение профилей организаций
- BidModifiers: управление корректировками ставок
- Campaigns: управление кампаниями
- Changes: проверка наличия изменений
- Clients: управление параметрами рекламодателя и настройками пользователя   get   update
- get
- update
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

- get
- update

- Узнайте больше
- Запрос
- Ответ

- Узнайте больше
- Запрос
- Ответ

- Как работает метод update
- Как обрабатывать ошибки

- пользователю, от имени которого выполняется запрос, — если запрос выполняется от имени любого представителя рекламодателя и в запросе отсутствует HTTP-заголовок  Client-Login ;
- пользователю, чей логин указан в HTTP-заголовке  Client-Login , — если запрос выполняется от имени главного представителя рекламодателя и в запросе присутствует HTTP-заголовок  Client-Login .

- RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.
- TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.
- TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

- CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.
- DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).

- LEGAL — юридическое лицо;
- PHYSICAL — физическое лицо;
- INDIVIDUAL — индивидуальный предприниматель;
- FOREIGN_LEGAL — иностранное юридическое лицо;
- FOREIGN_PHYSICAL — иностранное физическое лицо.

- CONTRACT — договор оказания услуг;
- INTERMEDIARY_CONTRACT — посреднический договор;
- ADDITIONAL_AGREEMENT — дополнительное соглашение. 
 Внимание 
 Значение ADDITIONAL_AGREEMENT устарело, больше не принимается.

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

- Как работает метод update
- Как обрабатывать ошибки

- пользователю, от имени которого выполняется запрос, — если запрос выполняется от имени любого представителя рекламодателя и в запросе отсутствует HTTP-заголовок  Client-Login ;
- пользователю, чей логин указан в HTTP-заголовке  Client-Login , — если запрос выполняется от имени главного представителя рекламодателя и в запросе присутствует HTTP-заголовок  Client-Login .

- RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.
- TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.
- TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

- CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.
- DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).

- LEGAL — юридическое лицо;
- PHYSICAL — физическое лицо;
- INDIVIDUAL — индивидуальный предприниматель;
- FOREIGN_LEGAL — иностранное юридическое лицо;
- FOREIGN_PHYSICAL — иностранное физическое лицо.

- CONTRACT — договор оказания услуг;
- INTERMEDIARY_CONTRACT — посреднический договор;
- ADDITIONAL_AGREEMENT — дополнительное соглашение. 
 Внимание 
 Значение ADDITIONAL_AGREEMENT устарело, больше не принимается.

- COMMERCIAL — коммерческое представительство;
- DISTRIBUTION — действия в целях распространения рекламы;
- CONCLUDE — заключение договоров;
- OTHER — иное.

- REPRESENTATION — представительство;
- MEDIATION — посредничество;
- DISTRIBUTION — договор на распространение рекламы;
- ORG_DISTRIBUTION — договор на организацию распространения рекламы;
- OTHER — иное.

`Client-Login`

`ClientInfo`

`Notification`

`Phone`

`Client-Login`

`Client-Login`

`Client-Login`

`Settings`

```
{
   "method" :  "update" ,
   "params" : {  /* params */ 
     "Clients" : [{  /* ClientUpdateItem */ 
       "ClientInfo" : (string),
       "Notification" : {  /* NotificationUpdate */ 
         "Lang" : (  "RU"  |  "UK"  |  "EN"  |  "TR"  ),
         "Email" : (string),
         "EmailSubscriptions" : [{   /* EmailSubscriptionItem */ 
           "Option" : (  "RECEIVE_RECOMMENDATIONS"  |  "TRACK_MANAGED_CAMPAIGNS"  |  "TRACK_POSITION_CHANGES"  ),  /* required */ 
           "Value" : (  "YES"  |  "NO"  )  /* required */ 
        }, ... ]
      },
       "Phone" : (string),
       "Settings" : [{  /* ClientSettingUpdateItem */ 
         "Option" : (  "CORRECT_TYPOS_AUTOMATICALLY"  |  "DISPLAY_STORE_RATING"  ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  )  /* required */ 
      }, ... ],
       "TinInfo"  : {  /* TinInfoUpdate */ 
         "TinType"  : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
         "Tin"  : (string)  /* nillable */ 
      },  /* nillable */ 
       "ErirAttributes" : {  /* ErirAttributesUpdate */ 
         "Organization" : {  /* OrganizationUpdate */ 
           "Name" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "OkvedCode" : (string)  /* nillable */ 
        },  /* nillable */ 
         "Contract" : {  /* ContractUpdate */ 
           "Number" : (string),  /* nillable */ 
           "Date" : (string),  /* nillable */ 
           "Type" : (  "CONTRACT"  |  "INTERMEDIARY_CONTRACT"  |  "ADDITIONAL_AGREEMENT"  ),  /* nillable */ 
           "ActionType" : (  "COMMERCIAL"  |  "DISTRIBUTION"  |  "CONCLUDE"  |  "OTHER"  ),  /* nillable */ 
           "SubjectType" : (  "REPRESENTATION"  |  "MEDIATION"  |  "DISTRIBUTION"  |  "ORG_DISTRIBUTION"  |  "OTHER"  ),  /* nillable */ 
           "Price" : {  /* PriceUpdate */ 
             "Amount" : (decimal),  /* required */ 
             "IncludingVat" : (  "YES"  |  "NO"  )  /* required */ 
          }  /* nillable */ 
        },  /* nillable */ 
         "Contragent" : {  /* ContragentUpdate */ 
           "Name" : (string),  /* nillable */ 
           "Phone" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "TinInfo" : {  /* TinInfoUpdate */ 
             "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
             "Tin" : (string)  /* nillable */ 
          }  /* nillable */ 
        }  /* nillable */ 
      }  /* nillable */ 
    }]  /* required */ 
  }
}
```

```
{
   "method" :  "update" ,
   "params" : {  /* params */ 
     "Clients" : [{  /* ClientUpdateItem */ 
       "ClientInfo" : (string),
       "Notification" : {  /* NotificationUpdate */ 
         "Lang" : (  "RU"  |  "UK"  |  "EN"  |  "TR"  ),
         "Email" : (string),
         "EmailSubscriptions" : [{   /* EmailSubscriptionItem */ 
           "Option" : (  "RECEIVE_RECOMMENDATIONS"  |  "TRACK_MANAGED_CAMPAIGNS"  |  "TRACK_POSITION_CHANGES"  ),  /* required */ 
           "Value" : (  "YES"  |  "NO"  )  /* required */ 
        }, ... ]
      },
       "Phone" : (string),
       "Settings" : [{  /* ClientSettingUpdateItem */ 
         "Option" : (  "CORRECT_TYPOS_AUTOMATICALLY"  |  "DISPLAY_STORE_RATING"  ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  )  /* required */ 
      }, ... ],
       "TinInfo"  : {  /* TinInfoUpdate */ 
         "TinType"  : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
         "Tin"  : (string)  /* nillable */ 
      },  /* nillable */ 
       "ErirAttributes" : {  /* ErirAttributesUpdate */ 
         "Organization" : {  /* OrganizationUpdate */ 
           "Name" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "OkvedCode" : (string)  /* nillable */ 
        },  /* nillable */ 
         "Contract" : {  /* ContractUpdate */ 
           "Number" : (string),  /* nillable */ 
           "Date" : (string),  /* nillable */ 
           "Type" : (  "CONTRACT"  |  "INTERMEDIARY_CONTRACT"  |  "ADDITIONAL_AGREEMENT"  ),  /* nillable */ 
           "ActionType" : (  "COMMERCIAL"  |  "DISTRIBUTION"  |  "CONCLUDE"  |  "OTHER"  ),  /* nillable */ 
           "SubjectType" : (  "REPRESENTATION"  |  "MEDIATION"  |  "DISTRIBUTION"  |  "ORG_DISTRIBUTION"  |  "OTHER"  ),  /* nillable */ 
           "Price" : {  /* PriceUpdate */ 
             "Amount" : (decimal),  /* required */ 
             "IncludingVat" : (  "YES"  |  "NO"  )  /* required */ 
          }  /* nillable */ 
        },  /* nillable */ 
         "Contragent" : {  /* ContragentUpdate */ 
           "Name" : (string),  /* nillable */ 
           "Phone" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "TinInfo" : {  /* TinInfoUpdate */ 
             "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
             "Tin" : (string)  /* nillable */ 
          }  /* nillable */ 
        }  /* nillable */ 
      }  /* nillable */ 
    }]  /* required */ 
  }
}
```

`Clients`

`ClientInfo`

`Notification`

`Phone`

`Settings`

`TinInfo`

`ErirAttributes`

`Lang`

`Email`

`EmailSubscriptions`

`Option`

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

```
{
   "result" : {   /* result */ 
     "UpdateResults" : [{   /* ClientsActionResult */ 
       "ClientId" : (long),
       "Warnings" : [{   /* ExceptionNotification */ 
         "Code" : (int),  /* required */ 
         "Message" : (string),  /* required */ 
         "Details" : (string)
       }, ...
      ],
       "Errors" : [{   /* ExceptionNotification */ 
         "Code" : (int),  /* required */ 
         "Message" : (string),  /* required */ 
         "Details" : (string)
       }, ...
      ]
    }, ... ]  /* required */ 
  }
}
```

```
{
   "result" : {   /* result */ 
     "UpdateResults" : [{   /* ClientsActionResult */ 
       "ClientId" : (long),
       "Warnings" : [{   /* ExceptionNotification */ 
         "Code" : (int),  /* required */ 
         "Message" : (string),  /* required */ 
         "Details" : (string)
       }, ...
      ],
       "Errors" : [{   /* ExceptionNotification */ 
         "Code" : (int),  /* required */ 
         "Message" : (string),  /* required */ 
         "Details" : (string)
       }, ...
      ]
    }, ... ]  /* required */ 
  }
}
```

`UpdateResults`

`ClientId`

`Warnings`

`Errors`

`Client-Login`

`ClientInfo`

`Notification`

`Phone`

`Client-Login`

`Client-Login`

`Client-Login`

`Settings`

```
{
   "method" :  "update" ,
   "params" : {  /* params */ 
     "Clients" : [{  /* ClientUpdateItem */ 
       "ClientInfo" : (string),
       "Notification" : {  /* NotificationUpdate */ 
         "Lang" : (  "RU"  |  "UK"  |  "EN"  |  "TR"  ),
         "Email" : (string),
         "EmailSubscriptions" : [{   /* EmailSubscriptionItem */ 
           "Option" : (  "RECEIVE_RECOMMENDATIONS"  |  "TRACK_MANAGED_CAMPAIGNS"  |  "TRACK_POSITION_CHANGES"  ),  /* required */ 
           "Value" : (  "YES"  |  "NO"  )  /* required */ 
        }, ... ]
      },
       "Phone" : (string),
       "Settings" : [{  /* ClientSettingUpdateItem */ 
         "Option" : (  "CORRECT_TYPOS_AUTOMATICALLY"  |  "DISPLAY_STORE_RATING"  ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  )  /* required */ 
      }, ... ],
       "TinInfo"  : {  /* TinInfoUpdate */ 
         "TinType"  : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
         "Tin"  : (string)  /* nillable */ 
      },  /* nillable */ 
       "ErirAttributes" : {  /* ErirAttributesUpdate */ 
         "Organization" : {  /* OrganizationUpdate */ 
           "Name" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "OkvedCode" : (string)  /* nillable */ 
        },  /* nillable */ 
         "Contract" : {  /* ContractUpdate */ 
           "Number" : (string),  /* nillable */ 
           "Date" : (string),  /* nillable */ 
           "Type" : (  "CONTRACT"  |  "INTERMEDIARY_CONTRACT"  |  "ADDITIONAL_AGREEMENT"  ),  /* nillable */ 
           "ActionType" : (  "COMMERCIAL"  |  "DISTRIBUTION"  |  "CONCLUDE"  |  "OTHER"  ),  /* nillable */ 
           "SubjectType" : (  "REPRESENTATION"  |  "MEDIATION"  |  "DISTRIBUTION"  |  "ORG_DISTRIBUTION"  |  "OTHER"  ),  /* nillable */ 
           "Price" : {  /* PriceUpdate */ 
             "Amount" : (decimal),  /* required */ 
             "IncludingVat" : (  "YES"  |  "NO"  )  /* required */ 
          }  /* nillable */ 
        },  /* nillable */ 
         "Contragent" : {  /* ContragentUpdate */ 
           "Name" : (string),  /* nillable */ 
           "Phone" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "TinInfo" : {  /* TinInfoUpdate */ 
             "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
             "Tin" : (string)  /* nillable */ 
          }  /* nillable */ 
        }  /* nillable */ 
      }  /* nillable */ 
    }]  /* required */ 
  }
}
```

```
{
   "method" :  "update" ,
   "params" : {  /* params */ 
     "Clients" : [{  /* ClientUpdateItem */ 
       "ClientInfo" : (string),
       "Notification" : {  /* NotificationUpdate */ 
         "Lang" : (  "RU"  |  "UK"  |  "EN"  |  "TR"  ),
         "Email" : (string),
         "EmailSubscriptions" : [{   /* EmailSubscriptionItem */ 
           "Option" : (  "RECEIVE_RECOMMENDATIONS"  |  "TRACK_MANAGED_CAMPAIGNS"  |  "TRACK_POSITION_CHANGES"  ),  /* required */ 
           "Value" : (  "YES"  |  "NO"  )  /* required */ 
        }, ... ]
      },
       "Phone" : (string),
       "Settings" : [{  /* ClientSettingUpdateItem */ 
         "Option" : (  "CORRECT_TYPOS_AUTOMATICALLY"  |  "DISPLAY_STORE_RATING"  ),  /* required */ 
         "Value" : (  "YES"  |  "NO"  )  /* required */ 
      }, ... ],
       "TinInfo"  : {  /* TinInfoUpdate */ 
         "TinType"  : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
         "Tin"  : (string)  /* nillable */ 
      },  /* nillable */ 
       "ErirAttributes" : {  /* ErirAttributesUpdate */ 
         "Organization" : {  /* OrganizationUpdate */ 
           "Name" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "OkvedCode" : (string)  /* nillable */ 
        },  /* nillable */ 
         "Contract" : {  /* ContractUpdate */ 
           "Number" : (string),  /* nillable */ 
           "Date" : (string),  /* nillable */ 
           "Type" : (  "CONTRACT"  |  "INTERMEDIARY_CONTRACT"  |  "ADDITIONAL_AGREEMENT"  ),  /* nillable */ 
           "ActionType" : (  "COMMERCIAL"  |  "DISTRIBUTION"  |  "CONCLUDE"  |  "OTHER"  ),  /* nillable */ 
           "SubjectType" : (  "REPRESENTATION"  |  "MEDIATION"  |  "DISTRIBUTION"  |  "ORG_DISTRIBUTION"  |  "OTHER"  ),  /* nillable */ 
           "Price" : {  /* PriceUpdate */ 
             "Amount" : (decimal),  /* required */ 
             "IncludingVat" : (  "YES"  |  "NO"  )  /* required */ 
          }  /* nillable */ 
        },  /* nillable */ 
         "Contragent" : {  /* ContragentUpdate */ 
           "Name" : (string),  /* nillable */ 
           "Phone" : (string),  /* nillable */ 
           "EpayNumber" : (string),  /* nillable */ 
           "RegNumber" : (string),  /* nillable */ 
           "OksmNumber" : (string),  /* nillable */ 
           "TinInfo" : {  /* TinInfoUpdate */ 
             "TinType" : (  "PHYSICAL"  |  "FOREIGN_PHYSICAL"  |  "LEGAL"  |  "FOREIGN_LEGAL"  |  "INDIVIDUAL"  ),
             "Tin" : (string)  /* nillable */ 
          }  /* nillable */ 
        }  /* nillable */ 
      }  /* nillable */ 
    }]  /* required */ 
  }
}
```

`Clients`

`ClientInfo`

`Notification`

`Phone`

`Settings`

`TinInfo`

`ErirAttributes`

`Lang`

`Email`

`EmailSubscriptions`

`Option`

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

```
{
   "result" : {   /* result */ 
     "UpdateResults" : [{   /* ClientsActionResult */ 
       "ClientId" : (long),
       "Warnings" : [{   /* ExceptionNotification */ 
         "Code" : (int),  /* required */ 
         "Message" : (string),  /* required */ 
         "Details" : (string)
       }, ...
      ],
       "Errors" : [{   /* ExceptionNotification */ 
         "Code" : (int),  /* required */ 
         "Message" : (string),  /* required */ 
         "Details" : (string)
       }, ...
      ]
    }, ... ]  /* required */ 
  }
}
```

```
{
   "result" : {   /* result */ 
     "UpdateResults" : [{   /* ClientsActionResult */ 
       "ClientId" : (long),
       "Warnings" : [{   /* ExceptionNotification */ 
         "Code" : (int),  /* required */ 
         "Message" : (string),  /* required */ 
         "Details" : (string)
       }, ...
      ],
       "Errors" : [{   /* ExceptionNotification */ 
         "Code" : (int),  /* required */ 
         "Message" : (string),  /* required */ 
         "Details" : (string)
       }, ...
      ]
    }, ... ]  /* required */ 
  }
}
```

`UpdateResults`

`ClientId`

`Warnings`

`Errors`


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Clients | array of ClientUpdateItem |
| ClientInfo | string |
| Notification | NotificationUpdate |
| Phone | string |
| Settings | array of ClientSettingUpdateItem |
| TinInfo | TinInfoUpdate |
| ErirAttributes | ErirAttributesUpdate |
| Lang | LangEnum |
| Email | string |
| EmailSubscriptions | array of EmailSubscriptionItem |
| Option | EmailSubscriptionEnum |
| Value | YesNoEnum |
| Option | ClientSettingUpdateEnum |
| Value | YesNoEnum |
| TinType | TinTypeEnum |
| Tin | string |
| Organization | OrganizationUpdate |
| Contract | ContractUpdate |
| Contragent | ContragentUpdate |
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
| TinInfo | TinInfoUpdate |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| UpdateResults | array of ClientsActionResult |
| ClientId | long |
| Warnings | array of ExceptionNotification |
| Errors | array of ExceptionNotification |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Clients | array of ClientUpdateItem |
| ClientInfo | string |
| Notification | NotificationUpdate |
| Phone | string |
| Settings | array of ClientSettingUpdateItem |
| TinInfo | TinInfoUpdate |
| ErirAttributes | ErirAttributesUpdate |
| Lang | LangEnum |
| Email | string |
| EmailSubscriptions | array of EmailSubscriptionItem |
| Option | EmailSubscriptionEnum |
| Value | YesNoEnum |
| Option | ClientSettingUpdateEnum |
| Value | YesNoEnum |
| TinType | TinTypeEnum |
| Tin | string |
| Organization | OrganizationUpdate |
| Contract | ContractUpdate |
| Contragent | ContragentUpdate |
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
| TinInfo | TinInfoUpdate |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| UpdateResults | array of ClientsActionResult |
| ClientId | long |
| Warnings | array of ExceptionNotification |
| Errors | array of ExceptionNotification |

