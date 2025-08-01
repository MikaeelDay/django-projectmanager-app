# 🚀 Project Manager - سیستم مدیریت پروژه

یک سیستم مدیریت پروژه مدرن و کاربردی با رابط کاربری زیبا و امکانات کامل.

## ✨ ویژگی‌ها

- 🎨 **رابط کاربری مدرن** با طراحی Dark Theme
- 👥 **مدیریت کاربران** با سیستم احراز هویت
- 📋 **مدیریت پروژه‌ها** با امکان تخصیص مسئول
- 📊 **داشبورد ادمین** برای مدیریت کامل
- 👤 **داشبورد کاربر** برای مشاهده پروژه‌های تخصیص داده شده
- ✅ **علامت‌گذاری پروژه‌ها** به عنوان انجام شده
- 📅 **مدیریت تاریخ‌ها** برای شروع و پایان پروژه
- 🔒 **امنیت بالا** با سیستم احراز هویت Django
- 📱 **طراحی ریسپانسیو** برای تمام دستگاه‌ها

## 🛠️ تکنولوژی‌های استفاده شده

- **Backend:** Django 5.2
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite
- **Styling:** Custom CSS با Glassmorphism
- **Authentication:** Django Built-in Auth
- **Testing:** Django Test Framework

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.8+
- pip

### مراحل نصب

1. **کلون کردن پروژه:**
```bash
git clone https://github.com/yourusername/project-manager.git
cd project-manager
```

2. **ایجاد محیط مجازی:**
```bash
python -m venv venv
```

3. **فعال‌سازی محیط مجازی:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **نصب وابستگی‌ها:**
```bash
pip install -r requirements.txt
```

5. **اجرای مایگریشن‌ها:**
```bash
python manage.py migrate
```

6. **ایجاد کاربر ادمین:**
```bash
python manage.py createsuperuser
```

7. **اجرای سرور:**
```bash
python manage.py runserver
```

8. **باز کردن در مرورگر:**
```
http://127.0.0.1:8000
```

## 📁 ساختار پروژه

```
ProjectManager/
├── ProjectManager/          # تنظیمات اصلی Django
├── projects/               # اپلیکیشن اصلی
│   ├── models.py          # مدل‌های داده
│   ├── views.py           # ویوهای اپلیکیشن
│   ├── tests.py           # تست‌های واحد
│   └── templates/         # قالب‌های HTML
├── static/                # فایل‌های استاتیک
│   └── base_style.css     # استایل‌های اصلی
├── templates/             # قالب‌های عمومی
├── manage.py              # فایل مدیریت Django
└── requirements.txt       # وابستگی‌های پروژه
```

## 🧪 اجرای تست‌ها

```bash
# اجرای تمام تست‌ها
python manage.py test projects.tests

# اجرای تست خاص
python manage.py test projects.tests.ProjectModelTest

# اجرای تست با جزئیات
python manage.py test projects.tests --verbosity=2
```

## 👥 نحوه استفاده

### برای ادمین‌ها:
1. وارد داشبورد ادمین شوید
2. پروژه‌های جدید ایجاد کنید
3. کاربران را به پروژه‌ها تخصیص دهید
4. پروژه‌ها را ویرایش یا حذف کنید

### برای کاربران:
1. وارد داشبورد کاربر شوید
2. پروژه‌های تخصیص داده شده را مشاهده کنید
3. پروژه‌های تکمیل شده را علامت‌گذاری کنید

## 🎨 ویژگی‌های طراحی

- **Dark Theme** با رنگ‌بندی مدرن
- **Glassmorphism** برای افکت‌های بصری
- **Animations** برای تعامل بهتر
- **Responsive Design** برای تمام دستگاه‌ها
- **Persian RTL** برای زبان فارسی

## 🔧 تنظیمات

### تغییر تنظیمات پایگاه داده:
در فایل `settings.py` می‌توانید تنظیمات پایگاه داده را تغییر دهید.

### تغییر استایل‌ها:
فایل `static/base_style.css` را ویرایش کنید.

## 🤝 مشارکت

1. پروژه را Fork کنید
2. یک Branch جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را Commit کنید (`git commit -m 'Add amazing feature'`)
4. Branch را Push کنید (`git push origin feature/amazing-feature`)
5. یک Pull Request ایجاد کنید

## 📝 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## 📞 پشتیبانی

برای سوالات و مشکلات:
- Issue در GitHub ایجاد کنید
- ایمیل: your-email@example.com


---

⭐ اگر این پروژه برایتان مفید بود، لطفاً آن را ستاره‌دار کنید! 
