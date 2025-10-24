# sms_api.py (SUNUCU İÇİN – HTTP + SSL KAPAT + HATA YOK)
import requests
from dotenv import load_dotenv
import os
import time
import urllib3

# SSL UYARILARINI KAPAT (Sunucuda gerek yok)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
SMS_API_KEY = os.getenv("SMS_API_KEY")

def get_sms_number():
    """Numara al (İsrail Orange)"""
    url = "http://smspva.com/priem.php"  # HTTP DOĞRU!
    params = {
        "metod": "get_number",
        "service": "tw",
        "country": "israel",
        "operator": "orange",
        "apikey": SMS_API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=30, verify=False).text
        print("SMS API Yanıtı:", r.strip())
        if "OK:" in r:
            parts = r.split(":")
            sms_id = parts[1]
            phone = parts[2]
            print(f"Numara alındı: {phone} (ID: {sms_id})")
            return sms_id, phone
        else:
            print("Numara alınamadı. Yanıt:", r.strip())
            return None, None
    except Exception as e:
        print("SMS Bağlantı Hatası:", e)
        return None, None

def get_sms_code(sms_id):
    url = "http://smspva.com/priem.php"
    for _ in range(42):
        try:
            params = {"metod": "get_sms", "id": sms_id, "apikey": SMS_API_KEY}
            r = requests.get(url, params=params, verify=False, timeout=30).text
            if "STATUS_OK:" in r:
                code = r.split(":")[1]
                print(f"Kod geldi: {code}")
                return code
        except Exception as e:
            print("SMS kodu hatası:", e)
        time.sleep(10)
    print("Kod gelmedi.")
    return None

def refuse_number(sms_id):
    """İptal et (para iade)"""
    url = "http://smspva.com/priem.php"
    params = {"metod": "set_status", "status": "8", "id": sms_id, "apikey": SMS_API_KEY}
    try:
        r = requests.get(url, params=params, verify=False).text
        print("İptal yanıtı:", r.strip())
    except Exception as e:
        print("İptal hatası:", e)