
Документы
Облачный API WhatsApp
Облачный API WhatsApp
Обзор
Начало работы
Начало работы: информация для партнеров по решениям
Get Started for Tech Providers
Совместные партнерские решения
Обмен сообщениями
Шаблоны
Webhooks
Calling
Блокировка пользователей
Номера телефонов
Продажа товаров и услуг
Payments API - India
Payments API - Brazil
Справка
Поддержка
WhatsApp Business Platform

We are making changes to the WhatsApp Business Platform pricing model.

Effective July 1, 2025 for all businesses on our platform:

The conversation-based pricing model will be deprecated
We will charge per-message for template messages instead of per-conversation
Utility templates sent within an open customer service window will be free
See Pricing Updates on the WhatsApp Business Platform for additional details.

Облачный API
Meta Blueprint
Set up the WhatsApp Business Platform
Отправляйте и получайте сообщения, используя облачную версию платформы WhatsApp Business. Облачный API, расположенный на серверах Meta, позволяет реализовать API WhatsApp Business, не тратя средств на размещение собственных серверов, и упрощает масштабирование переписок.

If you are a developer who wants direct access to the Cloud API to build on the behalf of a client’s business, fill out this form and we will reach out with more information.

Содержание документации
Общие сведения
Узнайте, как работает облачный API. Ознакомьтесь с информацией об ограничении числа обращений, метриках, масштабировании, конфиденциальности данных, безопасности и шифровании.

Начало работы
Отправьте свое первое сообщение с помощью облачного API. Партнерам по решениям необходимо ознакомиться с этим руководством по началу работы.

Руководства
Узнайте, как использовать наши доступные конечные точки.

Справка
Узнайте, какие узлы API и границы контекста сейчас доступны.

Webhooks
Получайте уведомления о своих сообщениях и их статусе.

Часто задаваемые вопросы
Часто задаваемые вопросы об облачном API.

Устранение неполадок
Узнайте, как решать проблемы, которые могут возникнуть при использовании этого API.

Коды ошибок
Ознакомьтесь со структурой сообщений об ошибках и посмотрите все доступные коды ошибок.

Платформа WhatsApp Business | Облачный API  | API Business Management
На этой Странице
Облачный API
Содержание документации

Мы в социальных сетях
Подпишитесь на нас на FacebookПодпишитесь на нас в InstagramПодпишитесь на нас в TwitterПодпишитесь на нас в LinkedInПодпишитесь на нас на YouTube
Продукты
Искусственный интеллект
Дополненная и виртуальная реальность
Инструменты для компаний
Игры
ПО с открытым исходным кодом
Размещение публикаций
Интеграция с социальными сетями
Социальное присутствие
Программы
ThreatExchange
Поддержка
Поддержка разработчиков
Ошибки
Статус платформы
Сообщить об инциденте с данными платформы
Группа сообщества Facebook for Developers
Карта сайта
Новости
Блог
Истории успеха
Видео
Страница Meta for Developers
Условия и правила
Центр инициатив для платформы
Условия использования платформы
Правила для разработчиков
Обязательства перед Европейской комиссией
© 2025 Meta
Информация
Создать рекламу
Вакансии
Политика конфиденциальности
Файлы cookie
Условия

Русский

Русский
Был ли этот документ полезен?
ДаНет
Удалить

Документы
Облачный API WhatsApp
Обзор
Облачный API WhatsApp
Обзор
Конфиденциальность и безопасность данных
Локальное хранилище
Начало работы
Начало работы: информация для партнеров по решениям
Get Started for Tech Providers
Совместные партнерские решения
Обмен сообщениями
Шаблоны
Webhooks
Calling
Блокировка пользователей
Номера телефонов
Продажа товаров и услуг
Payments API - India
Payments API - Brazil
Справка
Поддержка
Сменить язык обратно на Русский
Этот документ обновлен.
Перевод (Русский) еще не готов.
Последнее обновление (английский): Вчера
Последнее обновление (Русский): 20 июн
WhatsApp Business Platform > Cloud API

Overview
Cloud API, hosted by Meta, allows medium and large businesses to communicate with customers at scale. Using the API, businesses can build systems that connect thousands of customers with agents or bots, enabling both programmatic and manual communication. Additionally, businesses can integrate the API with numerous backend systems, such as CRM and marketing platforms.

HTTP Protocol
Cloud API is built on Graph API, so requests are expressed using the HTTP protocol and combinations of URL parameters, headers, and request bodies. For example, a common call to Cloud API from UNIX-based command line looks like this:

curl 'https://graph.facebook.com/v17.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505555555",
  "type": "text",
  "text": {
    "preview_url": true,
    "body": "Here'\''s the info you requested! https://www.meta.com/quest/quest-3/"
  }
}'
If you are unfamiliar with Graph API, refer to our Graph API documentation to learn the basics. The main differences between Graph API and Cloud API are which access token types you will commonly be using, resource permissions, request syntax, and webhooks syntax. These differences are described in further detail in appropriate sections of the Cloud API documentation set.

Resources
These are the primary resources you will be interacting with when using the API.

Business portfolios
To use the API, you must have a business portfolio. If you do not have a portfolio, you will be prompted to create one as part of our Get Started process. Business portfolios serve as a container for your WhatsApp Business Account (WABA) and business phone numbers.

To learn more about business portfolios, see our About business portfolios in Meta Business Suite help center article.

WhatsApp Business Accounts
A WhatsApp Business Account represents a business on the WhatsApp Business Platform and is composed primarily of metadata about a specific business. Most other WhatsApp resources, such as WhatsApp Business Phone Numbers and WhatsApp Message Templates are associated with a WABA.

You can create a WABA by following the steps in our Get Started document. To learn more about WABAs and their limitations, see WhatsApp Business Accounts.

WhatsApp business phone numbers
A WhatsApp Business Phone Number (business phone number) represents a real phone number, which, once registered for use with Cloud API, can be used to send and receive messages to and from WhatsApp users via the API.

Business phone numbers are composed mostly of metadata about the number itself and your business, and this metadata can be surfaced in the WhatsApp client when users interact with your business phone number.

You can create a business phone number by following the steps in our Get Started document. Note that there are restrictions and limitations on business phone numbers and their uses, which are described in detail in our Business Phone Numbers document.

WhatsApp message templates
WhatsApp Message Templates (template) are customizable templates that you can construct via the API using various template components. Once created, they are automatically reviewed, and if approved, can be used in template messages.

There are two basic types of messages that you can send via the API: free-form messages and template messages. Of the two, template messages are the most restrictive, since they require the use of an approved WhatsApp Message Template. However, since templates must undergo review and be approved before they can be used, template messages are less likely to receive negative feedback from recipients, which can jeopardize your ability to message customers entirely.

To learn more about templates, refer to our Templates document.

Webhooks
Webooks are simply JSON payloads sent using the HTTP protocol to a public endpoint on your server. Cloud API relies heavily on webhooks, as the contents of any messages sent from a WhatsApp user to your business phone number will be sent as a webhook, and all outgoing message delivery status updates are reported via webhook.

Note that we do offer a sample webhook app that you can clone on Glitch and use for testing. The app just dumps webhooks payloads directly to a console so you can see their contents. Keep in mind that you eventually need to build your own endpoint on your own server at some point which digests webhooks according to your own business logic.

See Meta Webhooks to learn more about webhooks and how to digest them, and our Webhooks for WhatsApp Business Accounts document.

Test Resources
When you first complete the steps in our Get Started document, a test WABA and test business phone number are automatically created for you.

Test WABAs and test phone numbers are useful for testing purposes, as they bypass most messaging limits and don't require a payment method on file in order to send template messages.

You can delete your business portfolio and its test resources if:

you are an admin on the business portfolio associated with the app
no other apps are associated with the business portfolio
the business portfolio is not associated with any other WABAs
the WABA is not associated with any other business phone numbers.
To delete your business portfolio and its test resources:

Go to the App Dashboard > WhatsApp > Configuration panel.
Locate the Test Account section.
Click the Delete button.
Authentication and Authorization
Access Tokens
The API supports three types of tokens:

System User Access Tokens
Business Integration System User Access Tokens
User Access Tokens
See our Access Tokens to determine which type of token you should use. Note that tokens should be passed via request headers, not as a query string parameter.

Permissions
The API relies on the following Graph API permissions. The exact combination of permissions your app needs depends on which endpoints your app will be accessing.

business_management — needed if interacting with a business portfolio.
whatsapp_business_management — needed if interacting with a WABA and its analytics, or any of its templates or business phone numbers.
whatsapp_business_messaging — needed to send and receive messages to and from WhatsApp users.
These permissions are typically granted when generating access tokens in the Meta Business Suite. See the token generation sections in our Access Tokens document.

Versioning
Versioning uses Graph API's versioning protocol. This means that all endpoint requests can include a version number, and each version will be available for roughly 2 years before it will be retired and can no longer be called.

Throughput
For each registered business phone number, Cloud API supports up to 80 messages per second (mps) by default, and up to 1,000 mps by automatic upgrade.

Throughput is inclusive of inbound and outbound messages and all message types. Note that business phone numbers, regardless of throughput, are still subject to their WhatsApp Business Account's business use case rate limit and template messaging limits.

If you attempt to send more messages than your current throughput level allows, the API will return error code 130429 until you are within your allowed level again. Also, throughput levels are intended for messaging campaigns involving different WhatsApp user phone numbers. If you attempt to send too many messages to the same WhatsApp user number, you may encounter a pair rate limit error.

WhatsApp Business app phone numbers
In order to remain compatible with the WhatsApp Business app, business phone numbers that are in use with both the WhatsApp Business app and Cloud API ("coexistence numbers") have a fixed throughput of 5 mps.

Higher Throughput
If you meet our eligibility requirements, we will automatically upgrade your business phone number to 1,000 mps at no cost to you. Higher throughput does not incur additional charges or affect pricing.

The upgrade process itself can take up to 1 minute. During this time the number will not be usable on our platform. If used in an API request, the API will return error code 131057. Once a business phone number has been upgraded, it will automatically be upgraded for any future throughput increases with no downtime.

Once your number is upgraded to higher throughput, a phone_number_quality_update webhook will be triggered with event set to THROUGHPUT_UPGRADE and current_limit set to TIER_UNLIMITED.

Eligibility Requirements
The business phone number must be able to initiate an unlimited number of messages in a rolling 24-hour period.
The business phone number must be registered for use with Cloud API. If the number is registered for use with On-Premises API, it must be migrated to Cloud API first.
The business phone number must have a Medium quality rating or higher.
Webhooks
Your webhook servers should be able to withstand 3x the capacity of outgoing message traffic and 1x the capacity of expected incoming message traffic. For example, if sending 1,000 mps with a 30% expected response rate, your servers should be able to process up to 3000 message status webhooks plus an additional 300 incoming message webhooks.

We attempt to deliver webhooks concurrently, so we recommend you configure and load test your webhook server to handle concurrent requests with the following latency standard:

Median latency not to exceed 250ms.
Less than 1% latency exceeds 1s.
We will attempt to re-deliver failed webhooks for up to 7 days, with exponential backoff.

Media Messages
To take full advantage of higher throughput, we recommend that you upload your media assets to our servers and use the returned media IDs, instead of hosting the assets on your own servers and using media asset URLs, when [sending messages](/docs/whatsapp/cloud-api/guides/send-messages that include a media asset. If you prefer (or must) host the assets on your own servers, we recommend that you use media caching.

Getting Throughput Level
Use the WhatsApp Business Phone Number endpoint to get a phone number's current throughput level:

GET /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>?fields=throughput
Migration
If you migrate a business phone number that has multiconnect running 2 or more shards from On-Premises API to Cloud API, it will automatically be upgraded to higher throughput.

Rate Limits
See WhatsApp Business Management API rate limits.

In addition to these rate limits, we have more granular limits on individual resources such as template messages and test business phone numbers:

Test message rate limit: Applies to unverified WABAs.
Quality rating and messaging limits: Applies to verified WABAs.
Capacity rate limit: Applies to all accounts.
Business phone rate limit: Applies to all accounts and limits the throughput per business phone number.
Available Metrics
As a Cloud API user, you can see the number of messages sent and delivered, as well as other metrics. See Get Account Metrics for information.

Scaling
Within Meta's infrastructure, the Cloud API automatically scales and adjusts to handle your workload, within your rate limit (messaging volume and number of WABAs).

Data Privacy & Security
See our Privacy & Security Overview for information.

Encryption
With the Cloud API, every WhatsApp message continues to be protected by Signal protocol encryption that secures messages before they leave the device. This means messages with a WABA are securely delivered to the destination chosen by each business.

The Cloud API uses industry standard encryption techniques to protect data in transit and at rest. The API uses Graph API for sending messages and Webhooks for receiving events, and both operate over industry standard HTTPS, protected by TLS. See our Encryption Overview whitepaper for additional details.

See our Encryption Overview whitepaper for additional details.

Pair Rate Limits
Business phone numbers are limited to sending 1 message every 6 seconds to the same WhatsApp user phone number (0.17 messages/second). This is roughly equivalent to 10 messages per minute, or 600 messages per hour. If you exceed this limit, the API will return error code 131056 until you are within your limit again.

If necessary, you can send up to 45 messages within 6 seconds as a burst. If you send a burst, you are essentially borrowing against your pair rate limit, so you will be prevented from sending subsequent messages to the same user until the amount of time it would normally take to send that many "non-burst" messages to the user has passed. For example, it takes ~2 minutes to send 20 "non-burst" messages to a user, so if you send a burst of 20, you will have to wait ~2 minutes before you can send another message to the user.

To avoid having to calculate post-burst message wait times, we recommend that if a message send request fails after sending a burst, you try again 4^X seconds later, where X = 0, and increases by 1 after each failed attempt, until the request succeeds.

Tools
WhatsApp Manager
The WhatsApp Manager is our web app that allows you to manually manage WhatsApp resources, such as WABAs, business phone numbers, and templates, and provides an easy way to see insights and quality ratings or limits on these resources. Most functionality offered by the WhatsApp Manager is also available via the API, with a few minor exceptions.

There are several ways to access the WhatsApp Manager. Each path assumes you have already completed all steps in our Get Started document.

Via the Meta Business Suite
Log into the Meta Business Suite.
If you have multiple business portfolios, use the dropdown menu on the left to select the account that owns, or has access to, the WABA you wish to load in the WhatsApp Manager.
In the menu on the left, navigate to Accounts > WhatsApp Accounts.
Select the WABA.
In the Summary tab, click the WhatsApp Manager button.
Via the App Dashboard
Go to My Apps.
Select the app that is associated with the WABA you want to load in the WhatsApp Manager.
In the menu on the left, navigate to WhatsApp > Quickstart.
Click the Account information tile in the WhatsApp Business section.
Via URL
You can go directly to the WhatsApp Manager Overview, which displays all of the WABAs owned by, or shared with, a given business portfolio, by visiting:

https://business.facebook.com/wa/manage/home/

By default, the overview loads the most recent WABA you created or were granted access to, but you can use the dropdown menu on the left to select the business portfolio that contains the WABA you are trying to access . This will take you out of the overview, however, and you must then use the menu on the left and navigate to Accounts > WhatsApp Accounts > (select the desired WABA) > Settings > WhatsApp Manager (button).

Alternatively, if you have multiple business portfolios, you can append an account's ID to the end of the URL and bookmark it for easier access:

https://business.facebook.com/wa/manage/home/?business_id=<META_BUSINESS_ACCOUNT_ID>

Third-party SDKs
The following third-party SDKs are not affiliated with, nor maintained by, Meta.

PyWa — a Python wrapper for WhatsApp Cloud API
Postman
We have a Cloud API Postman collection containing common queries in our WhatsApp Business Platform workspace.

Платформа WhatsApp Business | Облачный API  | API Business Management

Мы в социальных сетях
Подпишитесь на нас на FacebookПодпишитесь на нас в InstagramПодпишитесь на нас в TwitterПодпишитесь на нас в LinkedInПодпишитесь на нас на YouTube
Продукты
Искусственный интеллект
Дополненная и виртуальная реальность
Инструменты для компаний
Игры
ПО с открытым исходным кодом
Размещение публикаций
Интеграция с социальными сетями
Социальное присутствие
Программы
ThreatExchange
Поддержка
Поддержка разработчиков
Ошибки
Статус платформы
Сообщить об инциденте с данными платформы
Группа сообщества Facebook for Developers
Карта сайта
Новости
Блог
Истории успеха
Видео
Страница Meta for Developers
Условия и правила
Центр инициатив для платформы
Условия использования платформы
Правила для разработчиков
Обязательства перед Европейской комиссией
© 2025 Meta
Информация
Создать рекламу
Вакансии
Политика конфиденциальности
Файлы cookie
Условия

Русский

Русский
Был ли этот документ полезен?
ДаНет
Удалить
Документы
Облачный API WhatsApp
Начало работы
Облачный API WhatsApp
Обзор
Начало работы
Add a Phone Number
Migrate an Existing WhatsApp Number to a Business Account
Начало работы: информация для партнеров по решениям
Get Started for Tech Providers
Совместные партнерские решения
Обмен сообщениями
Шаблоны
Webhooks
Calling
Блокировка пользователей
Номера телефонов
Продажа товаров и услуг
Payments API - India
Payments API - Brazil
Справка
Поддержка
Платформа WhatsApp Business > Облачный API

Начало работы
Это руководство поможет вам отправить и получить первое сообщение с использованием облачного API. Вы также узнаете, как настраивать Webhooks для использования с примером приложения.

Это руководство предназначено для людей, которые разрабатывают приложения для себя или для своей организации. Если вы разрабатываете приложение, которое будет использоваться другими компаниями, обратитесь к статье Поставщики решений.

Прежде чем начать
Вам понадобятся:

Аккаунт разработчика Meta (подробнее о регистрации в качестве разработчика Meta).
Приложение для бизнеса (подробнее о создании приложений). Если вы не видите опции для создания приложения для бизнеса, выберите Другие > Далее > Бизнес.
Шаг 1. Добавление продукта WhatsApp в приложение
Если вы создали новое приложение, вам будет предложено добавить в него продукты. Прокрутите вниз и в разделе WhatsApp выберите Настроить. Можно также выбрать приложение на панели Мои приложения, а затем добавить продукт WhatsApp в приложение, следуя тем же инструкциям.

Если у вас уже есть бизнес-портфолио, вам будет предложено его прикрепить. Если же у вас нет бизнес-портфолио, вы увидите инструкции, которые помогут его создать и прикрепить.

При добавлении продукта WhatsApp в приложение и прикреплении бизнес-портфолио происходит следующее:

Создается тестовый аккаунт WhatsApp Business, который можно использовать для отправки себе бесплатных тестовых сообщений.
Создается тестовый номер телефона компании. Он связывается с вашим аккаунтом WhatsApp Business, и вы можете использовать его для отправки бесплатных сообщений на 5 номеров телефонов получателей.
Создается уже утвержденный шаблон "hello world".
Шаг 2. Генерация маркера доступа
В панели приложений слева выберите WhatsApp > Настройка API и нажмите синюю кнопку Сгенерировать маркер доступа. Выполните необходимые действия, чтобы сгенерировать маркер доступа пользователя. Обычно для работы используется системный маркер или маркер компании, но для выполнения этих действий достаточно маркера доступа пользователя.

Шаг 3. Добавление номера получателя
Добавьте действительный номер WhatsApp, на который вы сможете отправить тестовые сообщения. В разделе Отправка и получение сообщений выберите поле Кому, а затем — Управление списком номеров телефонов.

В качестве получателя можно добавить любой действительный номер WhatsApp. На выбранный номер получателя в WhatsApp будет отправлен код подтверждения, предназначенный для проверки номера.

После проверки номера получателя его следует выбрать в поле Кому. Повторите эти действия, если необходимо добавить ещё одного получателя (всего не более 5).

Шаг 4. Отправка тестового сообщения
Используя предварительно утвержденный шаблон hello_world, отправьте сообщение на выбранный номер получателя.

На панели WhatsApp > Настройка API:

Убедитесь, что в поле От указан тестовый номер телефона вашей компании.
Убедитесь, что в поле Кому указан номер телефона получателя, на который нужно отправить сообщение. Если вы указали несколько номеров, можно одновременно отправить несколько сообщений.
На панели Отправка сообщений с помощью API нажмите кнопку Отправить сообщение.
Либо вы можете скопировать команду cURL, затем вставить ее в новое окно терминала и выполнить.

Обратите внимание: этот код указывает, что вы отправляете сообщение с шаблоном (”type”:”template”) и используете конкретный шаблон (”name”:”hello_world”).

Шаг 5. Клонирование нашего примера приложения и настройка Webhooks
Webhooks позволяют в режиме реального времени получать уведомления HTTP об изменениях определенных объектов. В WhatsApp вы можете получать уведомления Webhooks о разных событиях в вашем приложении, таких как доставка или прочтение сообщения, и даже об изменениях в аккаунте.

Для просмотра контента Webhooks добавьте URL обратного вызова. Следуйте нашему руководству Тестовый URL обратного вызова для тестирования Webhooks, чтобы клонировать наш пример приложения, которое принимает уведомления Webhooks и отображает содержащиеся в них полезные данные в формате JSON на экране.

После настройки Webhooks повторно отправьте сообщение с шаблоном, а затем ответьте на него. Вы должны увидеть четыре отдельных уведомления Webhooks: сообщение отправлено, доставлено и прочитано, а также контент входящего сообщения.

Шаг 6. Добавление настоящего номера компании (необязательно)
Имея тестовый номер компании и тестовый аккаунт WhatsApp Business, вы можете начинать разработку приложения. Используя эти тестовые компоненты, вы не платите за отправку сообщений, поскольку занимаетесь разработкой своего приложения.

Как только всё будет готово к отправке сообщений клиентам, вы сможете добавить настоящий номер компании на панели Настройка API и создать настоящий аккаунт WhatsApp Business.

Дальнейшие действия
Информация о маркерах доступа и системных пользователях
Информация о шаблонах сообщений
Платформа WhatsApp Business | Облачный API  | API Business Management

Мы в социальных сетях
Подпишитесь на нас на FacebookПодпишитесь на нас в InstagramПодпишитесь на нас в TwitterПодпишитесь на нас в LinkedInПодпишитесь на нас на YouTube
Продукты
Искусственный интеллект
Дополненная и виртуальная реальность
Инструменты для компаний
Игры
ПО с открытым исходным кодом
Размещение публикаций
Интеграция с социальными сетями
Социальное присутствие
Программы
ThreatExchange
Поддержка
Поддержка разработчиков
Ошибки
Статус платформы
Сообщить об инциденте с данными платформы
Группа сообщества Facebook for Developers
Карта сайта
Новости
Блог
Истории успеха
Видео
Страница Meta for Developers
Условия и правила
Центр инициатив для платформы
Условия использования платформы
Правила для разработчиков
Обязательства перед Европейской комиссией
© 2025 Meta
Информация
Создать рекламу
Вакансии
Политика конфиденциальности
Файлы cookie
Условия

Русский

Русский
Был ли этот документ полезен?
ДаНет
Удалить
Документы
Платформа WhatsApp Business
Solution Providers
Become a Solution Partner
Платформа WhatsApp Business
О платформе
Упразднение локального API
Cloud vs On-Prem
Номера телефонов
Сообщения
Расценки
Оценка качества и ограничения числа обращений
Webhooks
Solution Providers
Become a Solution Partner
Become a Tech Provider
Measurement Partners
Become a Tech Provider (Legacy Flow)
Upgrade to Tech Partner
Multi-Partner Solutions
MPS Embedded Creation
Partner-led Business Verification
Partner-initiated WABA creation
Поддержка
Регистрация на сайте поставщика
Link Previews
Обеспечение соблюдения политик
Журнал изменений
Поддержка
Платформа WhatsApp Business > Облачный API

Get Started as a Solution Partner
This guide goes over the steps Solution Partners need to take in order to offer the Cloud API to their customers. There are 4 main stages:

Prepare & Plan
Set up Assets
Sign Contracts
Build Integration
After you’re done, please keep up with monthly updates.

Prepare & Plan
Read Documentation
Before you start, we recommend reading through our developer documentation and our Postman collection. This helps you understand how the Cloud API works, including how to get started and migrate numbers.

Plan Onboarding & Migration
You must use Embedded Signup to onboard new customers to the Cloud API. If you haven’t already, integrate and launch Embedded Signup. Embedded Signup is the fastest and easiest way to register customers, enabling them to start sending messages in less than five minutes.

Next, think about which clients you want to migrate to the Cloud API first. Our general recommendation is to migrate all of your clients from the On-Premises to the Cloud API, but each client’s need may vary. As you think about which clients to migrate, consider:

Consideration	More Context
Are my client’s throughputs and message volumes supported by Cloud API?

The Cloud API supports most businesses at 250 messages/second cumulative peak throughput, including text/media and incoming/outgoing.

Are my client’s compliance needs met by the Cloud API?

The Cloud API is GDPR compliant and has SOC 2 certification. Servers are hosted in North America and Europe.

Are my clients using features supported by the Cloud API?

Most major features are supported. See full list here.

Once you know who’s going to be migrated, you can build a migration plan and timeline.

As you create your plan, remember to design your system for two scenarios: onboarding new customers and migrating current customers from On-Premises to Cloud API. For the migration scenario, include plans to backup your current On-Premises instance and migrate those numbers to the Cloud API.

Plan Communication With Clients
First, you need to decide whether to notify existing clients about migration. Then, you should determine if you need to create or update any documentation to support the Cloud API setup.

Make Pricing Decisions
Since the hosting costs for the Cloud API are covered by Meta, you should decide if you would like to update your prices accordingly.

Set up Assets
To use the Cloud API, Solution Partners need to have the following assets:

Asset	Specific Instructions
Business Manager

You can use an existing, or set up a new one. Save the Business Manager ID.

WhatsApp Business Account (WABA)

See Create a WhatsApp Business Account for the WhatsApp Business API for help.

Meta App

If you don’t have an app, you need to create one with the “Business” type. Remember to add a display name and a contact email to your app.


As a (Solution Partner), your app must go through App Review and request Advanced Access to the following permissions:

whatsapp_business_management — Used to manage phone numbers, message templates, registration, business profile under a WhatsApp Business Account. To get this permission, your app must go through App Review.
whatsapp_business_messaging — Used to send/receive messages from WhatsApp users, upload/download media under a WhatsApp Business Account. To get this permission, your app must go through App Review.
See a sample App Review submission here.


As a Solution Partner, you can also feel free to use the same Meta app across different clients and WABAs. But be aware that each app can only have one webhook endpoint and each app needs to go through App Review.

System User

See Add System Users to Your Business Manager for help.


Currently, a Meta App with whatsapp_business_messaging, whatsapp_business_management, and business_messaging permissions has access to up to:

1 admin system user, and
1 employee system user
We recommend using the admin system user for your production deployment. See About Business Manager Roles and Permissions for more information.

Business Phone Number

This is the phone number the business will use to send messages. Phone numbers need to be verified through SMS/voice call.


For Solution Partners and Direct Businesses: If you wish to use your own number, then you should add a phone number in WhatsApp Manager and verify it with the verify endpoint via Graph API.


For businesses using Solution Partners: If you wish to use your own number, then you should add and verify their numbers using the Solution Partner's Embedded Signup flow.


Статус подтверждения номера телефона не влияет на процесс миграции между локальным и облачным API. Если у вас нет доступа к регистрации на сайте поставщика, чтобы подтвердить номера телефонов, рекомендуем подтвердить их с использованием локального решения, а затем перенести эти номера в облачный API.

There is no limit to the amount of business phone numbers that can be onboarded to the Cloud API.


На одной платформе может одновременно использоваться только один номер телефона: один номер для облачного API и другой номер для локального API. Это означает, что вы не можете использовать рабочий номер телефона одновременно с локальными и с облачными API. Рекомендуем для всех проверок использовать тестовый номер (будь то уже имеющийся или новый), а затем зарегистрировать свой личный номер телефона с облачным API, когда вы поймете, что готовы перейти к его рабочему использованию.
Consumer Phone Number

This is a phone number that is currently using the consumer WhatsApp app. This number will be receiving the messages sent by your business phone number.

Sign Contracts
Accepting Terms of Service
In order to access the WhatsApp Business Messaging Cloud API you need to first accept the WhatsApp Business Platform Terms of Service on behalf of your business.

To do so, navigate to WhatsApp Manager and accept the terms of service in the informational banner.


For any new Cloud API businesses, including those migrating from the on-premises API, you will need to accept terms of service before you can start using the Cloud API. Registration calls will fail until you accept the terms of service.

You as a developer need to accept the terms of service. If you are a Solution Partner, you do not need your customers to accept.

Build Integration
Step 1: Get System User Access Token
Graph API calls use access tokens for authentication. For more information, see Access Tokens. We recommend using your system user to generate your token.

To generate a system user access token:

Go to Business Manager > Business Settings > Users > System Users to view the system user you created.
Click on that user and select Add Assets. This action launches a new window.
Under Select Asset Type on the left side pane, select Apps. Under Select Assets, choose the Meta app you want to use (your app must have the correct permissions). Enable Develop App for that app.
Select Save Changes to save your settings and return to the system user main screen.
Now you are ready to generate your token. In the system user main screen, click Generate Token and select your Meta app. After selecting the app, you see a list of available permissions. Select whatsapp_business_management and whatsapp_business_messaging. Click Generate Token.
A new window opens with your system user, assigned app and access token. Save your token.
Optionally, you can click on your token and see the Token Debugger. In your debugger, you should see the two permissions you have selected. You can also directly paste your token into the Access Token Debugger.
Step 2: Set up Webhooks
With Webhooks set up, you can receive real-time HTTP notifications from the WhatsApp Business Platform. This means you get notified when, for example, you get a message from a customer or there are changes to your WhatsApp Business Account (WABA).

To set up your Webhook, you need to create an internet-facing web server with a URL that meets Meta’s and WhatsApp’s requirements. See Creating an Endpoint for instructions on how to do that. If you need an endpoint for testing purposes, you can generate a test Webhooks endpoint.

App Setup
Once the endpoint is ready, configure it to be used by your Meta app:

На Панели приложений найдите продукт WhatsApp и нажмите Конфигурация. Найдите раздел Webhooks и нажмите Настроить Webhook. Откроется окно с запросом на ввод двух параметров:

URL обратного вызова: это URL, на который Meta будет отправлять события. Информацию о создании этого URL см. в руководстве по началу работы с Webhooks.
Маркер подтверждения: эта строка указывается вами при создании конечной точки Webhooks.
После добавления информации нажмите Подтвердить и сохранить.

Снова перейдите на Панель приложений и нажмите WhatsApp > Конфигурация на панели слева. В разделе Webhooks нажмите Настроить. Отобразится окно со всеми объектами, о которых можно получать уведомления. Чтобы получать сообщения от своих пользователей, нажмите Подписаться для сообщений.

You only need to set up Webhooks once for every application you have. You can use the same Webhook to receive multiple event types from multiple WhatsApp Business Accounts. For more information, see our Webhooks section.

Для каждого приложения Meta может быть одновременно настроена только одна конечная точка. Если вам нужно отправлять обновления Webhooks на разные конечные точки, создайте несколько приложений Meta.

Step 3: Subscribe to your WABA
To make sure you get notifications for the correct account, subscribe your app:

curl -X POST \
'https://graph.facebook.com/v23.0/WHATSAPP_BUSINESS_ACCOUNT_ID/subscribed_apps' \
-H 'Authorization: Bearer ACCESS_TOKEN'
If you get the response below, all Webhook events for the phone numbers under this account will be sent to your configured Webhooks endpoint.

{
  "success": true
}
Step 4: Get Phone Number ID
To send messages, you need to register the phone number you want to use. Before you can register it, you need to get the phone number’s ID. To get your phone number’s ID, make the following API call:

curl -X GET \
'https://graph.facebook.com/v23.0/WHATSAPP_BUSINESS_ACCOUNT_ID/phone_numbers' \
-H 'Authorization: Bearer ACCESS_TOKEN'
If the request is successful, the response includes all phone numbers connected to your WABA:

{
  "data": [
    {
      "verified_name": "Jasper's Market",
      "display_phone_number": "+1 631-555-5555",
      "id": "1906385232743451",
      "quality_rating": "GREEN"
    },
    {
      "verified_name": "Jasper's Ice Cream",
      "display_phone_number": "+1 631-555-5556",
      "id": "1913623884432103",
      "quality_rating": "NA"
    }
  ]
}
Save the ID for the phone number you want to register. See Read Phone Numbers for more information about this endpoint.

Migration Exception
Если вы переводите номер телефона из локального API в облачный, вам потребуется выполнить дополнительные шаги перед его регистрацией. Полный процесс см. в статье Перевод из локального API в облачный.

Step 5: Register Phone Number
With the phone number’s ID in hand, you can register it. In the registration API call, you perform two actions at the same time:

Register the phone.
Enable two-step verification by setting a 6-digit registration code —you must set this code on your end. Save and memorize this code as it can be requested later.
Setting up two-factor authentication is a requirement to use the Cloud API. If you do not set it up, you will get an onboarding failure message:


Sample request:

curl -X POST \
'https://graph.facebook.com/v23.0/FROM_PHONE_NUMBER_ID/register' \
-H 'Authorization: Bearer ACCESS_TOKEN' \
-H 'Content-Type: application/json' \
-d '{"messaging_product": "whatsapp","pin": "6_DIGIT_PIN"}'
Sample response:

{
  "success": true
}
Embedded Signup Users
Номер телефона должен быть зарегистрирован в течение 14 дней после прохождения процесса встроенной регистрации на сайте поставщика. Если в течение этого периода времени номер не будет зарегистрирован, то перед регистрацией этого номера телефона для него необходимо будет снова выполнить процедуру встроенной регистрации на сайте поставщика.

Step 6: Receive a Message From Consumer App
Once participating customers send a message to your business, you get 24 hours of free messages with them —that window of time is called the customer service window. For testing purposes, we want to enable this window, so you can send as many messages as you would like.

From a personal WhatsApp iOS/Android app, send a message to the phone number you just registered. Once the message is sent, you should receive an incoming message to your Webhook with a notification in the following format.

{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "16315551234",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Kerry Fisher"
                },
                "wa_id": "16315555555"
              }
            ],
            "messages": [
              {
                "from": "16315555555",
                "id": "wamid.ABGGFlA5FpafAgo6tHcNmNjXmuSf",
                "timestamp": "1602139392",
                "text": {
                  "body": "Hello!"
                },
                "type": "text"
                }
            ]
          },
        "field": "messages"
        }
      ]
    }
  ]
}
Step 7: Send a Test Message
Once you have enabled the customer service window, you can send a test message to the consumer number you used in the previous step. To do that, make the following API call:

curl -X  POST \
'https://graph.facebook.com/v23.0/FROM_PHONE_NUMBER_ID/messages' \
-H 'Authorization: Bearer ACCESS_TOKEN' \
-H 'Content-Type: application/json' \
-d '{"messaging_product": "whatsapp", "to": "16315555555","text": {"body" : "hello world!"}}'
If your call is successful, your response will include a message ID. Use that ID to track the progress of your messages through Webhooks. The maximum length of the ID is 128 characters.

Sample response:

{
  "id":"wamid.gBGGFlaCGg0xcvAdgmZ9plHrf2Mh-o"
}
При использовании облачного API больше нет способа четко проверить, имеет ли тот или иной номер телефона ID WhatsApp. Чтобы отправить сообщение с использованием облачного API, просто отправьте его напрямую на номер телефона клиента — после того, как он согласился их принимать. Примеры см. в статье Справка, Сообщения.

Keep up with Monthly Updates
We will release Cloud API updates on the first Tuesday of every month. Those will include new features and improvements. You don’t need to do any work to use any of the new features, since the Cloud API updates automatically.

FAQs
General FAQs
Which company will be providing the Cloud API?
Are there any additional costs for the Cloud API?
Will consumers know whether a business is using the Cloud API or the On-Premises API?
Does the introduction of Cloud API mean WhatsApp is deprecating the existing On-Premises API?
Technical Implementation FAQs
What is the architecture of the Cloud API?
Will the Solution Partner or direct client need containers and what data will be in those containers?
What will disaster recovery look like: if a region is unavailable, how much time does it take to move messages to another region?
How does WhatsApp recommend I conduct load tests for the Cloud API?
Data Privacy & Security FAQs
Где находятся серверы Cloud API?
Защищен ли Cloud API сквозным шифрованием? Что такое модель шифрования?
Что происходит с данными сообщений при хранении? Как долго они хранятся?
Есть ли у Meta доступ к ключам шифрования?
Regulatory Compliance FAQs
Как Cloud API соблюдает требования региональных законов о защите данных (например, Общего регламента по защите данных, Закона Бразилии о защите данных и Закона Индии о защите цифровых персональных данных)?
Платформа WhatsApp Business | Облачный API  | API Business Management

Мы в социальных сетях
Подпишитесь на нас на FacebookПодпишитесь на нас в InstagramПодпишитесь на нас в TwitterПодпишитесь на нас в LinkedInПодпишитесь на нас на YouTube
Продукты
Искусственный интеллект
Дополненная и виртуальная реальность
Инструменты для компаний
Игры
ПО с открытым исходным кодом
Размещение публикаций
Интеграция с социальными сетями
Социальное присутствие
Программы
ThreatExchange
Поддержка
Поддержка разработчиков
Ошибки
Статус платформы
Сообщить об инциденте с данными платформы
Группа сообщества Facebook for Developers
Карта сайта
Новости
Блог
Истории успеха
Видео
Страница Meta for Developers
Условия и правила
Центр инициатив для платформы
Условия использования платформы
Правила для разработчиков
Обязательства перед Европейской комиссией
© 2025 Meta
Информация
Создать рекламу
Вакансии
Политика конфиденциальности
Файлы cookie
Условия

Русский

Русский
Был ли этот документ полезен?
ДаНет
Удалить
Документы
Платформа WhatsApp Business
Solution Providers
Become a Tech Provider
Платформа WhatsApp Business
О платформе
Упразднение локального API
Cloud vs On-Prem
Номера телефонов
Сообщения
Расценки
Оценка качества и ограничения числа обращений
Webhooks
Solution Providers
Become a Solution Partner
Become a Tech Provider
Measurement Partners
Become a Tech Provider (Legacy Flow)
Upgrade to Tech Partner
Multi-Partner Solutions
MPS Embedded Creation
Partner-led Business Verification
Partner-initiated WABA creation
Поддержка
Регистрация на сайте поставщика
Link Previews
Обеспечение соблюдения политик
Журнал изменений
Поддержка
Become a Tech Provider
This document describes the steps you must take to become a Tech Provider. Once you complete these steps, you can begin onboarding business customers onto the WhatsApp Business Platform, and access their WhatsApp data using our various APIs.

As a Tech Provider, you can independently provide all WhatsApp messaging services to business customers who you have onboarded, or you can work with a Solution Partner to jointly offer these services. If you are partnering with a Solution Partner, ask them for their app ID, as you will need it to complete these steps.

Step 1: Create a business portfolio
If you already have a business portfolio, you can skip this step.

Go to business.facebook.com and create a Meta Business Suite account using your Facebook credentials. This will generate a business portfolio, which will serve as a container for any WhatsApp related assets you will be creating later.

Step 2: Register as a Meta developer
If you are already registered as a Meta developer, you can skip this step.

Go to developers.facebook.com and click Get Started (upper-right corner) and complete the registration flow. This will convert your Facebook account to a Meta developer account, which is necessary for app creation.

Step 3: Create an app
Go to developers.facebook.com/apps and create a new Business app, which will generate your Meta app ID. If you are signed into your Meta Business Suite account, the app creation flow will present you with a list of existing business portfolios you have already created, or have been added to:


If you are not presented with a list of businesses, go to business.facebook.com and sign into your Meta Business Suite account, then reload developers.facebook.com/apps.

Select your business portfolio and continue. In the next screen, select Other, then Business app, and add an app name and your email address. Be sure to select your business portfolio in the Business portfolio dropdown menu before creating your app.


Step 4: Add basic data about your app
In the App Dashboard, navigate to App settings > Basic and add the following information:

App icon
Privacy Policy URL
Category
Platform
Be sure to save your changes. You can add additional information if you wish, but the information above is the only information required to complete the remaining steps.

Step 5: Add the WhatsApp product
In the App Dashboard panel, scroll down to Add products to your app, locate the WhatsApp product, and click its Set Up button.


Complete the flow until you are presented with the Quickstart panel:


Step 6: Indicate how you will work with customers
In the Quickstart panel, locate the Become a Tech Provider section and click the Start onboarding button:


Work through the flow until you are asked to choose between Independent Tech Provider and Working with a Solution Partner:


Choose the option (described below) that best matches how you will be working with your onboarded business customers. After making your choice and continuing, you will be taken to the Quickstart > Onboarding panel.

Note that by clicking the Start onboarding button, you are agreeing to our Tech Provider Terms.

Independent Tech Provider
Choose this option if you will be onboarding business customers onto the WhatsApp Business Platform and providing them with WhatsApp messaging services entirely on your own (i.e., without the help of another solution provider).

Note that choosing this option does not prevent you from partnering with other Solution Partners in the future, it just skips part of the setup process; you can always partner with a Solution Partner at a later date.

Working with a Solution Partner
Choose this option if you are partnering with a Solution Partner in order to provide WhatsApp messaging services to business customers, who can be onboarded by you or the Solution Partner. You must know your Solution Partner's app ID if you choose this option, as you will need it in a later step.

Note that choosing this option does not prevent you from terminating your partnership with the Solution Partner in the future; you can always switch Solution Partners or operate independently at a later date.

Step 6: Verify your business
If your business is already verified, (the Verify your business row has a green checkmark and a green Approved dropdown menu label) you can skip this step.

Before you can complete the remaining steps, your business must be verified and approved. In the Quickstart > Onboarding panel, click the Start verification button.


Complete the flow and submit your business for verification. As part of the verification process, you will be asked to provide information about your business. See our How to verify your business on Meta help center article, which lists all of the information you may be asked to provide.

The verification process can take several days. The article linked above describes the process in more detail, as well as how outcomes are communicated.

The Business Verification section of the Quickstart > Onboarding panel will also be updated once you submit for verification, indicating if the submission is still in progress or if your business has been verified.

You can also see your business's verification status in the Meta Business Suite > Business information panel:

https://business.facebook.com/settings/info

Step 7: Create or Choose a Multi-Partner solution
Skip this step if you chose Independent Tech Provider in step 5.

In the Quickstart > Onboarding panel, locate the App Review section and the Create a partner solution row:


Note that if you already have a solution associated with this app, you will see a Choose solution button instead. Click the button and select an existing solution to complete this step.

If you see the Create a partner solution button, click it to display the solution creation window:


Enter a name for the partner solution and add the Solution Partner's app ID. Use a name that will help you distinguish the solution from other solutions you may create in the future. Note that only Solution Partner app IDs will be accepted; Tech Provider app IDs will be rejected.

Once your solution has been created it will appear in the Create a partner solution row with a Pending Acceptance status. You can proceed to the next steps while it is in a pending state.

Step 7: Review app settings
In the Quickstart > Onboarding panel, locate the Review your app settings row and click the Review app settings button:


In the interface that appears, confirm that the information you supplied in step 4 is still accurate, and update if necessary.

Step 8: Capture videos for App Review
In the Quickstart > Onboarding panel, locate the Record video documentation row.


As part of the App Review process you will be asked to provide two video recordings:

The first video must show a message created and sent from your app and received in the WhatsApp client (mobile app or web app).
The second video must show your app being used to create a message template.
If you are partnering with a Solution Partner, you can use your current integration with them to show these actions.

Clicking the Record video buttons in the panel will display helpful information for creating these videos (the buttons don't actually capture any video, you must do this on your own).

As an alternative, you can capture a screen recording of the API Setup cURL script being used by you to send a message to a WhatsApp user number you have added as a test recipient number, in lieu of sending a message using your or your partner's app. Similarly, you can capture a screen recording of the WhatsApp Manager being used by you to create a template message, instead of your or your partner's app.

Whichever method you decide upon to generate your videos or screen recordings, save the recordings for the next step.

Step 8: Submit for App Review
In the Quickstart > Onboarding panel, locate the Submit documentation for App Review row and click the Begin App Review button. This flow will load the App Review > Requests panel, where you should see an app review request ready for you to edit:


Click the Edit button to access the App Review flow. As part of this process, you will be asked to explain how your, or your Solution Partner's app, uses your business customer's data, and why your app needs advanced access for the whatsapp_business_messaging and whatsapp_business_management permissions.

When describing how your app uses each of these permissions, attach the appropriate screen recording or video you created in the previous step:

For whatsapp_business_messaging, attach the screen recording or video showing a message being sent with your or your Solution Partner's app and appearing in the WhatsApp client, or the screen recording of the API Setup cURL script being used by you.
For whatsapp_business_management, attach the screen recording or video showing your or your Solution Partner's app being used to create a message template, or the screen recording of the WhatsApp Manager being used by you to create a message template.
Important: For the App verification details dialog, when your app review submission only involves whatsapp_business_messaging and/or whatsapp_business_management you do not need to provide the testing instructions. For e.g:


Complete the flow and submit your request. Outcomes will be communicated via email, developer alert, and its status will be updated in the App Review > Requests panel.

Step 9: Complete Access Verification
In the Quickstart > Onboarding panel, locate the Complete access verification row and click the Start verification button.


This flow gathers basic information about your business in order to verify that it qualifies as a Tech Provider.

Complete the flow and submit for verification.

Step 10: Confirm status
After you have completed the steps above, the Quickstart > Onboarding panel should indicate that all steps are complete (with a green checkmark) and and congratulate you on your status as a Tech Provider:


Next Steps
Onboarding Business Customers
Once you have confirmed your status as a Tech Provider, you can begin onboarding business customers via Embedded Signup.

If you are working as an independent tech provider, you must implement Embedded Signup and surface it to potential customers on your own. See our Embedded Signup document to learn how to implement and test with a sandbox account, and how to use the data that Embedded Signup generates to onboard business customers.

If you are working with a Solution Partner, your partner can implement Embedded Singup to onboard business customers for you. However, if you also want to surface Embedded Signup somewhere on your website or customer portal and onboard business customers, you can do so, but it will require a Multi-Partner Solution. Work with your Solution Partner if you are choosing this option.

Webhooks
If you are working as an independent tech provider, before your app users can use your app to send and receive messages or manage templates, you must set up Webhooks.

If you are working with a solution partner who has already set up webhooks, work with your partner to determine if you need to set up webhooks as well.

Billing
If you are partnering with a Solution Partner, your partner will share their line of credit with onboarded business customers.

If you are working independently, your onboarded business customers must add a payment method to their WhatsApp Business Account. They can do this by following the steps described in our Add a credit card to your WhatsApp Business Platform account help center article.

Support
Confirmed Tech Providers have access to all support channels. See Support.


Мы в социальных сетях
Подпишитесь на нас на FacebookПодпишитесь на нас в InstagramПодпишитесь на нас в TwitterПодпишитесь на нас в LinkedInПодпишитесь на нас на YouTube
Продукты
Искусственный интеллект
Дополненная и виртуальная реальность
Инструменты для компаний
Игры
ПО с открытым исходным кодом
Размещение публикаций
Интеграция с социальными сетями
Социальное присутствие
Программы
ThreatExchange
Поддержка
Поддержка разработчиков
Ошибки
Статус платформы
Сообщить об инциденте с данными платформы
Группа сообщества Facebook for Developers
Карта сайта
Новости
Блог
Истории успеха
Видео
Страница Meta for Developers
Условия и правила
Центр инициатив для платформы
Условия использования платформы
Правила для разработчиков
Обязательства перед Европейской комиссией
© 2025 Meta
Информация
Создать рекламу
Вакансии
Политика конфиденциальности
Файлы cookie
Условия

Русский

Русский
Был ли этот документ полезен?
ДаНет
Удалить
Документы
Платформа WhatsApp Business
Регистрация на сайте поставщика
Платформа WhatsApp Business
О платформе
Упразднение локального API
Cloud vs On-Prem
Номера телефонов
Сообщения
Расценки
Оценка качества и ограничения числа обращений
Webhooks
Solution Providers
Регистрация на сайте поставщика
Implementation
Onboarding for Solution Partners
Как поставщику технологий зарегистрировать бизнес-клиента?
Default flow
Custom flows
Кредитные линии
Webhooks
Номера телефонов
Управление системными пользователями
Аккаунты WhatsApp Business
Проверка приложения
Отслеживание с помощью пикселя
Automatic Events API
Часто задаваемые вопросы
Versions
Ошибки
Link Previews
Обеспечение соблюдения политик
Журнал изменений
Поддержка
Мы вводим изменение, в соответствии с которым общий доступ к API будет предоставляться в процессе регистрации на сайте поставщика при сохранении маркера. В случае непредвиденных проблем или изменений в процессе регистрации на сайте поставщика обращайтесь в службу поддержки.

Регистрация на сайте поставщика
Регистрация на сайте поставщика представляет собой совместимый с настольными и мобильными устройствами интерфейс аутентификации и предоставления разрешений. Он позволяет компаниям-клиентам легко генерировать объекты, необходимые вам для их подключения к платформе WhatsApp Business.

Воспроизвести	
-2:51
Выключить звук
Дополнительные визуальные настройкиHD
Открыть во весь экран	


В процессе регистрации на сайте поставщика с ваших клиентов собирается связанная с их компаниями информация, автоматически генерируются все объекты WhatsApp, необходимые платформе, и вашему приложению предоставляются доступ к этим объектам, чтобы вы могли быстро предоставлять своим клиентами услуги обмена сообщениями в WhatsApp.

Клиенты, подключенные путем регистрации на сайте поставщика, владеют всеми своими объектами WhatsApp и могут использовать их в других решениях Meta, например в рекламе с переходом в WhatsApp.

Принцип работы
В регистрации на сайте поставщика используется продукт "Вход через Facebook для компаний" и наш JavaScript SDK. Настроив этот процесс, вы можете добавить на свой сайт или порта ссылку или кнопку, которая запускает этот процесс.

Клиенты, нажавшие эту ссылку или кнопку, увидят новое окно, в котором они смогут:

подтвердить свою личность с указанием учетных данных Facebook или Meta Business;
предоставить вашему приложению доступ к своим объектам WhatsApp;
выбрать существующее бизнес-портфолио или создать новое;
выбрать существующий аккаунт WhatsApp Business или создать новый;
войти и подтвердить свой номер телефона компании (собственный или предоставленный вами);
ввести отображаемое имя, которое будет отображаться вместо их номера телефона в клиенте WhatsApp.

После завершения процесса регистрации на сайте поставщика в окно, где он был запущен, возвращается ID аккаунта WhatsApp Business клиента, ID номера телефона и код маркера, который можно обменять. Вы должны отправить эти данные на свой сервер и использовать их в межсерверных вызовах, чтобы:

обменять код на маркер компании в пределах клиента;
зарегистрировать номер телефона компании клиента для использования с облачным API;
подписать свое приложение на Webhooks в аккаунте WhatsApp Business клиента;
предоставить клиенту свою кредитную линию (только для партнеров по решениям).
Если вы поставщик решений или его партнер и все эти действия выполнены, клиент может сразу же начать пользоваться вашим или партнерским приложением для обмена сообщениями. Если вы не является поставщиком решений или его партнером, клиент должен сначала задать способ оплаты в своем аккаунте WhatsApp Business, после чего он сможет начать обмениваться сообщениями.

Ограничения
Ограничения на подключение
По умолчанию вы можете подключить до 10 новых компаний в течение любого 7-дневного периода. Учитываются только новые клиенты. Проверить текущие лимиты на подключение можно на панели WhatsApp Manager > Обзор партнеров. Вы получите уведомление о приближении к этому пределу по электронной почте.

Если вы пройдете подтверждение компании, проверку приложения и подтверждение прав доступа, мы автоматически увеличим этот лимит до 200 новых клиентов-компаний в рамках 7-дневного окна. Если вам нужно регистрировать больше 200 клиентов в неделю, подайте заявку на получение статуса бизнес-партнера Meta.

Ограничения на обмен сообщениями для клиентов-компаний
Клиенты, подключенные в процессе регистрации на сайте поставщика, начинают работать со стандартными ограничениями на количество сообщений, которые можно увеличить с помощью API.

Ограничения на номера телефонов клиентов
Номера телефонов компаний можно регистрировать только для использования с облачным API.
Номера телефонов, зарегистрированные для использования с локальным API или используемые в приложении WhatsApp, не поддерживаются.
Номера телефонов компаний, которые уже используются в приложении WhatsApp Business, поддерживаются, однако для подключения пользователей приложения WhatsApp Business (также известного как Coexistence) потребуется дополнительно настроить процесс.
Клиенты, подключенные в процессе регистрации на сайте поставщика, начинают работу с ограничениями на номера телефонов компаний, действующими по умолчанию.
Процесс по умолчанию
Описания всех экранов, которые увидят клиенты вашей компании в рамках реализации регистрации на сайте поставщика по умолчанию, см. в статье Процесс по умолчанию.

Обратите внимание: если вы владеете информацией о бизнесе своего клиента, вы можете внести эти данные в несколько экранов, что может значительно сократить количество экранов, с которыми придется взаимодействовать вашим клиентам.

Маркеры доступа
В процессе регистрации на сайте поставщика генерируются маркеры доступа системного пользователя бизнес-интеграции ("маркеры компании"). Когда компания-клиент завершит регистрацию на сайте поставщика, обмениваемый маркер будет возвращен в виде события сообщения. Его получит JavaScript SDK. Вы должны обменять этот код на маркер компании, используя межсерверный вызов.

Поставщики технологий будут использовать маркеры компании только самостоятельно.

Поставщики решений будут использовать свои маркеры доступа системного пользователя ("системные маркеры"), чтобы предоставить зарегистрировавшимся клиентам доступ к своей кредитной линии, и маркеры компаний для всех прочих целей. Обратите внимание: чтобы вы могли предоставить доступ к своей кредитной линии, системный пользователь, которого представляет маркер, должен предоставить вашему приложению разрешение business_management и назначить вашему бизнес-портфолио роли Admin или Financial Editor.

Разрешения
Процесс регистрации на сайте поставщика можно настроить таким образом, чтобы запрашивать у клиентов большинство разрешений, однако, скорее всего, вам понадобятся только эти:

whatsapp_business_management — потребуется, если вашему приложению нужен доступ к настройкам и шаблонам сообщений аккаунта WhatsApp Business Account подключаемого клиента;
whatsapp_business_messaging — потребуется, если вашему приложению нужен доступ к настройкам номера телефона подключаемого клиента или если клиенты будут использовать ваше приложение для обменя сообщениями.
Задать необходимые приложению разрешению можно в процессе реализации.

Обратите внимание: когда ваше приложение находится в режиме разработки, эти разрешения будут появляться на экране предоставления разрешений в процессе регистрации на сайте поставщика для всех пользователей, имеющих в вашем приложении роль администратора, разработчика или тестировщика. Однако когда вы опубликуете приложение, в процессе регистрации будут отображаться разрешения, расширенный доступ к которым был утвержден во время проверки приложения.

Биллинг
Партнеры по решениям
У партнеров по решениям уже должна быть кредитная линия. Кроме того, должны быть приняты условия Credit Allocation API на панели Настройки компании > Платежи в Meta Business Suite. Вы также должны предоставлять свою кредитную линию всем клиентам в процессе подключения.

Поставщики технологий и партнеры по технологиям
Подключенные бизнес-клиенты поставщиков технологий и партнеров по технологиям должны добавить способ оплаты в своем аккаунте WhatsApp Business. Инструкции, как это сделать, представлены в статье Добавление кредитной карты в аккаунт на платформе WhatsApp Business Справочного центра.

Аккаунт-песочница
Вы можете тестировать регистрацию на сайте поставщика, используя собственный аккаунт Facebook, но это может привести к созданию дополнительных бизнес-портфолио, аккаунтов WhatsApp Business и номеров телефонов компаний. Чтобы не перегружать аккаунт тестовыми данными, вы можете запросить аккаунт-песочницу для симуляции процедуры регистрации клиентом компании.

В этом случае, завершив процедуру, вы получите ID аккаунта WhatsApp Business, ID номер телефона компании тестового аккаунта-песочницы и обмениваемый код маркера, как если бы процедуру проходил реальный клиент.

Чтобы получить аккаунт-песочницу, перейдите на Панель приложений > WhatsApp > Начало работы, найдите раздел Testing Integrations (Тестирование интеграций) и нажмите Claim sandbox account (Получить аккаунт-песочницу).

Ограничения аккаунтов-песочниц
Срок действия аккаунта-песочницы составляет 30 дней, после чего он деактивируется. Если вы хотите пользоваться им и дальше, нужно будет получить его повторно.
Аккаунт-песочницу нельзя использовать для создания дополнительных бизнес-портфолио, аккаунтов WhatsApp Business или номеров телефонов компаний. Они генерируются автоматически в ходе процедуры регистрации на сайте поставщика.
Аккаунт-песочница связан с администратором приложения. Чтобы объекты аккаунта-песочницы появились в процедуре регистрации на сайте поставщика, администратор приложения должен быть авторизован в своем аккаунте разработчика Meta.
Бизнес-портфолио аккаунта-песочницы не будет отображаться в Meta Business Suite или WhatsApp Manager.
Вы можете обменять полученный код маркера на маркер компании, связанной с аккаунтом-песочницей, и использовать его для получения ID аккаунта WhatsApp Business. При этом нельзя использовать номер телефона компании для отправки и получения сообщений.
Номера телефонов компаний с кодом 555
Бизнес-клиенты могут зарегистрировать до двух телефонных номеров с кодом 555 для компании. Эти номера работают так же, как и обычные номера телефонов компаний (к ним применяются правила ценообразования, рейтинги качества и т. д.), но прежде чем использовать их для отправки сообщений, необходимо утвердить их отображаемые имена. Кроме того, номера с кодом 555:

должны иметь код страны США (+1);
должны иметь код региона 555;
должны подтверждаться автоматически;
нельзя переносить в другой аккаунт WhatsApp Business Account и использовать за пределами платформы WhatsApp Business.
Если ваши бизнес-клиенты могут пользоваться номером с кодом 555, то на экране добавления номера телефона будет автоматически предоставлена возможность выбрать номер с кодом 555:


Перенос объектов
Регистрация на сайте поставщика может быть использована для переноса объектов подключенных клиентов компании несколькими способами. См. Перенос объектов клиентов компании.

Проверка приложения
Вы не сможете подключать бизнес-клиентов до тех пор, пока не получите одобрение на расширенный доступ для каждого из необходимых разрешений.

Подробнее о проверке приложения и о том, что нужно предоставить, чтобы успешно пройти этот процесс, см. в статье Проверка приложения.

Помощник по интеграции
Помощник по интеграции регистрации на сайте поставщика — это инструмент для установки и тестирования, доступный в панели приложений. Этот инструмент позволяет вам:

запускать процесс регистрации на сайте поставщика;
просматривать возвращаемые данные, когда клиент компании пройдет процесс;
генерировать код реализации и запросы для подключения клиентов, которые вы можете скопировать и вставить на свой веб-сайт, на портал клиента компании и на сервер;
отправлять запросы API к конечным точкам, которые вам необходимо будет использовать при подключении клиентов, которые пройдут процесс.
Чтобы получить доступ к Помощнику по интеграции, выберите Панель приложений > WhatsApp > Интеграция на сайте поставщика.

Webhooks
В рамках процесса подключения вы должны подписать свое приложение на Webhooks в аккаунте WhatsApp Business каждого бизнес-клиента, прошедшего процесс регистрации на сайте поставщика.

Webhooks будут срабатывать и отправлять URL обратного вызова, настроенный в вашем приложении, в соответствии с полями Webhooks, на которые вы подписались. Это значит, что все Webhooks для всех ваших подключенных бизнес-клиентов будут отправляться на URL обратного вызова вашего приложения. Однако вы можете переопределить URL обратного вызова в любом отдельном аккаунте WhatsApp Business или для любого номера телефона компании. Информацию о том, как это сделать, см. в статье Переопределение Webhooks.

Локализация
Процесс регистрации на сайте поставщика поддерживает 30 языков. Его локализованная версия выбирается автоматически в зависимости от языка, на котором конечный бизнес-клиент работает с Facebook.

Английский (Великобритания), арабский, венгерский, вьетнамский, греческий, датский, иврит, индонезийский, испанский (Испания), испанский, итальянский, китайский традиционный (Гонконг), китайский традиционный (Тайвань), китайский упрощенный (Китай), корейский, нидерландский, норвежский (букмол), польский, португальский (Бразилия), португальский (Португалия), румынский, русский, тайский, турецкий, финский, французский (Франция), хинди, чешский, шведский, японский.

Дальнейшие действия
Подробнее о том, как реализовать регистрацию на сайте или портале.


Мы в социальных сетях
Подпишитесь на нас на FacebookПодпишитесь на нас в InstagramПодпишитесь на нас в TwitterПодпишитесь на нас в LinkedInПодпишитесь на нас на YouTube
Продукты
Искусственный интеллект
Дополненная и виртуальная реальность
Инструменты для компаний
Игры
ПО с открытым исходным кодом
Размещение публикаций
Интеграция с социальными сетями
Социальное присутствие
Программы
ThreatExchange
Поддержка
Поддержка разработчиков
Ошибки
Статус платформы
Сообщить об инциденте с данными платформы
Группа сообщества Facebook for Developers
Карта сайта
Новости
Блог
Истории успеха
Видео
Страница Meta for Developers
Условия и правила
Центр инициатив для платформы
Условия использования платформы
Правила для разработчиков
Обязательства перед Европейской комиссией
© 2025 Meta
Информация
Создать рекламу
Вакансии
Политика конфиденциальности
Файлы cookie
Условия

Русский

Русский
Был ли этот документ полезен?
ДаНет
Удалить
Платформа WhatsApp Business
О платформе
Упразднение локального API
Cloud vs On-Prem
Номера телефонов
Сообщения
Расценки
Оценка качества и ограничения числа обращений
Webhooks
Solution Providers
Регистрация на сайте поставщика
Link Previews
Обеспечение соблюдения политик
Журнал изменений
Поддержка
Link Previews
WhatsApp supports link previews when the link is sent via chat or shared via status. WhatsApp will attempt to perform a link preview when possible for a better user experience. To enable this experience, WhatsApp relies on link owners to define properties that are specifically optimized for WhatsApp. Not meeting these requirements may risk the link to be not previewed.


Get Started
To get started with enabling link previews, websites need to add HTML mark-ups to the HEAD section on the page.

<head>
  <meta property="og:title" content=”WhatsApp"/>
  <meta property="og:description" content="Simple. Secure. Reliable messaging."/>
  <meta property="og:url" content="https://whatsapp.com"/>
  <meta property="og:image"content="https://static.whatsapp.net/rsrc.php/ym/r/36B424nhiL4.svg"/>
</head>
The <head> containing the HTML mark-ups must appear within the first 300KB of the HTML. The entire HTML does not need to fit within 300KB.

The <og:title>, <og:description> and <og:url> mark-ups must be inside the <head> tag. They should not be empty.

The <og:title> mark-up represents the title of the content without any branding. WhatsApp will display this in primary text color, in bold and in at most 2 lines.

The <og:description> mark-up represents the description of the content. WhatsApp will display this in a smaller size than the title and in secondary text color. It is limited to 1 or 2 lines and 80 characters will suffice.

The <og:url> mark-up represents the canonical URL of the page. The URL should be undecorated, without session variables, user identifying parameters and counters.

The <og:image> mark-up is an absolute URL for an image used as the thumbnail for the link preview. This image should be under 600KB in size. Image should be 300px or more in width with 4:1 width/height or less aspect ratio.

WhatsApp will make the best attempt to show link previews, eg: relaxing requirements, looking for other HTML mark-ups and reverting to small link previews. However, this should not be relied on. It’s not guaranteed to work (and continue to work).

WhatsApp crawls the web page via an HTTP GET request.

The request will have the User-Agent header set to WhatsApp/2.x.x.x A|I|N, where x are major/minor numeric versions of WhatsApp and A|I|N is for Android, iOS and web respectively. Some examples of valid User-Agent header values: WhatsApp/2.22.20.72 A, WhatsApp/2.22.19.78 I, WhatsApp/2.2236.3 N. Web site owners can identify such incoming requests and can customize the content (mark-ups and images) accordingly.

The request will also have the Accept-Language header set to the language selected by the sender, if any. Some examples of valid Accept-Language header values are: en , fr, de. Similarly, web site owners can customize the content language accordingly. Note that the language set and seen by the sender will also be seen by the sender.

How to verify?
Start with composing a message with the link to test (not tap to send yet). On behalf of the sender, WhatsApp will crawl this URL and attempt to generate a link preview.

If a preview does not come up above the composer box after 10 seconds, please check all the requirements above are met. Else, continue with sending the message by tapping the "send" button.

If a preview does not show up in the expected large size, please check the image requirements above are met. Else, link previews are all working as expected. Congratulations, you're all set!


Мы в социальных сетях
Подпишитесь на нас на FacebookПодпишитесь на нас в InstagramПодпишитесь на нас в TwitterПодпишитесь на нас в LinkedInПодпишитесь на нас на YouTube
Продукты
Искусственный интеллект
Дополненная и виртуальная реальность
Инструменты для компаний
Игры
ПО с открытым исходным кодом
Размещение публикаций
Интеграция с социальными сетями
Социальное присутствие
Программы
ThreatExchange
Поддержка
Поддержка разработчиков
Ошибки
Статус платформы
Сообщить об инциденте с данными платформы
Группа сообщества Facebook for Developers
Карта сайта
Новости
Блог
Истории успеха
Видео
Страница Meta for Developers
Условия и правила
Центр инициатив для платформы
Условия использования платформы
Правила для разработчиков
Обязательства перед Европейской комиссией
© 2025 Meta
Информация
Создать рекламу
Вакансии
Политика конфиденциальности
Файлы cookie
Условия

Русский

Русский
Был ли этот документ полезен?
ДаНет
Удалить