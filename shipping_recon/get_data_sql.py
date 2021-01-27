from datetime import datetime
from dateutil.relativedelta import *
import pymysql.cursors


class GetData:

    def __init__(self, user_id):
        self.user_id = user_id
        self.connection = pymysql.connect('13.233.239.105', 'root', 'evanik@2019', f'invento_{user_id}')
        self.non_fa_data = None
        self.fa_data = None
        self.cursor = None

    def get_data(self):
        print("Inside query method..")
        date_now = datetime.today().date()
        date_six_prior = (date_now - relativedelta(months=6)).strftime("%Y-%m-%d")
        try:
            non_fa_query = f"""
                    SELECT s.PinCode AS To_pincode,ch.postal_code AS From_pincode,ch.whid,s.OrderId,s.warehouse_id,
                    s.OrderItemID, s.shippingZone,s.sale_status, s.date, c.type, s.weight, s.shipmentLength,
                    s.shipmentBreadth, s.shipmentHeight,p.ShippingFee,s.sellerId,pr.length,pr.breadth,
                    pr.height,pr.weight,c.type,ch.postal_code, p.extra_details FROM sales AS s
                    LEFT JOIN channels AS c ON c.sellerId=s.sellerId
                    LEFT JOIN channel_warehouse AS ch ON
                    ((s.sellerId=ch.sellerId  AND s.whid=ch.whid) OR (s.sellerId=ch.sellerId))
                    LEFT JOIN payments_process AS p ON p.OrderItemID=s.OrderItemID
                    LEFT JOIN products AS pr ON pr.code = s.SKUcode
                    WHERE (s.whid IS NULL AND s.PinCode IS NOT NULL AND s.PinCode!=0 AND s.shipmentLength IS NOT NULL
                    AND ch.postal_code IS NOT NULL AND p.extra_details IS NOT NULL AND c.type='flipkart' AND
                    (s.date BETWEEN '{date_six_prior}' and '{date_now}')) LIMIT 4000 , 1000
                    """
            fa_query = f"""
                    SELECT s.PinCode AS To_pincode,c.pincode AS From_pincode,ch.whid,s.OrderId,s.warehouse_id,
                    s.OrderItemID, s.shippingZone,s.sale_status, s.date, c.type, s.weight, s.shipmentLength,
                    s.shipmentBreadth, s.shipmentHeight,p.ShippingFee,s.sellerId,pr.length,pr.breadth,
                    pr.height,pr.weight,c.type,ch.postal_code, p.extra_details FROM sales AS s
                    LEFT JOIN channels AS c ON c.sellerId=s.sellerId
                    LEFT JOIN channel_warehouse AS ch ON
                    ((s.sellerId=ch.sellerId  AND s.whid=ch.whid) OR (s.sellerId=ch.sellerId))
                    LEFT JOIN payments_process AS p ON p.OrderItemID=s.OrderItemID
                    LEFT JOIN products AS pr ON pr.code = s.SKUcode
                    WHERE (s.PinCode IS NOT NULL AND s.PinCode!=0 AND s.shipmentLength
                    IS NOT NULL AND c.pincode IS NOT NULL AND p.extra_details IS NOT NULL AND c.type='flipkart' AND
                    (s.date BETWEEN '{date_six_prior}' and '{date_now}')) LIMIT 4000, 1000
                    """
            print(non_fa_query)
            print()
            print(fa_query)

            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(non_fa_query)
                self.non_fa_data = list(self.cursor.fetchall())
                self.non_fa_data = [t for t in (set(tuple(i) for i in self.non_fa_data))]
                if self.non_fa_data:
                    return self.non_fa_data
                else:
                    self.cursor.execute(fa_query)
                    self.fa_data = list(self.cursor.fetchall())
                    self.fa_data = [t for t in (set(tuple(i) for i in self.fa_data))]
                    return self.fa_data
            except Exception as e:
                print(e)
            finally:
                self.cursor.close()
                self.connection.close()
        except Exception as e:
            print(e)
