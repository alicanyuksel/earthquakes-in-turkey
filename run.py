from tools import extract_from_web
from tools import clean_data
from tools import create_json_file

def run(file_name):
    extract_from_web(file_name=file_name)
    clean_data(file_name=file_name)
    create_json_file(file_name=file_name)


run(file_name="data.txt")