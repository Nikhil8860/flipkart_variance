import pymysql.cursors
import requests
connection = pymysql.connect('localhost', 'root', 'evanik@2019', 'evanik_erp_cronjobs')
cursor = connection.cursor()
query = "SELECT i.UserId FROM inv_userlist AS i WHERE i.exp_date > NOW() AND i.type IN ('flipkart', 'amazon') ORDER BY i.UserId DESC"
cursor.execute(query)
data = cursor.fetchall()
for user in data:
    url = "http://cron.evanik.com/regular/filpkartcommsioncapture.php?UserID=" + str(user[0])
    r = requests.get(url)
    print(r.text)
