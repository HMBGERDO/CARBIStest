import sqlite3

class DatabaseClient:
    def __init__(self, dbname:str="db.sqlite3") -> None:
        """
        Creating connection to sqlite3 file, getting cursor
        """
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()
        pass

    def save_settings(self, settings:dict) -> None:
        """
        Saving settings in database
        """
        api_url = settings.get("api_url")
        api_key = settings.get("api_key")
        language = settings.get("language")
        prepare_command = "CREATE TABLE IF NOT EXISTS settings (id INT AUTO_INCREMENT PRIMARY KEY, api_url TEXT, api_key VARCHAR(50), language VARCHAR(2));"
        self.cursor.execute(prepare_command)
        main_command = f"INSERT OR REPLACE INTO settings(id, api_url, api_key, language) VALUES(1, '{api_url}', '{api_key}', '{language}');"
        self.cursor.execute(main_command)
        self.connection.commit()
        pass

    def load_settings(self) -> dict:
        """
        Getting settings from database
        """
        self.cursor.execute("SELECT * FROM settings WHERE id=1;")
        db_responce = self.cursor.fetchall()
        result = _parse_settings(db_responce)
        return result

def _parse_settings(settings:list) -> dict:
    result = {'api_url':None, 'api_key':None, 'language':None}
    if len(settings) == 0:
        return result
    settings = settings[0]
    if len(settings) == 0:
        return result
    result["api_url"] = settings[1]
    result["api_key"] = settings[2]
    result["language"] = settings[3]
    return result

if __name__ == '__main__':
    dbclient = DatabaseClient(dbname='example.sqlite3')
    # dbclient.save_settings({'api_url':'testurl', 'api_key':'testkey', 'language':'testlanguage'})
    print(dbclient.load_settings())