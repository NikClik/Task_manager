import json

def check_json_settings():
    try:
        file = open('Settings.json')
    except IOError as e:
        with open('Settings.json', 'w') as outfile:
            json.dump({"Settings_for_dataBase": [{
                            "database": "postgres",
                            "user": "postgres",
                            "host": "localhost",
                            "port": "5432",
                            "password": "1234"
                        }
                ]}, outfile)


def get_json_settings():
    check_json_settings()
    with open('Settings.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
        JSON_database = data['Settings_for_dataBase'][0].get('database')
        JSON_user = data['Settings_for_dataBase'][0].get('user')
        JSON_host = data['Settings_for_dataBase'][0].get('host')
        JSON_port = data['Settings_for_dataBase'][0].get('port')
        JSON_password = data['Settings_for_dataBase'][0].get('password')
    conn_str = "postgresql://"+JSON_user+":"+JSON_password+"@"+JSON_host+":"+JSON_port+"/"+JSON_database
    return conn_str


def connect_str_to_db():
    connect_str = get_json_settings()
    return connect_str
