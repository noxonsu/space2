# HTTP-заголовки  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/concepts/headers

**Дата скачивания:** 2025-07-01 12:35:56

---

## В этой статье :

# HTTP-заголовки

## Заголовки запроса

### Authorization

### Accept-Language

### Client-Login

### Use-Operator-Units: true

### Accept-Encoding: gzip

### Payment-Token

## Заголовки ответа

### RequestId

### Units

### Units-Used-Login

### Была ли статья полезна?

# HTTP-заголовки

## Заголовки запроса

### Authorization

### Accept-Language

### Client-Login

### Use-Operator-Units: true

### Accept-Encoding: gzip

### Payment-Token

## Заголовки ответа

### RequestId

### Units

### Units-Used-Login

### Была ли статья полезна?

Содержит  OAuth-токен  пользователя Яндекс Директа, от имени которого осуществляется запрос к API.

Пример:

Язык ответных сообщений. На выбранном языке возвращаются текстовые пояснения к статусам объектов (кампаний, объявлений и др.), тексты ошибок и предупреждений. Поддерживаются следующие языки:

Пример:

Если заголовок не указан или содержит язык, не поддерживаемый в API Директа, ответные сообщения формируются на английском языке.

Логин рекламодателя — клиента рекламного агентства. Обязателен, если запрос осуществляется от имени агентства.

Пример:

Расходовать баллы агентства, а не рекламодателя при выполнении запроса. См. раздел  Ограничения, баллы . Заголовок допустим только в запросах от имени агентства.

Получение тела ответа с использованием GZIP сжатия.

Финансовый токен. Необходим при вызове финансовых методов.

Пример запроса:

Уникальный идентификатор запроса (строка), присвоенный сервером API Директа. Возвращается как для успешных, так и для ошибочных запросов.

Пожалуйста, указывайте этот идентификатор при обращении в  службу поддержки .

Пример:

Количество баллов: 1. израсходовано при выполнении запроса, 2. доступный остаток суточного лимита, 3. суточный лимит. См. раздел  Ограничения, баллы .

Пример:

Логин представителя рекламодателя, если при выполнении запроса израсходованы баллы рекламодателя, или логин представителя агентства, если при выполнении запроса израсходованы баллы агентства.

Пример:

Пример ответа:

Содержит  OAuth-токен  пользователя Яндекс Директа, от имени которого осуществляется запрос к API.

Пример:

Язык ответных сообщений. На выбранном языке возвращаются текстовые пояснения к статусам объектов (кампаний, объявлений и др.), тексты ошибок и предупреждений. Поддерживаются следующие языки:

Пример:

Если заголовок не указан или содержит язык, не поддерживаемый в API Директа, ответные сообщения формируются на английском языке.

Логин рекламодателя — клиента рекламного агентства. Обязателен, если запрос осуществляется от имени агентства.

Пример:

Расходовать баллы агентства, а не рекламодателя при выполнении запроса. См. раздел  Ограничения, баллы . Заголовок допустим только в запросах от имени агентства.

Получение тела ответа с использованием GZIP сжатия.

Финансовый токен. Необходим при вызове финансовых методов.

Пример запроса:

Уникальный идентификатор запроса (строка), присвоенный сервером API Директа. Возвращается как для успешных, так и для ошибочных запросов.

Пожалуйста, указывайте этот идентификатор при обращении в  службу поддержки .

Пример:

Количество баллов: 1. израсходовано при выполнении запроса, 2. доступный остаток суточного лимита, 3. суточный лимит. См. раздел  Ограничения, баллы .

Пример:

Логин представителя рекламодателя, если при выполнении запроса израсходованы баллы рекламодателя, или логин представителя агентства, если при выполнении запроса израсходованы баллы агентства.

Пример:

Пример ответа:

- Как начать работу с API
- Руководство разработчика   О руководстве   Обзор API Директа версии 5   Варианты использования   Быстрый старт   Основные объекты   Доступ и авторизация   Формат взаимодействия   HTTP-заголовки   Формат JSON   Протокол SOAP   Обработка ошибок   Ограничения, баллы   Общие свойства методов API версии 5   Практика использования   Песочница   Список терминов
- О руководстве
- Обзор API Директа версии 5
- Варианты использования
- Быстрый старт
- Основные объекты
- Доступ и авторизация
- Формат взаимодействия   HTTP-заголовки   Формат JSON   Протокол SOAP   Обработка ошибок
- HTTP-заголовки
- Формат JSON
- Протокол SOAP
- Обработка ошибок
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
- Основные объекты
- Доступ и авторизация
- Формат взаимодействия   HTTP-заголовки   Формат JSON   Протокол SOAP   Обработка ошибок
- HTTP-заголовки
- Формат JSON
- Протокол SOAP
- Обработка ошибок
- Ограничения, баллы
- Общие свойства методов API версии 5
- Практика использования
- Песочница
- Список терминов

- HTTP-заголовки
- Формат JSON
- Протокол SOAP
- Обработка ошибок

- Заголовки запроса
- Authorization
- Accept-Language
- Client-Login
- Use-Operator-Units: true
- Accept-Encoding: gzip
- Payment-Token
- Заголовки ответа
- RequestId
- Units
- Units-Used-Login

- Заголовки запроса Authorization Accept-Language Client-Login Use-Operator-Units: true Accept-Encoding: gzip Payment-Token
- Authorization
- Accept-Language
- Client-Login
- Use-Operator-Units: true
- Accept-Encoding: gzip
- Payment-Token
- Заголовки ответа RequestId Units Units-Used-Login
- RequestId
- Units
- Units-Used-Login

- Authorization
- Accept-Language
- Client-Login
- Use-Operator-Units: true
- Accept-Encoding: gzip
- Payment-Token

- RequestId
- Units
- Units-Used-Login

- en — английский;
- ru — русский;
- tr — турецкий;

- Заголовки запроса Authorization Accept-Language Client-Login Use-Operator-Units: true Accept-Encoding: gzip Payment-Token
- Authorization
- Accept-Language
- Client-Login
- Use-Operator-Units: true
- Accept-Encoding: gzip
- Payment-Token
- Заголовки ответа RequestId Units Units-Used-Login
- RequestId
- Units
- Units-Used-Login

- Authorization
- Accept-Language
- Client-Login
- Use-Operator-Units: true
- Accept-Encoding: gzip
- Payment-Token

- RequestId
- Units
- Units-Used-Login

- en — английский;
- ru — русский;
- tr — турецкий;

`Authorization: Bearer 0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f`

`Authorization: Bearer 0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f`

`Accept-Language: ru`

`Accept-Language: ru`

`Client-Login: agrom`

`Client-Login: agrom`

```
POST  /json/v5/ads/  HTTP / 1.1 
 Host : api. direct . yandex . com 
 Authorization :  Bearer  0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
 Accept - Language : ru
 Client - Login : agrom
 Use - Operator - Units :  true 
 Content - Type : application/json; charset=utf- 8 

{
   "method" : "add" ,
   "params" : {
    ...
  }
}
```

```
POST  /json/v5/ads/  HTTP / 1.1 
 Host : api. direct . yandex . com 
 Authorization :  Bearer  0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
 Accept - Language : ru
 Client - Login : agrom
 Use - Operator - Units :  true 
 Content - Type : application/json; charset=utf- 8 

{
   "method" : "add" ,
   "params" : {
    ...
  }
}
```

`RequestId: 8695244274068608439`

`RequestId: 8695244274068608439`

`Units: 10/20828/64000`

`Units: 10/20828/64000`

`Units-Used-Login: ttt-agency`

`Units-Used-Login: ttt-agency`

```
HTTP/1.1 200 OK
Connection:close
Content-Type:application/json; charset=utf-8
Date:Fri, 28 Nov 2014 17:07:02 GMT
RequestId:8695244274068608439
Units:10/20828/64000
Units-Used-Login:ttt-agency
Server:nginx
Transfer-Encoding:chunked

{
  "result": {
    ...
  }
}
```

```
HTTP/1.1 200 OK
Connection:close
Content-Type:application/json; charset=utf-8
Date:Fri, 28 Nov 2014 17:07:02 GMT
RequestId:8695244274068608439
Units:10/20828/64000
Units-Used-Login:ttt-agency
Server:nginx
Transfer-Encoding:chunked

{
  "result": {
    ...
  }
}
```

`Authorization: Bearer 0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f`

`Authorization: Bearer 0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f`

`Accept-Language: ru`

`Accept-Language: ru`

`Client-Login: agrom`

`Client-Login: agrom`

```
POST  /json/v5/ads/  HTTP / 1.1 
 Host : api. direct . yandex . com 
 Authorization :  Bearer  0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
 Accept - Language : ru
 Client - Login : agrom
 Use - Operator - Units :  true 
 Content - Type : application/json; charset=utf- 8 

{
   "method" : "add" ,
   "params" : {
    ...
  }
}
```

```
POST  /json/v5/ads/  HTTP / 1.1 
 Host : api. direct . yandex . com 
 Authorization :  Bearer  0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
 Accept - Language : ru
 Client - Login : agrom
 Use - Operator - Units :  true 
 Content - Type : application/json; charset=utf- 8 

{
   "method" : "add" ,
   "params" : {
    ...
  }
}
```

`RequestId: 8695244274068608439`

`RequestId: 8695244274068608439`

`Units: 10/20828/64000`

`Units: 10/20828/64000`

`Units-Used-Login: ttt-agency`

`Units-Used-Login: ttt-agency`

```
HTTP/1.1 200 OK
Connection:close
Content-Type:application/json; charset=utf-8
Date:Fri, 28 Nov 2014 17:07:02 GMT
RequestId:8695244274068608439
Units:10/20828/64000
Units-Used-Login:ttt-agency
Server:nginx
Transfer-Encoding:chunked

{
  "result": {
    ...
  }
}
```

```
HTTP/1.1 200 OK
Connection:close
Content-Type:application/json; charset=utf-8
Date:Fri, 28 Nov 2014 17:07:02 GMT
RequestId:8695244274068608439
Units:10/20828/64000
Units-Used-Login:ttt-agency
Server:nginx
Transfer-Encoding:chunked

{
  "result": {
    ...
  }
}
```

