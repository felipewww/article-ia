from data import Data
from pre_process import PreProcess
from beeai import BeeAI

processedData = PreProcess(
    Data.userArticlesNotViewed(),
    Data.userTags(),
    Data.dayViews()
)

beeAI = BeeAI(processedData).calc()
