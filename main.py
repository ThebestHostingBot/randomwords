import requests
from bs4 import BeautifulSoup
import random
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1411707301391368222/78Dg-gLraRJgeomiLBkS_GRgZOXZJu2RQ_IXaXqxbZmyZGugr9_H_cp4HjYKclKNAjAv"
URL = "https://www.enchantedlearning.com/wordlist/objects.shtml"

used_words = set()

def fetch_objects():
    """Scrape website and return list of unused objects."""
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, "html.parser")
        words = [li.text.strip().lower() for li in soup.find_all("li")]
        return [w for w in words if w not in used_words]
    except Exception as e:
        print(f"Error fetching objects: {e}")
        return []

def get_random_object():
    objects = fetch_objects()
    if not objects:
        return None
    word = random.choice(objects)
    used_words.add(word)
    return word

def send_webhook():
    word = get_random_object()
    if word:
        phrase = f"HELLO KITTY ({word})"
        try:
            r = requests.post(WEBHOOK_URL, json={"content": phrase})
            if r.status_code == 204:
                print(f"✅ Sent: {phrase}")
            else:
                print(f"❌ Failed to send: {r.status_code}")
        except Exception as e:
            print(f"❌ Error sending webhook: {e}")
    else:
        print("All objects used!")

# ===== MAIN LOOP =====
if __name__ == "__main__":
    while True:
        send_webhook()
        time.sleep(120)  # 10 minutes
