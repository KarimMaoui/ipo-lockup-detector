import requests, datetime as dt
from bs4 import BeautifulSoup

SEC_HEADERS = {"User-Agent": "KarimMaoui Contact karim.maoui@edu.em-lyon.com"}  

def fetch_recent_filings(days_back=14):
    # fenêtre de 2 semaines par défaut
    end = dt.date.today()
    start = end - dt.timedelta(days=days_back)
    url = (
      "https://www.sec.gov/cgi-bin/srch-edgar"
      f"?text=FORM%3D424B4+OR+FORM%3DS-1&first={start:%Y%m%d}&last={end:%Y%m%d}&output=atom"
    )
    r = requests.get(url, headers=SEC_HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml-xml")
    out = []
    for entry in soup.find_all("entry"):
        title = (entry.title or "").get_text(strip=True)
        link = entry.link["href"] if entry.link else None
        updated = (entry.updated or "").get_text(strip=True)
        out.append({"title": title, "filing_url": link, "filing_date": updated})
    return out

if __name__ == "__main__":
    items = fetch_recent_filings()
    for it in items[:5]:
        print(it)
