import mysql.connector
import pandas
from sklearn import tree
import pydotplus
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.image as pltimg
from mysql.connector import connect, Error

with open('pss.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
password = lines[0]
db = lines[1]

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database=db,
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


df = pandas.read_csv("Result_32.csv")
for title in steps_title_list:
    if title[0] == 'نیازمند تعیین وضعیت':
        d_steps_title[title[0]] = 0
    elif title[0] == 'تایید برای مصاحبه':
        d_steps_title[title[0]] = 1
    elif title[0] == 'استخدام شده':
        d_steps_title[title[0]] = 2
    elif title[0] == 'رد شده':
        d_steps_title[title[0]] = 3
    elif title[0] == 'انصراف از مصاحبه':
        d_steps_title[title[0]] = 4
    else:
        d_steps_title[title[0]] = 6
i = 0
for title in university_name_list:
    d_uni_name[title] = i
    i += 1

print(d_steps_title)
df['steps_title'] = df['steps_title'].map(d_steps_title)
pandas.set_option('display.max_rows', df.shape[0]+1)
print(df['gender'])
pandas.set_option('display.max_rows', df.shape[0]+1)
# print(df['steps_title'])
df['university'] = df['university'].map(d_uni_name)
features = ['gender']

X = df[features]
y = df['steps_title']

print(X)
print(y)


dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)
data = tree.export_graphviz(dtree, out_file=None, feature_names=features)
graph = pydotplus.graph_from_dot_data(data)
graph.write_png('mydecisiontree.png')

img=pltimg.imread('mydecisiontree.png')
imgplot = plt.imshow(img)
plt.show()

