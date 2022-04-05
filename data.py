import io
import pandas as pd
from google.cloud import storage
from io import StringIO
import csv
from datetime import date


class Data:

    @staticmethod
    def userTags():
        return Data.csvFromStorage('i9/i9_users_tags.csv')

    @staticmethod
    def userArticlesNotViewed():
        return Data.csvFromStorage('i9/i9_articles.csv')

    @staticmethod
    def dayViews():
        return Data.csvFromStorage('i9/i9_day_views.csv')

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
    def jsonCreator(beeaiCalcs):

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

            fullPath = path+"/"+filname

            s_io = io.StringIO()

            wr = csv.DictWriter(s_io, fieldnames=cols)
            wr.writeheader()

            for recomendation in userRecomendations:
                wr.writerow(recomendation)

            blob = bucket.blob(fullPath)
            blob.upload_from_string(s_io.getvalue())

            s_io.close()
