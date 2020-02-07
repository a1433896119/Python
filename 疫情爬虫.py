#爬取全国疫情实施情况
import requests
from bs4 import BeautifulSoup
import re
import pymysql
mainURL = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
req = requests.get(url=mainURL)
#req.encoding = 'utf-8'
html = req.text
soup = BeautifulSoup(html, 'lxml')
db = pymysql.connect(host='127.0.0.1', user='root', password='root', db='pytest', port=3306, charset='utf8')
cursor = db.cursor()
zhcn = """alter table content convert to character set utf8;"""
cursor.execute(zhcn)
def main():
    soup1 = soup.text.replace('{', '')
    soup2 = soup1.replace('"', '')
    soup3 = soup2.replace('\\', '')
    soup4 = soup3.replace('[', '')
    soup5 = soup4.replace(']', '')
    soup6 = soup5.replace('}', '')
    soup7 = re.search('\d{3,10}',soup6).group() #全国确诊
    soup8 = soup6.replace(soup7, '')
    soup9 = re.search('\d{3,10}',soup8).group() #疑似病例
    soup10 = soup8.replace(soup9, '')
    soup11 = re.search('\d{3,10}',soup10).group() #死亡人数
    soup12 = soup10.replace(soup11, '')
    soup13 = re.search('\d{3,10}',soup12).group() #治愈人数
    soup14 = re.search('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', soup12).group() #时间\
    AllPeople = int(soup7)+int(soup9)
    DeadRate = (int(soup11)/AllPeople)*100
    HealRate = (int(soup13)/AllPeople)*100
    print('全国确诊:'+soup7)
    print('疑似病例:'+soup9)
    print('死亡人数:'+soup11)
    print('治愈人数:'+soup13)
    print('截至:'+soup14)
    print("死亡率:%.2f%%" % DeadRate)
    print("治愈率:%.2f%%" % HealRate)
    sql = "INSERT INTO content(id,全国确诊,疑似病例,治愈人数,死亡人数,时间) " \
          "VALUES(null,'{}','{}','{}','{}','{}')"
    sql2 = sql.format((soup7), (soup9), (soup13), (soup11),('截至 '+soup14))
    cursor.execute(sql2)
    db.commit()
    t = soup.text
    last = t[::-1].replace('{', '')
    last1 =last.replace('"', '')
    last2 =last1.replace('\\', '')
    last3 = last2.replace('[', '')
    last4 = last3.replace(']', '')
    last5 = last4.replace('}', '')
    l_Date = re.search('\d{2}.\d{2}', last5).group() #时间
    l_Dates = last5.replace(l_Date, '')
    l_HealRate = re.search('\d{1,2}.\d{1,2}', l_Dates).group()
    l_HealsRate = l_Dates.replace(l_HealRate, '')
    l_DeadRate = re.search('\d{1,2}.\d{1,2}', l_HealsRate).group()
    l_DeadRates = l_HealsRate.replace(l_DeadRate, '')
    last6 = re.search('\d{2,7}',l_DeadRates).group() #治愈人数
    last7 = l_DeadRates.replace(last6, '')
    last8 = re.search('\d{2,7}',last7).group() #死亡人数
    last9 = last7.replace(last8, '')
    last10 = re.search('\d{2,7}',last9).group() #疑似病例
    last11 = last9.replace(last10, '')
    last12 = re.search('\d{2,7}',last11).group() #全国确诊
    print('昨天相比前天增加治愈人数:'+last6[::-1])
    print('昨天相比前天增加死亡人数:'+last8[::-1])
    print('昨天相比前天增加疑似病例:'+last10[::-1])
    print('昨天相比前天增加全国确诊:'+last12[::-1])
    print('昨天时间:'+l_Date[::-1])
if __name__ == '__main__':
    main()