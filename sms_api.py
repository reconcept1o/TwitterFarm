# sms_api.py (KESİN ÇALIŞIR – HTTP + SSL KAPAT + UYARI KAPAT)
import requests
from dotenv import load_dotenv
import os
import time
import urllib3

# SSL UYARISINI KAPAT
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
SMS_API_KEY = os.getenv("SMS_API_KEY")

def get_sms_number():
    """Numara al (İsrail Orange)"""
    url = "http://smspva.com/priem.php"  # SADECE HTTP!
    params = {
        "metod": "get_number",
        "service": "tw",
        "country": "israel",
        "operator": "orange",
        "apikey": SMS_API_KEY
    }
    try:
        # HTTP + SSL KAPAT
        r = requests.get(url, params=params, timeout=30, verify=False).text
        print("API ham yanıt:", r)  # DEBUG
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
        print("Bağlantı hatası:", e)
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
        except: pass
        time.sleep(10)
    print("Kod gelmedi.")
    return None