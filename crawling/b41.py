from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

data =[] #하나씩 읽어서 여기다 모을 것

for i in range(1,5):
    response = requests.get(f"https://startcoding.pythonanywhere.com/basic?page={i}")
    html=response.text
    soup= BeautifulSoup(html,'html.parser')

    items = soup.select(".product")


    # print(f'가져온 상품 개수: {len(items)}개\n'+ '-'*30)

    for item in items:
        category = item.select_one(".product-category").text #카테고리
        category_name = item.select_one(".product-name").text # 상품명
        category_link = item.select_one(".product-name > a").attrs["href"] #상품상세 페이지 링크 '>' 내 후손만 찾음
        price = item.select_one(".product-price").text.split("원")[0].replace(",","") + "원" #가격
        data.append([category,category_name, category_link, price])

        print(category,category_name, category_link, price)

df = pd.DataFrame(data, columns=["카테고리","상품 명","상세페이지링크","가격"])

df.to_excel("data.xlsx",index=False)
