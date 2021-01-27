class A:
    def print(s):
        print("HELLO!@#")
        print("A")


class B:
    def print(s):
        print("B")


class C(A):
    def print(s):
        print("HELLO")
        super().print()
        print("C")


class M(C, B, A):
    def print(s):
        super().print()


# a = "ME and YOU"
# temp = ''
# b = a.split()
# temp += b[-1] + ' '
# temp += b[1] + ' '
# temp += b[0]
# print(temp)


# import requests
# file_path = r'C:\Users\nikhils3\Downloads\CompOrderReport_13_01_2021_12_00_04_070-440563970.xlsx'
# url = "http://cron.evanik.com/manual/snapdeal/orders/fileupload.php"
# with open(file_path, "rb") as a_file:
#     file_dict = {"userfile": a_file}
#     data = {"fileupload": "yes"}
#     r = requests.post(url=url, files=file_dict, data=data)
# print(r.text)
import requests
import json


def getArticleTitles(author):
    # Write your code here
    if not author:
        return []
    titles = []
    st, total = 1, float('inf')
    while st <= total:
        url = "https://jsonmock.hackerrank.com/api/articles?author={0}&page={1}".format(author, st)
        response = requests.get(url)
        res = json.loads(response.content)
        total = res['total_pages']

        for t in res['data']:
            if not t['title'] and not t['story_title']:
                continue
            elif not t['title']:
                titles += [t['story_title']]
            else:
                titles += [t['title']]
        st += 1
    return titles


def binary_search(arr, target, low, high):
    if low > high:
        return False
    else:
        mid = (low + high) // 2
        if target == arr[mid]:
            return True
        elif target < arr[mid]:
            return binary_search(arr, target, low, mid - 1)
        else:
            return binary_search(arr, target, mid + 1, high)


if __name__ == '__main__':
    import datetime
    data = [i for i in range(19999999)]
    print(data[-1])
    s = datetime.datetime.now()
    print(binary_search(data, 8686, 1, 19999998))
    e = datetime.datetime.now()
    print("FINAL TIME TO EXECUTE : ", str(e - s))
