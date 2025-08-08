import pandas as pd
from datetime import date
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"

def render_table(df: pd.DataFrame, n=10) -> str:
    cols = ["Ticker", "Company", "IPODate", "LockUpDays", "LockUpEnd"]
    df = df.loc[:, cols].sort_values("LockUpEnd").head(n)
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join(["---"]*len(cols)) + " |"
    rows = "\n".join("| " + " | ".join(str(df.iloc[i][c]) for c in cols) + " |" for i in range(len(df)))
    return "\n".join([header, sep, rows])

if __name__ == "__main__":
    df = pd.read_csv("data/ipo_lockup.csv")
    table_md = render_table(df)
    md = f"""# IPO & Lock-Up Event Detector

_Last update: {date.today().isoformat()}_

## Upcoming lock-up expiries
{table_md}

See `data/ipo_lockup.ics` to import events into your calendar.
"""
    README.write_text(md, encoding="utf-8")
