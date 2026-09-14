# 🌍 프로젝트명 (예: TripPulse / NomadDesk)
> 환율, 날씨, 지도 API를 결합한 여행자 올인원 컨텍스트 앱

---

## 1. 프로젝트 개요 (Overview)
- **목적:** 여행 중 환율 앱, 날씨 앱, 지도 앱을 번갈아 켜야 하는 번거로움을 해결
- **타겟 사용자:** 해외/국내 자유 여행자, 디지털 노마드

---

## 2. 핵심 기능 (Key Features)

### 📍 1. 지도 기반 스마트 핀 (Map API)
- 인터랙티브 지도 탐색 및 현재 위치 추적
- 특정 장소 클릭 시 날씨/환율 통합 정보 팝업

### ⛅ 2. 위치 연동 실시간 날씨 (Weather API)
- 현재 위치 및 검색 목적지의 실시간 기상/주간 예보
- 비/눈 예보 시 실내 관광지 추천 및 알림

### 💱 3. 원터치 환율 계산기 (Exchange Rate API)
- 현지 통화 ↔ 원화(KRW) 실시간 변환
- 카메라/수기 입력 기반 빠른 영수증 금액 계산

---

## 3. 기술 스택 및 API 아키텍처 (Tech Stack & Architecture)
- **Frontend:** (예: React Native / Flutter / Next.js)
- **Backend/Storage:** (예: Supabase / Firebase / Node.js)
- **External APIs:**
  - **Map:** (예: Google Maps Platform / Mapbox)
  - **Weather:** (예: OpenWeatherMap / 기상청 API)
  - **Exchange Rate:** (예: ExchangeRate-API / 한국수출입은행 API)

---

## 4. 데이터 흐름 (Data Flow)
1. `User Location` 감지 (Map)
2. `Location Coordinates` -> `City / Country Code` 변환 (Reverse Geocoding)
3. 위경도 기반 `Weather API` 호출 + 국가 코드 기반 `Exchange Rate API` 호출
4. 통합 대시보드 렌더링

---

## 5. 개발 로드맵 (Roadmap)
- [ ] **Phase 1 (MVP):** 각 API 연동 테스트 및 3단 분할 뷰 프로토타입
- [ ] **Phase 2 (UX 결합):** 지도 핀 클릭 시 날씨·환율 연동 바텀 시트 구현
- [ ] **Phase 3 (추가 기능):** 환율 캐싱(오프라인 대응), 즐겨찾는 도시 프리셋