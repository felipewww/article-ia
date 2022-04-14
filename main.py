import os
import sys

from data import Data
from pre_process import PreProcess
from beeai import BeeAI


def calc_sponsored(event, context):

    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    processedData = PreProcess(
        Data.userArticlesNotViewed(),
        Data.userTags(),
        Data.dayViews()
    )

    beeAI = BeeAI(processedData)
    beeAI.calc()

    Data.csvCreator(beeAI.calcs)

if os.environ["APP_ENV"] != 'prod':
    from dotenv import load_dotenv
    load_dotenv()

    if __name__ == '__main__':
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sponsored-article-credential.json"
        globals()[sys.argv[1]](False, False)