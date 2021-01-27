import requests
import urllib3
import json
from urllib.parse import urlencode
import pprint

http = urllib3.PoolManager()


class LoginSeller:
    def __init__(self):
        self.url = 'https://seller.flipkart.com/login'
        self.payload = {}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/87.0.4280.88 Safari/537.36"}

    def user_details(self, username, password):
        self.payload['authName'] = 'Flipkart'
        self.payload['username'] = username
        self.payload['password'] = password
        # url = "https://seller.flipkart.com/napi/get-locations?"
        url = "https://seller.flipkart.com/getFeaturesForSeller"
        #  get data from the login url

        with requests.Session() as s:
            r = s.post(self.url, data=self.payload)
            seller_id = r.json()['data']['sellerId']
            encoded_args = urlencode({"locationType": "pickup", "include": "state", "sellerId": seller_id})
            # url = url + encoded_args
            self.headers['Cookie'] = s.cookies.get('connect.sid')
            data = s.get(url, headers=self.headers)
            print(data.text)


if __name__ == '__main__':
    USER = LoginSeller()
    user = 'manoj.rout@indus-valley.com'
    pwd = 'Sarya@123#'
    USER.user_details(user, pwd)




