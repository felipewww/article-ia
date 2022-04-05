class PreProcess:

    articlesIds = []

    usersArticles = {}

    userTags = {}

    def __init__(
            self,
            dfNotViewed,
            dfUserTags,
            dfDayViews
    ):
        self.dfNotViewed = dfNotViewed
        self.dfUserTags = dfUserTags
        self.dfDayViews = dfDayViews

        self.indexArticles()
        self.indexUsersTags()

    def indexArticles(self):

        for key, row in self.dfNotViewed.iterrows():

            if row['help_id'] not in self.articlesIds:
                self.articlesIds.append(row['help_id'])

            if row['user_id'] not in self.usersArticles:
                self.usersArticles[row['user_id']] = []

            articleRow = {
                "user_id": row["user_id"],
                "id": row["help_id"],
                "team_id": row["team_id"],
                "views_last_days": int(row["views_last_days"]) if row["views_last_days"] else 0,
                "total_views": int(row["total_views"]) if row["total_views"] else 0,
                "tags_related": 0 if not row["tags"] else self.tagsRelationsCount(row["tags"], row["user_id"]),
                "last_update_in_days": int(row["last_update_in_days"]) if row["last_update_in_days"] else 0,
                "total_users": int(row["total_users"]) if row["total_users"] else 0,
            }

            self.usersArticles[row["user_id"]].append(articleRow)

    def indexUsersTags(self):
        for key, row in self.dfUserTags.iterrows():
            self.userTags[int(row["id"])] = row["tags"].split("|")

    def tagsRelationsCount(self, tags, userId):
        if userId not in self.userTags:
            return 0

        count = 0
        userTags = self.userTags[userId]
        tagsSplit = tags.split("|")

        for tag in tagsSplit:
            if tag in userTags:
                count += 1

        return count