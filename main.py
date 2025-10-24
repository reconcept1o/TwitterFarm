# main.py
from sms_api import get_sms_number, get_sms_code
from mail_api import mail_ve_token_uret, x_kodu_oku
from x_api import x_hesap_ac, client
import time
import random

for i in range(28):
    print(f"\n{i+1}. Hesap oluşturuluyor...")

    # 1. Mail + Token
    email, mail_pass, mail_token = mail_ve_token_uret()
    if not email:
        continue

    # 2. SMS Numara
    sms_id, phone = get_sms_number()
    if not phone:
        continue

    # 3. X Hesabı Aç
    driver = x_hesap_ac(email, phone)

    # 4. SMS Kodu
    sms_code = get_sms_code(sms_id)
    if sms_code:
        driver.find_element(By.NAME, "verification_code").send_keys(sms_code)
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        time.sleep(3)

    # 5. X Doğrulama Kodu
    x_code = x_kodu_oku(mail_token)
    if x_code:
        driver.find_element(By.NAME, "verification_code").send_keys(x_code)
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        time.sleep(3)
        
        # Şifre
        driver.find_element(By.NAME, "password").send_keys("Pass123!@#")
        driver.find_element(By.XPATH, "//span[text()='Sign up']").click()
        time.sleep(5)
        
        # Tweet
        client.create_tweet(text=f"Merhaba #{i}")
        
        # Kaydet
        with open("hesaplar.txt", "a") as f:
            f.write(f"{email}:{mail_pass}:{phone}\n")
        print("HESAP HAZIR!")
    
    driver.quit()
    time.sleep(30)