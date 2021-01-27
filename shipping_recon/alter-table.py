import pymysql.cursors
from datetime import datetime

DAD = datetime.today().strftime("%Y-%m-%d")


class DB:
    conn = None

    def connect(self, user_id):
        self.conn = pymysql.connect('localhost', 'root', 'evanik@2019', f'invento_{user_id}')

    def query(self, sql, val):
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql, val)
            except:
                pass
            self.conn.commit()
            print(cursor.rowcount, "record(s) affected")
            print('success')
        except (AttributeError, pymysql.err.InterfaceError, pymysql.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql, val)
            except:
                pass
            self.conn.commit()
            print("success11")
        return cursor


db = DB()

f = open("demofile2.txt", "a")

connection = pymysql.connect('localhost', 'root', 'evanik@2019', 'invento')
cursor = connection.cursor()

query = f'SELECT id FROM users WHERE exp_date > DATE("{DAD}");'
cursor.execute(query)
data = cursor.fetchall()
count = 0
for idd in data:
    user_id = idd[0]
    try:
        db.connect(user_id)
        connection = pymysql.connect('localhost', 'root', 'evanik@2019', f'invento_{user_id}')
        cursor = connection.cursor()
        query = "DROP INDEX channel_warehouse_order_id_item_id ON shipping_variance"
        # query = "ALTER TABLE shipping_variance ADD CONSTRAINT uc_item_id UNIQUE (id,item_id);"
        cursor.execute(query)
        data = cursor.fetchone()
        if not data:
            f.write(f'{user_id} -- Truncated\n')
            print(f'{user_id} -- Truncated')

    except Exception as e:
        print(e)
        continue

f.close()
cursor.close()
connection.close()
