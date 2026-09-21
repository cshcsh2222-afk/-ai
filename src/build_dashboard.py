import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/financials.json").read_text(encoding="utf-8"))
rows = data["rows"]

def norm(s): return str(s).replace(" ", "").replace("\n", "")
def pick(y, names):
    for r in rows:
        if r["year"] == y and norm(r["account_nm"]) in {norm(n) for n in names}:
            return r["thstrm_amount"]
    return None

def div(a,b): return None if a is None or not b else a/b

years = sorted({r["year"] for r in rows})
rec=[]
for y in years:
    revenue=pick(y,["매출액","수익(매출액)"]); op=pick(y,["영업이익","영업이익(손실)"]); ni=pick(y,["당기순이익","당기순이익(손실)"])
    assets=pick(y,["자산총계"]); liab=pick(y,["부채총계"]); equity=pick(y,["자본총계"]); cfo=pick(y,["영업활동현금흐름","영업활동으로인한현금흐름"]); capex=pick(y,["유형자산의취득","유형자산 취득"])
    rec.append({"year":y,"revenue":revenue,"op":op,"ni":ni,"assets":assets,"liab":liab,"equity":equity,"cfo":cfo,"capex":capex,"op_margin":div(op,revenue),"net_margin":div(ni,revenue),"debt_ratio":div(liab,equity),"equity_ratio":div(equity,assets),"fcf":(cfo-abs(capex)) if cfo is not None and capex is not None else None})

js=json.dumps(rec,ensure_ascii=False)
html='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>삼성전자 DART 재무 Dashboard</title><script src="https://cdn.jsdelivr.net/npm/chart.js"></script><style>body{font-family:system-ui,sans-serif;margin:0;background:#f6f7fb;color:#1f2937}main{max-width:1200px;margin:auto;padding:32px 18px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}.card,.panel{background:white;border-radius:16px;padding:18px;margin:14px 0;box-shadow:0 2px 12px #0001}.value{font-size:24px;font-weight:750;margin-top:8px}.muted{color:#6b7280}table{width:100%;border-collapse:collapse}th,td{padding:8px;border-bottom:1px solid #eee;text-align:right}th:first-child,td:first-child{text-align:left}</style></head><body><main><h1>삼성전자 DART 재무 Dashboard</h1><p class="muted">OpenDART 사업보고서 · 연결 기준 · 자동 업데이트</p><div id="cards" class="grid"></div><div class="panel"><h2>매출 · 영업이익 · 순이익</h2><canvas id="profit"></canvas></div><div class="panel"><h2>주요 재무비율</h2><canvas id="ratio"></canvas></div><div class="panel"><h2>연도별 주요 수치</h2><div style="overflow:auto"><table id="tbl"></table></div></div><p class="muted">자료: OpenDART API. 자동 계산값은 원자료와 공시 정의를 확인하여 사용하세요.</p></main><script>const rows=__DATA__;const fmt=v=>v==null?'-':new Intl.NumberFormat('ko-KR',{maximumFractionDigits:0}).format(v);const pct=v=>v==null?'-':(v*100).toFixed(1)+'%';const last=rows[rows.length-1]||{};const cards=[['매출액',fmt(last.revenue)],['영업이익',fmt(last.op)],['영업이익률',pct(last.op_margin)],['당기순이익',fmt(last.ni)],['부채비율',pct(last.debt_ratio)],['자기자본비율',pct(last.equity_ratio)],['영업현금흐름',fmt(last.cfo)],['FCF',fmt(last.fcf)]];document.getElementById('cards').innerHTML=cards.map(x=>`<div class="card"><div class="muted">${x[0]}</div><div class="value">${x[1]}</div></div>`).join('');const labels=rows.map(r=>r.year);new Chart(document.getElementById('profit'),{type:'line',data:{labels,datasets:[{label:'매출액',data:rows.map(r=>r.revenue)},{label:'영업이익',data:rows.map(r=>r.op)},{label:'순이익',data:rows.map(r=>r.ni)}]},options:{responsive:true}});new Chart(document.getElementById('ratio'),{type:'line',data:{labels,datasets:[{label:'영업이익률',data:rows.map(r=>r.op_margin*100)},{label:'순이익률',data:rows.map(r=>r.net_margin*100)},{label:'부채비율',data:rows.map(r=>r.debt_ratio*100)},{label:'자기자본비율',data:rows.map(r=>r.equity_ratio*100)}]},options:{responsive:true}});document.getElementById('tbl').innerHTML='<tr><th>연도</th><th>매출액</th><th>영업이익</th><th>순이익</th><th>영업이익률</th><th>부채비율</th><th>CFO</th><th>FCF</th></tr>'+rows.slice().reverse().map(r=>`<tr><td>${r.year}</td><td>${fmt(r.revenue)}</td><td>${fmt(r.op)}</td><td>${fmt(r.ni)}</td><td>${pct(r.op_margin)}</td><td>${pct(r.debt_ratio)}</td><td>${fmt(r.cfo)}</td><td>${fmt(r.fcf)}</td></tr>`).join('');</script></body></html>'''.replace('__DATA__',js)
(ROOT/'docs/index.html').write_text(html,encoding='utf-8')
