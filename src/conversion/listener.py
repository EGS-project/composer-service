import stomp
import stomp.utils
import logging
from src.activemq.cache.cache import ActivemqMessageCache
from src.activemq.listener import ReplyListener

from src.conversion.message import ConvertImageReplyMsg


class ConvertImageReplyListener(ReplyListener):
    def __init__(
        self, 
        activemq_message_cache: ActivemqMessageCache
        ) -> None:
        ReplyListener.__init__(
            self,
            activemq_message_cache=activemq_message_cache
            )
        
    def on_message(self, frame: stomp.utils.Frame):
        msg = ConvertImageReplyMsg()
        msg.deserialize(frame=frame)
        # for debug
        # with open('sample_images/reply.png', 'wb') as f:
        #     f.write(msg.image_data)
        self.activemq_message_cache.push(msg=msg)
