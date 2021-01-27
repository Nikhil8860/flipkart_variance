import math
import fk_payment_calculator
from get_data_sql import GetData
import MySQLdb


class FlipkartReco:

    def __init__(self, user_id):
        self.user_id = user_id
        self.connection = MySQLdb.connect(host="localhost", user="root", password='evanik@2019',
                                          database=f'invento_{self.user_id}')
        self.connection_evanik_main = MySQLdb.connect(host="localhost", user="root", password='evanik@2019',
                                                      database='evanik_main')
        self.cursor = self.connection.cursor()
        self.cursor_evanik_main = self.connection_evanik_main.cursor()
        self.applicable_zone = None
        self.conn = None
        self.data = None

    def connect(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", password='evanik@2019',
                                    database=f'invento_{self.user_id}')

    def query(self, sql, val):
        try:
            cursor = self.conn.cursor()
            try:
                cursor.executemany(sql, val)
            except Exception as e:
                print(e)
            self.conn.commit()
            print(cursor.rowcount, "record(s) affected")
        except (AttributeError, MySQLdb.err.InterfaceError, MySQLdb.OperationalError, MySQLdb.err.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            try:
                cursor.executemany(sql, val)
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
        try:
            query = "SELECT tier FROM channel_tiers WHERE " + "'" + str(
                order_date) + "'" + " BETWEEN start_date AND end_date and sellerId=" + "'" + seller_id + "'"
            print(query)
            self.cursor.execute(query)
            data = self.cursor.fetchone()
            if data:
                tiers = data[0]
            else:
                tiers = 'bronze'

            return tiers

        except Exception as e:
            print(e)

    def get_state(self):
        f = open('log.txt', 'a', encoding='utf-8')
        OBJ_1 = GetData(self.user_id)
        data = OBJ_1.get_data()
        k = 0
        tmp = []
        try:
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
                except Exception as e:
                    f.write(str(e) + ' ' + str(self.user_id) + '\n')
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
                print("applicable weight: ", applicable_weight, shipping_zone, self.applicable_zone, self.user_id,
                      tiers,
                      sep='--')

                print("applied_weight", applied_weight, shipping_zone, self.applicable_zone, self.user_id, tiers,
                      sep='--')

                if not applicable_weight:
                    try:
                        # getting price from applied_weight and applicable_zone
                        applicable_shipping_fee = fk_payment_calculator.cal_payment(float(applied_weight),
                                                                                    self.applicable_zone, tiers)
                    except Exception as e:
                        print(e)
                        applicable_shipping_fee = 0

                else:
                    try:
                        # getting price from applicable_weight and applicable_zone
                        applicable_shipping_fee = fk_payment_calculator.cal_payment(float(applicable_weight),
                                                                                    self.applicable_zone, tiers)
                    except Exception as e:
                        print(e)
                        applicable_shipping_fee = 0

                gap = applied_shipping_fee - applicable_shipping_fee

                if (
                        shipping_zone != self.applicable_zone) and sale_status != 'Return' and shipping_zone != '0' and shipping_zone:
                    print(shipping_zone, order_id, self.applicable_zone, to_district, to_fk_region, to_state,
                          from_district, from_fk_region, from_state, sep='--')
                sql = "INSERT INTO shipping_variance (channel, warehouse, order_id, item_id, applied_zone, " \
                      "applicable_zone, applied_shipping, applicable_shipping, gap, sale_status, payment_status, " \
                      "order_date, applied_weight, applicable_weight) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                      "ON DUPLICATE KEY UPDATE channel = %s, warehouse = %s, order_id = %s, item_id = %s, " \
                      "applied_zone = %s, applicable_zone = %s, applied_shipping = %s, applicable_shipping = %s, " \
                      "gap = %s, sale_status = %s, payment_status = %s, " \
                      "order_date = %s, applied_weight = %s, applicable_weight = %s"
                if (shipping_zone != '0') and shipping_zone:
                    val = (
                        channel, whid, order_id, order_item_id, shipping_zone, self.applicable_zone,
                        applied_shipping_fee,
                        applicable_shipping_fee, gap,
                        sale_status, '', order_date, applied_weight, applicable_weight,
                        channel, whid, order_id, order_item_id, shipping_zone, self.applicable_zone,
                        applied_shipping_fee,
                        applicable_shipping_fee, gap,
                        sale_status, '', order_date, applied_weight, applicable_weight)
                    tmp.append(val)
                    if k == 100:
                        OBJ.query(sql, tmp)
                        k = 0
                        tmp = []
                    else:
                        k += 1

            OBJ.query(sql, tmp)

        except Exception as e:
            f.write(str(e) + ' ' + str(self.user_id) + '\n')
        self.cursor.close()
        self.connection.close()
        self.cursor_evanik_main.close()
        self.connection_evanik_main.close()


if __name__ == '__main__':
    OBJ = FlipkartReco(78019)
    OBJ.get_state()
