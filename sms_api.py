# sms_api.py (İsrail "IL" olarak güncellendi)

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SMSPVA_API_KEY") 
# YENİ BASE_URL (Dökümantasyon Sürüm 2'ye göre)
BASE_URL = "https://api.smspva.com" 

# Dökümantasyondaki servis listesine göre Twitter'ın kodu "opt41"
SERVICE_CODE = "opt41"

def numara_al():
    # Ülke kodunu isteğiniz üzerine "IL" (İsrail) olarak değiştirdim.
    country_code = "IL" 
    
    # YENİ Endpoint: /activation/number/{country}/{service}
    url = f"{BASE_URL}/activation/number/{country_code.upper()}/{SERVICE_CODE}"
    
    # YENİ: API Key artık header içinde gönderiliyor
    headers = {
        "apikey": API_KEY
    }
    
    try:
        # Parametreleri (params) kaldırdık, yerine headers ekledik
        r = requests.get(url, headers=headers, timeout=10)
        
        print(f"SMS API Yanıtı (Status Code): {r.status_code}")
        print(f"SMS API Yanıtı (Body): {r.text}")

        # Başarılı yanıt kodu 200'dür (Dökümana göre)
        if r.status_code == 200:
            data = r.json()
            # Dönen veriden orderId ve phoneNumber'ı alıyoruz
            num_id = data["data"]["orderId"]
            phone = data["data"]["phoneNumber"]
            print(f"Numara alındı: {phone}, Sipariş ID: {num_id}")
            return num_id, phone
        else:
            # Diğer durumlar (407 bakiye yetersiz, 501 numara yok, 502 sunucu hatası vb.)
            print(f"API Hatası: {r.status_code} - {r.text}")
            return None, None
            
    except Exception as e:
        print(f"Numara alınamadı (İstisna oluştu): {e}")
        return None, None

def kodu_bekle(num_id):
    # YENİ Endpoint: /activation/sms/{orderid}
    url = f"{BASE_URL}/activation/sms/{num_id}"
    
    print(f"{num_id} için SMS bekleniyor...")
    
    # Dökümanda 9 dk 40 sn (580sn) bekleme süresi öneriliyor.
    # 5 saniye aralıklarla 60 kez (5 dakika) deneyelim.
    for _ in range(60): 
        try:
            r = requests.get(url, timeout=10)
            
            # YENİ: Başarılı kod 200, "bekle" kodu 202
            if r.status_code == 200:
                data = r.json()
                sms_code = data["data"]["sms"] # Dönen kod
                print(f"SMS Kodu Alındı: {sms_code}")
                return sms_code
                
            elif r.status_code == 202:
                # 202 = SMS henüz gelmedi, beklemeye devam et
                print("SMS henüz gelmedi, 5sn sonra tekrar denenecek...")
                time.sleep(5)
                
            else:
                # 406 (order not found), 410 (order closed) vb.
                print(f"Kod beklenirken hata: {r.status_code} - {r.text}")
                return None
                
        except Exception as e:
            print(f"Kod beklenirken istisna: {e}")
            time.sleep(5)
            
    print("Zaman aşımı! SMS kodu 5 dakika içinde gelmedi.")
    return None