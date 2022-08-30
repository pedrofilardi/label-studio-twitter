import configparser
from label_studio_sdk import Client
import psycopg2

parser = configparser.ConfigParser()
parser.read("config.cfg")

API_KEY = parser.get("label_studio_credential", "LABEL_STUDIO_TOKEN")
LABEL_STUDIO_URL = parser.get("label_studio_credential", "LABEL_STUDIO_URL")
PROJECT_NAME=parser.get("label_studio_credential", "PROJECT_NAME")

def getProject(name):
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    ls.check_connection()
    all_projects=[i.title for i in ls.get_projects()]
    if PROJECT_NAME in all_projects:
        #recuperar proyecto
        for project in ls.get_projects():
            if name==project.title:
                return project
    else:
        raise Exception("No project named" + name)

def parse_tasks(data):
    return [(task["data"]["text"],
    task["annotations"][0]["result"][0]["value"]["choices"][0]) for task in data if task["annotations"][0]["result"]]

if __name__ == "__main__":

    conexion = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="admin", port=5433)
    cur = conexion.cursor()

    project=getProject(PROJECT_NAME)
    data=project.export_tasks()
    values=parse_tasks(data)
    
    cur.execute("CREATE TABLE IF NOT EXISTS labeled_data_{} (text varchar, label varchar);".format(PROJECT_NAME))
    cur.executemany("INSERT INTO labeled_data_{} VALUES(%s,%s)".format(PROJECT_NAME), values)
    conexion.commit()
