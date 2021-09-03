import ast
from datetime import date


class Education:
    def __init__(self, field, university, gpa, began_at, finished_at, degree):
        self.field = field
        self.university = university
        self.gpa = gpa
        self.interval = self.calculate_interval(began_at, finished_at)
        self.degree = degree

    def calculate_interval(self, began_at, finished_at):
        if not began_at:
            return -1

        if type(began_at) != type(date.today()):
            return -1

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


def map_language(lang):
    if lang == 'persian':
        lang = '1'
    elif lang == 'english':
        lang = '2'
    elif lang == 'arabic':
        lang = '3'
    elif lang == 'germany':
        lang = '4'
    elif lang == 'french':
        lang = '5'
    elif lang == 'spanish':
        lang = '6'
    else:
        lang = '18'
    return lang


def map_level(lvl):
    if lvl == 'beginner':
        lvl = '1'
    elif lvl == 'intermediate':
        lvl = '2'
    elif lvl == 'advanced':
        lvl = '3'
    elif lvl == 'native':
        lvl = '4'
    return lvl


class PersonalInfo:
    def __init__(self, job_applicant_id, steps_title, job_title, contract_type):
        self.job_applicant_id = job_applicant_id
        self.gender = -1
        self.age = -1
        self.num_skills = 0
        self.marriage_status = -1
        self.language = []
        self.skills = []
        self.educations = []
        self.work_experiences = []
        self.steps_title = job_title
        self.job_title = job_title
        if steps_title:
            self.steps_title = steps_title
        else:
            self.steps_title = -1

        self.contract_type = contract_type

    def set_gender(self, gender):
        if not gender:
            self.gender = gender

    def set_age(self, birthday):
        if birthday:
            today = date.today()
            self.age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        else:
            self.age = -1

    def set_marriage_status(self, marriage):
        if marriage:
            marriage_status = int.from_bytes(marriage, "big") - ord('0')
            if marriage_status == 0 and marriage == 1:
                self.marriage_status = marriage_status
        else:
            self.marriage_status = -1

    def set_language(self, language):
        if language is not None:
            res = ast.literal_eval(language.strip("[]"))
            if 'title' not in res and type(res[0]) == dict:
                num = len(res)
                for languages in res:
                    try:
                        if 'english_title' in languages['title']:
                            title = languages['title']['english_title']
                            title = map_language(title)
                            languages['title'] = title
                            level = languages['level']['english_title']
                            level = map_level(level)
                            languages['level'] = level
                            num = num * int(level)
                            # print(num)
                        else:
                            num = num * int(languages['level'])
                    except:
                        num = num * int(languages['level'])
                self.language = num
            elif 'title' in res and type(res['title']) == dict:
                num = 1
                title = res['title']['english_title']
                title = map_language(title)
                res['title'] = title
                level = res['level']['english_title']
                level = map_level(level)
                res['level'] = level
                num = num * int(level)
                self.language = num
            else:
                if 'title' in res:
                    # print(res)
                    num = 1 * int(res['level'])
                    self.language = num
        else:
            self.language = -1

    def get_language(self):
        return self.language

    def add_skill(self, skill):
        self.skills.append(skill)
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
            return -1
        return sum / num

    def get_vector(self):
        personal_info = [self.job_applicant_id, self.gender, self.age, self.marriage_status,
                         self.language, self.contract_type]

        education_info = [self.get_max_degree(), self.get_average_gpa()]
        skill_info = [self.num_skills]
        work_exp_info = [len(self.work_experiences), self.get_work_interval()]
        return personal_info + education_info + skill_info + work_exp_info + [self.steps_title]
