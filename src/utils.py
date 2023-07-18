from src.api import ApiHH, ApiSuperJob
from src.jsonsaver import JSONSaver
from src.vacancy import Vacancy


def get_hh_vacancies_list(raw_hh_data):
    """
    Преобразование вакансий из HeadHunter в значения атрибутов экземпляров класса Vacancy
    :param raw_hh_data:
    :return:
    """
    vacancies = []
    for raw_hh_vacancy in raw_hh_data:
        try:
            title = raw_hh_vacancy['name']
            url = raw_hh_vacancy['alternate_url']
            salary = raw_hh_vacancy['salary'].get('from')
            if raw_hh_vacancy['snippet']['requirement'] is None:
                requirements = "Описание не указано"
            else:
                requirements = raw_hh_vacancy['snippet']['requirement']
        except AttributeError:
            title = raw_hh_vacancy['name']
            url = raw_hh_vacancy['alternate_url']
            salary = None
            if raw_hh_vacancy['snippet']['requirement'] is None:
                requirements = "Описание не указано"
            else:
                requirements = raw_hh_vacancy['snippet']['requirement']
        validate_salary = Vacancy.validate_salary(salary)
        validate_requirements = Vacancy.validate_requirements(requirements)
        hh_vacancy = Vacancy(title, url, validate_salary, validate_requirements)
        vacancies.append(hh_vacancy)
    return vacancies


def get_sj_vacancies_list(raw_sj_data):
    """
    Преобразование вакансий из SuperJob в значения атрибутов экземпляров класса Vacancy
    :param raw_sj_data:
    :return:
    """
    vacancies = []
    for raw_sj_vacancy in raw_sj_data:
        try:
            title = raw_sj_vacancy['profession']
            url = raw_sj_vacancy['link']
            salary = raw_sj_vacancy['payment_from']
            requirements = raw_sj_vacancy['candidat']
        except AttributeError:
            title = raw_sj_vacancy['profession']
            url = raw_sj_vacancy['link']
            salary = None
            requirements = raw_sj_vacancy['candidat']

        validate_salary = Vacancy.validate_salary(salary)
        validate_requirements = Vacancy.validate_requirements(requirements)
        sj_vacancy = Vacancy(title, url, validate_salary, validate_requirements)
        vacancies.append(sj_vacancy)
    return vacancies


def user_interaction(json_saver: JSONSaver):
    """
    Функция взаимодействия с пользователем
    :param json_saver:
    :return:
    """
    hh_vacancies = ApiHH()
    superjob_vacancies = ApiSuperJob()
    while True:
        user_input = input("Добрый день!С какой платформы хотите получить вакансии: 1 - HeadHunter, 2 - SuperJob, 3 - обе платформы: ")
        search_word = input("Введите ключевое слово для поиска: ")
        if user_input == "1":
            raw_hh_data = hh_vacancies.get_vacancies(search_word)["items"]
            vacancies = get_hh_vacancies_list(raw_hh_data)
            break
        elif user_input == "2":
            raw_sj_data = superjob_vacancies.get_vacancies(search_word)["objects"]
            vacancies = get_sj_vacancies_list(raw_sj_data)
            break
        elif user_input == "3":
            raw_hh_data = hh_vacancies.get_vacancies(search_word)["items"]
            raw_sj_data = superjob_vacancies.get_vacancies(search_word)["objects"]
            vacancies_hh = get_hh_vacancies_list(raw_hh_data)
            vacancies_sj = get_sj_vacancies_list(raw_sj_data)
            vacancies = vacancies_hh + vacancies_sj
            break
        else:
            print("Введите цифру 1, 2 или 3")
    json_saver.add_vacancy(vacancies)
    while True:
        print('Выберите одно из доступных действий:')
        print('1. Получить список всех вакансий')
        print('2. Удалить вакансию')
        print('3. Получить список вакансий по ключевым словам')
        print('4. Получить список вакансий с зарплатой выше указанной')
        print('5. Получить топ N вакансий по зарплате')
        print('6. Выйти')

        choice = input('> ')
        if choice == '1':
            for vacancy in vacancies:
                print(vacancy)
                print()
        elif choice == '2':
            vacancy = input("Введите ссылку удаляемой вакансии: ")
            json_saver.delete_vacancy(vacancy)
            print('Вакансия удалена!')
        elif choice == '3':
            filter_words = input('Введите ключевые слова для фильтрации вакансий: ')
            for vacancy in vacancies:
                if filter_words in vacancy.requirements:
                    print(vacancy)
                    print()
        elif choice == '4':
            min_salary = float(input('Введите минимальную зарплату: '))
            for vacancy in vacancies:
                if min_salary < float(vacancy.salary):
                    print(vacancy)
                    print()
        elif choice == '5':
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            sorted_vacancies = sorted(vacancies, reverse=True)
            for vacancy in sorted_vacancies[:top_n]:
                print(vacancy)
                print()
        elif choice == '6':
            break
        else:
            print('Некорректный ввод!')


if __name__ == "__main__":
    json_saver = JSONSaver()
    user_interaction(json_saver)
