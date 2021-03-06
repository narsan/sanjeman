import math
from datetime import date
from parsivar import Normalizer, Tokenizer

my_normalizer = Normalizer(statistical_space_correction=True)
my_tokenizer = Tokenizer()


class Education:
    def __init__(self,  field, university, gpa, began_at, finished_at, degree):
        self.field = field
        self.university = university
        self.gpa = gpa
        self.interval = self.calculate_interval(began_at, finished_at)
        self.degree = degree

    def calculate_interval(self, began_at, finished_at):
        if not began_at:
            return 0

        if type(began_at) != type(date.today()):
            return 0

        if finished_at:
            finish = finished_at
        else:
            finish = date.today()

        return finish.year - began_at.year - ((finish.month, finish.day) < (began_at.month, began_at.day))


class WorkExperience:
    def __init__(self, company, field, quit_reason, began_at, finished_at):
        self.company = company
        self.field = field
        self.quit_reason = quit_reason
        self.work_interval = self.calculate_work_interval(began_at, finished_at)

    def calculate_work_interval(self, began_at, finished_at):
        if not began_at:
            return 0

        if finished_at:
            finish = finished_at
        else:
            finish = date.today()
        return finish.year - began_at.year - ((finish.month, finish.day) < (began_at.month, began_at.day))


class Skill:
    def __init__(self, text):
        self.vector = dict()
        self.txt = text
        self.vector = dict()
        self.len_vector = 0

    def get_vector(self):
        if not self.txt:
            self.vector = None
            return

        if len(self.vector) != 0:
            return

        normalized_text = my_normalizer.normalize(self.txt)
        tokens = my_tokenizer.tokenize_words(normalized_text)
        for token in tokens:
            if token in self.vector:
                self.vector[token] = self.vector[token] + 1
            # else:
            #     self.vector[token] = 1

        self.get_length_vector()

    def get_length_vector(self):
        if not self.vector:
            return 0
        sum = 0
        for token in self.vector:
            sum += math.pow(self.vector[token], 2)

        return math.pow(sum, 0.5)

    def dot_vector(self, skill):
        self.get_vector()
        skill.get_vector()
        self.len_vector = self.get_length_vector()
        skill.len_vector = skill.get_length_vector()

        vector1 = skill.vector
        vector2 = self.vector

        if self.len_vector == 0 or skill.len_vector == 0:
            return 0

        intersect = [value for value in vector1 if value in vector2]

        sum = 0
        for token in intersect:
            sum += (1+math.log(vector1[token], 2)) * (1+math.log(vector2[token], 2))

        return sum/(self.len_vector * skill.len_vector)


class PersonalInfo:
    def __init__(self, job_applicant_id, steps_title, job_title, contract_type, job_skills):
        self.job_applicant_id = job_applicant_id
        self.gender = None
        self.age = None
        self.num_skills = 0
        self.marriage_status = None
        self.language = []
        self.skills = []
        self.educations = []
        self.work_experiences = []
        self.steps_title = job_title
        self.job_title = job_title
        self.map_steps_title(steps_title)
        self.contract_type = contract_type
        self.job_skills = Skill(job_skills)

    def map_steps_title(self, title):
        if title == '?????????????? ?????????? ??????????':
            self.steps_title = 0
        elif title == '?????????? ???????? ????????????':
            self.steps_title = 1
        elif title == '?????????????? ??????':
            self.steps_title = 2
        elif title == '???? ??????':
            self.steps_title = 3
        elif title == '???????????? ???? ????????????':
            self.steps_title = 4
        else:
            if title:
                self.steps_title = 6
            else:
                self.steps_title = None

    def set_gender(self, gender):
        if not gender:
            self.gender = gender

    def set_age(self, birthday):
        if birthday:
            today = date.today()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

            if age < 20:
                self.age = 1

            elif 20 <= age < 30:
                self.age = 2

            elif 30 <= age < 40:
                self.age = 3

            elif 40 <= age < 50:
                self.age = 4

            elif age >= 50:
                self.age = 5

    def set_marriage_status(self, marriage):
        if marriage:
            marriage_status = int.from_bytes(marriage, "big") - ord('0')
            if marriage_status == 0 and marriage == 1:
                self.marriage_status = marriage_status

    def add_skill(self, skill):
        self.skills.append(Skill(skill))
        self.num_skills += 1

    def add_education(self, field, university, gpa, began_at, finished_at, degree):
        self.educations.append(Education(field, university, gpa, began_at, finished_at, degree))

    def get_max_degree(self):
        edu = max(self.educations, key=lambda education: education.degree)
        if not edu:
            return -1
        return edu.degree

    def add_work_exp(self, company, field, quit_reason, began_at, finished_at):
        self.work_experiences.append(WorkExperience(company, field, quit_reason, began_at, finished_at))

    def get_skill_score(self):
        return self.num_skills

    def get_work_interval(self):
        sum_work_interval = 0
        for work_exp in self.work_experiences:
            if work_exp.work_interval:
                sum_work_interval += work_exp.work_interval

        return sum_work_interval

    def get_average_gpa(self):
        sum = 0
        num = 0
        for education in self.educations:
            if education.gpa:
                sum += education.gpa
                num += 1

        if num == 0:
            return None
        gpa = sum/num
        if gpa >= 17:
            return 1
        elif gpa >= 14:
            return 2
        elif gpa >= 12:
            return 3
        elif gpa >= 10:
            return 4
        else:
            return 5

    def get_max_university(self):
        max_degree = self.get_max_degree()
        for education in self.educations:
            if education.degree == max_degree:
                return education.university

        return None

    def get_sim_skills(self):
        if len(self.skills) == 0:
            return 0

        text_skills = ''
        for skill in self.skills:
            if skill.txt:
                text_skills += skill.txt + ' '

        all_skills = Skill(text_skills)
        all_skills.get_vector()
        return all_skills.dot_vector(self.job_skills)

    def set_language(self, language):
        self.language = language

    def get_language(self):
        return self.language

    def get_vector(self):
        personal_info = [self.job_applicant_id, self.gender, self.age, self.marriage_status,
                         self.language, self.contract_type]

        education_info = [self.get_max_degree(), self.get_average_gpa()]
        skill_info = [1]
        work_exp_info = [len(self.work_experiences), self.get_work_interval()]
        return personal_info + education_info + skill_info + work_exp_info + [self.steps_title]

