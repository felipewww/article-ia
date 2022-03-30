import json
import math
import pprint

import utils

# file_not_viewed = open('user-5-not-view-correct.json')
# file_not_viewed = open('user-5-not-view-PROD.json')
file_not_viewed = open('mar-29-1.json')
sevendays = open('7days-views-hist.json')
# file_user_tags = open('user-tags.json')
file_user_tags = open('user-tags-PROD.json')
dataNotViewed = json.load(file_not_viewed)
dataUserTags = json.load(file_user_tags)

userTagsIndex = {}
usersArticles = {}

import pandas as pd
import numpy as np


def findOutliers(articles):
    df = pd.DataFrame(articles)

    df['day_views'] = pd.to_numeric(df['day_views'], errors='coerce').fillna(0).astype(int)

    percentile75, percentile25 = np.percentile(df['day_views'], [75, 25])
    iqr = percentile75 - percentile25

    upper_limit = percentile75 + 1.5 * iqr
    # lower_limit = percentile25 - 1.5 * iqr

    out_up = df[df['day_views'] > upper_limit]

    print('out_up?????????')


    return out_up


def findArticlesViews(articlesIds):
    # todo - consultar no banco
    return json.load(sevendays)


def init():
    indexUsersTags()
    articlesIds = indexArticles()

    articles = findArticlesViews(articlesIds)
    outliers = findOutliers(articles)

    calcs = []
    for row in usersArticles:
        rowCalc = calcWeights(row, outliers)
        # if rowCalc[0][0] == '948': # daniel
        # if rowCalc[0][0] == '23758': # joao
        if rowCalc[0][0] == '24506': # eu
            print('eu!')
            pprint.pprint(rowCalc)

        calcs.append(rowCalc)


def indexUsersTags():
    for row in dataUserTags:
        userTagsIndex[row["id"]] = row["f0_"].split(",")


def indexArticles():

    articlesIds = []
    for row in dataNotViewed:

        # print(articlesIds.index('1'))
        if row['help_id'] not in articlesIds:
            articlesIds.append(row['help_id'])
        # if articlesIds.index(row['help_id']) < 0:
        #     articlesIds.append(row['help_id'])

        if row["user_id"] not in usersArticles:
            usersArticles[row["user_id"]] = []

        articleRow = {
            "user_id": row["user_id"],
            "id": row["help_id"],
            "views_last_days": int(row["views_last_days"]) if row["views_last_days"] else 0,
            "views_all": int(row["views_all"]) if row["views_all"] else 0,
            "tags_related": 0 if not row["tags"] else tagsRelationsCount(row["tags"], row["user_id"]),
            "last_update_in_days": int(row["last_update_in_days"]) if row["last_update_in_days"] else 0,
            "total_users": int(row["total_users"]) if row["total_users"] else 0,
        }

        usersArticles[row["user_id"]].append(articleRow)

    # print("FOUND articlesIds")
    # print(articlesIds)
    return articlesIds


def tagsRelationsCount(tags, userId):
    if userId not in userTagsIndex:
        return 0

    count = 0
    userTags = userTagsIndex[userId]
    tagsSplit = tags.split(",")

    for tag in tagsSplit:
        if tag in userTags:
            count += 1

    return count


# def calcWeights(articles):
def calcWeights(userId, outliers):

    # print(outliers)
    # print("outliers[outliers['help_id']]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    # OK!
    # r = outliers.query("help_id == '1342052'")
    # print(r)
    # print(len(r))

    # mais ou menos
    # t = [outliers.loc[lambda df: outliers['help_id'] == '1342052']]
    # print(t)
    # print(len(t))

    # OK
    # t = outliers.loc[outliers['help_id'] == '134205', ['help_id']]
    # print(t)
    # print(len(t))

    articles = usersArticles[userId]
    # ttlLastUpdateInDays = utils.sumIndex("last_update_in_days", articles)
    bigger = utils.getBigger("views_last_days", articles)

    totalTags = 0
    if userId in userTagsIndex:
        totalTags = len(userTagsIndex[userId])

    # if totalTags > 0:
    #     print(totalTags)

    # todo - trazer artigos não visto nos ultimos 15 dias que tenham pelo menos uma quantidade razoavel de views nestes 15 dias.

    calcs = []
    for article in articles:

        # print(article['id'])
        # if outliers[outliers['help_id'] == article['id']]:
        #     print('o artigo é um outlier!!!')
        isOutlier = False;

        t = outliers.loc[outliers['help_id'] == article['id'], ['help_id']]
        if len(t):
            isOutlier = True
            # print('OUTLIER FOUND!', article['id'])

        # article = articles[articleIdx]
        # TODO - salvar estes dados abaixo no mysql
        lastUpdate = article["last_update_in_days"]
        percentTagsRelation = utils.percent(article["tags_related"], totalTags)
        # percentViewsLastDays = utils.percent(article["views_last_days"], bigger)
        percentViewsLastDays = utils.percent(article["views_last_days"], article["views_all"])
        percentViewsRelationTotalUsersLastDay = utils.percent(article["views_last_days"], article["total_users"])
        percentViewsRelationTotal = utils.percent(article["views_all"], article["total_users"])

        percentLastUpdate = 1 if lastUpdate == 0 else utils.calcInvertedPercent(article["last_update_in_days"])

        t = (
            article['user_id'],
            article['id'],
            # allWeightOne,
            round(percentTagsRelation, 3),
            round(percentViewsLastDays, 3),
            round(percentLastUpdate, 3),
            round(percentViewsRelationTotalUsersLastDay, 3),
            round(percentViewsRelationTotal, 3),
            round(percentTagsRelation + percentViewsLastDays + percentLastUpdate + percentViewsRelationTotalUsersLastDay + percentViewsRelationTotal, 3),
            isOutlier
        )
        calcs.append(t)

    # sorted_list = sorted(calcs, key=lambda x: x[4], reverse=True)
    sorted_list = sorted(calcs, key=lambda x: x[7], reverse=True)

    # print('newlist!-------------------------------')
    # pprint.pprint(newlist)
    return sorted_list


init()

# distância euclidiana - aula 6 - modulo 1

#daniel
# '172144'
# '204475'
# '192494'
# '182388'
# '211500'

#joao
# [('23758', '167466', 4.313, 5.063, 4.748, 4.36, 7.251),
#  ('23758', '172144', 2.502, 3.002, 3.271, 2.635, 3.602),
#  ('23758', '204475', 2.332, 3.332, 3.241, 2.426, 2.661),
#  ('23758', '112739', 2.634, 3.134, 2.665, 2.677, 4.623),
#  ('23758', '211500', 1.359, 1.734, 2.128, 1.395, 1.395)]
