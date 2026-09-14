# folium으로 지도에 마커를 표시하는 예제 코드
# import folium
# 서울 시내 명소 4곳의 좌표(경도/위도)와 이름을 리스트로 받아 folium 지도를 만들고
# 각 좌표에 이름표가 붙은 마커를 찍은 다음, basic_map.html 파일로 저장하는 예제 코드입니다.
# 저장된 basic_map.html 웹 브라우저로 열어서 확인
# 실행 : python 0914_1.py

# 0914_1.py
import os
import folium

# 1. 서울 시내 주요 명소 4곳 데이터
places = [
    {"name": "경복궁", "lat": 37.579617, "lng": 126.977041},
    {"name": "N서울타워", "lat": 37.551169, "lng": 126.988227},
    {"name": "북촌한옥마을", "lat": 37.582604, "lng": 126.983572},
    {"name": "롯데월드타워", "lat": 37.512564, "lng": 127.102540}
]

# 2. 서울 중심부 기준 지도 생성 (차단되지 않는 CartoDB 타일 사용)
seoul_center = [37.5665, 126.9780]
m = folium.Map(location=seoul_center, zoom_start=12, tiles="CartoDB positron")

# 3. 마커 추가
for place in places:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], max_width=200),
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# 4. 파일 저장 및 경로 출력
output_file = "basic_map.html"
m.save(output_file)

absolute_path = os.path.abspath(output_file)
print(f"파일 저장 절대 경로: {absolute_path}")