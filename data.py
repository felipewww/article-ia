import io
import os

import pandas as pd
from google.cloud import storage
from io import StringIO
import csv
from datetime import date


class Data:

    @staticmethod
    def userTags():
        return Data.csvFromStorage(Data.filePathByEnv('users_tags'))

    @staticmethod
    def userArticlesNotViewed():
        return Data.csvFromStorage(Data.filePathByEnv('articles'))

    @staticmethod
    def dayViews():
        return Data.csvFromStorage(Data.filePathByEnv('day_views'))

    @staticmethod
    def filePathByEnv(key):
        return {
            # todo - trocar para pasta PROD (gerada via databricks, confirmar nome...)
            "prod": {
                "users_tags": "i9/i9_users_tags.csv",
                "articles": "i9/i9_articles.csv",
                "day_views": "i9/i9_day_views.csv"
            },

            "hml": {
                "users_tags": "hml/users_tags.csv",
                "articles": "hml/articles.csv",
                "day_views": "hml/day_views.csv"
            },
        }[os.environ["APP_ENV"]][key]

    @staticmethod
    def csvFromStorage(fileName):
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
