import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import os
import config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

user = os.environ.get('COSMOS_CONTAINER', 'user')
question = os.environ.get('COSMOS_CONTAINER', 'question')
answer = os.environ.get('COSMOS_CONTAINER', 'answer')


def createuser(time, id):
    users = {
            'PartitionKey': 'id',
            'id': id,
            'userentry': time
            }
    return users


def createquestion(question, userid, time, id):
    question = {'PartitionKey': 'qid',
                'id': id,
                'question': question,
                'userid': userid,
                'timeask': time
            }
    return question

def createanswer(answer, userid, time, id):
    answer = {
            'partitionKey': 'aid',
            'id': id,
            'answer': answer,
            'userid': userid,
            'timeask': time
            }
    return answer

def create_item(container, item):
    try:
        container.create_item(body=item)
    except exceptions.CosmosResourceExistsError:
        print('this resource exists')


def upsert_item(container, item):
    print('\nUpserting an item\n')
    container.upsert_item(body=item)

def read_all(container, uid):
    total = []
    for doc in container.read_all_items(max_item_count=10):
        if uid == doc["userid"]:
           total.append(doc)
    return total



client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})
db = client.get_database_client(DATABASE_ID)
print('Database with id \'{0}\' was found'.format(DATABASE_ID))
ucontainer = db.get_container_client(user)
qcontainer = db.get_container_client(question)
acontainer = db.get_container_client(answer)
print('Container with id \'{0}\' was found'.format(user))



