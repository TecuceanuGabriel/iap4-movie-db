from app.extensions import scheduler
from app.extensions import mongo

from datetime import datetime
from datetime import timedelta

@scheduler.task("interval", id="clear_friend_requests", hours=12)
def clear_friend_requests():
    mongo.db.fd_requests.delete_many(
        {
            "status": "rejected",
            "created_at": {"$lt": datetime.now() - timedelta(days=1)},
        }
    )
    mongo.db.fd_requests.delete_many(
        {
            "status": "accepted",
            "created_at": {"$lt": datetime.now() - timedelta(days=1)},
        }
    )
    print("Cleared old friend requests")
