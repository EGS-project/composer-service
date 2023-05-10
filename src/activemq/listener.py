import stomp

from src.activemq.cache.cache import ActivemqMessageCache

class ReplyListener(stomp.ConnectionListener):
    def __init__(
        self,
        activemq_message_cache: ActivemqMessageCache
        ) -> None:
        super().__init__()
        self.activemq_message_cache = activemq_message_cache        
