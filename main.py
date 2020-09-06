from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
from query_string import QueryString 
if __name__ == "__main__":
    query_string = QueryString()
    ten_the_loai = 'tien-hiep'
    for i in range(100):    
        try:
            link_the_loai = "https://truyenyy.vn/truyen-huyen-huyen/danh-sach/?page="+str(i+1)
            query_string.insert_elastic(ten_the_loai,link_the_loai)
        except Exception as ex:
            print(ex)