from app.extensions import mongo

import threading


def add_to_feed_thread(userEmail, feedItem):
    """Add a feed message to the user's feed, in a separate thread."""

    def add_to_feed(userEmail, feedItem):
        user = mongo.db.users.find_one({"email": userEmail})

        if not user:
            return

        feed = user.get("feed")
        feed.append(feedItem.to_message())
        feed.pop(0) if len(feed) > 20 else None

        mongo.db.users.update_one(
            {"email": userEmail},
            {"$set": {"feed": feed}},
        )

    print("Adding to feed")

    thread = threading.Thread(target=add_to_feed, args=(userEmail, feedItem))
    thread.start()

    return thread


def add_to_friends_feed_thread(userEmail, feedItem):
    """Add a feed message to all the user's friends' feeds, in a separate
    thread."""

    def add_to_friends_feed(userEmail, feedItem):
        user = mongo.db.users.find_one({"email": userEmail})

        if not user:
            return

        friends = mongo.db.friendship.find(
            {"$or": [{"sender": userEmail}, {"recipient": userEmail}]}
        )
        for friend in friends:
            friendEmail = (
                friend.get("sender")
                if friend.get("recipient") == userEmail
                else friend.get("recipient")
            )

            friend = mongo.db.users.find_one({"email": friendEmail})

            feed = friend.get("feed")
            feed.append(feedItem.to_message())
            feed.pop(0) if len(feed) > 20 else None

            mongo.db.users.update_one(
                {"email": friendEmail},
                {"$set": {"feed": feed}},
            )

    print("Adding to friends feed")

    thread = threading.Thread(
        target=add_to_friends_feed, args=(userEmail, feedItem)
    )
    thread.start()

    return thread
