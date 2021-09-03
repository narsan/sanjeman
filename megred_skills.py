import csv

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


def get_marriage_status(marriage):
    if not marriage:
        return -1
    marriage_status = int.from_bytes(marriage, "big") - ord('0')
    if marriage_status != 0 and marriage != 1:
        return -1

    return marriage_status


def calculate_age(born):
    if not born:
        return None

    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def add_personal_info():
    query = "SELECT DISTINCT job_applicant_id, gender, birthday,  JSON_UNQUOTE(json_extract(marriage,'$.status')), " \
            "(useful_data.languages IS not NULL) AS lanquage_exists, job_title, " \
            "steps_title, job_contract_type, job_skills " \
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
            job_skills = item[8]
            person = PersonalInfo(job_applicant_id, steps_title, job_title, contract_type, job_skills)
            person.set_gender(gender)
            person.set_age(birthday)
            person.set_marriage_status(marriage)
            person.set_language(language)
            resumes[job_applicant_id] = person


def add_education():
    query = "SELECT DISTINCT job_applicant_id, " \
            "degree, field, university, gpa, began_edu_at, finished_edu_at " \
            "FROM useful_data"

    my_cursor.execute(query)
    for item in my_cursor:
        job_applicant_id = item[0]
        degree = item[1]
        field = item[2]
        university = item[3]
        gpa = item[4]
        began_edu_at = item[5]
        finished_edu_at = item[6]
        resumes[job_applicant_id].add_education(field, university, gpa, began_edu_at, finished_edu_at, degree)


def add_skills():
    query = "SELECT DISTINCT job_applicant_id, " \
            "skills_title " \
            "FROM useful_data"

    my_cursor.execute(query)
    for item in my_cursor:
        job_applicant_id = item[0]
        skill = item[1]
        resumes[job_applicant_id].add_skill(skill)


def add_work_exp():
    query = "SELECT DISTINCT useful_data.job_applicant_id, " \
            "company, useful_data.field, began_at, finished_at, useful_data.quit_reason " \
            "FROM useful_data " \
            "LEFT JOIN work_experiences ON work_experiences.job_applicant_id = useful_data.job_applicant_id"

    my_cursor.execute(query)
    for item in my_cursor:
        job_applicant_id = item[0]
        company = item[1]
        field = item[2]
        began_at = item[3]
        finished_at = item[4]
        quit_reason = item[5]
        resumes[job_applicant_id].add_work_exp(company, field, quit_reason, began_at, finished_at)


def get_people_data():
    add_personal_info()
    add_education()
    add_skills()
    add_work_exp()


def get_applicant_info(job_applicant_id):
    query = "SELECT DISTINCT job_applicant_id, gender, birthday, JSON_UNQUOTE(json_extract(marriage,'$.status')), " \
            "(useful_data.languages IS not NULL) AS lanquage_exists, " \
            "steps_title " + \
            "FROM useful_data"

    my_cursor.execute(query)
    for item in my_cursor:
        return [item[0], calculate_age(item[1]), get_marriage_status(item[2]), item[3]], item[4]


def write_file():
    with open('final_data.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for job_applicant_id in resumes:
            row = resumes[job_applicant_id].get_vector()
            writer.writerow(row)


def write_tagged_data():
    with open('tagged_data.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for job_applicant_id in resumes:
            row = resumes[job_applicant_id].get_vector()
            print(row)
            if row[-1] == 'رد شده' or row[-1] == 'استخدام شده':
                writer.writerow(row)


get_people_data()
write_file()
write_tagged_data()
