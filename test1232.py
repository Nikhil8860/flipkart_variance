import csv


def write_data_from_csv():
    book = {'id': [101, 102, 103, 104],
            'name': ['java', 'Python with Automation', 'Data Analytics', 'Let us C', '.Net']}
    with open('city_data.csv', 'w') as book_data:
        writ = csv.writer(book_data)
        writ.writerow(book.keys())
        writ.writerow(book.values())
    print('csv File data write successfully')


file_descriptors = []
for x in range(1000000):
    with open('city_data.csv', 'w') as book_data:
        file_descriptors.append(book_data)

print(file_descriptors)
