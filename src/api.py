from abc import ABC, abstractmethod
import requests
import os
from pprint import pprint

API_KEY = os.getenv("API_KEY_SUPERJOB")
class Api(ABC):
    """
    Класс для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_vacancies(self, vacancy):
        pass

class ApiHH(Api):

    def get_vacancies(self, vacancy):
        hh_dict = {}
        for page in range(0,3):
            params = {
                "text": vacancy,
                "per_page": 100,
                "page" : page,
            }
            response = requests.get("https://api.hh.ru/vacancies", params=params).json()
            hh_dict.update(response)
        return hh_dict



class ApiSuperJob(Api):

    def get_vacancies(self, vacancy):
        params = {
            "keyword": vacancy
        }
        headers = {
            'X-Api-App-Id': API_KEY

        }
        response = requests.get("https://api.superjob.ru/2.0/vacancies", params=params, headers=headers).json()
        return response

# api_hh = ApiHH()
# pprint(api_hh.get_vacancies("Python"))



# api_sj = ApiSuperJob()
# pprint(api_sj.get_vacancies("Python"))
