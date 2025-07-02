# Обработка ошибок  Яндекс Директ API

**Источник:** https://yandex.ru/dev/direct/doc/ru/concepts/errors

**Дата скачивания:** 2025-07-01 12:36:07

---

# Обработка ошибок

## Ошибки выполнения запроса

### Была ли статья полезна?

# Обработка ошибок

## Ошибки выполнения запроса

### Была ли статья полезна?

При вызове метода возможно возникновение ошибок и предупреждений:

Ошибки, исключающие возможность выполнения запроса: неверный формат запроса (в том числе отсутствие обязательного параметра), неверный токен, недоступность сервера API и т. п.

Ошибки и предупреждения при выполнении операции с одним из объектов в запросе, которые не влияют на успешность выполнения операции с другими объектами. Подробно об ошибках операции читайте в разделе  Операции над массивом объектов .

Коды и описания ошибок и предупреждений приведены в разделе  Ошибки и предупреждения .

Примечание

Язык сообщений об ошибках определяется заголовком запроса  Accept-Language .

Если выполнение запроса невозможно, возвращается следующая структура:

Параметр

Тип

Описание

Объект Fault

faultstring

string

Текст сообщения об ошибке.

detail

ApiExceptionMessage

Сведения об ошибке.

Объект ApiExceptionMessage

requestId

string

Уникальный идентификатор запроса, присвоенный сервером API Директа. Также передается в HTTP-заголовке  RequestId .

errorCode

int

Числовой код ошибки.

errorDetail

string

Подробное описание ошибки.

Параметр

Тип

Описание

request_id

string

Уникальный идентификатор запроса, присвоенный сервером API Директа. Также передается в HTTP-заголовке  RequestId .

error_code

int

Числовой код ошибки.

error_string

string

Текст сообщения об ошибке.

error_detail

string

Подробное описание ошибки.

При вызове метода возможно возникновение ошибок и предупреждений:

Ошибки, исключающие возможность выполнения запроса: неверный формат запроса (в том числе отсутствие обязательного параметра), неверный токен, недоступность сервера API и т. п.

Ошибки и предупреждения при выполнении операции с одним из объектов в запросе, которые не влияют на успешность выполнения операции с другими объектами. Подробно об ошибках операции читайте в разделе  Операции над массивом объектов .

Коды и описания ошибок и предупреждений приведены в разделе  Ошибки и предупреждения .

Примечание

Язык сообщений об ошибках определяется заголовком запроса  Accept-Language .

Если выполнение запроса невозможно, возвращается следующая структура:

Параметр

Тип

Описание

Объект Fault

faultstring

string

Текст сообщения об ошибке.

detail

ApiExceptionMessage

Сведения об ошибке.

Объект ApiExceptionMessage

requestId

string

Уникальный идентификатор запроса, присвоенный сервером API Директа. Также передается в HTTP-заголовке  RequestId .

errorCode

int

Числовой код ошибки.

errorDetail

string

Подробное описание ошибки.

Параметр

Тип

Описание

request_id

string

Уникальный идентификатор запроса, присвоенный сервером API Директа. Также передается в HTTP-заголовке  RequestId .

error_code

int

Числовой код ошибки.

error_string

string

Текст сообщения об ошибке.

error_detail

string

Подробное описание ошибки.

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

- Ошибки, исключающие возможность выполнения запроса: неверный формат запроса (в том числе отсутствие обязательного параметра), неверный токен, недоступность сервера API и т. п.
- Ошибки и предупреждения при выполнении операции с одним из объектов в запросе, которые не влияют на успешность выполнения операции с другими объектами. Подробно об ошибках операции читайте в разделе  Операции над массивом объектов .

- Ошибки, исключающие возможность выполнения запроса: неверный формат запроса (в том числе отсутствие обязательного параметра), неверный токен, недоступность сервера API и т. п.
- Ошибки и предупреждения при выполнении операции с одним из объектов в запросе, которые не влияют на успешность выполнения операции с другими объектами. Подробно об ошибках операции читайте в разделе  Операции над массивом объектов .

```
< SOAP-ENV:Fault > 
   < faultcode > SOAP-ENV:Client </ faultcode > 
   < faultstring > (string) </ faultstring > 
   < detail > 
     < ns3:FaultResponse   xmlns:ns3 = "http://direct.yandex.com/api/v5/general" > 
       < requestId > (string) </ requestId > 
       < errorCode > (int) </ errorCode > 
       < errorDetail > (string) </ errorDetail > 
     </ ns3:FaultResponse > 
   </ detail > 
 </ SOAP-ENV:Fault >
```

```
< SOAP-ENV:Fault > 
   < faultcode > SOAP-ENV:Client </ faultcode > 
   < faultstring > (string) </ faultstring > 
   < detail > 
     < ns3:FaultResponse   xmlns:ns3 = "http://direct.yandex.com/api/v5/general" > 
       < requestId > (string) </ requestId > 
       < errorCode > (int) </ errorCode > 
       < errorDetail > (string) </ errorDetail > 
     </ ns3:FaultResponse > 
   </ detail > 
 </ SOAP-ENV:Fault >
```

`RequestId`

```
{
   "error"  : {
     "request_id" : (string),
     "error_code" : (int),
     "error_string" : (string),
     "error_detail" : (string)
  }
}
```

```
{
   "error"  : {
     "request_id" : (string),
     "error_code" : (int),
     "error_string" : (string),
     "error_detail" : (string)
  }
}
```

`request_id`

`RequestId`

`error_code`

`error_string`

`error_detail`

```
< SOAP-ENV:Fault > 
   < faultcode > SOAP-ENV:Client </ faultcode > 
   < faultstring > (string) </ faultstring > 
   < detail > 
     < ns3:FaultResponse   xmlns:ns3 = "http://direct.yandex.com/api/v5/general" > 
       < requestId > (string) </ requestId > 
       < errorCode > (int) </ errorCode > 
       < errorDetail > (string) </ errorDetail > 
     </ ns3:FaultResponse > 
   </ detail > 
 </ SOAP-ENV:Fault >
```

```
< SOAP-ENV:Fault > 
   < faultcode > SOAP-ENV:Client </ faultcode > 
   < faultstring > (string) </ faultstring > 
   < detail > 
     < ns3:FaultResponse   xmlns:ns3 = "http://direct.yandex.com/api/v5/general" > 
       < requestId > (string) </ requestId > 
       < errorCode > (int) </ errorCode > 
       < errorDetail > (string) </ errorDetail > 
     </ ns3:FaultResponse > 
   </ detail > 
 </ SOAP-ENV:Fault >
```

`RequestId`

```
{
   "error"  : {
     "request_id" : (string),
     "error_code" : (int),
     "error_string" : (string),
     "error_detail" : (string)
  }
}
```

```
{
   "error"  : {
     "request_id" : (string),
     "error_code" : (int),
     "error_string" : (string),
     "error_detail" : (string)
  }
}
```

`request_id`

`RequestId`

`error_code`

`error_string`

`error_detail`


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| faultstring | string |
| detail | ApiExceptionMessage |
| requestId | string |
| errorCode | int |
| errorDetail | string |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| request_id | string |
| error_code | int |
| error_string | string |
| error_detail | string |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| faultstring | string |
| detail | ApiExceptionMessage |
| requestId | string |
| errorCode | int |
| errorDetail | string |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Тип |
| request_id | string |
| error_code | int |
| error_string | string |
| error_detail | string |

