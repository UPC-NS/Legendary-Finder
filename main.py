import requests
from ratelimit import limits, sleep_and_retry
from bs4 import BeautifulSoup as bs

nations = []
finds = []

with open("nations.txt", "r") as f:
    nations = f.read().splitlines()
USER = f"UPC's Legendary Finder, being used by {nations.pop(0)}"


@sleep_and_retry
@limits(calls=50, period=30)
def api_call(nation):
    headers = {"User-Agent": USER}
    url = f"https://www.nationstates.net/cgi-bin/api.cgi?q=cards+deck;nationname={nation}"
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(r.headers)
        raise Exception(f'API Response: {r.status_code}')

    return r


for nation in nations:
    print(f"Checking {nation} for legendaries")
    r = bs(api_call(nation).text, "xml")

    for card in r.find_all("CARD"):
        if card.CATEGORY.text == "legendary":
            finds.append(f"{nation} - https://www.nationstates.net/page=deck/card={r.CARDID.text}/season={r.SEASON.text}")

with open("output.txt", "w") as f:
    for find in finds:
        f.write(f"{find}\n")
    