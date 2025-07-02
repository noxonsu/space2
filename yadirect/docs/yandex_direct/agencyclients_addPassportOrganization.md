# addPassportOrganization  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/agencyclients/addPassportOrganization

**Дата скачивания:** 2025-07-01 12:37:53

---

## В этой статье :

# addPassportOrganization

## Запрос

## Ответ

### Была ли статья полезна?

# addPassportOrganization

## Запрос

## Ответ

### Была ли статья полезна?

Создает бизнес-аккаунт организации.

Примечание

В запросе к сервису  AgencyClients :

Узнайте больше

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / AddPassportOrganization (для SOAP)

Name

string

Название паспортной организации, которая будет выступать в качестве главного представителя рекламодателя. В кабинете Директа будет отображаться автоматически сгенерированный логин паспортной организации.

Для указанного названия в Яндекс ID создается новая паспортная организация, которая привязывается к бизнес-группе агентства.  Подробнее про организации .

В созданную паспортную организацию добавляется  Главный представитель  агентства с ролью  Владелец .

Пользователь, чей токен передан в заголовке  Authorization , будет добавлен в паспортную организацию с ролью  Администратор .

Пользователь, чей токен передан в заголовке  Member-Authorization  будет добавлен в Паспортную Организацию с ролью Участник.

Подробнее про ролевую модель сотрудников паспортных организаций

Логин может состоять из латинских символов, цифр, одинарного дефиса или точки. Он должен содержать не более 30 символов. Не допускаются символы  &=\<\> .

Да

Currency

CurrencyEnum

Валюта рекламодателя.

Да

Grants

array of GrantItem

Полномочия рекламодателя по управлению кампаниями. Если не заданы — полномочия отсутствуют.

Нет

Notification

NotificationAdd

Настройки email-уведомлений для главного представителя рекламодателя.

Да

Settings

array of ClientSettingAddItem

Настройки рекламодателя, допускаются только значения YES или NO.

Нет

TinInfo

TinInfoAdd

Налоговые данные конечного рекламодателя.

Да

Структура GrantItem

Privilege

PrivilegeEnum

Название полномочия:

EDIT_CAMPAIGNS — редактирование кампаний.

IMPORT_XLS — управление кампаниями с помощью файлов (см. разделы  Управление кампаниями с помощью файлов формата XLS и XLSX  и  Загрузка кампаний из CSV-файлов  помощи Директа).

TRANSFER_MONEY — перенос средств между кампаниями (см. раздел  Перенос средств между кампаниями ).

Если полномочие не указано, оно будет создано со значением NO.

Для полномочия IMPORT_XLS можно указать значение YES только при условии, что для полномочия EDIT_CAMPAIGNS также указано значение YES, в противном случае возвращается ошибка.

Да

Value

YesNoEnum

Есть ли у рекламодателя данное полномочие.

Да

Структура NotificationAdd

Lang

LangEnum

Язык уведомлений.

Да

Email

string

Адрес электронной почты для отправки уведомлений, связанных с аккаунтом.

Да

EmailSubscriptions

array of EmailSubscriptionItem

Типы уведомлений, отправляемых по электронной почте.

Да

Структура EmailSubscriptionItem

Option

EmailSubscriptionEnum

Тип уведомления:

RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.

TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.

TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

Если тип уведомления не указан, он будет создан со значением NO.

Да

Value

YesNoEnum

Отправлять ли уведомления данного типа.

Да

Структура ClientSettingAddItem

Option

ClientSettingAddEnum

Имя настройки:

CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.

DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).

Если настройка не указана, она будет создана со значением NO.

Да

Value

YesNoEnum

Значение настройки.

Да

Структура TinInfoAdd

TinType

TinTypeEnum

Тип организации:

LEGAL — юридическое лицо;

PHYSICAL — физическое лицо;

INDIVIDUAL — индивидуальный предприниматель;

FOREIGN_LEGAL — иностранное юридическое лицо;

FOREIGN_PHYSICAL — иностранное физическое лицо.

Да

Tin

string

Номер налогоплательщика либо его аналог в стране регистрации.

Да

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / AddResponse (для SOAP)

Login

string

Логин пользователя Директа — главного представителя рекламодателя. Возвращается в случае отсутствия ошибок, см. раздел  Операции над массивом объектов .

ClientId

long

Идентификатор созданного рекламодателя. Возвращается в случае отсутствия ошибок.

Warnings

array of ExceptionNotification

Предупреждения, возникшие при выполнении операции.

Errors

array of ExceptionNotification

Ошибки, возникшие при выполнении операции.

Создает бизнес-аккаунт организации.

Примечание

В запросе к сервису  AgencyClients :

Узнайте больше

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / AddPassportOrganization (для SOAP)

Name

string

Название паспортной организации, которая будет выступать в качестве главного представителя рекламодателя. В кабинете Директа будет отображаться автоматически сгенерированный логин паспортной организации.

Для указанного названия в Яндекс ID создается новая паспортная организация, которая привязывается к бизнес-группе агентства.  Подробнее про организации .

В созданную паспортную организацию добавляется  Главный представитель  агентства с ролью  Владелец .

Пользователь, чей токен передан в заголовке  Authorization , будет добавлен в паспортную организацию с ролью  Администратор .

Пользователь, чей токен передан в заголовке  Member-Authorization  будет добавлен в Паспортную Организацию с ролью Участник.

Подробнее про ролевую модель сотрудников паспортных организаций

Логин может состоять из латинских символов, цифр, одинарного дефиса или точки. Он должен содержать не более 30 символов. Не допускаются символы  &=\<\> .

Да

Currency

CurrencyEnum

Валюта рекламодателя.

Да

Grants

array of GrantItem

Полномочия рекламодателя по управлению кампаниями. Если не заданы — полномочия отсутствуют.

Нет

Notification

NotificationAdd

Настройки email-уведомлений для главного представителя рекламодателя.

Да

Settings

array of ClientSettingAddItem

Настройки рекламодателя, допускаются только значения YES или NO.

Нет

TinInfo

TinInfoAdd

Налоговые данные конечного рекламодателя.

Да

Структура GrantItem

Privilege

PrivilegeEnum

Название полномочия:

EDIT_CAMPAIGNS — редактирование кампаний.

IMPORT_XLS — управление кампаниями с помощью файлов (см. разделы  Управление кампаниями с помощью файлов формата XLS и XLSX  и  Загрузка кампаний из CSV-файлов  помощи Директа).

TRANSFER_MONEY — перенос средств между кампаниями (см. раздел  Перенос средств между кампаниями ).

Если полномочие не указано, оно будет создано со значением NO.

Для полномочия IMPORT_XLS можно указать значение YES только при условии, что для полномочия EDIT_CAMPAIGNS также указано значение YES, в противном случае возвращается ошибка.

Да

Value

YesNoEnum

Есть ли у рекламодателя данное полномочие.

Да

Структура NotificationAdd

Lang

LangEnum

Язык уведомлений.

Да

Email

string

Адрес электронной почты для отправки уведомлений, связанных с аккаунтом.

Да

EmailSubscriptions

array of EmailSubscriptionItem

Типы уведомлений, отправляемых по электронной почте.

Да

Структура EmailSubscriptionItem

Option

EmailSubscriptionEnum

Тип уведомления:

RECEIVE_RECOMMENDATIONS — новости Директа и рекомендации.

TRACK_MANAGED_CAMPAIGNS — уведомления по кампаниям, обслуживаемым персональным менеджером.

TRACK_POSITION_CHANGES — предупреждения о снижении прогноза трафика относительно того, который обеспечивали ставки на момент установки.

Если тип уведомления не указан, он будет создан со значением NO.

Да

Value

YesNoEnum

Отправлять ли уведомления данного типа.

Да

Структура ClientSettingAddItem

Option

ClientSettingAddEnum

Имя настройки:

CORRECT_TYPOS_AUTOMATICALLY — автоматически исправлять ошибки и опечатки.

DISPLAY_STORE_RATING — дополнять объявления данными из внешних источников (см. раздел  Данные из внешних источников  помощи Директа).

Если настройка не указана, она будет создана со значением NO.

Да

Value

YesNoEnum

Значение настройки.

Да

Структура TinInfoAdd

TinType

TinTypeEnum

Тип организации:

LEGAL — юридическое лицо;

PHYSICAL — физическое лицо;

INDIVIDUAL — индивидуальный предприниматель;

FOREIGN_LEGAL — иностранное юридическое лицо;

FOREIGN_PHYSICAL — иностранное физическое лицо.

Да

Tin

string

Номер налогоплательщика либо его аналог в стране регистрации.

Да

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / AddResponse (для SOAP)

Login

string

Логин пользователя Директа — главного представителя рекламодателя. Возвращается в случае отсутствия ошибок, см. раздел  Операции над массивом объектов .

ClientId

long

Идентификатор созданного рекламодателя. Возвращается в случае отсутствия ошибок.

Warnings

array of ExceptionNotification

Предупреждения, возникшие при выполнении операции.

Errors

array of ExceptionNotification

Ошибки, возникшие при выполнении операции.

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

- Запрос
- Ответ

- Запрос
- Ответ

- В HTTP-заголовке  Authorization  укажите токен, полученный для представителя агентства.
- В HTTP-заголовке  Member-Authorization  укажите токен для логина, который должен быть добавлен в бизнес-аккаунт в качестве участника

- Как работает метод add
- Как обрабатывать ошибки

- В созданную паспортную организацию добавляется  Главный представитель  агентства с ролью  Владелец .
- Пользователь, чей токен передан в заголовке  Authorization , будет добавлен в паспортную организацию с ролью  Администратор .
- Пользователь, чей токен передан в заголовке  Member-Authorization  будет добавлен в Паспортную Организацию с ролью Участник.

- EDIT_CAMPAIGNS — редактирование кампаний.
- IMPORT_XLS — управление кампаниями с помощью файлов (см. разделы  Управление кампаниями с помощью файлов формата XLS и XLSX  и  Загрузка кампаний из CSV-файлов  помощи Директа).
- TRANSFER_MONEY — перенос средств между кампаниями (см. раздел  Перенос средств между кампаниями ).

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

- Запрос
- Ответ

- В HTTP-заголовке  Authorization  укажите токен, полученный для представителя агентства.
- В HTTP-заголовке  Member-Authorization  укажите токен для логина, который должен быть добавлен в бизнес-аккаунт в качестве участника

- Как работает метод add
- Как обрабатывать ошибки

- В созданную паспортную организацию добавляется  Главный представитель  агентства с ролью  Владелец .
- Пользователь, чей токен передан в заголовке  Authorization , будет добавлен в паспортную организацию с ролью  Администратор .
- Пользователь, чей токен передан в заголовке  Member-Authorization  будет добавлен в Паспортную Организацию с ролью Участник.

- EDIT_CAMPAIGNS — редактирование кампаний.
- IMPORT_XLS — управление кампаниями с помощью файлов (см. разделы  Управление кампаниями с помощью файлов формата XLS и XLSX  и  Загрузка кампаний из CSV-файлов  помощи Директа).
- TRANSFER_MONEY — перенос средств между кампаниями (см. раздел  Перенос средств между кампаниями ).

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

`AgencyClients`

`Authorization`

`Member-Authorization`

```
{ 
   "method" :   "addPassportOrganization" , 
   "params" :   { 
       "Name" :  (string) , 
       "Currency" :  ( "RUB" | "BYN" | "CHF" | "EUR" | "KZT" | "TRY" | "UAH" | "USD" ) , 
       "Grants" :   [ { 
         "Privilege" :  ( "EDIT_CAMPAIGNS" | "IMPORT_XLS" | "TRANSFER_MONEY" ) , 
         "Value" :  ( "YES" | "NO" )
       } ,  ...  ] , 
       "Notification" : 
         "Lang" :  ( "RU" | "UK" | "EN" | "TR" ) , 
         "Email" :  (string) , 
         "EmailSubscriptions" :   [ { 
           "Option" :  ( "RECEIVE_RECOMMENDATIONS" | "TRACK_MANAGED_CAMPAIGNS" | "TRACK_POSITION_CHANGES" ) , 
           "Value" :  ( "YES" | "NO" )
         } ,  ...  ] , 
       "Settings" :   [ { 
         "Option" :  ( "CORRECT_TYPOS_AUTOMATICALLY" | "DISPLAY_STORE_RATING" ) , 
         "Value" :  ( "YES" | "NO" )
       } ,  ...  ] , 
       "TinInfo" :   { 
         "TinType" :  ( "PHYSICAL" | "FOREIGN_PHYSICAL" | "LEGAL" | "FOREIGN_LEGAL" | "INDIVIDUAL"  ) , 
         "Tin" :  (string)
       } 
   } 
 }
```

```
{ 
   "method" :   "addPassportOrganization" , 
   "params" :   { 
       "Name" :  (string) , 
       "Currency" :  ( "RUB" | "BYN" | "CHF" | "EUR" | "KZT" | "TRY" | "UAH" | "USD" ) , 
       "Grants" :   [ { 
         "Privilege" :  ( "EDIT_CAMPAIGNS" | "IMPORT_XLS" | "TRANSFER_MONEY" ) , 
         "Value" :  ( "YES" | "NO" )
       } ,  ...  ] , 
       "Notification" : 
         "Lang" :  ( "RU" | "UK" | "EN" | "TR" ) , 
         "Email" :  (string) , 
         "EmailSubscriptions" :   [ { 
           "Option" :  ( "RECEIVE_RECOMMENDATIONS" | "TRACK_MANAGED_CAMPAIGNS" | "TRACK_POSITION_CHANGES" ) , 
           "Value" :  ( "YES" | "NO" )
         } ,  ...  ] , 
       "Settings" :   [ { 
         "Option" :  ( "CORRECT_TYPOS_AUTOMATICALLY" | "DISPLAY_STORE_RATING" ) , 
         "Value" :  ( "YES" | "NO" )
       } ,  ...  ] , 
       "TinInfo" :   { 
         "TinType" :  ( "PHYSICAL" | "FOREIGN_PHYSICAL" | "LEGAL" | "FOREIGN_LEGAL" | "INDIVIDUAL"  ) , 
         "Tin" :  (string)
       } 
   } 
 }
```

`Name`

`Authorization`

`Member-Authorization`

`&=\<\>`

`Currency`

`Grants`

`Notification`

`Settings`

`TinInfo`

`Privilege`

`Value`

`Lang`

`Email`

`EmailSubscriptions`

`Option`

`Value`

`Option`

`Value`

`TinType`

`Tin`

```
{ 
   "result" :   { 
     "Login" :  (string) , 
     "ClientId" :  (long) , 
     "Warnings" :   [ { 
       "Code" :  (int) , 
       "Message" :  (string) , 
       "Details" :  (string)
     } ,  ...  ] , 
     "Errors" :   [ { 
       "Code" :  (int) , 
       "Message" :  (string) , 
       "Details" :  (string)
     } ,  ...  ] 
   } 
 }
```

```
{ 
   "result" :   { 
     "Login" :  (string) , 
     "ClientId" :  (long) , 
     "Warnings" :   [ { 
       "Code" :  (int) , 
       "Message" :  (string) , 
       "Details" :  (string)
     } ,  ...  ] , 
     "Errors" :   [ { 
       "Code" :  (int) , 
       "Message" :  (string) , 
       "Details" :  (string)
     } ,  ...  ] 
   } 
 }
```

`Login`

`ClientId`

`Warnings`

`Errors`

`AgencyClients`

`Authorization`

`Member-Authorization`

```
{ 
   "method" :   "addPassportOrganization" , 
   "params" :   { 
       "Name" :  (string) , 
       "Currency" :  ( "RUB" | "BYN" | "CHF" | "EUR" | "KZT" | "TRY" | "UAH" | "USD" ) , 
       "Grants" :   [ { 
         "Privilege" :  ( "EDIT_CAMPAIGNS" | "IMPORT_XLS" | "TRANSFER_MONEY" ) , 
         "Value" :  ( "YES" | "NO" )
       } ,  ...  ] , 
       "Notification" : 
         "Lang" :  ( "RU" | "UK" | "EN" | "TR" ) , 
         "Email" :  (string) , 
         "EmailSubscriptions" :   [ { 
           "Option" :  ( "RECEIVE_RECOMMENDATIONS" | "TRACK_MANAGED_CAMPAIGNS" | "TRACK_POSITION_CHANGES" ) , 
           "Value" :  ( "YES" | "NO" )
         } ,  ...  ] , 
       "Settings" :   [ { 
         "Option" :  ( "CORRECT_TYPOS_AUTOMATICALLY" | "DISPLAY_STORE_RATING" ) , 
         "Value" :  ( "YES" | "NO" )
       } ,  ...  ] , 
       "TinInfo" :   { 
         "TinType" :  ( "PHYSICAL" | "FOREIGN_PHYSICAL" | "LEGAL" | "FOREIGN_LEGAL" | "INDIVIDUAL"  ) , 
         "Tin" :  (string)
       } 
   } 
 }
```

```
{ 
   "method" :   "addPassportOrganization" , 
   "params" :   { 
       "Name" :  (string) , 
       "Currency" :  ( "RUB" | "BYN" | "CHF" | "EUR" | "KZT" | "TRY" | "UAH" | "USD" ) , 
       "Grants" :   [ { 
         "Privilege" :  ( "EDIT_CAMPAIGNS" | "IMPORT_XLS" | "TRANSFER_MONEY" ) , 
         "Value" :  ( "YES" | "NO" )
       } ,  ...  ] , 
       "Notification" : 
         "Lang" :  ( "RU" | "UK" | "EN" | "TR" ) , 
         "Email" :  (string) , 
         "EmailSubscriptions" :   [ { 
           "Option" :  ( "RECEIVE_RECOMMENDATIONS" | "TRACK_MANAGED_CAMPAIGNS" | "TRACK_POSITION_CHANGES" ) , 
           "Value" :  ( "YES" | "NO" )
         } ,  ...  ] , 
       "Settings" :   [ { 
         "Option" :  ( "CORRECT_TYPOS_AUTOMATICALLY" | "DISPLAY_STORE_RATING" ) , 
         "Value" :  ( "YES" | "NO" )
       } ,  ...  ] , 
       "TinInfo" :   { 
         "TinType" :  ( "PHYSICAL" | "FOREIGN_PHYSICAL" | "LEGAL" | "FOREIGN_LEGAL" | "INDIVIDUAL"  ) , 
         "Tin" :  (string)
       } 
   } 
 }
```

`Name`

`Authorization`

`Member-Authorization`

`&=\<\>`

`Currency`

`Grants`

`Notification`

`Settings`

`TinInfo`

`Privilege`

`Value`

`Lang`

`Email`

`EmailSubscriptions`

`Option`

`Value`

`Option`

`Value`

`TinType`

`Tin`

```
{ 
   "result" :   { 
     "Login" :  (string) , 
     "ClientId" :  (long) , 
     "Warnings" :   [ { 
       "Code" :  (int) , 
       "Message" :  (string) , 
       "Details" :  (string)
     } ,  ...  ] , 
     "Errors" :   [ { 
       "Code" :  (int) , 
       "Message" :  (string) , 
       "Details" :  (string)
     } ,  ...  ] 
   } 
 }
```

```
{ 
   "result" :   { 
     "Login" :  (string) , 
     "ClientId" :  (long) , 
     "Warnings" :   [ { 
       "Code" :  (int) , 
       "Message" :  (string) , 
       "Details" :  (string)
     } ,  ...  ] , 
     "Errors" :   [ { 
       "Code" :  (int) , 
       "Message" :  (string) , 
       "Details" :  (string)
     } ,  ...  ] 
   } 
 }
```

`Login`

`ClientId`

`Warnings`

`Errors`


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Структура params (для JSON) / AddPassportOrganization (для SOAP) |  |
| Name | string |
| Currency | CurrencyEnum |
| Grants | array of GrantItem |
| Notification | NotificationAdd |
| Settings | array of ClientSettingAddItem |
| TinInfo | TinInfoAdd |
| Структура GrantItem |  |
| Privilege | PrivilegeEnum |
| Value | YesNoEnum |
| Структура NotificationAdd |  |
| Lang | LangEnum |
| Email | string |
| EmailSubscriptions | array of EmailSubscriptionItem |
| Структура EmailSubscriptionItem |  |
| Option | EmailSubscriptionEnum |
| Value | YesNoEnum |
| Структура ClientSettingAddItem |  |
| Option | ClientSettingAddEnum |
| Value | YesNoEnum |
| Структура TinInfoAdd |  |
| TinType | TinTypeEnum |
| Tin | string |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Login | string |
| ClientId | long |
| Warnings | array of ExceptionNotification |
| Errors | array of ExceptionNotification |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Структура params (для JSON) / AddPassportOrganization (для SOAP) |  |
| Name | string |
| Currency | CurrencyEnum |
| Grants | array of GrantItem |
| Notification | NotificationAdd |
| Settings | array of ClientSettingAddItem |
| TinInfo | TinInfoAdd |
| Структура GrantItem |  |
| Privilege | PrivilegeEnum |
| Value | YesNoEnum |
| Структура NotificationAdd |  |
| Lang | LangEnum |
| Email | string |
| EmailSubscriptions | array of EmailSubscriptionItem |
| Структура EmailSubscriptionItem |  |
| Option | EmailSubscriptionEnum |
| Value | YesNoEnum |
| Структура ClientSettingAddItem |  |
| Option | ClientSettingAddEnum |
| Value | YesNoEnum |
| Структура TinInfoAdd |  |
| TinType | TinTypeEnum |
| Tin | string |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| Login | string |
| ClientId | long |
| Warnings | array of ExceptionNotification |
| Errors | array of ExceptionNotification |

