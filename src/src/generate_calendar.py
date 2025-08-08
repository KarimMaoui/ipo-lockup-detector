import pandas as pd
from datetime import date, timedelta
from ics import Calendar, Event

def build_calendar(csv_path: str, ics_path: str):
    df = pd.read_csv(csv_path)
    cal = Calendar()
    for _, row in df.iterrows():
        if pd.isna(row.get("LockUpEnd")): 
            continue
        event = Event()
        event.name = f"Lock-up expiry: {row['Ticker']} ({row['Company']})"
        event.begin = str(row["LockUpEnd"])
        event.make_all_day()
        cal.events.add(event)
    with open(ics_path, "w") as f:
        f.writelines(cal)
