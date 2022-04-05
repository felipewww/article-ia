from data import Data
from pre_process import PreProcess
from beeai import BeeAI
# from dotenv import load_dotenv
# load_dotenv()


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

    Data.jsonCreator(beeAI.calcs)
