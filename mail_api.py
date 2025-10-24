# mail_api.py
import requests
import random
import time

def mail_ve_token_uret():
    try:
        domain = requests.get("https://api.mail.tm/domains").json()["hydra:member"][0]["domain"]
        email = f"bot{random.randint(1000,9999)}@{domain}"
        password = "Pass123!@#"

        requests.post("https://api.mail.tm/accounts", json={"address": email, "password": password})
        token = requests.post("https://api.mail.tm/token", json={"address": email, "password": password}).json()["token"]
        print(f"Mail üretildi: {email}")
        return email, password, token
    except Exception as e:
        print("Mail üretilemedi:", e)
        return None, None, None

def x_kodu_oku(token):
    headers = {"Authorization": f"Bearer {token}"}
    for _ in range(30):
        try:
            msgs = requests.get("https://api.mail.tm/messages", headers=headers).json()["hydra:member"]
            for msg in msgs:
                if "verify" in msg["subject"].lower():
                    text = msg.get("text", "")
                    code = ''.join(filter(str.isdigit, text))[:6]
                    print(f"X Doğrulama Kodu: {code}")
                    return code
        except: pass
        time.sleep(10)
    print("X kodu gelmedi.")
    return None