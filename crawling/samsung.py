import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 크롤링 대상 종목 코드 및 설정
code = "005930"  # 삼성전자
base_url = f"https://finance.naver.com/item/sise_day.naver?code={code}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

data = []

# 2. 1페이지부터 5페이지까지 수집 (약 50영업일)
total_pages = 5
print(f"삼성전자 주가 데이터 수집 시작 (총 {total_pages}페이지)...")

for page in range(1, total_pages + 1):
    url = f"{base_url}&page={page}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"접속 실패 (Status: {response.status_code})")
        break
        
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table.type2 tr")
    
    for row in rows:
        cols = row.select("td")
        
        # 유효한 행 데이터 추출
        if len(cols) >= 7 and cols[0].get_text(strip=True):
            date = cols[0].get_text(strip=True)
            close_price = int(cols[1].get_text(strip=True).replace(",", ""))
           # 전일비 텍스트 가져오기 (콤마 제거)
            raw_diff_text = cols[2].get_text(strip=True).replace(",", "")

            # 하락 여부 확인
            is_down = "하락" in raw_diff_text or "하한" in raw_diff_text

            # 한글 텍스트 제거 후 순수 숫자만 추출
            diff_num_str = raw_diff_text.replace("상승", "").replace("하락", "").replace("보합", "").replace("상한가", "").replace("하한가", "").strip()

            # 숫자로 변환 (하락이면 음수, 보합/빈값이면 0)
            if diff_num_str.isdigit():
                diff = -int(diff_num_str) if is_down else int(diff_num_str)
            else:
                diff = 0
                
            open_price = int(cols[3].get_text(strip=True).replace(",", ""))
            high_price = int(cols[4].get_text(strip=True).replace(",", ""))
            low_price = int(cols[5].get_text(strip=True).replace(",", ""))
            volume = int(cols[6].get_text(strip=True).replace(",", ""))
            
            data.append({
                "날짜": date,
                "종가": close_price,
                "전일비": diff,
                "시가": open_price,
                "고가": high_price,
                "저가": low_price,
                "거래량": volume
            })
            
    time.sleep(0.5)  # 서버 부하 방지 딜레이

# 3. 데이터프레임 변환
df = pd.DataFrame(data)

# 4. 엑셀 파일(.xlsx)로 저장
excel_filename = "samsung_stock_price.xlsx"

# openpyxl 엔진을 사용하여 서식과 함께 깔끔하게 저장
with pd.ExcelWriter(excel_filename, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="일별시세", index=False)
    
    # 워크시트 객체 가져와서 열 너비 자동 조정
    ws = writer.sheets["일별시세"]
    for col in ws.columns:
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = 15

print(f"수집 완료! '{excel_filename}' 파일로 저장되었습니다.")