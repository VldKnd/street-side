STORAGE_PATH = "../storage"

def put_binary(data, path_to_save, name):
    file_path = f"{STORAGE_PATH}/{path_to_save}/{name}"
    with open(file_path, 'wb') as file:
        file.write(data)

def put_to_storage(data, company_name, date, quater, file_name):
    file_path = f"{company_name}/{date}/{quater}"
    put_binary(data, file_path, file_name)