import pymysql.cursors
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import re

connection = pymysql.connect('13.233.239.105', 'root', 'evanik@2019', 'invento')
cursor = connection.cursor()
query = f'SELECT id FROM users WHERE exp_date > "{datetime.today().strftime("%Y-%m-%d")}";'
cursor.execute(query)
data = cursor.fetchall()
STATUS = True
count = 0
for idd in data:
    user_id = idd[0]
    if user_id == 76806 or user_id == 78021 or user_id == 78166 or user_id == 78498 or user_id == 78598:
        continue
    print(user_id)
    # count +=1
    connection1 = pymysql.connect('13.233.239.105', 'root', 'evanik@2019', 'invento_{}'.format(user_id))
    cursor1 = connection1.cursor()
    query1 = "SELECT id FROM channels WHERE type='flipkart';"
    cursor1.execute(query1)
    data1 = cursor1.fetchall()
    for iddd in data1:
        channel_id = iddd[0]
        print(channel_id)
        for j in range(2):
            requests.get(
                f'http://aws.evanik.com/cronjobs/Others/autoCron.php?UserID={user_id}&ChannelID={channel_id}&RequestType=Payments')
            print(f'repeat - {j}')
            time.sleep(5)
        url1 = f'http://aws.evanik.com/cronjobs/alok/flipkart/filpkartsnapdealmonth.php?UserID={user_id}&channel_id={channel_id}&yymm=2020_12'
        page = requests.get(url1)
        time.sleep(10)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table')
        print(table)
        try:
            for i in range(8, 500, 9):
                try:
                    if table.find_all('td')[i - 7].text:
                        s_no = table.find_all('td')[i - 7].text
                        moved = table.find_all('td')[i - 6].text
                        nft = table.find_all('td')[i].text
                        print(s_no, moved, nft, sep='--')
                        print('hello', moved, type(moved), sep='--')
                        if int(moved) != 1:
                            while STATUS:
                                url2 = f"http://aws.evanik.com/cronjobs/Flipkart/Payment/flipkartPaymentsSync2.php?UserID={user_id}&channel_id={channel_id}&settlementRefId={nft}"
                                page2 = requests.get(url2)
                                time.sleep(10)
                                soup2 = BeautifulSoup(page2.content, 'html.parser')
                                print(soup2)
                                a = re.search('Net Payout:=', soup2.text)
                                b = re.search(
                                    'You have exceeded your daily quota of 20 reports, please try again tomorrow.',
                                    soup2.text)
                                if not a or not b:
                                    STATUS = False
                except IndexError as e:
                    pass
        except Exception as e:
            print(e)
