

from http import HTTPStatus
from fastapi import Response, UploadFile
from src.conversion.message import ConvertImageMsg

from src.conversion.schemas import ConversionCreate, ConversionRead


class ResponseFactory:
    def __init__(self) -> None:
        pass
    
    def conversion_response(self, conv_read: ConversionRead) -> Response:      
        return Response(status_code=HTTPStatus.OK, content=conv_read.json())
