import requests
from bs4 import BeautifulSoup
import random
import json
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1411707301391368222/78Dg-gLraRJgeomiLBkS_GRgZOXZJu2RQ_IXaXqxbZmyZGugr9_H_cp4HjYKclKNAjAv"
USED_FILE = "used_words.json"

if os.path.exists(USED_FILE):
    with open(USED_FILE, "r") as f:
        used_words = set(json.load(f))
else:
    used_words = set()

URL = "https://www.enchantedlearning.com/wordlist/objects.shtml"

def fetch_objects():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    words = [li.text.strip().lower() for li in soup.find_all("li")]
    return [w for w in words if w not in used_words]

def get_random_object():
    objects = fetch_objects()
    if not objects:
        return None
    word = random.choice(objects)
    used_words.add(word)
    with open(USED_FILE, "w") as f:
        json.dump(list(used_words), f)
    return word

def send_webhook():
    word = get_random_object()
    if word:
        phrase = f"HELLO KITTY ({word})"
        requests.post(WEBHOOK_URL, json={"content": phrase})
        print(f"✅ Sent: {phrase}")
    else:
        print("All objects used!")

if __name__ == "__main__":
    send_webhook()
