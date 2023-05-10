from src.activemq.cache.message import CachedMessage

class ActivemqMessageCache:
    
    REPLY_MESSAGE_CACHE: dict = {}
    
    @classmethod
    def push(cls, msg: CachedMessage) -> None:
        cls.REPLY_MESSAGE_CACHE[msg.correlation_id] = msg
    
    @classmethod
    def pop(cls, correlation_id: str) -> None:
        del cls.REPLY_MESSAGE_CACHE[correlation_id]
    
    @classmethod
    def get(cls, correlation_id: str) -> CachedMessage:
        if correlation_id in cls.REPLY_MESSAGE_CACHE:
            return cls.REPLY_MESSAGE_CACHE[correlation_id]
        return None
