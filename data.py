import io
import os

import pandas as pd
from google.cloud import storage
from io import StringIO
import csv
from datetime import date


class Data:

    @staticmethod
    def userTags(teamFilename):
        return Data.csvFromStorage(teamFilename)
        # return Data.csvFromStorage(Data.filePathByEnv('users_tags'))

    @staticmethod
    def userArticlesNotViewed(filename):
        return Data.csvFromStorage(filename)

    @staticmethod
    def dayViews(teamFilename):
        return Data.csvFromStorage(teamFilename)
        # return Data.csvFromStorage(Data.filePathByEnv('day_views'))

    @staticmethod
    def filePathByEnv(key):
        return {
            # todo - trocar para pasta PROD (gerada via databricks, confirmar nome...)
            "prod": {
                "users_tags": "analytics_learning/user_tags/user_tags.csv",
                "articles": "analytics_learning/users_articles/users_articles.csv",
                "day_views": "analytics_learning/day_view/day_view.csv"
            },

            "hml": {
                "users_tags": "hml/users_tags.csv",
                "articles": "hml/articles.csv",
                "day_views": "hml/day_views.csv"
            },
        }[os.environ["APP_ENV"]][key]

    @staticmethod
    def localCsv(filename):
        print('reading local!!!!!!!!!!!' + filename)
        return pd.read_csv('./jsonfiles/hml/' + filename + '.csv')


    @staticmethod
    def csvFromStorage(fileName):
        # if os.environ["APP_ENV"] != 'prod':
        #     return Data.localCsv(fileName)

        storage_client = storage.Client()
        bucket = storage_client.get_bucket('beeai-sponsored-article')

        blob = bucket.blob(fileName)
        blob = blob.download_as_string()
        blob = blob.decode('utf-8')

        blob = StringIO(blob)

        return pd.read_csv(blob)

    @staticmethod
    def csvCreator(beeaiCalcs):

        for userRecomendations in beeaiCalcs:
            teamId = userRecomendations[0]["team_id"]
            userId = userRecomendations[0]["user_id"]

            path = str(teamId)
            filname = str(teamId) + '_' + str(userId) + "_" + str(date.today()) + '.csv'

            storage_client = storage.Client()
            bucket = storage_client.get_bucket('beeai-sponsored-article')

            cols = [
                "user_id",
                "id",
                "team_id",
                "percentTagsRelation",
                "percentLastUpdate",
                "percentViewsLastDays",
                "percentViewsRelationTotalUsersLastDay",
                "percentViewsRelationTotal",
                "sum",
                "isOutlier",
            ]

            fullPath = os.environ["APP_ENV"]+"/"+path+"/"+filname

            s_io = io.StringIO()

            wr = csv.DictWriter(s_io, fieldnames=cols)
            wr.writeheader()

            for recomendation in userRecomendations:
                wr.writerow(recomendation)

            blob = bucket.blob(fullPath)
            blob.upload_from_string(s_io.getvalue())

            s_io.close()
