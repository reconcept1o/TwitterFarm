# mail_api.py → TAM KOD
import requests
import random

def mail_uret():
    domains = ["tiffincrane.com", "mail.tm", "temp-mail.org"]
    username = f"bot{random.randint(1000,9999)}"
    domain = random.choice(domains)
    email = f"{username}@{domain}"
    
    # mail.tm için API (örnek)
    if "mail.tm" in domain:
        try:
            r = requests.get("https://api.mail.tm/accounts", 
                           headers={"Content-Type": "application/json"},
                           json={"address": email, "password": "Pass123!@#"})
            if r.status_code == 201:
                return email
        except:
            pass
    return email