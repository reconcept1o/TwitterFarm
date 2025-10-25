# main.py
from mail_api import mail_uret
from sms_api import numara_al, kodu_bekle
from x_api import x_hesap_ac
import time

for i in range(2):  # SADECE 2 HESAP!
    print(f"\n{i+1}. Hesap oluşturuluyor...")
    
    # 1. Mail üret
    email = mail_uret()
    print(f"Mail üretildi: {email}")
    
    # 2. Numara al
    num_id, phone = numara_al()
    if not phone:
        print("Numara alınamadı, geçiliyor...")
        continue
    print(f"Numara alındı: {phone}")
    
    # 3. X hesabı aç
    password = "Pass123!@#"
    success = x_hesap_ac(email, password, phone)
    if not success:
        print("Hesap açılamadı, geçiliyor...")
        continue
    
    # 4. Kodu bekle
    code = kodu_bekle(num_id)
    if not code:
        print("Kod gelmedi, geçiliyor...")
        continue
    print(f"Kod geldi: {code}")
    
    # 5. Kodu gir (x_hesap_ac içinde zaten giriliyor)
    
    # 6. Kaydet
    with open("hesaplar.txt", "a", encoding="utf-8") as f:
        f.write(f"{email}:{password}:{phone}\n")
    
    print("HESAP HAZIR!")
    time.sleep(10)