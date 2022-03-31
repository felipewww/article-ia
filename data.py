import json
import pandas as pd


class Data:

    @staticmethod
    def userTags():
        file_user_tags = open('jsonfiles/user-tags-PROD.json')
        return json.load(file_user_tags)

    @staticmethod
    def userArticlesNotViewed():
        return pd.read_csv('jsonfiles/pasch/users-articles.csv')

    @staticmethod
    def sevenDaysHistory():
        return pd.read_csv('jsonfiles/pasch/day-views.csv')

    @staticmethod
    def dayViews():
        return pd.read_csv('jsonfiles/pasch/day-views.csv')