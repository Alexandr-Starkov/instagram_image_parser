from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import requests
import time
import os


load_dotenv()

# Получаем путь к ChromeDriver, Login и Password пользователя Instagram
chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
instagram_login = os.getenv("INSTAGRAM_LOGIN")
instagram_password = os.getenv("INSTAGRAM_PASSWORD")


if not chromedriver_path or not instagram_login or not instagram_password:
    raise ValueError(
        "CHROMEDRIVER_PATH/INSTAGRAM_LOGIN/INSTAGRAM_PASSWORD не задан в .env файле")


# Настраиваем ChromeDriver
service = Service(chromedriver_path)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Работать в фоновом режиме


def open_profile(driver: webdriver.Chrome, profile_url: str):
    driver.get(profile_url)
    time.sleep(5)  # Время на загрузку страницы
    print(f"Открыт профиль: {profile_url}")


def get_post_links(driver: webdriver.Chrome, max_posts=10):
    """
    Прокручивает профиль и собирает ссылки на публикации.
    """
    SCROLL_PAUSE_TIME = 2
    post_links = set()

    while len(post_links) < max_posts:
        # Ищем элементы с публикациями
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and "/p/" in href:  # Проверяем, что это ссылка на публикацию
                post_links.add(href)
                if len(post_links) >= max_posts:
                    break

        # Прерываем цикл, если уже собрано достаточно ссылок
        if len(post_links) >= max_posts:
            break

        # Прокручиваем вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

    print(f"Найдено {len(post_links)} публикаций")
    return list(post_links)


def get_images_from_post(driver: webdriver.Chrome, post_url):
    """
    Открывает публикацию, собирает ссылки на изображения и сохраняет их в папке 'images'
    """
    driver.get(post_url)
    time.sleep(5)  # Даем время на загрузку страницы

    # Создаём папку для сохранения изображений, если её нет
    images_folder = "images"
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Ищем изображения
    images = set()
    try:
        img_elements = driver.find_elements(By.XPATH, "//div[contains(@class, '_aagv')]/img")
        for img in img_elements:
            src = img.get_attribute("src")
            if src:
                images.add(src)
    except Exception as e:
        print(f"Ошибка при парсинге изображений: {e}")

    # Сохраняем изображения
    for idx, img_url in enumerate(images):
        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                # Сохраняем изображение в папке 'images'
                image_path = os.path.join(images_folder, f"post_{idx + 1}.jpg")
                with open(image_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Изображение сохранено: {image_path}")
            else:
                print(f"Не удалось загрузить изображение: {img_url}")
        except Exception as e:
            print(f"Ошибка при сохранении изображения {img_url}: {e}")

    print(f"Собрано {len(images)} изображений с поста: {post_url}")
    return list(images)


def wait_for_verification():
    print("Пожалуйста, введите код подтверждения вручную, если требуется!")
    input("После ввода кода нажмите Enter...")


# Функция авторизации
def login(driver: webdriver.Chrome, username: str, password: str):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)  # Загрузка страницы
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(10)

    if "accounts/login" in driver.current_url:
        raise Exception(
            "Не удалось войти в Instagram. Проверьте логин и пароль.")
    print("Успешно вошли в Instagramm")


def main():
    # URL профиля
    while True:
        try:
            profile_url = input("Введите URL Instagram профиля: ").strip()
        except ValueError:
            print("Введите корректный URL Instagram профиля\n")
        else:
            break

    # Создаём WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        login(driver, instagram_login, instagram_password)
        wait_for_verification()  # Ввод кода вручную

        # Открываем профиль
        open_profile(driver, profile_url)

        # Количество публикаций
        while True:
            try:
                max_posts = int(input("Введите количество публикаций: "))
            except ValueError:
                print("Введите число\n")
            else:
                break

        # Получаем ссылки на публикации
        post_links = get_post_links(driver, max_posts=max_posts)

        # Собираем изображения с публикаций
        all_images = []
        for post_url in post_links:
            images = get_images_from_post(driver, post_url)
            all_images.extend(images)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
