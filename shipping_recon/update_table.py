import pandas as pd
import pymysql.cursors


df = pd.read_csv(r'C:\Users\nikhils3\Downloads\Amazon_UP_ZoneB.csv')

connection = pymysql.connect('117.239.182.180', 'root', 'evanik@2019', 'evanik_main')
cursor = connection.cursor()
id = df['ID'].tolist()
Amazon = df['Amazon'].tolist()
for i, j in zip(id, Amazon):
    sql = "UPDATE pincodes set amazon_region="+"'" + str(j) + "'"+" where id="+"'"+str(i)+"'"+""
    print(sql)
    cursor.execute(sql)
    connection.commit()
    print(cursor.rowcount, "record(s) affected")


