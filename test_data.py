import csv
import random


data_accepted = []
data_rejected = []
# data_interview = []
percent_test = 0.2


def get_column_steps(header):
    return header.index('steps_title')


def get_data(path):
    first_row = True
    index_steps = None
    with open(path, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in reader:
            if first_row:
                first_row = False
                header = row
                index_steps = header.index('steps_title')
                continue

            if index_steps:
                if row[index_steps] == '2':
                    data_accepted.append(row)

                elif row[index_steps] == '3':
                    data_rejected.append(row)

                # elif row[index_steps] == '1':
                #     data_interview.append(row)

    return header


def separate_test_data():
    num_test = int(len(data_accepted) * percent_test)
    random.shuffle(data_accepted)
    random.shuffle(data_rejected)
    # random.shuffle(data_interview)

    test = data_accepted[0: num_test].copy() + data_rejected[0: num_test].copy() \
           # + data_interview[0: num_test].copy()
    random.shuffle(test)
    train = data_accepted[num_test + 1: len(data_accepted)]+data_rejected[num_test+1: len(data_rejected)]\
            # + data_interview[num_test+1: len(data_interview)]
    random.shuffle(train)

    return train, test


def write_in_file(data, path, header):
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(header)

        for row in data:
            writer.writerow(row)


header = get_data('final_data.csv')
train, test = separate_test_data()
write_in_file(train, 'train.csv', header)
write_in_file(test, 'test.csv', header)
