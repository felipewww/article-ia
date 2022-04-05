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
        # self.calcs = []
        self.preProcess = preProcess

    def calc(self):
        self.calcOutliers()

        idx = 0

        for row in self.preProcess.usersArticles:
            rowCalc = self.calcWeightsForUser(row)

            # self.printTest(idx, rowCalc)
            idx = idx + 1

            self.calcs.append(rowCalc)

    def calcOutliers(self):
        self.preProcess.dfDayViews['day_views'] = pd.to_numeric(self.preProcess.dfDayViews['day_views'], errors='coerce').fillna(0).astype(int)

        percentile75, percentile25 = np.percentile(self.preProcess.dfDayViews['day_views'], [75, 25])
        iqr = percentile75 - percentile25

        upper_limit = percentile75 + 1.5 * iqr
        # lower_limit = percentile25 - 1.5 * iqr

        self.outliers = self.preProcess.dfDayViews[self.preProcess.dfDayViews['day_views'] > upper_limit]

    def calcWeightsForUser(self, userId):
        articles = self.preProcess.usersArticles[userId]

        # ttlLastUpdateInDays = utils.sumIndex("last_update_in_days", articles)
        # bigger = utils.getBigger("views_last_days", articles)

        totalTags = 0
        if userId in self.preProcess.userTags:
            totalTags = len(self.preProcess.userTags[userId])

        calcs = []
        for article in articles:

            isOutlier = 0

            t = self.outliers.loc[self.outliers['help_id'] == article['id'], ['help_id']]
            if len(t):
                isOutlier = 1

            # article = articles[articleIdx]
            # TODO - salvar estes dados abaixo no mysql
            lastUpdate = article["last_update_in_days"]
            percentTagsRelation = utils.percent(article["tags_related"], totalTags)
            # percentViewsLastDays = utils.percent(article["views_last_days"], bigger)
            percentViewsLastDays = utils.percent(article["views_last_days"], article["total_views"])
            percentViewsRelationTotalUsersLastDay = utils.percent(article["views_last_days"], article["total_users"])
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

        # sorted_list = sorted(calcs, key=lambda x: x[7], reverse=True)

        # return sorted_list
        return calcs

    @staticmethod
    def printTest(idx, rowCalc):
        if idx == 10 or idx == 1000 or idx == 2000 or idx == 3000 or idx == 4000:
            print('\nrowCalc')
            pprint.pprint(rowCalc)

        # print(rowCalc)
        # if rowCalc[0][0] == '948': # daniel
        # if rowCalc[0][0] == '23758': # joao
        if rowCalc[0][0] == '24506':  # eu
            print('eu!')
            # pprint.pprint(rowCalc)