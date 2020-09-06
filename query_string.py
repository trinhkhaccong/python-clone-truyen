# -*- coding: utf-8 -*-
from datetime import datetime
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from unidecode import unidecode
import time
import re
from unidecode import unidecode;
from elasticsearch import Elasticsearch
es = Elasticsearch(
    ['localhost'],
    port=9200,
)
class QueryString:
    def insert_elastic(self,ten_truyen,link_web_truyen):
        try:
            print(link_web_truyen)
            session = HTMLSession()
            r = session.get(link_web_truyen)
            a = BeautifulSoup(r.html.html, 'lxml')
            tile_and_href  = a.find_all('li', {"class":"with-border"})
            check_list = list(set(tile_and_href))

            for i in check_list:
                try:
                    id = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    title =(i.find("h3",{"class":"book-title"})).find('a')
                    url_truyen = (i.find("a",{"class":"book-img position-relative"})).attrs["href"]
                    tac_gia=i.find("a",{"class":"book-author mr-auto"})
                    link_image=(i.find('img')).attrs["data-src"]
                    count_chuong =i.find("span",{"class":"badge-novel mr-1"})
                    date_time = (i.find("time",{"class":"timeago align-middle"})).attrs["datetime"]
                    list_the_loai = i.find_all("li",{"class":"tag"})
                    the_loai=""
                    find_content =""

                    session_child = HTMLSession()
                    r_child = session.get("https://truyenyy.vn"+url_truyen)
                    a_child = BeautifulSoup(r_child.html.html, 'lxml')
                    find_content = a_child.find("section",{"class":"section intro"})
                    the_loai = (a_child.find("ul",{"class":"tag-list list-unstyled mt-2"})).get_text()

                    data_in={
                        "the_loai":the_loai.replace("\n","-"),
                        "id_the_loai": unidecode(((the_loai.lower()).replace(" ","-")).replace("\n"," ")),
                        "ten":title.get_text(),
                        "id_ten":url_truyen.split("/")[2],
                        "tac_gia":tac_gia.get_text(),
                        "date":date_time,
                        "link":link_image,
                        "chuong":count_chuong.get_text(),
                        "content":find_content.get_text()
                    }
                    data_search ={
                        "query": {
                        "query_string": {
                            "query": "ten:\""+title.get_text()+"\"",
                            "default_operator": "and"
                            }
                        }
                    }
                    res_search = es.search(index="menu_truyen", body=data_search)
                    if(res_search['hits']['total']['value'] == 0):
                        res = es.index(index="menu_truyen", id=int(id), body=data_in)
                        time.sleep(1)

                    self.find_tring("https://truyenyy.vn"+url_truyen,title.get_text(),url_truyen.split("/")[2],int(count_chuong.get_text().replace(",","")))
                    
                except Exception as ex:
                    print(ex)
                    continue
        except Exception as ex:
                print(ex)
        # print(text)
        


    def find_tring(self,link_chuong,ten_truyen,id_ten,x):
       
            for chuong in range(x):
                try:
                    link_convert = link_chuong+"chuong-"+str(chuong+1)+".html"
                    session = HTMLSession()
                    r = session.get(link_convert)
                    a = BeautifulSoup(r.html.html, 'lxml')

                    tile_chap  = a.find('h1', {"class":"chapter-title"})
                    data = a.find('div', {"class":"inner"})
                    # print(text_chaper)
                    # print(text)
                    id = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    insert_data = {
                        "ten":ten_truyen,
                        "id_ten":id_ten,
                        "date":(datetime.now()).strftime("%Y-%m-%dT%H:%M:%S"),
                        "chuong": tile_chap.get_text(),
                        "id_chuong":"chuong-"+str(chuong+1),
                        "content":data.get_text()
                    }
                    res = es.index(index="data_truyen", id=int(id), body=insert_data)
                    print(tile_chap.get_text())
                except Exception as ex:
                    print(ex)
                    break
