import time
from src.activemq.cache.message import CachedMessage
from src.activemq.cache.cache import ActivemqMessageCache


class ActivemqCacheManager:
    def __init__(
        self,
        activemq_message_cache: ActivemqMessageCache
        ) -> None:
        self.activemq_message_cache = activemq_message_cache
        self.timeout = 200
        self.refresh_time = 0.1
        
    async def await_reply_message(
        self,
        correlation_id: str
        ) -> CachedMessage:
        start_time = time.time()
        while not (msg:= self.activemq_message_cache.get(correlation_id=correlation_id)):
            elapsed_time = time.time() - start_time
            if elapsed_time > self.timeout:
                raise TimeoutError()
            time.sleep(self.refresh_time)

        return msg
