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


class PersonalInfo:
    def __init__(self, job_applicant_id):
        self.job_applicant_id = job_applicant_id
        self.gender = -1
        self.age = -1
        self.num_skills = 0
        self.marriage_status = -1
        self.skills = []
        self.educations = []

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



