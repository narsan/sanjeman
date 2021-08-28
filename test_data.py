import csv
import random


data_accepted = []
data_rejected = []


def get_data(path):
    first_row = True
    with open(path, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in reader:
            if first_row:
                first_row = False
                header = row
                continue

            if row[13] == 'استخدام شده':
                data_accepted.append(row)

            elif row[13] == 'رد شده':
                data_rejected.append(row)

    # print(data)
    return header


def separate_test_data():
    num_test = int(len(data_accepted)/10)
    random.shuffle(data_accepted)
    random.shuffle(data_rejected)

    test = data_accepted[0: num_test].copy() + data_rejected[0: num_test].copy()
    random.shuffle(test)

    train = data_accepted[num_test+1: len(data_accepted)] + data_rejected[num_test+1: len(data_rejected)]
    random.shuffle(train)

    return train, test


def write_in_file(data, path, header):
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(header)

        for row in data:
            writer.writerow(row)


header = get_data('Result_32.csv')
train, test = separate_test_data()
write_in_file(train, 'train.csv', header)
write_in_file(test, 'test.csv', header)
