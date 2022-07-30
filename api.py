from dadata import Dadata

def get_api_data(api_key: str, address:str, language:str) -> list:
    """
    Creates connection to API service and getting data
    """
    with Dadata(api_key) as client:
        responce = client.suggest(name="address", query=address, language=language)
        return responce

def get_absolute_data(api_key: str, address:str, language:str) -> list:
    """
    Creates connection to API service and getting data
    """
    with Dadata(api_key) as client:
        responce = client.suggest(name="address", query=address, language=language, count=1)
        return responce

if __name__ == '__main__':
    api_key = input("Введите API ключ\nAPI ключ= ")
    address = input("Введите адрес\nАдрес= ")
    print(get_api_data(api_key=api_key, address=address))
