# Upload  API Яндекс Директа

**Источник:** https://yandex.ru/dev/direct/doc/dg-v4/ru/live/AdImage_Upload.html

**Дата скачивания:** 2025-07-01 12:40:13

---

## В этой статье :

# Upload

## Входные данные

## Результирующие данные

## Примеры входных данных

# Python

# PHP

# Perl

### Была ли статья полезна?

# Upload

## Входные данные

## Результирующие данные

## Примеры входных данных

# Python

# PHP

# Perl

### Была ли статья полезна?

Выполняет асинхронную загрузку изображений по списку URL. Синхронный ответ содержит номера заданий на загрузку.

Ниже показана структура входных данных в формате JSON.

Ниже приведено описание параметров.

Параметр

Описание

Требуется

Объект AdImageRequest

Action

Выполняемая операция: Upload.

Да

AdImageURLData

Массив объектов  AdImageURL  (не более 10 000), содержащих информацию о загружаемых изображениях.

Да

Объект AdImageURL

Login

Логин клиента — владельца изображения.

Для рекламодателей параметр игнорируется.

Для агентств

URL

Ссылка на изображение.

Да

Name

Произвольное наименование (описание) изображения.

Да

Внимание

Ошибка при создании задания на загрузку (постановке в очередь) одного из изображений не влечет отмену всей операции и не влияет на успешность создания заданий на загрузку остальных изображений.

Ниже показана структура результирующих данных в формате JSON.

Ниже приведено описание параметров.

Параметр

Описание

Объект AdImageResponse

ActionsResult

Массив объектов  AdImageActionResult . Каждый объект соответствует элементу входного массива  AdImageURLData  и содержит:

Элементы массива следуют в том же порядке, что и объекты входного массива  AdImageURL .

Объект AdImageActionResult

AdImageUploadTaskID

Номер созданного задания на загрузку. Номер можно использовать для проверки статуса загрузки с помощью операции  CheckUploadStatus .

Errors

Массив объектов  Error  — ошибок, возникших при постановке изображений в очередь на загрузку.

Объект Error

FaultCode

Код ошибки.

FaultString

Текст сообщения об ошибке.

FaultDetail

Подробное описание причины ошибки.

Выполняет асинхронную загрузку изображений по списку URL. Синхронный ответ содержит номера заданий на загрузку.

Ниже показана структура входных данных в формате JSON.

Ниже приведено описание параметров.

Параметр

Описание

Требуется

Объект AdImageRequest

Action

Выполняемая операция: Upload.

Да

AdImageURLData

Массив объектов  AdImageURL  (не более 10 000), содержащих информацию о загружаемых изображениях.

Да

Объект AdImageURL

Login

Логин клиента — владельца изображения.

Для рекламодателей параметр игнорируется.

Для агентств

URL

Ссылка на изображение.

Да

Name

Произвольное наименование (описание) изображения.

Да

Внимание

Ошибка при создании задания на загрузку (постановке в очередь) одного из изображений не влечет отмену всей операции и не влияет на успешность создания заданий на загрузку остальных изображений.

Ниже показана структура результирующих данных в формате JSON.

Ниже приведено описание параметров.

Параметр

Описание

Объект AdImageResponse

ActionsResult

Массив объектов  AdImageActionResult . Каждый объект соответствует элементу входного массива  AdImageURLData  и содержит:

Элементы массива следуют в том же порядке, что и объекты входного массива  AdImageURL .

Объект AdImageActionResult

AdImageUploadTaskID

Номер созданного задания на загрузку. Номер можно использовать для проверки статуса загрузки с помощью операции  CheckUploadStatus .

Errors

Массив объектов  Error  — ошибок, возникших при постановке изображений в очередь на загрузку.

Объект Error

FaultCode

Код ошибки.

FaultString

Текст сообщения об ошибке.

FaultDetail

Подробное описание причины ошибки.

- Введение
- Версии API
- Варианты использования
- Начните разрабатывать свое приложение
- Доступ
- Практика использования
- Первоначальные сведения
- Песочница
- Методы   Прогноз бюджета и подбор фраз   Метки объявлений   Изображения в объявлениях   AdImage (Live)   Upload   CheckUploadStatus   UploadRawData   Delete   Get   GetLimits   AdImageAssociation (Live)   Ретаргетинг   Финансовые операции   Общий счет   Баллы   Прочие методы   Отключенные методы   Коды ошибок и предупреждений
- Прогноз бюджета и подбор фраз
- Метки объявлений
- Изображения в объявлениях   AdImage (Live)   Upload   CheckUploadStatus   UploadRawData   Delete   Get   GetLimits   AdImageAssociation (Live)
- AdImage (Live)   Upload   CheckUploadStatus   UploadRawData   Delete   Get   GetLimits
- Upload
- CheckUploadStatus
- UploadRawData
- Delete
- Get
- GetLimits
- AdImageAssociation (Live)
- Ретаргетинг
- Финансовые операции
- Общий счет
- Баллы
- Прочие методы
- Отключенные методы
- Коды ошибок и предупреждений
- Примеры

- Прогноз бюджета и подбор фраз
- Метки объявлений
- Изображения в объявлениях   AdImage (Live)   Upload   CheckUploadStatus   UploadRawData   Delete   Get   GetLimits   AdImageAssociation (Live)
- AdImage (Live)   Upload   CheckUploadStatus   UploadRawData   Delete   Get   GetLimits
- Upload
- CheckUploadStatus
- UploadRawData
- Delete
- Get
- GetLimits
- AdImageAssociation (Live)
- Ретаргетинг
- Финансовые операции
- Общий счет
- Баллы
- Прочие методы
- Отключенные методы
- Коды ошибок и предупреждений

- AdImage (Live)   Upload   CheckUploadStatus   UploadRawData   Delete   Get   GetLimits
- Upload
- CheckUploadStatus
- UploadRawData
- Delete
- Get
- GetLimits
- AdImageAssociation (Live)

- Upload
- CheckUploadStatus
- UploadRawData
- Delete
- Get
- GetLimits

- Входные данные
- Результирующие данные
- Примеры входных данных

- Входные данные
- Результирующие данные
- Примеры входных данных

- в случае успешной постановки изображения в очередь — номер задания на загрузку;
- в случае ошибки — массив  Errors .

- Входные данные
- Результирующие данные
- Примеры входных данных

- в случае успешной постановки изображения в очередь — номер задания на загрузку;
- в случае ошибки — массив  Errors .

```
{
    "method" :  "AdImage" ,
    "param" : {
       /* AdImageRequest */ 
       "Action" : (string),
       "AdImageURLData" : [
         {   /* AdImageURL */ 
             "Login" : (string),
             "URL" : (string),
             "Name" : (string)
         }
         ...
      ]
   }
}
```

```
{
    "method" :  "AdImage" ,
    "param" : {
       /* AdImageRequest */ 
       "Action" : (string),
       "AdImageURLData" : [
         {   /* AdImageURL */ 
             "Login" : (string),
             "URL" : (string),
             "Name" : (string)
         }
         ...
      ]
   }
}
```

`Action`

`AdImageURLData`

`AdImageURL`

`Login`

`URL`

`Name`

```
{
    "data" : {
       /* AdImageResponse */ 
       "ActionsResult" : [
         {   /* AdImageActionResult */ 
             "AdImageUploadTaskID" : (int),
             "Errors" : [
               {   /* Error */ 
                   "FaultCode" : (int),
                   "FaultString" : (string),
                   "FaultDetail" : (string)
               }
               ...
            ],
         }
         ...
      ]
   }
}
```

```
{
    "data" : {
       /* AdImageResponse */ 
       "ActionsResult" : [
         {   /* AdImageActionResult */ 
             "AdImageUploadTaskID" : (int),
             "Errors" : [
               {   /* Error */ 
                   "FaultCode" : (int),
                   "FaultString" : (string),
                   "FaultDetail" : (string)
               }
               ...
            ],
         }
         ...
      ]
   }
}
```

`ActionsResult`

`AdImageActionResult`

`AdImageURLData`

`Errors`

`AdImageURL`

`AdImageUploadTaskID`

`Errors`

`Error`

`FaultCode`

`FaultString`

`FaultDetail`

```
{
    'Action' :  'Upload' ,
    'AdImageURLData' : [
      {
          'Login' :  'agrom' ,
          'URL' :  'http://site.ru/files/image001.png' ,
          'Name' :  u'Слоны: новая коллекция' 
      },
      {
          'Login' :  'agrom' ,
          'URL' :  'http://site.ru/files/image002.png' ,
          'Name' :  u'Слоны: сертификация и обслуживание' 
      },
      {
          'Login' :  'larry' ,
          'URL' :  'http://example.net/files/pic.png' ,
          'Name' :  u'Сухари впрок' 
      }
   ]
}
```

```
{
    'Action' :  'Upload' ,
    'AdImageURLData' : [
      {
          'Login' :  'agrom' ,
          'URL' :  'http://site.ru/files/image001.png' ,
          'Name' :  u'Слоны: новая коллекция' 
      },
      {
          'Login' :  'agrom' ,
          'URL' :  'http://site.ru/files/image002.png' ,
          'Name' :  u'Слоны: сертификация и обслуживание' 
      },
      {
          'Login' :  'larry' ,
          'URL' :  'http://example.net/files/pic.png' ,
          'Name' :  u'Сухари впрок' 
      }
   ]
}
```

```
array (
    'Action'  =>  'Upload' ,
    'AdImageURLData'  =>  array (
       array (
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image001.png' ,
          'Name'  = 'Слоны: новая коллекция' 
      ),
       array (
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image002.png' ,
          'Name'  = 'Слоны: сертификация и обслуживание' 
      ),
       array (
          'Login'  =>  'larry' ,
          'URL'  =>  'http://example.net/files/pic.png' ,
          'Name'  = 'Сухари впрок' 
      )
   )
)
```

```
array (
    'Action'  =>  'Upload' ,
    'AdImageURLData'  =>  array (
       array (
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image001.png' ,
          'Name'  = 'Слоны: новая коллекция' 
      ),
       array (
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image002.png' ,
          'Name'  = 'Слоны: сертификация и обслуживание' 
      ),
       array (
          'Login'  =>  'larry' ,
          'URL'  =>  'http://example.net/files/pic.png' ,
          'Name'  = 'Сухари впрок' 
      )
   )
)
```

```
{
    'Action'  =>  'Upload' ,
    'AdImageURLData'  => [
      {
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image001.png' ,
          'Name'  = 'Слоны: новая коллекция' 
      },
      {
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image002.png' ,
          'Name'  = 'Слоны: сертификация и обслуживание' 
      },
      {
          'Login'  =>  'larry' ,
          'URL'  =>  'http://example.net/files/pic.png' ,
          'Name'  = 'Сухари впрок' 
      },
   ]
}
```

```
{
    'Action'  =>  'Upload' ,
    'AdImageURLData'  => [
      {
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image001.png' ,
          'Name'  = 'Слоны: новая коллекция' 
      },
      {
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image002.png' ,
          'Name'  = 'Слоны: сертификация и обслуживание' 
      },
      {
          'Login'  =>  'larry' ,
          'URL'  =>  'http://example.net/files/pic.png' ,
          'Name'  = 'Сухари впрок' 
      },
   ]
}
```

```
{
    "method" :  "AdImage" ,
    "param" : {
       /* AdImageRequest */ 
       "Action" : (string),
       "AdImageURLData" : [
         {   /* AdImageURL */ 
             "Login" : (string),
             "URL" : (string),
             "Name" : (string)
         }
         ...
      ]
   }
}
```

```
{
    "method" :  "AdImage" ,
    "param" : {
       /* AdImageRequest */ 
       "Action" : (string),
       "AdImageURLData" : [
         {   /* AdImageURL */ 
             "Login" : (string),
             "URL" : (string),
             "Name" : (string)
         }
         ...
      ]
   }
}
```

`Action`

`AdImageURLData`

`AdImageURL`

`Login`

`URL`

`Name`

```
{
    "data" : {
       /* AdImageResponse */ 
       "ActionsResult" : [
         {   /* AdImageActionResult */ 
             "AdImageUploadTaskID" : (int),
             "Errors" : [
               {   /* Error */ 
                   "FaultCode" : (int),
                   "FaultString" : (string),
                   "FaultDetail" : (string)
               }
               ...
            ],
         }
         ...
      ]
   }
}
```

```
{
    "data" : {
       /* AdImageResponse */ 
       "ActionsResult" : [
         {   /* AdImageActionResult */ 
             "AdImageUploadTaskID" : (int),
             "Errors" : [
               {   /* Error */ 
                   "FaultCode" : (int),
                   "FaultString" : (string),
                   "FaultDetail" : (string)
               }
               ...
            ],
         }
         ...
      ]
   }
}
```

`ActionsResult`

`AdImageActionResult`

`AdImageURLData`

`Errors`

`AdImageURL`

`AdImageUploadTaskID`

`Errors`

`Error`

`FaultCode`

`FaultString`

`FaultDetail`

```
{
    'Action' :  'Upload' ,
    'AdImageURLData' : [
      {
          'Login' :  'agrom' ,
          'URL' :  'http://site.ru/files/image001.png' ,
          'Name' :  u'Слоны: новая коллекция' 
      },
      {
          'Login' :  'agrom' ,
          'URL' :  'http://site.ru/files/image002.png' ,
          'Name' :  u'Слоны: сертификация и обслуживание' 
      },
      {
          'Login' :  'larry' ,
          'URL' :  'http://example.net/files/pic.png' ,
          'Name' :  u'Сухари впрок' 
      }
   ]
}
```

```
{
    'Action' :  'Upload' ,
    'AdImageURLData' : [
      {
          'Login' :  'agrom' ,
          'URL' :  'http://site.ru/files/image001.png' ,
          'Name' :  u'Слоны: новая коллекция' 
      },
      {
          'Login' :  'agrom' ,
          'URL' :  'http://site.ru/files/image002.png' ,
          'Name' :  u'Слоны: сертификация и обслуживание' 
      },
      {
          'Login' :  'larry' ,
          'URL' :  'http://example.net/files/pic.png' ,
          'Name' :  u'Сухари впрок' 
      }
   ]
}
```

```
array (
    'Action'  =>  'Upload' ,
    'AdImageURLData'  =>  array (
       array (
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image001.png' ,
          'Name'  = 'Слоны: новая коллекция' 
      ),
       array (
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image002.png' ,
          'Name'  = 'Слоны: сертификация и обслуживание' 
      ),
       array (
          'Login'  =>  'larry' ,
          'URL'  =>  'http://example.net/files/pic.png' ,
          'Name'  = 'Сухари впрок' 
      )
   )
)
```

```
array (
    'Action'  =>  'Upload' ,
    'AdImageURLData'  =>  array (
       array (
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image001.png' ,
          'Name'  = 'Слоны: новая коллекция' 
      ),
       array (
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image002.png' ,
          'Name'  = 'Слоны: сертификация и обслуживание' 
      ),
       array (
          'Login'  =>  'larry' ,
          'URL'  =>  'http://example.net/files/pic.png' ,
          'Name'  = 'Сухари впрок' 
      )
   )
)
```

```
{
    'Action'  =>  'Upload' ,
    'AdImageURLData'  => [
      {
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image001.png' ,
          'Name'  = 'Слоны: новая коллекция' 
      },
      {
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image002.png' ,
          'Name'  = 'Слоны: сертификация и обслуживание' 
      },
      {
          'Login'  =>  'larry' ,
          'URL'  =>  'http://example.net/files/pic.png' ,
          'Name'  = 'Сухари впрок' 
      },
   ]
}
```

```
{
    'Action'  =>  'Upload' ,
    'AdImageURLData'  => [
      {
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image001.png' ,
          'Name'  = 'Слоны: новая коллекция' 
      },
      {
          'Login'  =>  'agrom' ,
          'URL'  =>  'http://site.ru/files/image002.png' ,
          'Name'  = 'Слоны: сертификация и обслуживание' 
      },
      {
          'Login'  =>  'larry' ,
          'URL'  =>  'http://example.net/files/pic.png' ,
          'Name'  = 'Сухари впрок' 
      },
   ]
}
```


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Описание |
| Объект AdImageRequest |  |
| Action | Выполняемая операция: Upload. |
| AdImageURLData | Массив объектов  AdImageURL  (не более 10 000), содержащих информацию о загружаемых изображениях. |
| Объект AdImageURL |  |
| Login | Логин клиента — владельца изображения. 
 Для рекламодателей параметр игнорируется. |
| URL | Ссылка на изображение. |
| Name | Произвольное наименование (описание) изображения. |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Описание |
| Объект AdImageResponse |  |
| ActionsResult | Массив объектов  AdImageActionResult . Каждый объект соответствует элементу входного массива  AdImageURLData  и содержит: 
 
 в случае успешной постановки изображения в очередь — номер задания на загрузку; 
 в случае ошибки — массив  Errors . 
 
 Элементы массива следуют в том же порядке, что и объекты входного массива  AdImageURL . |
| Объект AdImageActionResult |  |
| AdImageUploadTaskID | Номер созданного задания на загрузку. Номер можно использовать для проверки статуса загрузки с помощью операции  CheckUploadStatus . |
| Errors | Массив объектов  Error  — ошибок, возникших при постановке изображений в очередь на загрузку. |
| Объект Error |  |
| FaultCode | Код ошибки. |
| FaultString | Текст сообщения об ошибке. |
| FaultDetail | Подробное описание причины ошибки. |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Описание |
| Объект AdImageRequest |  |
| Action | Выполняемая операция: Upload. |
| AdImageURLData | Массив объектов  AdImageURL  (не более 10 000), содержащих информацию о загружаемых изображениях. |
| Объект AdImageURL |  |
| Login | Логин клиента — владельца изображения. 
 Для рекламодателей параметр игнорируется. |
| URL | Ссылка на изображение. |
| Name | Произвольное наименование (описание) изображения. |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Описание |
| Объект AdImageResponse |  |
| ActionsResult | Массив объектов  AdImageActionResult . Каждый объект соответствует элементу входного массива  AdImageURLData  и содержит: 
 
 в случае успешной постановки изображения в очередь — номер задания на загрузку; 
 в случае ошибки — массив  Errors . 
 
 Элементы массива следуют в том же порядке, что и объекты входного массива  AdImageURL . |
| Объект AdImageActionResult |  |
| AdImageUploadTaskID | Номер созданного задания на загрузку. Номер можно использовать для проверки статуса загрузки с помощью операции  CheckUploadStatus . |
| Errors | Массив объектов  Error  — ошибок, возникших при постановке изображений в очередь на загрузку. |
| Объект Error |  |
| FaultCode | Код ошибки. |
| FaultString | Текст сообщения об ошибке. |
| FaultDetail | Подробное описание причины ошибки. |

