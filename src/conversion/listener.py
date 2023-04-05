import stomp
import logging


class ConvertImageReplyListener(stomp.ConnectionListener):
    def __init__(self) -> None:
        super().__init__()
        
    def on_message(self, message):
        logging.info(f'new convert image reply message: {message}')
