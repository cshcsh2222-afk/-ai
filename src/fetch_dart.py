import json, os, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
OUT = ROOT / "data" / "financials.json"
API_KEY = os.getenv("DART_API_KEY")
if not API_KEY:
    raise SystemExit("DART_API_KEY 환경변수가 없습니다.")

BASE = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
CORP_CODE = CONFIG["corp_code"]
REPORT_CODE = CONFIG["report_code"]
YEARS = int(CONFIG.get("years", 5))


def amount(x):
    if x in (None, ""):
        return None
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return None


def fetch(year):
    params = {
        "crtfc_key": API_KEY,
        "corp_code": CORP_CODE,
        "bsns_year": str(year),
        "reprt_code": REPORT_CODE,
        "fs_div": "C"
    }
    r = requests.get(BASE, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

now_year = __import__("datetime").datetime.now().year
rows, errors = [], []
for year in range(now_year, now_year - YEARS - 1, -1):
    data = fetch(year)
    if data.get("status") == "000":
        for x in data.get("list", []):
            rows.append({
                "year": year, "fs_div": x.get("fs_div"), "sj_div": x.get("sj_div"),
                "account_id": x.get("account_id"), "account_nm": x.get("account_nm"),
                "thstrm_amount": amount(x.get("thstrm_amount")),
                "frmtrm_amount": amount(x.get("frmtrm_amount")),
                "bfefrmtrm_amount": amount(x.get("bfefrmtrm_amount")),
                "currency": x.get("currency")
            })
    else:
        errors.append({"year": year, "status": data.get("status"), "message": data.get("message")})
    time.sleep(0.2)

payload = {
    "meta": {
        "corp_code": CORP_CODE, "corp_name": CONFIG["corp_name"],
        "report_code": REPORT_CODE, "fs_div": "C", "source": "OpenDART",
        "updated_at": __import__("datetime").datetime.now().isoformat(),
        "errors": errors
    },
    "rows": rows
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"saved {len(rows)} rows")
