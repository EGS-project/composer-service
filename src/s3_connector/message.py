import xml.etree.ElementTree as ET
import base64
from PIL import Image
from src.activemq.cache.message import CachedMessage


class StoreImageMsg(CachedMessage):
    def __init__(self, correlation_id: str, filename: str, image_data: bytes) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.filename = filename
        self.image_data = image_data
            
    def serialize(self):
        xml_root = ET.Element("store_image")
        xml_filename = ET.SubElement(xml_root, "filename")
        xml_filename.text = self.filename
        # todo serialize MIME
        return ET.tostring(xml_root, encoding='utf-8', xml_declaration=True)
    
class StoreImageReplyMsg(CachedMessage):
    def __init__(self, correlation_id: str) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
            
    def deserialize(self, message):
        xml_root = ET.fromstring(message.body)
        xml_root = xml_root.find("get_image_reply").text
        self.url= xml_root.find("url").text
        self.correlation_id = message.headers['correlation_id']

class GetImageMsg(CachedMessage):
    def __init__(self, correlation_id: str, filename: str) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.filename = filename
            
    def serialize(self):
        xml_root = ET.Element("get_image")
        xml_filename = ET.SubElement(xml_root, "filename")
        xml_filename.text = self.filename
        return ET.tostring(xml_root, encoding='utf-8', xml_declaration=True)
    
class GetImageReplyMsg(CachedMessage):
    def __init__(self, correlation_id: str, url: str) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.url = url
            
    def deserialize(self, message):
        xml_root = ET.fromstring(message.body)
        xml_root = xml_root.find("get_image_reply").text
        self.url= xml_root.find("url").text
        self.correlation_id = message.headers['correlation_id']

class DeleteImageMsg():
    def __init__(self, filename: str) -> None:
        self.filename = filename
            
    def serialize(self):
        xml_root = ET.Element("delete_image")
        xml_filename = ET.SubElement(xml_root, "filename")
        xml_filename.text = self.filename
        return ET.tostring(xml_root, encoding='utf-8', xml_declaration=True)