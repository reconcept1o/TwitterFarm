# main.py
from sms_api import get_sms_number, get_sms_code

print("SMS Test Başlıyor...")

sms_id, phone = get_sms_number()
if phone:
    print(f"Numara: {phone}")
    code = get_sms_code(sms_id)
    if code:
        print(f"BAŞARILI! Kod: {code}")
    else:
        print("Kod gelmedi.")
else:
    print("Numara alınamadı.")