# GetLimits  API Яндекс Директа

**Источник:** https://yandex.ru/dev/direct/doc/dg-v4/ru/live/AdImage_GetLimits.html

**Дата скачивания:** 2025-07-01 12:39:47

---

## В этой статье :

# GetLimits

## Входные данные

## Результирующие данные

## Примеры входных данных

# Python

# PHP

# Perl

### Была ли статья полезна?

# GetLimits

## Входные данные

## Результирующие данные

## Примеры входных данных

# Python

# PHP

# Perl

### Была ли статья полезна?

Возвращает общее количество изображений, которое клиент может загрузить, а также количество изображений, уже загруженных или находящихся в очереди на загрузку.

Ниже показана структура входных данных в формате JSON.

Ниже приведено описание параметров.

Параметр

Описание

Требуется

Объект AdImageRequest

Action

Выполняемая операция: GetLimits.

Да

SelectionCriteria

Объект  AdImageSelectionCriteria , содержащий критерий отбора логинов.

Для агентств

Объект AdImageSelectionCriteria

Logins

Для агентств — массив, содержащий логины клиентов (не более 1000), для которых нужно получить количество изображений.

Для рекламодателей параметр игнорируется.

Для агентств

Ниже показана структура результирующих данных в формате JSON.

Ниже приведено описание параметров.

Параметр

Описание

Объект AdImageResponse

AdImageLimits

Массив объектов AdImageLimit.

Объект AdImageLimit

Login

Логин клиента.

Capacity

Общее количество изображений, которое клиент может загрузить.

Utilized

Количество загруженных изображений плюс количество заданий на загрузку со статусом Pending.

Возвращает общее количество изображений, которое клиент может загрузить, а также количество изображений, уже загруженных или находящихся в очереди на загрузку.

Ниже показана структура входных данных в формате JSON.

Ниже приведено описание параметров.

Параметр

Описание

Требуется

Объект AdImageRequest

Action

Выполняемая операция: GetLimits.

Да

SelectionCriteria

Объект  AdImageSelectionCriteria , содержащий критерий отбора логинов.

Для агентств

Объект AdImageSelectionCriteria

Logins

Для агентств — массив, содержащий логины клиентов (не более 1000), для которых нужно получить количество изображений.

Для рекламодателей параметр игнорируется.

Для агентств

Ниже показана структура результирующих данных в формате JSON.

Ниже приведено описание параметров.

Параметр

Описание

Объект AdImageResponse

AdImageLimits

Массив объектов AdImageLimit.

Объект AdImageLimit

Login

Логин клиента.

Capacity

Общее количество изображений, которое клиент может загрузить.

Utilized

Количество загруженных изображений плюс количество заданий на загрузку со статусом Pending.

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

- Входные данные
- Результирующие данные
- Примеры входных данных

```
{
    "method" :  "AdImage" ,
    "param" : {
       /* AdImageRequest */ 
       "Action" : (string),
       "SelectionCriteria" : {
          /* AdImageSelectionCriteria */ 
          "Logins" : [
            (string)
            ...
         ]
      }
   }
}
```

```
{
    "method" :  "AdImage" ,
    "param" : {
       /* AdImageRequest */ 
       "Action" : (string),
       "SelectionCriteria" : {
          /* AdImageSelectionCriteria */ 
          "Logins" : [
            (string)
            ...
         ]
      }
   }
}
```

`Action`

`SelectionCriteria`

`AdImageSelectionCriteria`

`Logins`

```
{
    "data" : {
       /* AdImageResponse */ 
       "AdImageLimits" : [
         {   /* AdImageLimit */ 
             "Login" : (string),
             "Capacity" : (int),
             "Utilized" : (int)
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
       "AdImageLimits" : [
         {   /* AdImageLimit */ 
             "Login" : (string),
             "Capacity" : (int),
             "Utilized" : (int)
         }
         ...
      ]
   }
}
```

`AdImageLimits`

`Login`

`Capacity`

`Utilized`

```
{
    'Action' :  'GetLimits' ,
    'SelectionCriteria' : {
       'Logins' : [ 'agrom' , 'larry' ]
   }
}
```

```
{
    'Action' :  'GetLimits' ,
    'SelectionCriteria' : {
       'Logins' : [ 'agrom' , 'larry' ]
   }
}
```

```
array (
    'Action'  =>  'GetLimits' ,
    'SelectionCriteria'  =>  array (
       'Logins'  =>  array ( 'agrom' , 'larry' )
   )
)
```

```
array (
    'Action'  =>  'GetLimits' ,
    'SelectionCriteria'  =>  array (
       'Logins'  =>  array ( 'agrom' , 'larry' )
   )
)
```

```
{
    'Action'  =>  'GetLimits' ,
    'SelectionCriteria'  ={
       'Logins'  => [ 'agrom' , 'larry' ]
   }
}
```

```
{
    'Action'  =>  'GetLimits' ,
    'SelectionCriteria'  ={
       'Logins'  => [ 'agrom' , 'larry' ]
   }
}
```

```
{
    "method" :  "AdImage" ,
    "param" : {
       /* AdImageRequest */ 
       "Action" : (string),
       "SelectionCriteria" : {
          /* AdImageSelectionCriteria */ 
          "Logins" : [
            (string)
            ...
         ]
      }
   }
}
```

```
{
    "method" :  "AdImage" ,
    "param" : {
       /* AdImageRequest */ 
       "Action" : (string),
       "SelectionCriteria" : {
          /* AdImageSelectionCriteria */ 
          "Logins" : [
            (string)
            ...
         ]
      }
   }
}
```

`Action`

`SelectionCriteria`

`AdImageSelectionCriteria`

`Logins`

```
{
    "data" : {
       /* AdImageResponse */ 
       "AdImageLimits" : [
         {   /* AdImageLimit */ 
             "Login" : (string),
             "Capacity" : (int),
             "Utilized" : (int)
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
       "AdImageLimits" : [
         {   /* AdImageLimit */ 
             "Login" : (string),
             "Capacity" : (int),
             "Utilized" : (int)
         }
         ...
      ]
   }
}
```

`AdImageLimits`

`Login`

`Capacity`

`Utilized`

```
{
    'Action' :  'GetLimits' ,
    'SelectionCriteria' : {
       'Logins' : [ 'agrom' , 'larry' ]
   }
}
```

```
{
    'Action' :  'GetLimits' ,
    'SelectionCriteria' : {
       'Logins' : [ 'agrom' , 'larry' ]
   }
}
```

```
array (
    'Action'  =>  'GetLimits' ,
    'SelectionCriteria'  =>  array (
       'Logins'  =>  array ( 'agrom' , 'larry' )
   )
)
```

```
array (
    'Action'  =>  'GetLimits' ,
    'SelectionCriteria'  =>  array (
       'Logins'  =>  array ( 'agrom' , 'larry' )
   )
)
```

```
{
    'Action'  =>  'GetLimits' ,
    'SelectionCriteria'  ={
       'Logins'  => [ 'agrom' , 'larry' ]
   }
}
```

```
{
    'Action'  =>  'GetLimits' ,
    'SelectionCriteria'  ={
       'Logins'  => [ 'agrom' , 'larry' ]
   }
}
```


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Описание |
| Объект AdImageRequest |  |
| Action | Выполняемая операция: GetLimits. |
| SelectionCriteria | Объект  AdImageSelectionCriteria , содержащий критерий отбора логинов. |
| Объект AdImageSelectionCriteria |  |
| Logins | Для агентств — массив, содержащий логины клиентов (не более 1000), для которых нужно получить количество изображений. 
 Для рекламодателей параметр игнорируется. |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Описание |
| Объект AdImageResponse |  |
| AdImageLimits | Массив объектов AdImageLimit. |
| Объект AdImageLimit |  |
| Login | Логин клиента. |
| Capacity | Общее количество изображений, которое клиент может загрузить. |
| Utilized | Количество загруженных изображений плюс количество заданий на загрузку со статусом Pending. |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Описание |
| Объект AdImageRequest |  |
| Action | Выполняемая операция: GetLimits. |
| SelectionCriteria | Объект  AdImageSelectionCriteria , содержащий критерий отбора логинов. |
| Объект AdImageSelectionCriteria |  |
| Logins | Для агентств — массив, содержащий логины клиентов (не более 1000), для которых нужно получить количество изображений. 
 Для рекламодателей параметр игнорируется. |


| Столбец 1 | Столбец 2 |
|-----------|----------|
| Параметр | Описание |
| Объект AdImageResponse |  |
| AdImageLimits | Массив объектов AdImageLimit. |
| Объект AdImageLimit |  |
| Login | Логин клиента. |
| Capacity | Общее количество изображений, которое клиент может загрузить. |
| Utilized | Количество загруженных изображений плюс количество заданий на загрузку со статусом Pending. |

