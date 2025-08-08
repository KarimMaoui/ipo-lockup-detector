import re
from dateutil import parser as dp

LOCKUP_PATTERNS = [
    r"(\d{2,3})\s*day[s]?\s*lock-?up",                
    r"lock-?up\s*period\s*of\s*(\d{2,3})\s*day[s]?",  
    r"(\d{2,3})\s*days?\s*following\s*the\s*pricing", 
]

def find_lockup_days(text: str) -> int | None:
    lower = text.lower()
    for pat in LOCKUP_PATTERNS:
        m = re.search(pat, lower)
        if m:
            try:
                return int(m.group(1))
            except:
                pass
    return None

def try_parse_date(s: str) -> str | None:
    try:
        return dp.parse(s, fuzzy=True).date().isoformat()
    except Exception:
        return None
