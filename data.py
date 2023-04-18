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

        try:
            storage_client = storage.Client()
            bucket = storage_client.get_bucket('beeai-sponsored-article')

            blob = bucket.blob(fileName)
            blob = blob.download_as_string()
            blob = blob.decode('utf-8')

            blob = StringIO(blob)

            return pd.read_csv(blob)
        except:
            print('[FILE NOT EXISTS] '+fileName)
            return pd.DataFrame()

    @staticmethod
    def csvCreator(beeaiCalcs, dbName, teamId):

        for userRecomendations in beeaiCalcs:
            # teamId = userRecomendations[0]["team_id"]
            user_id = userRecomendations[0]["user_id"]

            path = str(teamId)
            filename = str(teamId) + '_' + str(user_id) + "_" + str(date.today()) + '.csv'

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

            # full_path = os.environ["APP_ENV"]+"/v2/"+dbName+"/"+path+"/"+filename
            full_path = "prod/v2/"+dbName+"/"+path+"/"+filename

            print("[CREATING] " + dbName + " " + teamId + " " + full_path)

            s_io = io.StringIO()

            wr = csv.DictWriter(s_io, fieldnames=cols)
            wr.writeheader()

            for recomendation in userRecomendations:
                wr.writerow(recomendation)

            blob = bucket.blob(full_path)
            blob.upload_from_string(s_io.getvalue())

            s_io.close()
