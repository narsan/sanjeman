import csv

import mysql.connector
import pandas
from datetime import date


skills = dict()
education = dict()
header = ['job_applicant_id', 'gender', 'age', 'education', 'skill', 'steps_title']


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
df = pandas.read_csv("Result_32.csv")


def count_skills(string_skills):
    if not string_skills:
        return 0

    return len(string_skills.split(' '))


def merge_skills():
    my_cursor.execute("SELECT DISTINCT  job_applicant_id, GROUP_CONCAT(distinct skills_title SEPARATOR ', ') FROM useful_data GROUP BY job_applicant_id;")

    for item in my_cursor:
        skills[item[0]] = count_skills(item[1])


def merge_education():
    my_cursor.execute("SELECT DISTINCT job_applicant_id, MAX(degree) FROM useful_data GROUP BY job_applicant_id;")
    for item in my_cursor:
        if item[1]:
            education[item[0]] = item[1]
        else:
            education[item[0]] = item[1]


def calculate_age(born):
    if not born:
        return None

    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_applicant_info(job_applicant_id):
    score_skills = skills[job_applicant_id]
    score_education = education[job_applicant_id]
    my_cursor.execute("SELECT DISTINCT gender, birthday, steps_title FROM useful_data WHERE " + str(job_applicant_id) + " = job_applicant_id;")
    for item in my_cursor:
        return item[0], calculate_age(item[1]), item[2]


def write_file():

    with open('final_data.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for job_applicant_id in skills.keys():
            score_skills = skills[job_applicant_id]
            score_education = education[job_applicant_id]
            gender, age, steps_title = get_applicant_info(job_applicant_id)
            writer.writerow([job_applicant_id, gender, age, score_education, score_skills, steps_title])


merge_skills()
merge_education()
write_file()
#left_df = merge_skills()
#merged = df.merge(left_df, left_on='job_applicant_id', right_index=True, how='left')
#merged.to_csv('merge.csv', encoding='utf-8')
