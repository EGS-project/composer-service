'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus

from fastapi import (APIRouter, Depends, FastAPI, File, Form, Request,
                     Response, UploadFile)

import src.config as config
import src.user.models as models
from src.activemq.cache.manager import ActivemqCacheManager
from src.activemq.cache.utils import CorrelationIdGenerator
from src.activemq.dependencies import (activemq_cache_manager,
                                       activemq_dispatcher)
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import MessageFactory
from src.auth.dependencies import session_data
from src.auth.schemas import SessionData
from src.conversion.factory import ResponseFactory
from src.conversion.message import ConvertImageReplyMsg
from src.conversion.schemas import ConversionCreate, ConversionRead
from src.s3_connector.message import StoreImageReplyMsg
from src.s3_connector.utils import FilenameGenerator
from src.user.dependencies import current_user

conversion_router = APIRouter()

@conversion_router.post('/api/v1/convert')
async def convert_to_jpeg(
    conv_create: ConversionCreate = Depends(ConversionCreate),
    file: UploadFile = File(),
    dispatcher: ActivemqDispatcher = Depends(activemq_dispatcher),
    activemq_cache_manager: ActivemqCacheManager = Depends(activemq_cache_manager),
    message_factory: MessageFactory = Depends(MessageFactory),
    response_factory: ResponseFactory = Depends(ResponseFactory),
    current_user: models.User = Depends(current_user),
    ):
    correlation_id = CorrelationIdGenerator.generate()
    # correlation_id = '1234' # integration local test
    dispatcher.send_convert_image_message(
        message_factory.create_convert_image_message(
            file=file, 
            conv_create=conv_create, 
            correlation_id=correlation_id
            )
        )
    convert_reply: ConvertImageReplyMsg = await activemq_cache_manager.await_reply_message(
        correlation_id=correlation_id
    )

    correlation_id = CorrelationIdGenerator.generate()
    # correlation_id = '5678' # integration local test
    dispatcher.send_store_image_message(
        message_factory.create_store_image_message(
            filename=FilenameGenerator.generate(
                user_id=current_user.id,
                original_filename=file.filename),
            image_data=convert_reply.image_data,
            correlation_id=correlation_id            
        )
    )
    store_reply: StoreImageReplyMsg = await activemq_cache_manager.await_reply_message(
        correlation_id=correlation_id
    )
    
    dispatcher.send_notification_message(
        message_factory.create_notification_message(
            email=current_user.email,
            subject='Your conversion download link!',
            message=f'Thank you for using our product. Your link is here: {store_reply.url}'
        )
    )

    return response_factory.conversion_response(
        conv_read=ConversionRead(
            format = conv_create.format,
            size = conv_create.size,
            link = store_reply.url
        )
    )
