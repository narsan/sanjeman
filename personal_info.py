from datetime import date


class Education:
    def __init__(self,  field, university, gpa, began_at, finished_at):
        self.field = field
        self.university = university
        self.gpa = gpa
        self.interval = self.calculate_interval(began_at, finished_at)

    def calculate_interval(self, began_at, finished_at):
        if not began_at:
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


class PersonalInfo:
    def __init__(self, job_applicant_id, steps_title, job_title):
        self.job_applicant_id = job_applicant_id
        self.gender = -1
        self.age = -1
        self.num_skills = 0
        self.marriage_status = -1
        self.skills = []
        self.educations = []
        self.work_experiences = []
        self.steps_title = job_title
        self.job_title = job_title

    def set_gender(self, gender):
        if not gender:
            self.gender = gender

    def set_age(self, birthday):
        if not birthday:
            today = date.today()
            self.age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    def set_marriage_status(self, marriage):
        marriage_status = int.from_bytes(marriage, "big") - ord('0')
        if marriage_status == 0 and marriage == 1:
            self.marriage_status = marriage_status

    def add_skill(self, skill):
        self.skills.append(skill)
        self.num_skills += 1

    def add_education(self, field, university, gpa, began_at, finished_at):
        self.educations.append(Education(field, university, gpa, began_at, finished_at))

    def add_work_exp(self, company, field, quit_reason, began_at, finished_at):
        self.work_experiences.append(WorkExperience(company, field, quit_reason, began_at, finished_at))

    def get_skill_score(self):
        return self.num_skills

    def get_work_interval(self):
        sum_work_interval = 0
        for work_exp in self.work_experiences:
            sum_work_interval += work_exp.work_interval

        return sum_work_interval

    def work_gap(self):
        if len(self.work_experiences) != 0:
            oldest = self.work_experiences[0]

            for work_exp in self.work_experiences:
                if work_exp.work_interval:
                    oldest = min(work_exp.work_interval, oldest)

            today = date.today()
            first_interval = today.year - oldest.year - ((today.month, today.day) < (oldest.month, oldest.day))
            return min(first_interval - self.get_work_interval(), 0)

        return -1


