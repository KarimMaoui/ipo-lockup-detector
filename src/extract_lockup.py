import requests, re
from bs4 import BeautifulSoup
from utils import find_lockup_days, try_parse_date

SEC_HEADERS = {"KarimMaoui": "YourName Contact karim.maoui@edu.em-lyon.com"}

def fetch_text(url: str) -> str:
    r = requests.get(url, headers=SEC_HEADERS, timeout=60)
    r.raise_for_status()
    # Beaucoup de filings sont en HTML; on extrait le texte lisible
    soup = BeautifulSoup(r.text, "lxml")
    return soup.get_text(separator=" ", strip=True)

def extract_pricing_date(text: str) -> str | None:
    # Heuristique: cherche "priced on <date>", "pricing date <date>"
    for pat in [r"priced on ([A-Za-z0-9, ]{6,30})", r"pricing date[: ]+([A-Za-z0-9, ]{6,30})"]:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            d = try_parse_date(m.group(1))
            if d: return d
    return None

def extract_lockup_info(filing_url: str) -> dict:
    text = fetch_text(filing_url)
    days = find_lockup_days(text)
    pricing = extract_pricing_date(text)  # peut être None; on tombera sinon sur la filing_date
    return {"lockup_days": days, "pricing_date": pricing}
