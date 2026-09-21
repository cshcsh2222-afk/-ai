# DART 재무분석 Agent — 삼성전자

OpenDART API에서 삼성전자(고유번호 `00126380`)의 사업보고서 재무정보를 가져와 주요 재무수치와 재무비율을 계산하고 GitHub Pages 대시보드로 보여주는 템플릿입니다.

## 1. API 키 입력
OpenDART에서 40자리 API 인증키를 발급받습니다: https://opendart.fss.or.kr/

GitHub 저장소 → **Settings → Secrets and variables → Actions → New repository secret**
- Name: `DART_API_KEY`
- Secret: 발급받은 40자리 인증키

API 키를 코드에 직접 입력하지 마세요.

## 2. 자동 업데이트
GitHub Actions가 매일 한국시간 06:10에 실행되도록 구성되어 있습니다. `workflow_dispatch`로 수동 실행도 가능합니다.

## 3. GitHub Pages
Repository → Settings → Pages → Source에서 GitHub Actions를 선택합니다.

## 4. 로컬 실행
```bash
pip install -r requirements.txt
export DART_API_KEY="발급받은키"
python src/fetch_dart.py
python src/build_dashboard.py
```

Windows PowerShell:
```powershell
$env:DART_API_KEY="발급받은키"
python src/fetch_dart.py
python src/build_dashboard.py
```

## 분석 기준
대시보드는 매출, 영업이익, 순이익, 영업이익률, 순이익률, 부채비율, 자기자본비율, 영업활동현금흐름, FCF 등을 보여줍니다. 재무분석 가이드의 원칙에 따라 단일 비율보다 성장→이익률→현금흐름→차입 부담의 연결을 볼 수 있도록 구성했습니다.
