import os
# import sys

import base64
import json
from data import Data
from pre_process import PreProcess
from beeai import BeeAI

# from dotenv import load_dotenv
# load_dotenv()

from datetime import date


def mount_path(db, team_id, folder_name):
    return 'v2/'+db+'/'+folder_name+'/'+str(date.today())+'/team_id_partition='+team_id+'/'+folder_name+'.csv'


def calc_sponsored(event, context):

    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    ############################################################################
    # TODO - testar team id invalida não encontrarndo DAY VIEWS ou USER_TAGS
    ############################################################################

    pubsub_message = {
        "filename": "v2/beedoo/user_articles/2023-01-24/team_id_partition=182/part-00006-tid-2827069645108385745-2046b092-7728-42f2-94d3-2b5840597471-8038-2.c000.csv",
        "dbName": "beedoo",
        "teamId": "182"
    }

    if (os.environ["APP_ENV"] == 'prod'):
        pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))

    path_tags = mount_path(pubsub_message['dbName'], pubsub_message['teamId'], 'user_tags')
    path_dv = mount_path(pubsub_message['dbName'], pubsub_message['teamId'], 'day_views')

    processedData = PreProcess(
        Data.userArticlesNotViewed(pubsub_message['filename']),
        Data.csvFromStorage(path_tags),
        Data.csvFromStorage(path_dv)
    )

    beeAI = BeeAI(processedData)
    beeAI.calc()

    Data.csvCreator(beeAI.calcs)

# if os.environ["APP_ENV"] != 'prod':
#     from dotenv import load_dotenv
#     load_dotenv()
#
#     if __name__ == '__main__':
#         os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sponsored-article-credential.json"
#         globals()[sys.argv[1]](False, False)

# if __name__ == '__main__':
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sponsored-article-credential.json"
#     globals()[sys.argv[1]](
#         "local", None
#     )