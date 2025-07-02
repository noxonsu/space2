# moderate  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/ads/moderate

**Дата скачивания:** 2025-07-01 12:39:38

---

## В этой статье :

# moderate

### Узнайте больше

## Ограничения

## Запрос

## Ответ

### Была ли статья полезна?

# moderate

### Узнайте больше

## Ограничения

## Запрос

## Ответ

### Была ли статья полезна?

Отправляет объявления на модерацию.

Не более 10 000 объявлений в одном вызове метода.

Отправить на модерацию можно только объявления со статусом DRAFT.

Не допускается отправка на модерацию объявления, если в группе нет условий показа (ключевых фраз, условий нацеливания на аудиторию, условий нацеливания для динамических объявлений). Не допускается отправка на модерацию объявлений, принадлежащих архивной кампании.

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / ModerateRequest (для SOAP)

SelectionCriteria

IdsCriteria

Критерий отбора объявлений, которые требуется отправить на модерацию.

Да

Структура IdsCriteria

Ids

array of long

Идентификаторы объявлений, которые требуется отправить на модерацию (не более  ids-select ).

Да

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / ModerateResponse (для SOAP)

ModerateResults

array of ActionResult

Результаты отправки на модерацию.

Структура ActionResult

Id

long

Идентификатор объявления. Возвращается в случае отсутствия ошибок, см. раздел  Операции над массивом объектов .

Warnings

array of ExceptionNotification

Предупреждения, возникшие при выполнении операции.

Errors

array of ExceptionNotification

Ошибки, возникшие при выполнении операции.

Отправляет объявления на модерацию.

Не более 10 000 объявлений в одном вызове метода.

Отправить на модерацию можно только объявления со статусом DRAFT.

Не допускается отправка на модерацию объявления, если в группе нет условий показа (ключевых фраз, условий нацеливания на аудиторию, условий нацеливания для динамических объявлений). Не допускается отправка на модерацию объявлений, принадлежащих архивной кампании.

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / ModerateRequest (для SOAP)

SelectionCriteria

IdsCriteria

Критерий отбора объявлений, которые требуется отправить на модерацию.

Да

Структура IdsCriteria

Ids

array of long

Идентификаторы объявлений, которые требуется отправить на модерацию (не более  ids-select ).

Да

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / ModerateResponse (для SOAP)

ModerateResults

array of ActionResult

Результаты отправки на модерацию.

Структура ActionResult

Id

long

Идентификатор объявления. Возвращается в случае отсутствия ошибок, см. раздел  Операции над массивом объектов .

Warnings

array of ExceptionNotification

Предупреждения, возникшие при выполнении операции.

Errors

array of ExceptionNotification

Ошибки, возникшие при выполнении операции.

- Как начать работу с API
- Руководство разработчика
- Справочник API   О справочнике   AdExtensions: операции с расширениями объявлений   AdGroups: операции с группами объявлений   AdImages: операции с изображениями   Ads: операции с объявлениями   add   archive   delete   get   moderate   resume   suspend   unarchive   update   AdVideos: операции с видео   AgencyClients: управление клиентами агентства   AudienceTargets: управление условиями нацеливания на аудиторию   Bids: управление ставками   Businesses: получение профилей организаций   BidModifiers: управление корректировками ставок   Campaigns: управление кампаниями   Changes: проверка наличия изменений   Clients: управление параметрами рекламодателя и настройками пользователя   Creatives: получение креативов   Dictionaries: получение справочных данных   Feeds: операции с фидами   KeywordBids: управление ставками   Keywords: управление ключевыми фразами и автотаргетингами   KeywordsResearch: предобработка ключевых фраз   Leads: получение данных из форм на Турбо-страницах   NegativeKeywordSharedSets: управление наборами минус-фраз   RetargetingLists: управление условиями ретаргетинга и подбора аудитории   Sitelinks: операции с быстрыми ссылками   Strategies: операции с пакетными стратегиями   TurboPages: получение параметров Турбо-страниц   Ошибки и предупреждения   Справочные данные
- О справочнике
- AdExtensions: операции с расширениями объявлений
- AdGroups: операции с группами объявлений
- AdImages: операции с изображениями
- Ads: операции с объявлениями   add   archive   delete   get   moderate   resume   suspend   unarchive   update
- add
- archive
- delete
- get
- moderate
- resume
- suspend
- unarchive
- update
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
- Ads: операции с объявлениями   add   archive   delete   get   moderate   resume   suspend   unarchive   update
- add
- archive
- delete
- get
- moderate
- resume
- suspend
- unarchive
- update
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
- archive
- delete
- get
- moderate
- resume
- suspend
- unarchive
- update

- Ограничения
- Запрос
- Ответ

- Ограничения
- Запрос
- Ответ

- Как работают методы, изменяющие данные
- Как обрабатывать ошибки

- Ограничения
- Запрос
- Ответ

- Как работают методы, изменяющие данные
- Как обрабатывать ошибки

```
{
   "method" :  "moderate" ,
   "params" : {   /* params */ 
     "SelectionCriteria" : {   /* IdsCriteria */ 
       "Ids" : [(long), ... ]  /* required */ 
    }  /* required */ 
  }
}
```

```
{
   "method" :  "moderate" ,
   "params" : {   /* params */ 
     "SelectionCriteria" : {   /* IdsCriteria */ 
       "Ids" : [(long), ... ]  /* required */ 
    }  /* required */ 
  }
}
```

`SelectionCriteria`

`Ids`

`ids-select`

```
{
   "result" : {  /* result */ 
     "ModerateResults" : [{   /* ActionResult */ 
       "Id" : (long),
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
   "result" : {  /* result */ 
     "ModerateResults" : [{   /* ActionResult */ 
       "Id" : (long),
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

`ModerateResults`

`Id`

`Warnings`

`Errors`

```
{
   "method" :  "moderate" ,
   "params" : {   /* params */ 
     "SelectionCriteria" : {   /* IdsCriteria */ 
       "Ids" : [(long), ... ]  /* required */ 
    }  /* required */ 
  }
}
```

```
{
   "method" :  "moderate" ,
   "params" : {   /* params */ 
     "SelectionCriteria" : {   /* IdsCriteria */ 
       "Ids" : [(long), ... ]  /* required */ 
    }  /* required */ 
  }
}
```

`SelectionCriteria`

`Ids`

`ids-select`

```
{
   "result" : {  /* result */ 
     "ModerateResults" : [{   /* ActionResult */ 
       "Id" : (long),
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
   "result" : {  /* result */ 
     "ModerateResults" : [{   /* ActionResult */ 
       "Id" : (long),
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

`ModerateResults`

`Id`

`Warnings`

`Errors`


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| SelectionCriteria | IdsCriteria |
| Ids | array of long |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| ModerateResults | array of ActionResult |
| Id | long |
| Warnings | array of ExceptionNotification |
| Errors | array of ExceptionNotification |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| SelectionCriteria | IdsCriteria |
| Ids | array of long |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| ModerateResults | array of ActionResult |
| Id | long |
| Warnings | array of ExceptionNotification |
| Errors | array of ExceptionNotification |

