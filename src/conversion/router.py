'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus
from fastapi import APIRouter, FastAPI, File, Depends, Form, Response, UploadFile, Request
from src.activemq.factory import MessageFactory
from src.activemq.cache.manager import ActivemqReplyQueueManager
from src.auth.schemas import SessionData
from src.activemq.dependencies import activemq_dispatcher
from src.activemq.dispatcher import ActivemqDispatcher
from src.conversion.factory import ResponseFactory
from src.conversion.schemas import ConversionCreate, ConversionRead

import src.config as config
from src.auth.dependencies import session_data

conversion_router = APIRouter()

@conversion_router.post('/api/v1/convert/to-jpeg')
async def convert_to_jpeg(
    conv_create: ConversionCreate = Depends(ConversionCreate),
    file: UploadFile = File(),
    session_data: SessionData = Depends(session_data),
    dispatcher: ActivemqDispatcher = Depends(activemq_dispatcher),
    reply_queue_manager: ActivemqReplyQueueManager = Depends(ActivemqReplyQueueManager),
    message_factory: MessageFactory = Depends(MessageFactory),
    response_factory: ResponseFactory = Depends(ResponseFactory),
    ):
    dispatcher.send_convert_image_message(
        message_factory.create_convert_image_message(
            file=file, 
            conv_create=conv_create, 
            correlation_id='generate me'
            )
        )
    # todo await conversion reply response
    converted_image_data = await bytes('im converted')
    # todo send store request
    # todo await store reply response
    download_link = await 'download.me'
    # todo send notification request

    return response_factory.conversion_response(
        conv_read=ConversionRead(
            format = conv_create.format,
            size = conv_create.size,
            link = download_link
        )
    )
