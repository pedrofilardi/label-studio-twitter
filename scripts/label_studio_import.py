import configparser
from label_studio_sdk import Client
import pymongo

parser = configparser.ConfigParser()
parser.read("config.cfg")

API_KEY = parser.get("label_studio_credential", "LABEL_STUDIO_TOKEN")
LABEL_STUDIO_URL = parser.get("label_studio_credential", "LABEL_STUDIO_URL")
PROJECT_NAME=parser.get("label_studio_credential", "PROJECT_NAME")
LABEL_CONFIG=open("template.xml", "r").read()
            


client = pymongo.MongoClient("mongodb://admin:password@localhost:27017")
db = client.tw
col = db.tweets



def getOrCreate_project(name):
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    ls.check_connection()
    all_projects=[i.title for i in ls.get_projects()]
    if PROJECT_NAME in all_projects:
        #recuperar proyecto
        for project in ls.get_projects():
            if name==project.title:
                return project
    else:
        project=ls.start_project(
            title=PROJECT_NAME,
            label_config=LABEL_CONFIG
        
        )
        return project
            

if __name__ == "__main__":

    project=getOrCreate_project(PROJECT_NAME)
    tasks=[{"data": {"text":text}} for text in list(col.distinct("text"))]
    project.import_tasks(tasks)



