# panel/app.py
from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    accounts = []
    if os.path.exists("hesaplar.txt"):
        with open("hesaplar.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 3:
                    accounts.append({"email": parts[0], "password": parts[1], "phone": parts[2]})
    return render_template("panel.html", accounts=accounts)

# VERCEL İÇİN GEREKLİ!
application = app