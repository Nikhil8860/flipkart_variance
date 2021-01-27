import requests
import pymysql.cursors


class DB:
    conn = None

    def connect(self):
        self.conn = pymysql.connect('117.239.182.180', 'root', 'evanik@2019', 'evanik_main')

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql)
            except:
                pass
            self.conn.commit()
            print(sql)
            print(cursor.rowcount, "record(s) affected")
            print('success')
        except (AttributeError, pymysql.err.InterfaceError, pymysql.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql)
            except:
                pass
            self.conn.commit()
            print("success11")
        return cursor


db = DB()
db.connect()
connection = pymysql.connect('117.239.182.180', 'root', 'evanik@2019', 'evanik_main')
cursor = connection.cursor()
query = "SELECT pincode FROM pincodes LIMIT 14000, 8000"
cursor.execute(query)
pincode = cursor.fetchall()
for i in pincode:
    if i[0]:
        url = f"https://api.postalpincode.in/pincode/{i[0]}"
        data = requests.get(url)
        if data.json()[0]['Status'] != 'Error':
            District = data.json()[0]['PostOffice'][0]['District']
            query1 = "UPDATE pincodes SET District=" + "'" + District + "'" + " WHERE pincode=" + str(
                i[0]) + " and District IS NULL"
            db.query(query1)

