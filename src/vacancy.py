
class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, title, url, salary, requirements):
        self.title = title
        self.url = url
        self.__salary = salary
        self.requirements = requirements

    @property
    def salary(self):
        return self.__salary

    def __str__(self):
        return f"'название': {self.title}, 'ссылка': {self.url}, 'зарплата': {self.__salary}, 'требования': {self.requirements}"

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.__salary < other.__salary
        raise ValueError("Сравнивать можно только объекту Vacancy и дочерние от них")

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.__salary <= other.__salary
        raise ValueError("Сравнивать можно только объекту Vacancy и дочерние от них")

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.__salary > other.__salary
        raise ValueError("Сравнивать можно только объекту Vacancy и дочерние от них")

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.__salary >= other.__salary
        raise ValueError("Сравнивать можно только объекту Vacancy и дочерние от них")

    @staticmethod
    def validate_salary(salary):
        if salary is None:
            return 0
        return salary

    @staticmethod
    def validate_requirements(requirements):
        if "<highlighttext>" in requirements or "</highlighttext>" in requirements:
            req_new = requirements.replace("<highlighttext>", "")
            req_new = req_new.replace("</highlighttext>", "")
            return req_new
        return requirements
