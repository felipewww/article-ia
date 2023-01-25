import pprint

import pandas as pd
import numpy as np
import utils


class BeeAI:

    outliers = []
    calcs = []

    def __init__(self, preProcess):
        """

        :param preProcess: PreProcess
        """
        self.preProcess = preProcess

    def calc(self):
        self.calcOutliers()

        idx = 0

        for row in self.preProcess.usersArticles:
            rowCalc = self.calcWeightsForUser(row)

            idx = idx + 1

            self.calcs.append(rowCalc)

    def calcOutliers(self):
        self.preProcess.dfDayViews['count'] = pd.to_numeric(self.preProcess.dfDayViews['count'], errors='coerce').fillna(0).astype(int)

        percentile75, percentile25 = np.percentile(self.preProcess.dfDayViews['count'], [75, 25])
        iqr = percentile75 - percentile25

        upper_limit = percentile75 + 1.5 * iqr

        self.outliers = self.preProcess.dfDayViews[self.preProcess.dfDayViews['count'] > upper_limit]

    def calcWeightsForUser(self, userId):
        articles = self.preProcess.usersArticles[userId]

        totalTags = 0
        if userId in self.preProcess.userTags:
            totalTags = len(self.preProcess.userTags[userId])

        calcs = []
        for article in articles:

            isOutlier = 0

            t = self.outliers.loc[self.outliers['hv_help_id'] == article['id'], ['hv_help_id']]
            if len(t):
                isOutlier = 1

            lastUpdate = article["last_update_in_days"]
            percentTagsRelation = utils.percent(article["tags_related"], totalTags)
            percentViewsLastDays = utils.percent(article["total_views_last_days"], article["total_views"])
            percentViewsRelationTotalUsersLastDay = utils.percent(article["total_views_last_days"], article["total_users"])
            percentViewsRelationTotal = utils.percent(article["total_views"], article["total_users"])

            percentLastUpdate = 1 if lastUpdate == 0 else utils.calcInvertedPercent(article["last_update_in_days"])

            t = {
                "user_id": article['user_id'],
                "id": article['id'],
                "team_id": article['team_id'],
                "percentTagsRelation": round(percentTagsRelation, 3),
                "percentLastUpdate": round(percentLastUpdate, 3),
                "percentViewsLastDays": round(percentViewsLastDays, 3),
                "percentViewsRelationTotalUsersLastDay": round(percentViewsRelationTotalUsersLastDay, 3),
                "percentViewsRelationTotal": round(percentViewsRelationTotal, 3),
                "sum": round(
                    percentTagsRelation + percentViewsLastDays + percentLastUpdate + percentViewsRelationTotalUsersLastDay + percentViewsRelationTotal,
                    3),
                "isOutlier": isOutlier
            }
            calcs.append(t)

        return calcs

    @staticmethod
    def printTest(idx, rowCalc):
        if idx == 10 or idx == 1000 or idx == 2000 or idx == 3000 or idx == 4000:
            print('\nrowCalc')
            pprint.pprint(rowCalc)

        if rowCalc[0][0] == '24506':  # eu
            print('eu!')
