import time
from fastapi import UploadFile
import pytest
import stomp
from src.conversion.schemas import ConversionCreate
from src.conversion.message import ConvertImageMsg, ConvertImageReplyMsg
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, MessageFactory, ActivemqWorkerFactory
from src.activemq.manager import ActivemqWorkerManager
from src.activemq.worker import ActiveMqWorker
from src.activemq.utils import SubIdGenerator
import src.config as config
import logging
from PIL import Image
import stomp.utils
from tests.test_base import *

@pytest.fixture()
def mocked_convert_image_worker() -> ActiveMqWorker:
    class MockedConvertImageListener(stomp.ConnectionListener):
        def __init__(self) -> None:
            super().__init__()
        def on_message(self, frame: stomp.utils.Frame):
            msg = ConvertImageMsg()
            msg.deserialize(frame=frame)
            with open('sample_images/result.jpg', 'wb') as f:
                f.write(msg.image_data)

            
    return ActiveMqWorker(
        connection=ActiveMqConnectionFactory.create_connection(
            listener=MockedConvertImageListener()
        ),
        sub_id=SubIdGenerator.generate_next(),
        queue=config.ACTIVEMQ_CONVERT_IMAGE_QUEUE
    )

@pytest.fixture()
def convert_image_reply_worker() -> ActiveMqWorker:
    return ActivemqWorkerFactory.create_convert_image_reply_worker()

@pytest.fixture()
def activemq_worker_manager(
    mocked_convert_image_worker: ActiveMqWorker,
    convert_image_reply_worker: ActiveMqWorker
):
    return ActivemqWorkerManager(workers=[
            mocked_convert_image_worker,
            convert_image_reply_worker
    ])

@pytest.fixture()
def mocked_convert_image_msg(
    message_factory: MessageFactory,
    mocked_upload_file: UploadFile
    ) -> ConvertImageMsg:
    return message_factory.create_convert_image_message(
        file=mocked_upload_file,
        conv_create=ConversionCreate(format='png', size=9876),
        correlation_id='generate_me_pls_123'
    )

def test_convert_image(
    activemq_dispatcher: ActivemqDispatcher, 
    activemq_worker_manager: ActivemqWorkerManager,
    mocked_convert_image_msg: ConvertImageMsg
    ):
    assert type(activemq_dispatcher) == ActivemqDispatcher
    assert type(activemq_worker_manager) == ActivemqWorkerManager
    assert type(mocked_convert_image_msg) == ConvertImageMsg
    
    activemq_worker_manager.submit_threadpool()
    
    activemq_dispatcher.send_convert_image_message(msg=mocked_convert_image_msg)
    
    
    time.sleep(180)
    activemq_worker_manager.stop_threadpool()
    
