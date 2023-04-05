import stomp
import logging


class GetImageReplyListener(stomp.ConnectionListener):
    def __init__(self) -> None:
        super().__init__()
        
    def on_message(self, message):
        logging.info(f'new get image reply message: {message}')
    
class StoreImageReplyListener(stomp.ConnectionListener):
    def __init__(self) -> None:
        super().__init__()
        
    def on_message(self, message):
        logging.info(f'new store image reply message: {message}')
    