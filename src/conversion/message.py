import email
from email.mime.image import MIMEImage
import xml.etree.ElementTree as ET
from src.activemq.cache.message import CachedMessage
import stomp.utils


class ConvertImageMsg(CachedMessage):
    def __init__(
        self, 
        correlation_id: str = None,
        image_data: bytes = None, 
        content_type: str = None, 
        image_format: str = None
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.image_data = image_data
        self.image_format = image_format
        self.content_type = content_type
        
    # def serialize(self) -> str:
    #     xml_root = ET.Element("convert_image")
    #     xml_image_format = ET.SubElement(xml_root, "image_format")
    #     xml_image_format.text = self.image_format
    #     xml_image_data_mimed = ET.SubElement(xml_root, "image_data_mimed")
    #     xml_image_data_mimed.text = MIMEImage(self.image_data).get_payload()
    #     return ET.tostring(xml_root, encoding='utf-8', xml_declaration=True)
    
    # def deserialize(self, frame: stomp.utils.Frame) -> None:
    #     xml_root = ET.fromstring(frame.body) # <convert_image>
    #     mime_message = email.message_from_string(xml_root.find("image_data_mimed").text)
    #     self.image_data = mime_message.get_payload(decode=True)
    #     self.correlation_id = frame.headers.get('correlation_id')
    #     self.image_format = xml_root.find("image_format").text
    #     self.content_type = frame.headers.get('content-type')
    
    def serialize(self) -> str:
        mimed_image = MIMEImage(self.image_data).get_payload()
        return 'todo'
    
    def deserialize(self, frame: stomp.utils.Frame) -> None:
        pass

class ConvertImageReplyMsg(CachedMessage):
    def __init__(self, correlation_id: str, image_data: bytes) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.image_data = image_data
        
    def deserialize(self, frame: stomp.utils.Frame):
        xml_root = ET.fromstring(frame.body)
        xml_root = xml_root.find("convert_image_reply").text
        xml_image_data_mimed = xml_root.find("image_data_mimed").text
        self.correlation_id = frame.headers['correlation_id']

