from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re

chromedriver_path = R'C:\Users\lautszchun\Desktop\data_science_book\air ticket scrapper\chromedriver.exe' 
driver = webdriver.Chrome(executable_path=chromedriver_path)

# url='https://www.kayak.com.hk/flights/HKG-NRT/2020-09-15/2020-09-20?sort=bestflight_a&fs=stops=~0'
url='https://www.kayak.com.hk/flights/HKG-NRT/2020-09-14/2020-09-20?sort=bestflight_a'
driver.get(url)

sleep(3)
xp_popup_close = '//button[contains(@id,"close-button") and contains(@class,"Button-No-Standard-Style close")]'
pop_up=driver.find_element_by_xpath(xp_popup_close)
pop_up.click()

sleep(3)
soup=BeautifulSoup(driver.page_source, 'lxml')

deptimes = soup.find_all('span', attrs={'class': 'depart-time base-time'})
arrtimes = soup.find_all('span', attrs={'class': 'arrival-time base-time'})

deptime = []
for div in deptimes:
    deptime.append(div.getText())    
        
arrtime = []
for div in arrtimes:
    arrtime.append(div.getText())   

# print("go time",deptime)
# print("back time",arrtime)

regex = re.compile('Common-Booking-MultiBookProvider (.*)multi-row Theme-featured-large(.*)')
price_list = soup.find_all('div', attrs={'class': regex})

price = []
cur=[]
for div in price_list:
    text=div.getText().split('\n')[3]
    # print(text)
    find=text.find('$',0,len(text))+1
    currency=text[:find]
    digit=''
    for a in text:
        if a>='0' and a<='9':
            digit+=a
    digit=int(digit)
    price.append(digit)
    cur.append(currency)
    # print(div.getText().split('\n'))

# print(price)
# print(cur)

go_num_of_stop=[]
go_air=[]
go_takeoff=[]
go_arrive=[]
re_direct=re.compile('(.*)-info-leg-0')
go_direct=soup.find_all(attrs={'id': re_direct})
for sub_1 in go_direct:
    sub_2=sub_1.find_all(attrs={'class':'container'})
    for sub_3 in sub_2:
        sub_4=sub_3.find_all(attrs={'class':'section stops'})
        for z in sub_4:
            k=z.find_all(attrs={'class':'top'})[0]
            l=k.getText()
            # print('fffffffffffffffffffffffffffffffffffffffffffff',len(k))
            zero=True
            for text in l:
                if text>='0' and text<='9':
                    zero=False
                    go_num_of_stop.append(int(text))
            if zero:
                go_num_of_stop.append(0)

        sub_4=sub_3.find_all(attrs={'class':'section times'})
        for z in sub_4:
            k=z.find_all(attrs={'class':'bottom'})[0]
            l=k.getText()
            air=''
            for g in l:
                if g!='\n' and g!=' ':
                    air+=g
            go_air.append(air)
            k=z.find_all(attrs={'class':'time-pair'})
            l=k[0].getText()
            go_time_fly=''
            for g in l:
                if g!='\n' and g!=' ':
                    go_time_fly+=g
            go_takeoff.append(go_time_fly)
            l=k[1].getText()
            go_time_arrive=''
            for g in l:
                if g!='\n' and g!=' ':
                    go_time_arrive+=g
            go_arrive.append(go_time_arrive)

back_num_of_stop=[]
back_air=[]
back_takeoff=[]
back_arrive=[]
re_direct=re.compile('(.*)-info-leg-1')
go_direct=soup.find_all(attrs={'id': re_direct})
for sub_1 in go_direct:
    sub_2=sub_1.find_all(attrs={'class':'container'})
    for sub_3 in sub_2:
        sub_4=sub_3.find_all(attrs={'class':'section stops'})
        for z in sub_4:
            k=z.find_all(attrs={'class':'top'})[0]
            l=k.getText()
            zero=True
            for text in l:
                if text>='0' and text<='9':
                    zero=False
                    back_num_of_stop.append(int(text))
            if zero:
                back_num_of_stop.append(0)

        sub_4=sub_3.find_all(attrs={'class':'section times'})
        for z in sub_4:
            k=z.find_all(attrs={'class':'bottom'})[0]
            l=k.getText()
            air=''
            for g in l:
                if g!='\n' and g!=' ':
                    air+=g
            back_air.append(air)
            k=z.find_all(attrs={'class':'time-pair'})
            l=k[0].getText()
            back_time_fly=''
            for g in l:
                if g!='\n' and g!=' ':
                    back_time_fly+=g
            back_takeoff.append(back_time_fly)
            l=k[1].getText()
            back_time_arrive=''
            for g in l:
                if g!='\n' and g!=' ':
                    back_time_arrive+=g
            back_arrive.append(back_time_arrive)


#put time in
cols={'Out day','back day','go_num_of_stop','back_num_of_stop','go_air','back_air','currency','price'}
data=pd.DataFrame({'Out day':'14-09-2020','back day':'20-09-2020','go_num_of_stop':go_num_of_stop
                    ,'back_num_of_stop':back_num_of_stop,'go_air':go_air,'back_air':back_air,'currency':cur,'price':price})[cols]

print(data)