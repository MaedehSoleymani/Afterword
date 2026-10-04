# Afterword

**Afterword** is a Django-based web application designed to let users create, store, and manage personal messages for specific recipients, with the long-term goal of delivering those messages by email after the user's death.

The project originally started as **PasNevesht (پس‌نوشت)**, a simple scheduled-message system. It has since evolved into **Afterword**, with a broader concept focused on preserving personal words, memories, and messages for the future.

---

## Features

### Authentication & Accounts

* Custom user model based on Django's `AbstractBaseUser`
* Email-based authentication
* User registration
* Password-based login
* Email verification
* Account activation/deactivation
* Secure password reset using time-limited tokens
* User and admin roles
* Django Admin integration

### Messages

* Create and manage personal messages
* Assign messages to specific recipients
* Store messages securely in the database
* Manage outgoing messages through the Outbox
* Support for message attachments
* Designed around the concept of preserving personal messages for the future

### Email

* Email-based message delivery infrastructure
* Support for sending messages to designated recipients
* Designed to support scheduled and automated delivery

### Scheduling

* Scheduled message delivery
* Scheduler-based architecture
* APScheduler integration
* Designed to support more advanced scheduling mechanisms in the future

### Blog

* Built-in blog section
* Separate Django application for blog functionality

### Simple API

Afterword currently includes a simple GET API.

The API is currently a **standalone component** and is **not yet connected to the Telegram bot or the main Afterword workflow**.

The API will be expanded and integrated with the rest of the system in future development.

### Telegram Bot

The project also includes a Telegram bot.

The bot was created as an **AI-assisted, vibe-coded component**, with the implementation generated entirely through AI-assisted coding.

At the moment, the Telegram bot operates independently and is **not connected to Afterword's API or database**.

Future development will connect:

```text
Telegram Bot
      ↓
     API
      ↓
  Afterword
      ↓
   Database
```

---

## The Core Idea

Afterword is built around a simple idea:

> **Some messages are meant for a future that we may not be there to see.**

A user can prepare messages for people they care about and store them in Afterword.

The long-term goal is for those messages to be delivered to their intended recipients after the user's death.

### Important

A reliable system for detecting or confirming a user's death **does not currently exist in the project**.

This is intentionally left as a future feature because reliable death verification is a complex problem that requires careful consideration of security, privacy, false positives, and trust.

---

## Technology Stack

### Backend

* Python
* Django
* Django ORM
* SQLite / relational database
* APScheduler

### Frontend

* HTML
* CSS
* Django Templates
* Bootstrap / template utilities where applicable

### Additional Components

* Email delivery
* Simple GET API
* Telegram Bot
* Django Admin
* File/attachment handling

---

## Project Structure

The project is organized into several Django applications, including:

```text
Afterword/
├── accounts/
├── blog/
├── emails/
├── outbox/
├── pages/
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

The exact structure may evolve as development continues.

---

## Future Plans

The project is still under active development.

Planned improvements include:

* Reliable death verification / confirmation mechanism
* Connecting the Telegram bot to the API
* Connecting the API to the main Afterword application
* Expanded API functionality
* More advanced scheduling
* Automated message delivery workflows
* Improved recipient management
* More comprehensive admin functionality
* Improved security and privacy mechanisms
* Further improvements to email delivery reliability

---

# Afterword

**Afterword** یک وب‌اپلیکیشن مبتنی بر Django است که با هدف ایجاد بستری برای نگهداری و مدیریت پیام‌های شخصی و ارسال آن‌ها برای گیرندگان مشخص طراحی شده است.

ایده‌ی اصلی پروژه این است که کاربر بتواند پیام‌هایی را برای افراد موردنظر خود ذخیره کند تا در آینده و پس از فوت او، این پیام‌ها از طریق ایمیل به گیرندگان تعیین‌شده ارسال شوند.

این پروژه در ابتدا با نام **PasNevesht (پس‌نوشت)** و با ایده‌ی یک سیستم ساده برای ارسال زمان‌بندی‌شده‌ی پیام‌ها شروع شد و در ادامه با تغییر ایده و توسعه‌ی قابلیت‌ها به **Afterword** تبدیل شد.


---

## قابلیت‌ها

### احراز هویت و حساب‌های کاربری

* استفاده از User Model اختصاصی مبتنی بر `AbstractBaseUser`
* ورود با ایمیل و رمز عبور
* ثبت‌نام کاربران
* تأیید ایمیل
* فعال و غیرفعال کردن حساب کاربری
* بازیابی رمز عبور با Token دارای محدودیت زمانی
* نقش‌های کاربر و مدیر
* اتصال به Django Admin

### مدیریت پیام‌ها

* ایجاد و مدیریت پیام‌های شخصی
* تعیین گیرنده برای هر پیام
* ذخیره‌ی پیام‌ها در پایگاه داده
* مدیریت پیام‌های خروجی از طریق Outbox
* پشتیبانی از پیوست‌ها
* طراحی سیستم بر اساس ایده‌ی نگهداری پیام‌ها برای آینده

### ارسال ایمیل

* زیرساخت ارسال پیام از طریق ایمیل
* امکان ارسال پیام برای گیرندگان تعیین‌شده
* طراحی سیستم برای ارسال خودکار و زمان‌بندی‌شده‌ی پیام‌ها

### زمان‌بندی

* امکان زمان‌بندی ارسال پیام‌ها
* استفاده از Scheduler
* استفاده از `APScheduler`
* آماده‌سازی ساختار برای سیستم‌های پیشرفته‌تر زمان‌بندی در آینده

### وبلاگ

* دارای بخش Blog
* پیاده‌سازی وبلاگ در قالب یک Django App مجزا

### API ساده

Afterword در حال حاضر دارای یک **API ساده‌ی GET** است.

این API در وضعیت فعلی یک بخش **مستقل** است و هنوز به ربات تلگرام یا جریان اصلی Afterword متصل نشده است.

قرار است در آینده API توسعه داده شده و به بخش‌های مختلف سیستم متصل شود.

### ربات تلگرام

پروژه دارای یک **Telegram Bot** نیز هست.

این ربات به‌صورت **AI-assisted و کاملاً vibe-coded** توسعه داده شده و پیاده‌سازی آن به‌طور کامل با کمک AI انجام شده است.

در حال حاضر ربات تلگرام مستقل از پروژه‌ی اصلی فعالیت می‌کند و هنوز به API یا دیتابیس Afterword متصل نشده است.

معماری موردنظر برای آینده:

```text
Telegram Bot
      ↓
     API
      ↓
  Afterword
      ↓
   Database
```

---

## ایده‌ی اصلی Afterword

Afterword بر پایه‌ی یک ایده‌ی ساده شکل گرفته است:

> **بعضی پیام‌ها برای آینده نوشته می‌شوند؛ حتی برای زمانی که دیگر خودمان حضور نداریم.**

کاربر می‌تواند پیام‌هایی را برای افراد موردنظر خود آماده و در Afterword ذخیره کند.

هدف نهایی پروژه این است که این پیام‌ها پس از فوت کاربر به گیرندگان مشخص‌شده ارسال شوند.

### وضعیت تأیید فوت

در نسخه‌ی فعلی پروژه **هیچ سیستم قابل‌اعتمادی برای تشخیص یا تأیید فوت کاربر وجود ندارد**.

این قابلیت به آینده موکول شده است؛ زیرا تشخیص قابل‌اعتماد فوت یک کار ساده نیست و مسائل مهمی مانند امنیت، حریم خصوصی، خطای تشخیص و جلوگیری از ارسال اشتباه پیام‌ها را دربرمی‌گیرد.

---

## تکنولوژی‌های استفاده‌شده

### Backend

* Python
* Django
* Django ORM
* Relational Database
* APScheduler

### Frontend

* HTML
* CSS
* Django Templates
* Template utilities

### سایر بخش‌ها

* Email System
* Simple GET API
* Telegram Bot
* Django Admin
* File / Attachment Handling

---

## ساختار پروژه

ساختار پروژه شامل چند Django App اصلی است:

```text
Afterword/
├── accounts/
├── blog/
├── emails/
├── outbox/
├── pages/
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

ساختار پروژه در طول توسعه ممکن است تغییر کند.

---

## برنامه‌های آینده

Afterword همچنان در حال توسعه است و قابلیت‌های زیر برای مراحل بعدی در نظر گرفته شده‌اند:

* پیاده‌سازی یک سیستم قابل‌اعتماد برای تأیید فوت کاربر
* اتصال Telegram Bot به API
* اتصال API به سیستم اصلی Afterword
* توسعه‌ی قابلیت‌های API
* سیستم پیشرفته‌تر زمان‌بندی
* خودکارسازی کامل فرایند ارسال پیام
* مدیریت پیشرفته‌تر گیرندگان
* توسعه‌ی امکانات پنل مدیریت
* بهبود امنیت و حریم خصوصی
* بهبود قابلیت اطمینان سیستم ارسال ایمیل