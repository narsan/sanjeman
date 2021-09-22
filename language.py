import ast
import csv
import json

import mysql.connector
import pandas
from datetime import date

from personal_info import PersonalInfo


skills = dict()
education = dict()
header = ['job_applicant_id', 'gender', 'age', 'marriage_status', 'language', 'contract_type',
          'degree', 'average_gpa', 'skill', 'num_prev_company', 'work_interval', 'steps_title']

resumes = dict()

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


def add_personal_info():
    query = "SELECT DISTINCT job_applicant_id, gender, birthday,  JSON_UNQUOTE(json_extract(marriage,'$.status')), " \
            "languages , job_title, " \
            "steps_title, job_contract_type " \
            "FROM useful_data;"

    my_cursor.execute(query)
    for item in my_cursor:
        job_applicant_id = item[0]
        if job_applicant_id not in resumes:
            gender = item[1]
            birthday = item[2]
            marriage = item[3]
            language = item[4]
            job_title = item[5]
            steps_title = item[6]
            contract_type = item[7]
            # print(language)
            person = PersonalInfo(job_applicant_id, steps_title, job_title, contract_type)
            person.set_gender(gender)
            person.set_age(birthday)
            person.set_marriage_status(marriage)
            person.set_language(language)
            resumes[job_applicant_id] = person



add_personal_info()