# Instagram Image Scraper

Этот проект предназначен для парсинга изображений из публикаций Instagram-профиля с использованием Selenium. Пользователь вводит URL профиля, а скрипт загружает указанное количество публикаций и сохраняет изображения из них в локальную папку.

## 📋 Функциональность
- Авторизация в Instagram через логин и пароль.
- Получение ссылок на публикации профиля.
- Сбор изображений из публикаций.
- Сохранение изображений в папке `images`.

## 🛠 Требования
Перед началом работы убедитесь, что на вашем компьютере установлены:
- Python 3.8+
- Google Chrome 131+
- WebDriver для Google Chrome (совместимый с установленной версией браузера)
- Сслыка на WebDriver для Win64 - https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.264/win64/chromedriver-win64.zip  
- [Selenium](https://pypi.org/project/selenium/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [requests](https://pypi.org/project/requests/)

## 📦 Установка
1. Склонируйте репозиторий или скачайте проект.
2. Установите зависимости:
   ```pip install -r requirements.txt```
3. Создайте файл .env в корне проекта и укажите свои логин и пароль для Instagram: 
    ```INSTAGRAM_LOGIN=ваш_логин```
    ```INSTAGRAM_PASSWORD=ваш_пароль```
4. Убедитесь, что WebDriver для Chrome находится в корне проекта


## 🚀 Использование  
1. Запустите скрипт:  
    ```python main.py```
2. Введите URL профиля Instagram, который вы хотите парсить:
    ```https://www.instagram.com/username/```
3. Укажите количество публикаций для парсинга.  
4. Изображения из публикаций будут сохранены в папке images.  

## 💡 Примечания
* Этот проект использует Selenium для автоматизации работы с Instagram, поэтому вам может потребоваться ручной ввод кода верификации, если Instagram запросит его.
* Если структура страниц Instagram изменится, потребуется обновление XPath в функциях парсинга.

## Контакты
Telegram - https://t.me/AlexStarkJr.  
Почта - a.starkovjr@gmail.com.  