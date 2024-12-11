class FeedItem:
    def __init__(self, friendEmail, message, timestamp):
        self.friendEmail = friendEmail
        self.message = message
        self.timestamp = timestamp

    def to_message(self):
        return f"{self.friendEmail}: {self.message}, {self.timestamp}"
