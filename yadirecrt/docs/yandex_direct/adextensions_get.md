# get  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/adextensions/get

**Дата скачивания:** 2025-07-01 12:35:39

---

## В этой статье :

# get

## Узнайте больше

## Ограничения

## Запрос

## Ответ

### Была ли статья полезна?

# get

## Узнайте больше

## Ограничения

## Запрос

## Ответ

### Была ли статья полезна?

Возвращает расширения, отвечающие заданным критериям.

В настоящее время доступен один тип расширения — уточнение.

Метод возвращает не более 10 000 объектов.

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / GetRequest (для SOAP)

SelectionCriteria

AdExtensionsSelectionCriteria

Критерий отбора расширений.

Чтобы получить все расширения рекламодателя, необходимо указать пустой  SelectionCriteria .

Да

FieldNames

array of AdExtensionFieldEnum

Имена параметров, общие для всех типов расширений, которые требуется получить.

Да

CalloutFieldNames

array of CalloutFieldEnum

Имена параметров расширения с типом “Уточнение”, которые требуется получить.

Нет

Page

LimitOffset

Структура, задающая страницу при  постраничной выборке  данных.

Нет

Структура AdExtensionsSelectionCriteria

Ids

array of long

Отбирать расширения с указанными идентификаторами. Не более 10 000 элементов в массиве.

Нет

Types

array of AdExtensionTypeEnum

Отбирать расширения с указанными типами. В настоящее время доступен один тип расширения — “Уточнение” (CALLOUT).

Нет

States

array of AdExtensionStateSelectionEnum

Отбирать расширения с указанными состояниями. См.  Соcтояние расширения .

Примечание

Метод get возвращает расширение в состоянии DELETED, только если в параметре  States  указано значение DELETED или в параметре  Ids  указан идентификатор этого расширения. Если параметры  Ids  и  States  оба не заданы, метод не возвращает расширений в состоянии DELETED.

Нет

Statuses

array of ExtensionStatusSelectionEnum

Отбирать расширения с указанными статусами. См.  Статус расширения .

Нет

ModifiedSince

string

Отбирать расширения, в которых были изменения,начиная с указанной даты.

Задается в формате  YYYY-MM-DDThh:mm:ssZ  (согласно ISO 8601), например  2015-05-24T23:59:59Z .

Нет

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / GetResponse (для SOAP)

AdExtensions

array of AdExtensionGetItem

Расширения к объявлениям.

LimitedBy

long

Порядковый номер последнего возвращенного объекта. Передается в случае, если количество объектов в ответе было ограничено лимитом. См. раздел  Постраничная выборка .

Структура AdExtensionGetItem

Id

long

Идентификатор расширения.

Associated

YesNoEnum

Привязано ли расширение хотя бы к одному объявлению клиента.

Type

AdExtensionTypeEnum

Тип расширения.

Callout

Callout

Параметры расширения с типом “Уточнение”.

State

StateEnum

Состояние расширения. См.  Соcтояние расширения .

Status

StatusEnum

Статус расширения. См.  Статус расширения .

StatusClarification

string

Текстовое пояснение к статусу и/или причины отклонения на модерации.

Структура Callout

CalloutText

string

Текст уточнения.

Возвращает расширения, отвечающие заданным критериям.

В настоящее время доступен один тип расширения — уточнение.

Метод возвращает не более 10 000 объектов.

Структура запроса в формате JSON:

Параметр

Тип

Описание

Обязательный

Структура params (для JSON) / GetRequest (для SOAP)

SelectionCriteria

AdExtensionsSelectionCriteria

Критерий отбора расширений.

Чтобы получить все расширения рекламодателя, необходимо указать пустой  SelectionCriteria .

Да

FieldNames

array of AdExtensionFieldEnum

Имена параметров, общие для всех типов расширений, которые требуется получить.

Да

CalloutFieldNames

array of CalloutFieldEnum

Имена параметров расширения с типом “Уточнение”, которые требуется получить.

Нет

Page

LimitOffset

Структура, задающая страницу при  постраничной выборке  данных.

Нет

Структура AdExtensionsSelectionCriteria

Ids

array of long

Отбирать расширения с указанными идентификаторами. Не более 10 000 элементов в массиве.

Нет

Types

array of AdExtensionTypeEnum

Отбирать расширения с указанными типами. В настоящее время доступен один тип расширения — “Уточнение” (CALLOUT).

Нет

States

array of AdExtensionStateSelectionEnum

Отбирать расширения с указанными состояниями. См.  Соcтояние расширения .

Примечание

Метод get возвращает расширение в состоянии DELETED, только если в параметре  States  указано значение DELETED или в параметре  Ids  указан идентификатор этого расширения. Если параметры  Ids  и  States  оба не заданы, метод не возвращает расширений в состоянии DELETED.

Нет

Statuses

array of ExtensionStatusSelectionEnum

Отбирать расширения с указанными статусами. См.  Статус расширения .

Нет

ModifiedSince

string

Отбирать расширения, в которых были изменения,начиная с указанной даты.

Задается в формате  YYYY-MM-DDThh:mm:ssZ  (согласно ISO 8601), например  2015-05-24T23:59:59Z .

Нет

Структура ответа в формате JSON:

Параметр

Тип

Описание

Структура result (для JSON) / GetResponse (для SOAP)

AdExtensions

array of AdExtensionGetItem

Расширения к объявлениям.

LimitedBy

long

Порядковый номер последнего возвращенного объекта. Передается в случае, если количество объектов в ответе было ограничено лимитом. См. раздел  Постраничная выборка .

Структура AdExtensionGetItem

Id

long

Идентификатор расширения.

Associated

YesNoEnum

Привязано ли расширение хотя бы к одному объявлению клиента.

Type

AdExtensionTypeEnum

Тип расширения.

Callout

Callout

Параметры расширения с типом “Уточнение”.

State

StateEnum

Состояние расширения. См.  Соcтояние расширения .

Status

StatusEnum

Статус расширения. См.  Статус расширения .

StatusClarification

string

Текстовое пояснение к статусу и/или причины отклонения на модерации.

Структура Callout

CalloutText

string

Текст уточнения.

- Как начать работу с API
- Руководство разработчика
- Справочник API   О справочнике   AdExtensions: операции с расширениями объявлений   add   delete   get   AdGroups: операции с группами объявлений   AdImages: операции с изображениями   Ads: операции с объявлениями   AdVideos: операции с видео   AgencyClients: управление клиентами агентства   AudienceTargets: управление условиями нацеливания на аудиторию   Bids: управление ставками   Businesses: получение профилей организаций   BidModifiers: управление корректировками ставок   Campaigns: управление кампаниями   Changes: проверка наличия изменений   Clients: управление параметрами рекламодателя и настройками пользователя   Creatives: получение креативов   Dictionaries: получение справочных данных   Feeds: операции с фидами   KeywordBids: управление ставками   Keywords: управление ключевыми фразами и автотаргетингами   KeywordsResearch: предобработка ключевых фраз   Leads: получение данных из форм на Турбо-страницах   NegativeKeywordSharedSets: управление наборами минус-фраз   RetargetingLists: управление условиями ретаргетинга и подбора аудитории   Sitelinks: операции с быстрыми ссылками   Strategies: операции с пакетными стратегиями   TurboPages: получение параметров Турбо-страниц   Ошибки и предупреждения   Справочные данные
- О справочнике
- AdExtensions: операции с расширениями объявлений   add   delete   get
- add
- delete
- get
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
- AdExtensions: операции с расширениями объявлений   add   delete   get
- add
- delete
- get
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
- delete
- get

- Узнайте больше
- Ограничения
- Запрос
- Ответ

- Узнайте больше
- Ограничения
- Запрос
- Ответ

- Как работает метод get

- Узнайте больше
- Ограничения
- Запрос
- Ответ

- Как работает метод get

```
{
   "method" :  "get" ,
     "params" : {  /* params */ 
     "SelectionCriteria" : {   /* AdExtensionsSelectionCriteria */ 
       "Ids" : [(long), ... ],
       "Types" : [(  "CALLOUT"  ), ... ],
       "States" : [(  "ON"  |  "DELETED"  ), ... ],
       "Statuses" : [(  "ACCEPTED"  |  "DRAFT"  |  "MODERATION"  |  "REJECTED"  ), ... ],
       "ModifiedSince" : (string)
    },  /* required */ 
     "FieldNames" : [(  "Id"  |  "Type"  |  "Status"  |  "StatusClarification"  |  "Associated"  ), ... ],  /* required */ 
     "CalloutFieldNames" : [(  "CalloutText"  )],
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
     "SelectionCriteria" : {   /* AdExtensionsSelectionCriteria */ 
       "Ids" : [(long), ... ],
       "Types" : [(  "CALLOUT"  ), ... ],
       "States" : [(  "ON"  |  "DELETED"  ), ... ],
       "Statuses" : [(  "ACCEPTED"  |  "DRAFT"  |  "MODERATION"  |  "REJECTED"  ), ... ],
       "ModifiedSince" : (string)
    },  /* required */ 
     "FieldNames" : [(  "Id"  |  "Type"  |  "Status"  |  "StatusClarification"  |  "Associated"  ), ... ],  /* required */ 
     "CalloutFieldNames" : [(  "CalloutText"  )],
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

`CalloutFieldNames`

`Page`

`Ids`

`Types`

`States`

`States`

`Ids`

`Ids`

`States`

`Statuses`

`ModifiedSince`

`YYYY-MM-DDThh:mm:ssZ`

`2015-05-24T23:59:59Z`

```
{
   "result" : {  /* result */ 
     "AdExtensions" : [{   /* AdExtensionGetItem */ 
       "Id" : (long),
       "Associated" : (  "YES"  |  "NO"  ),
       "Type" : (  "CALLOUT"  |  "UNKNOWN"  ),
       "Callout" : {   /* Callout */ 
         "CalloutText" : (string)  /* required */ 
      },
       "State" : [(  "ON"  |  "DELETED"  |  "UNKNOWN"  ), ... ],
       "Status" : (  "ACCEPTED"  |  "DRAFT"  |  "MODERATION"  |  "REJECTED"  |  "UNKNOWN"  ),
       "StatusClarification" : (string)
    }, ... ],
     "LimitedBy" : (long)
  }
}
```

```
{
   "result" : {  /* result */ 
     "AdExtensions" : [{   /* AdExtensionGetItem */ 
       "Id" : (long),
       "Associated" : (  "YES"  |  "NO"  ),
       "Type" : (  "CALLOUT"  |  "UNKNOWN"  ),
       "Callout" : {   /* Callout */ 
         "CalloutText" : (string)  /* required */ 
      },
       "State" : [(  "ON"  |  "DELETED"  |  "UNKNOWN"  ), ... ],
       "Status" : (  "ACCEPTED"  |  "DRAFT"  |  "MODERATION"  |  "REJECTED"  |  "UNKNOWN"  ),
       "StatusClarification" : (string)
    }, ... ],
     "LimitedBy" : (long)
  }
}
```

`AdExtensions`

`LimitedBy`

`Id`

`Associated`

`Type`

`Callout`

`State`

`Status`

`StatusClarification`

`CalloutText`

```
{
   "method" :  "get" ,
     "params" : {  /* params */ 
     "SelectionCriteria" : {   /* AdExtensionsSelectionCriteria */ 
       "Ids" : [(long), ... ],
       "Types" : [(  "CALLOUT"  ), ... ],
       "States" : [(  "ON"  |  "DELETED"  ), ... ],
       "Statuses" : [(  "ACCEPTED"  |  "DRAFT"  |  "MODERATION"  |  "REJECTED"  ), ... ],
       "ModifiedSince" : (string)
    },  /* required */ 
     "FieldNames" : [(  "Id"  |  "Type"  |  "Status"  |  "StatusClarification"  |  "Associated"  ), ... ],  /* required */ 
     "CalloutFieldNames" : [(  "CalloutText"  )],
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
     "SelectionCriteria" : {   /* AdExtensionsSelectionCriteria */ 
       "Ids" : [(long), ... ],
       "Types" : [(  "CALLOUT"  ), ... ],
       "States" : [(  "ON"  |  "DELETED"  ), ... ],
       "Statuses" : [(  "ACCEPTED"  |  "DRAFT"  |  "MODERATION"  |  "REJECTED"  ), ... ],
       "ModifiedSince" : (string)
    },  /* required */ 
     "FieldNames" : [(  "Id"  |  "Type"  |  "Status"  |  "StatusClarification"  |  "Associated"  ), ... ],  /* required */ 
     "CalloutFieldNames" : [(  "CalloutText"  )],
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

`CalloutFieldNames`

`Page`

`Ids`

`Types`

`States`

`States`

`Ids`

`Ids`

`States`

`Statuses`

`ModifiedSince`

`YYYY-MM-DDThh:mm:ssZ`

`2015-05-24T23:59:59Z`

```
{
   "result" : {  /* result */ 
     "AdExtensions" : [{   /* AdExtensionGetItem */ 
       "Id" : (long),
       "Associated" : (  "YES"  |  "NO"  ),
       "Type" : (  "CALLOUT"  |  "UNKNOWN"  ),
       "Callout" : {   /* Callout */ 
         "CalloutText" : (string)  /* required */ 
      },
       "State" : [(  "ON"  |  "DELETED"  |  "UNKNOWN"  ), ... ],
       "Status" : (  "ACCEPTED"  |  "DRAFT"  |  "MODERATION"  |  "REJECTED"  |  "UNKNOWN"  ),
       "StatusClarification" : (string)
    }, ... ],
     "LimitedBy" : (long)
  }
}
```

```
{
   "result" : {  /* result */ 
     "AdExtensions" : [{   /* AdExtensionGetItem */ 
       "Id" : (long),
       "Associated" : (  "YES"  |  "NO"  ),
       "Type" : (  "CALLOUT"  |  "UNKNOWN"  ),
       "Callout" : {   /* Callout */ 
         "CalloutText" : (string)  /* required */ 
      },
       "State" : [(  "ON"  |  "DELETED"  |  "UNKNOWN"  ), ... ],
       "Status" : (  "ACCEPTED"  |  "DRAFT"  |  "MODERATION"  |  "REJECTED"  |  "UNKNOWN"  ),
       "StatusClarification" : (string)
    }, ... ],
     "LimitedBy" : (long)
  }
}
```

`AdExtensions`

`LimitedBy`

`Id`

`Associated`

`Type`

`Callout`

`State`

`Status`

`StatusClarification`

`CalloutText`


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| SelectionCriteria | AdExtensionsSelectionCriteria |
| FieldNames | array of AdExtensionFieldEnum |
| CalloutFieldNames | array of CalloutFieldEnum |
| Page | LimitOffset |
| Ids | array of long |
| Types | array of AdExtensionTypeEnum |
| States | array of AdExtensionStateSelectionEnum |
| Statuses | array of ExtensionStatusSelectionEnum |
| ModifiedSince | string |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| AdExtensions | array of AdExtensionGetItem |
| LimitedBy | long |
| Id | long |
| Associated | YesNoEnum |
| Type | AdExtensionTypeEnum |
| Callout | Callout |
| State | StateEnum |
| Status | StatusEnum |
| StatusClarification | string |
| Структура Callout |  |
| CalloutText | string |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| SelectionCriteria | AdExtensionsSelectionCriteria |
| FieldNames | array of AdExtensionFieldEnum |
| CalloutFieldNames | array of CalloutFieldEnum |
| Page | LimitOffset |
| Ids | array of long |
| Types | array of AdExtensionTypeEnum |
| States | array of AdExtensionStateSelectionEnum |
| Statuses | array of ExtensionStatusSelectionEnum |
| ModifiedSince | string |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| AdExtensions | array of AdExtensionGetItem |
| LimitedBy | long |
| Id | long |
| Associated | YesNoEnum |
| Type | AdExtensionTypeEnum |
| Callout | Callout |
| State | StateEnum |
| Status | StatusEnum |
| StatusClarification | string |
| Структура Callout |  |
| CalloutText | string |

