import mysql.connector
import pandas

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

merged_skill_dict = {}
my_cursor = mydb.cursor()
df = pandas.read_csv("Result_32.csv")


my_cursor.execute("SELECT job_applicant_id, GROUP_CONCAT(distinct skills_title SEPARATOR ', ') FROM useful_data GROUP BY job_applicant_id;")
for item in my_cursor:
    merged_skill_dict[item[0]] = item[1]

l_df = pandas.DataFrame.from_dict(merged_skill_dict, orient='index')
l_df.columns = ['merged_skills']
merged = df.merge(l_df, left_on='job_applicant_id', right_index=True, how='left')
merged.to_csv('mrg_skill.csv', encoding='utf-8')
