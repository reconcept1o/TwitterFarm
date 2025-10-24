# sms_api.py
import requests
from dotenv import load_dotenv
import os

load_dotenv()
SMS_API_KEY = os.getenv("SMS_API_KEY")

def get_sms_number():
    url = "https://smspva.com/priem.php"
    params = {
        "metod": "get_number",
        "service": "tw",
        "country": "israel",
        "operator": "orange",
        "apikey": SMS_API_KEY
    }
    r = requests.get(url, params=params).text
    if "ACCESS_NUMBER" in r:
        parts = r.split(":")
        return parts[1], parts[2]  # id, phone
    print("SMS numara alınamadı:", r)
    return None, None

def get_sms_code(sms_id):
    for _ in range(42):
        r = requests.get(f"https://smspva.com/priem.php?metod=get_sms&id={sms_id}&apikey={SMS_API_KEY}").text
        if "STATUS_OK" in r:
            return r.split(":")[1]
        time.sleep(10)
    print("SMS kodu gelmedi.")
    return None