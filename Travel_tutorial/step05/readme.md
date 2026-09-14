travel_agency_app/
├── .streamlit/
│   └── config.toml           # 테마 및 서버 설정
├── assets/
│   └── images/               # 각 국가 대표 이미지 (korea.jpg, usa.jpg 등)
├── src/
│   ├── components/           # UI 컴포넌트 모듈
│   │   ├── __init__.py
│   │   └── card.py           # 국가별 정보 카드 렌더링
│   ├── data/                 # 국가별 정보 및 링크 데이터
│   │   ├── __init__.py
│   │   └── countries.py
│   └── utils/                # 보조 함수 (이미지 로더 등)
│       └── __init__.py
├── app.py                    # 앱 진입점 (메인 실행 파일)
└── requirements.txt          # 패키지 목록