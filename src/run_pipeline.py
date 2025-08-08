import csv, os
from datetime import date, timedelta
from pathlib import Path

from fetch_ipo import fetch_recent_filings
from extract_lockup import extract_lockup_info
from generate_calendar import build_calendar

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CSV_PATH = DATA_DIR / "ipo_lockup.csv"
ICS_PATH = DATA_DIR / "ipo_lockup.ics"

def ensure_csv():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Ticker","Company","IPODate","LockUpDays","LockUpEnd","FilingURL"])

def upsert_row(row):
    # charge existant
    rows = []
    seen = False
    if CSV_PATH.exists():
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    # clé = FilingURL (à défaut)
    key = row["FilingURL"]
    for r in rows:
        if r["FilingURL"] == key:
            r.update(row)
            seen = True
            break
    if not seen:
        rows.append(row)
    # réécrit
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Ticker","Company","IPODate","LockUpDays","LockUpEnd","FilingURL"])
        w.writeheader()
        w.writerows(rows)

def main():
    ensure_csv()

    # 1) filings récents (14 jours par défaut)
    filings = fetch_recent_filings(days_back=14)

    # 2) pour chaque filing, essaie d’extraire lock-up + pricing
    for f in filings:
        info = extract_lockup_info(f["filing_url"])  # {"lockup_days": int|None, "pricing_date": "YYYY-MM-DD"|None}

        # heuristiques simples
        lock_days = info.get("lockup_days")
        ipo_date = (f.get("filing_date") or "")[:10]  # fallback
        pricing_date = info.get("pricing_date") or ipo_date

        lock_end = ""
        if lock_days and pricing_date:
            try:
                y,m,d = map(int, pricing_date.split("-"))
                lock_end = str(date(y,m,d) + timedelta(days=int(lock_days)))
            except Exception:
                lock_end = ""

        row = {
            "Ticker": f.get("ticker",""),
            "Company": f.get("company",""),
            "IPODate": pricing_date or "",
            "LockUpDays": str(lock_days or ""),
            "LockUpEnd": lock_end,
            "FilingURL": f["filing_url"],
        }
        upsert_row(row)

    # 3) (re)génère le calendrier .ics
    build_calendar(str(CSV_PATH), str(ICS_PATH))

    # 4) met à jour le README (tableau des prochaines expirations)
    os.system("python src/update_readme.py")

if __name__ == "__main__":
    main()
