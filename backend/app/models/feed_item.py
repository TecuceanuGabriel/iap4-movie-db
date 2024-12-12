class FeedItem:
    """A class representing a feed item."""

    def __init__(self, friendEmail, message, timestamp):
        self.friendEmail = friendEmail
        self.message = message
        self.timestamp = timestamp

    def to_message(self):
        """Return the feed item as a message."""

        return f"{self.friendEmail}: {self.message}, {self.timestamp}"
