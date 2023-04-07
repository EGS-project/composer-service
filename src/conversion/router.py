'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus
from fastapi import APIRouter, FastAPI, File, Depends, Form, Response, UploadFile, Request
from src.conversion.message import ConvertImageReplyMsg
from src.activemq.factory import MessageFactory
from src.activemq.cache.manager import ActivemqCacheManager
from src.auth.schemas import SessionData
from src.activemq.dependencies import activemq_dispatcher, activemq_cache_manager
from src.activemq.dispatcher import ActivemqDispatcher
from src.conversion.factory import ResponseFactory
from src.conversion.schemas import ConversionCreate, ConversionRead

import src.config as config
from src.auth.dependencies import session_data

conversion_router = APIRouter()

@conversion_router.post('/api/v1/convert')
async def convert_to_jpeg(
    conv_create: ConversionCreate = Depends(ConversionCreate),
    file: UploadFile = File(),
    session_data: SessionData = Depends(session_data),
    dispatcher: ActivemqDispatcher = Depends(activemq_dispatcher),
    activemq_cache_manager: ActivemqCacheManager = Depends(activemq_cache_manager),
    message_factory: MessageFactory = Depends(MessageFactory),
    response_factory: ResponseFactory = Depends(ResponseFactory),
    ):
    correlation_id = 'generate me'
    dispatcher.send_convert_image_message(
        message_factory.create_convert_image_message(
            file=file, 
            conv_create=conv_create, 
            correlation_id=correlation_id
            )
        )
    converted_image_reply_msg: ConvertImageReplyMsg = await activemq_cache_manager.await_reply_message(
        correlation_id=correlation_id
    )
    # todo send store request
    # todo await store reply response
    download_link = 'download.me'
    # todo send notification request

    return response_factory.conversion_response(
        conv_read=ConversionRead(
            format = conv_create.format,
            size = conv_create.size,
            link = download_link
        )
    )
