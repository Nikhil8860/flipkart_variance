import pymysql.cursors
import math
import fk_payment_calculator
from datetime import datetime
from dateutil.relativedelta import *


class FlipkartReco:

    def __init__(self, user_id):
        self.user_id = user_id
        self.connection = pymysql.connect('localhost', 'root', 'evanik@2019', f'invento_{user_id}')
        self.connection_evanik_main = pymysql.connect('localhost', 'root', 'evanik@2019', 'evanik_main')
        self.cursor = self.connection.cursor()
        self.cursor_evanik_main = self.connection_evanik_main.cursor()
        self.applicable_zone = None
        self.conn = None
        self.data = None

    def connect(self):
        self.conn = pymysql.connect('localhost', 'root', 'evanik@2019', f'invento_{self.user_id}')

    def query(self, sql, val=None):
        try:
            self.connect()
            cursor = self.conn.cursor()
            try:
                if "SELECT" in sql:
                    cursor.execute(sql)
                    self.data = self.cursor.fetchall()
                else:
                    cursor.execute(sql, val)
            except Exception as e:
                print(e)
            self.conn.commit()
            print(cursor.rowcount, "record(s) affected")
        except (AttributeError, pymysql.err.InterfaceError, pymysql.OperationalError, pymysql.err.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            try:
                if "SELECT" in sql:
                    cursor.execute(sql)
                    self.data = self.cursor.fetchall()
                else:
                    cursor.execute(sql, val)
            except Exception as e:
                print(e)
            self.conn.commit()
            print(cursor.rowcount, "record(s) affected Success")

        return cursor

    def get_tiers(self, order_date, seller_id):
        """
        This function will take the order_id and seller_id

        :param order_date:
        :param seller_id:
        :return: tier
        """
        query = "SELECT tier FROM channel_tiers WHERE " + "'" + str(
            order_date) + "'" + " BETWEEN start_date AND end_date and sellerId=" + "'" + seller_id + "'"
        print(query)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        print("TIERS : ", data)
        if data:
            tiers = data[0]
        else:
            tiers = 'bronze'

        return tiers

    def get_state(self):

        date_now = datetime.today().date()
        date_six_prior = (date_now - relativedelta(months=6)).strftime("%Y-%m-%d")

        query = f"""
                SELECT s.PinCode AS To_pincode,ch.postal_code AS From_pincode,
                s.whid,s.OrderId,s.warehouse_id, s.OrderItemID, s.shippingZone,s.sale_status, s.date, c.type, s.weight,
                s.shipmentLength, s.shipmentBreadth, s.shipmentHeight,p.ShippingFee,ch.sellerId,pr.length,pr.breadth, 
                pr.height,pr.weight FROM sales AS s
                LEFT JOIN channel_warehouse AS ch ON s.SellerId=ch.SellerId AND s.whid=ch.whid
                LEFT JOIN channels AS c ON c.sellerId=ch.sellerId
                LEFT JOIN payments_process AS p ON p.OrderItemID=s.OrderItemID
                LEFT JOIN products AS pr ON pr.code = s.SKUcode
                WHERE (s.PinCode IS NOT NULL AND s.PinCode!=0 AND ch.postal_code IS NOT NULL AND c.type='flipkart' AND
                (s.date BETWEEN '{date_six_prior}' and '{date_now}')) GROUP BY p.OrderItemID LIMIT 100
        """
        OBJ.query(query)
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
        except pymysql.err.OperationalError:
            self.cursor.execute(query)
            data = self.cursor.fetchall()

        for i in data:
            to_pin = i[0]
            from_pin = i[1]
            whid = i[2]
            order_id = i[3]
            warehouse_id = i[4]
            order_item_id = i[5]
            shipping_zone = i[6]
            sale_status = i[7]
            order_date = i[8]
            channel = i[9]
            if i[10]:
                weight = float(i[10])
                shipment_length = float(i[11])
                shipment_breath = float(i[12])
                shipment_height = float(i[13])

                calculated_weight = (shipment_length * shipment_breath * shipment_height) / 5000
                applied_weight = max(weight, calculated_weight)
                # convert weight to ceil 0.5
                applied_weight = 0.5 * math.ceil(2.0 * float(applied_weight))

            else:
                applied_weight = None

            if i[14]:
                applied_shipping_fee = abs(float(i[14]))
            else:
                applied_shipping_fee = 0.0
            seller_id = i[15]
            length = i[16]
            breadth = i[17]
            height = i[18]
            weight = i[19]

            #  To get the tiers

            tiers = self.get_tiers(order_date, seller_id)

            query_to = "Select flipkart_region,District, statename from pincodes where pincode=" + str(to_pin) + ""
            query_from = "Select flipkart_region, District, statename from pincodes where pincode=" + str(
                from_pin) + ""

            self.cursor_evanik_main.execute(query_from)
            data_from = self.cursor_evanik_main.fetchone()

            from_fk_region = data_from[0]
            from_district = data_from[1]
            from_state = data_from[2]

            self.cursor_evanik_main.execute(query_to)
            data_to = self.cursor_evanik_main.fetchone()

            try:
                to_fk_region = data_to[0]
                to_district = data_to[1]
                to_state = data_to[2]
            except:
                to_fk_region = ''
                to_district = ''
                to_state = ''

            #  To get the Zone
            if to_district == from_district:
                self.applicable_zone = 'Local'
            elif (to_district != from_district) and (to_fk_region == from_fk_region):
                self.applicable_zone = 'Zonal'
            else:
                self.applicable_zone = 'National'

            if length and breadth and height:
                calculated_weight_applicable = (float(length) * float(breadth) * float(height)) / 5000
                applicable_weight = max(calculated_weight_applicable, float(weight))
                applicable_weight = 0.5 * math.ceil(2.0 * float(applicable_weight))
            else:
                applicable_weight = None
            print("applicable weight: ", applicable_weight, shipping_zone, self.applicable_zone, tiers, sep='--')

            print("applied_weight", applied_weight, shipping_zone, self.applicable_zone, tiers, sep='--')

            if not applicable_weight:
                print("NOT")
                # getting price from applied_weight and applicable_zone
                applicable_shipping_fee = fk_payment_calculator.cal_payment(float(applied_weight),
                                                                            self.applicable_zone, tiers)
            else:
                print("YES")
                # getting price from applicable_weight and applicable_zone
                applicable_shipping_fee = fk_payment_calculator.cal_payment(float(applicable_weight),
                                                                            self.applicable_zone, tiers)
            gap = applied_shipping_fee - applicable_shipping_fee

            if (
                    shipping_zone != self.applicable_zone) and sale_status != 'Return' and shipping_zone != '0' and shipping_zone:
                print(shipping_zone, order_id, self.applicable_zone, to_district, to_fk_region, to_state,
                      from_district,
                      from_fk_region, from_state, sep='--')

            if (shipping_zone != '0') and shipping_zone:
                sql = "INSERT INTO shipping_variance (channel, warehouse, order_id, item_id, applied_zone, " \
                      "applicable_zone, applied_shipping, applicable_shipping, gap, sale_status, payment_status, " \
                      "order_date, applied_weight, applicable_weight) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    channel, whid, order_id, order_item_id, shipping_zone, self.applicable_zone,
                    applied_shipping_fee,
                    applicable_shipping_fee, gap,
                    sale_status, '', order_date, applied_weight, applicable_weight)
                print(val)
                OBJ.query(sql, val)
        self.cursor.close()
        self.connection.close()
        self.cursor_evanik_main.close()
        self.connection_evanik_main.close()


if __name__ == '__main__':
    OBJ = FlipkartReco('78823')
    OBJ.get_state()
    quit()
    # connection = pymysql.connect('localhost', 'root', 'evanik@2019', 'invento')
    # cursor = connection.cursor()
    # query = f'SELECT id FROM users WHERE exp_date > "{datetime.today().strftime("%Y-%m-%d")}";'
    # cursor.execute(query)
    # data = cursor.fetchall()
    # count = 0
    # for idd in data:
    #     OBJ = FlipkartReco(str(idd[0]))
    #     OBJ.get_state()
    import pandas as pd
    user_list = pd.read_csv("flipkart_user.csv")
    user_list = user_list['user_id'].tolist()
    for user in user_list:
        try:
            print(user)
            if user != 76105:
                OBJ = FlipkartReco(str(user))
                OBJ.get_state()
        except TypeError as e:
            print(e)
