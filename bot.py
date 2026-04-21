import requests
import os
import time
import schedule
import json
import random

print("=== Passive Income Bot Started ===")

DESIGNS_FOLDER = "designs"
os.makedirs(DESIGNS_FOLDER, exist_ok=True)

NICHES = [
    "funny cat lover gift",
    "motivational gym fitness",
    "dog mom cute",
    "african pride pattern",
    "vintage sunset nature",
    "mushroom cottagecore aesthetic",
    "anime minimalist art",
    "hustle entrepreneur mindset",
    "nurse life appreciation",
    "teacher gift funny",
    "pizza lover humor",
    "plant mom botanical",
    "fishing dad hobby",
    "gamer retro vintage",
    "coffee addict morning",
]

STYLES = [
    "flat vector art, white background, t-shirt design ready",
    "bold typography, minimalist, clean background",
    "retro vintage style, distressed look, poster art",
    "cute cartoon illustration, pastel colors, white background",
    "modern geometric design, simple, white background",
]

def generate_image(prompt, filename):
    formatted_prompt = prompt.replace(" ", "%20")
    url = f"https://image.pollinations.ai/prompt/{formatted_prompt}?width=1024&height=1024&nologo=true"
    print(f"[+] Generating: {prompt[:50]}...")

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=120)
            if response.status_code == 200:
                filepath = os.path.join(DESIGNS_FOLDER, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"    Saved: {filename}")
                return filepath
            elif response.status_code == 429:
                print(f"    Rate limited. Waiting 30 seconds...")
                time.sleep(30)
            else:
                print(f"    Failed: {response.status_code}")
                time.sleep(10)
        except Exception as e:
            print(f"    Error attempt {attempt+1}: {e}")
            time.sleep(20)

    print(f"    Giving up after 3 attempts.")
    return None

def generate_listing(niche):
    titles = [
        f"{niche.title()} — Perfect Gift",
        f"Funny {niche.title()} Design",
        f"Best {niche.title()} Lover Gift",
        f"{niche.title()} Art Print",
        f"Unique {niche.title()} Collection",
    ]
    tags = niche.split() + [
        "gift", "funny", "cute", "aesthetic",
        "trendy", "unique", "art", "design",
        "vintage", "minimalist", "graphic"
    ]
    description = (
        f"Perfect for anyone who loves {niche}. "
        f"Makes a great gift for birthdays, holidays or any occasion. "
        f"Available on t-shirts, hoodies, stickers, mugs, phone cases and more!"
    )
    return {
        "title": random.choice(titles),
        "tags": tags[:15],
        "description": description
    }

def run_daily_job():
    print(f"\n[BOT] Running daily job...")
    results = []
    selected_niches = random.sample(NICHES, 5)

    for i, niche in enumerate(selected_niches):
        style = random.choice(STYLES)
        prompt = f"{niche}, {style}, no watermark, high resolution, professional"
        filename = f"design_{i}_{int(time.time())}.png"
        filepath = generate_image(prompt, filename)

        if filepath:
            listing = generate_listing(niche)
            results.append({
                "file": filename,
                "niche": niche,
                "title": listing["title"],
                "tags": listing["tags"],
                "description": listing["description"]
            })

        time.sleep(15)

    with open("listings_ready.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[BOT] Done! {len(results)} designs generated today.")
    print("[BOT] Check listings_ready.json for upload details.")

run_daily_job()
schedule.every(24).hours.do(run_daily_job)

while True:
    schedule.run_pending()
    time.sleep(60)
