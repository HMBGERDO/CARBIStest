from api import get_api_data, get_absolute_data
from dbapp import DatabaseClient

default_api_url = "https://dadata.ru/api/"
default_language = "ru"

def _get_new_api_url(default:str=default_api_url) -> str:
    print(f"Введите новое значение API URL.")
    if not default is None:
        print(f"Введите пустую строку, чтобы установить значение {default}")
    responce = input("API URL = ")
    while responce == "":
        if not default is None:
            return default
        print("Значение не может быть пустым.")
        responce = input("API URL = ")
    return responce

def _get_new_api_key(default:str=None) -> str:
    print("Введите новое значение ключа API.")
    if not default is None:
        print(f"Введите пустую строку, чтобы установить значение {default}")
    responce = input("Ключ API = ")
    while responce == "":
        if not default is None:
            return default
        print("Значение не может быть пустым.")
        responce = input("Ключ API = ")
    return responce

def _get_new_language(default:str=default_language) -> str:
    print(f"Введите желаемый язык(например, en)")
    if not default is None:
        print(f"Введите пустую строку, чтобы установить значение {default}")
    responce = input("Язык получаемых данных = ")
    while responce == "":
        if not default is None:
            return default
        print("Значение не может быть пустым.")
        responce = input("Язык получаемых данных = ")
    return responce

class CoordinateFinder:
    def __init__(self, dbname:str="db.sqlite3") -> None:
        print("Подключаемся к базе данных")
        self.dbclient = DatabaseClient(dbname)
        print("Подключение завершено\nЗагружаем настройки")
        self.settings = self.dbclient.load_settings()
        print("Настройки загружены\n")
        self._prepare_settings()
        self._show_settings()
        while True:
            print("Введите адрес, координаты которого желаете узнать\n"
            "Введите settings, чтобы изменить настройки\n"
            "Введите exit, чтобы закончить работу\n")
            command = input("Команда: ")
            if command == "exit":
                break
            if command == "settings":
                self._change_settings()
                continue
            api_responce = get_api_data(address=command, api_key=self.settings.get("api_key"), language=self.settings.get("language"))
            if len(api_responce) > 1:
                print("По заданному паттерну найдено несколько совпадений, выберите нужное")
                for k, v in enumerate(api_responce):
                    print(f"({k + 1}) {v.get('unrestricted_value')}")
                num = input("Введите номер верного варианта или введите stop, если все варианты неверны.\n")
                if num == "stop":
                    print("\n\n\n")
                    continue
                api_responce = api_responce[int(num) - 1]
            if len(api_responce) == 0:
                print("По указанному паттерну не найдено результатов, попробуйте еще\n\n\n")
                continue
            result = get_absolute_data(address=api_responce.get('unrestricted_value'), api_key=self.settings.get("api_key"), language=self.settings.get("language"))[0]
            print(f"Широта: {result['data'].get('geo_lat')} Долгота: {result['data'].get('geo_lon')}\n\n\n")

    def _prepare_settings(self) -> None:
        if self.settings.get("api_url") is None:
            print(f"Не указан URL API сервиса.")
            new_api_url = _get_new_api_url()
            self.settings["api_url"] = new_api_url
            self.dbclient.save_settings()
            print(f"Указано значение: {new_api_url}\n")
        if self.settings.get("api_key") is None:
            print("Не указан ключ API сервиса.")
            new_api_key = _get_new_api_key()
            self.settings["api_key"] = new_api_key
            self.dbclient.save_settings()
            print(f"Указано значение: {new_api_key}\n")
        if self.settings.get("language") is None:
            print("Не указан язык получаемых данных. Введите желаемый язык(например, en) или нажмите Enter, чтобы оставить русский язык")
            new_language = _get_new_language()
            self.settings["language"] = new_language
            self.dbclient.save_settings()
            print(f"Указано значение: {new_language}\n")

    def _show_settings(self) -> None:
        print("Текущие настройки")
        print(f"API URL: {self.settings.get('api_url')}")
        print(f"API KEY: {self.settings.get('api_key')}")
        print(f"Язык получаемых данных: {self.settings.get('language')}\n")

    def _change_settings(self) -> None:
        new_api_url = _get_new_api_url(self.settings.get("api_url"))
        self.settings["api_url"] = new_api_url
        self.dbclient.save_settings(settings=self.settings)
        print(f"Указано значение: {new_api_url}\n")

        new_api_key = _get_new_api_key(self.settings.get("api_key"))
        self.settings["api_key"] = new_api_key
        self.dbclient.save_settings(settings=self.settings)
        print(f"Указано значение: {new_api_key}\n")

        new_language = _get_new_language(self.settings.get("language"))
        self.settings["language"] = new_language
        self.dbclient.save_settings(settings=self.settings)
        print(f"Указано значение: {new_language}\n")

        self._show_settings()

if __name__ == '__main__':
    client = CoordinateFinder()
