import email
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import stomp
import stomp.utils
from src.activemq.cache.message import CachedMessage

class StoreImageMsg(CachedMessage):
    def __init__(
        self, 
        correlation_id: str = None,
        filename: str = None, 
        image_data: bytes = None
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.filename = filename
        self.image_data = image_data
            
    def serialize(self):
        pass
    
    def deserialize(self, frame: stomp.utils.Frame):
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'image_data':
                self.image_data = part.get_payload(decode=True)
            elif part.get('Content-ID') == 'filename':
                self.image_format = part.get_payload(decode=True)
        self.correlation_id = frame.headers.get('correlation_id')
    
class StoreImageReplyMsg(CachedMessage):
    def __init__(
        self,
        correlation_id: str
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
    
    def serialize(self):
        mime_multipart = MIMEMultipart()
        part = MIMEText(self.url)
        part.add_header('Content-ID', 'url')
        mime_multipart.attach(part)
        return mime_multipart.as_string()  
    
    def deserialize(self, frame: stomp.utils.Frame):
        pass

class GetImageMsg(CachedMessage):
    def __init__(self, correlation_id: str, filename: str) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.filename = filename
            
    def serialize(self):
        pass        
    
    def deserialize(self, frame: stomp.utils.Frame):
        pass
    
class GetImageReplyMsg(CachedMessage):
    def __init__(self, correlation_id: str, url: str) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.url = url
            
    def serialize(self):
        pass        
    
    def deserialize(self, frame: stomp.utils.Frame):
        pass

class DeleteImageMsg():
    def __init__(self, filename: str) -> None:
        self.filename = filename
            
    def serialize(self):
        pass        
