import mysql.connector
import pandas
from sklearn import tree
import pydotplus
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.image as pltimg

from mysql.connector import connect, Error

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1378@1378",
    database="sanjeman",
    use_pure=True
)

my_cursor = mydb.cursor()
steps_title_list = []
d_steps_title = {}
university_name_list = []
d_uni_name = {}


my_cursor.execute('select distinct steps_title from useful_data')
for item in my_cursor:
    steps_title_list.append(item)

my_cursor.execute('select distinct university from useful_data')
for item in my_cursor:
    university_name_list.append(item)


df = pandas.read_csv("Result_41.csv")
for title in steps_title_list:
    if title[0] == 'نیازمند تعیین وضعیت':
        d_steps_title[title[0]] = 0
    if title[0] == 'تایید برای مصاحبه':
        d_steps_title[title[0]] = 1
    if title[0] == 'استخدام شده':
        d_steps_title[title[0]] = 2
    if title[0] == 'رد شده':
        d_steps_title[title[0]] = 3
    if title[0] == 'انصراف از مصاحبه':
        d_steps_title[title[0]] = 4
    else:
        d_steps_title[title[0]] = 6
i = 0
for title in university_name_list:
    d_uni_name[title] = i
    i += 1
print(d_steps_title)
df['steps_title'] = df['steps_title'].map(d_steps_title)
df['university'] = df['university'].map(d_uni_name)
print(df['university'])

