class Vacancy:
    def __init__(self, company_name="", phone="", position="", education="", experience=""):
        self.company_name = company_name
        self.phone = phone
        self.position = position
        self.education = education
        self.experience = experience

    def to_list(self):
        return [self.company_name, self.phone, self.position, self.education, self.experience]

    def equals(self, other):
        return self.to_list() == other.to_list()


class VacancyManager:
    def __init__(self):
        self.vacancies = {}
        self.count = 0

    def add(self, data):
        self.vacancies[self.count] = Vacancy(*data)
        self.count += 1

    def delete(self, data):
        key = self.find_key(data)
        if key != -1:
            del self.vacancies[key]
            self.count -= 1

    def edit(self, key, data):
        self.vacancies[key] = Vacancy(*data)

    def get_all_vacancies(self):
        return list(self.vacancies.values())

    def get_vacancies_sorted_by_experience(self):
        return sorted(self.vacancies.values(), key=lambda v: float(v.experience))

    def get_vacancies_sorted_by_company(self):
        return sorted(self.vacancies.values(), key=lambda v: v.company_name.lower())

    def find_key(self, data):
        target = Vacancy(*data)
        for key, item in self.vacancies.items():
            if item.equals(target):
                return key
        return -1

    def filter_by_position(self, query):
        query = query.lower()
        return [v for v in self.vacancies.values() if query in v.position.lower()]

    def load_data(self, filename="vacancies_data.txt"):
        self.vacancies = {}
        self.count = 0
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("&")
                    if len(parts) == 5:
                        self.add(parts)
        except FileNotFoundError:
            pass

    def save_data(self, filename="vacancies_data.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for vacancy in self.vacancies.values():
                f.write("&".join(vacancy.to_list()) + "\n")