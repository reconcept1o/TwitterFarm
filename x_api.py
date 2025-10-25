# x_api.py (Güncellenmiş hali)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # YENİ
from selenium.webdriver.common.by import By
import time
import tweepy
from dotenv import load_dotenv
import os
import random

# WebDriverWait için gerekli yeni importlar
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_SECRET")
)

def x_hesap_ac(email, password, phone):
    # ChromeDriver'ı proje klasöründen al
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(current_dir, "chromedriver.exe")
    service = Service(executable_path=chromedriver_path)

    options = Options()
    
    # --- Otomasyon izlerini gizle (kritik!) ---
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
    
    # Diğer stabilite argümanları
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # Hata ayıklama için kapalı — doğru

    driver = webdriver.Chrome(service=service, options=options)

    # JavaScript ile webdriver özelliğini gizle (çok kritik!)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get("https://x.com/i/flow/signup")  # Boşluk silindi

        wait = WebDriverWait(driver, 15)  # Zaman aşımını 15 sn yapalım

        print("Sayfa açıldı, 'Ad' alanı bekleniyor...")
        name_field = wait.until(EC.element_to_be_clickable((By.NAME, "name")))
        name_field.send_keys(f"Bot{random.randint(1,999)}")
        print("'Ad' alanı dolduruldu.")

        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        email_field.send_keys(email)
        print("E-posta alanı dolduruldu.")
        
        try:
            password_field = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_field.send_keys(password)
            print("Şifre alanı dolduruldu.")
        except TimeoutException:
            print("Uyarı: Şifre alanı ilk ekranda bulunamadı, devam ediliyor...")

        next_button_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        next_button_1.click()
        print("İlk 'Next' butonuna tıklandı.")

        next_button_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        next_button_2.click()
        print("İkinci 'Next' butonuna tıklandı.")

        phone_field = wait.until(EC.element_to_be_clickable((By.NAME, "phone_number")))
        phone_field.send_keys(phone)
        print(f"Telefon numarası ({phone}) girildi.")
        
        phone_next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        phone_next_button.click()
        print("Telefon 'Next' butonuna tıklandı. Kod bekleniyor...")

        time.sleep(5)
        print("Selenium akışı tamamlandı, driver döndürülüyor.")
        return driver

    except Exception as e:
        print(f"Selenium otomasyonunda HATA oluştu: {e}")
        driver.save_screenshot("hata_ekrani.png")
        print("Ekran görüntüsü 'hata_ekrani.png' olarak kaydedildi.")
        driver.quit()
        return None