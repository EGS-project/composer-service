import pytest
import stomp
import stomp.utils
from src.activemq.manager import ActivemqWorkerManager
from src.s3_connector.message import GetImageMsg, StoreImageMsg
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, MessageFactory
from src.s3_connector.listener import GetImageReplyListener, StoreImageReplyListener
import src.config as config
import logging
from tests.test_base import *

@pytest.fixture()
def store_image_conn() -> stomp.connect.StompConnection11:
    class MockedS3ConnectorStoreImageListener(stomp.ConnectionListener):
        def __init__(self) -> None:
            super().__init__()
        def on_message(self, frame: stomp.utils.Frame):
            msg = StoreImageMsg()
    
    return ActiveMqConnectionFactory.create_connection(
        broker_host=config.ACTIVEMQ_HOST,
        broker_port=int(config.ACTIVEMQ_PORT),
        broker_username=config.ACTIVEMQ_USERNAME,
        broker_password=config.ACTIVEMQ_PASSWORD,
        listener=MockedS3ConnectorStoreImageListener()
    )

@pytest.fixture()
def store_image_reply_conn() -> stomp.connect.StompConnection11:
    return ActiveMqConnectionFactory.create_connection(
        broker_host=config.ACTIVEMQ_HOST,
        broker_port=int(config.ACTIVEMQ_PORT),
        broker_username=config.ACTIVEMQ_USERNAME,
        broker_password=config.ACTIVEMQ_PASSWORD,
        listener=StoreImageReplyListener()
    )

@pytest.fixture()
def get_image_conn() -> stomp.connect.StompConnection11:
    class MockedS3ConnectorGetImageListener(stomp.ConnectionListener):
        def __init__(self) -> None:
            super().__init__()
        def on_message(self, message):
            logging.info(f'new store image message: {message}')
    
    return ActiveMqConnectionFactory.create_connection(
        broker_host=config.ACTIVEMQ_HOST,
        broker_port=int(config.ACTIVEMQ_PORT),
        broker_username=config.ACTIVEMQ_USERNAME,
        broker_password=config.ACTIVEMQ_PASSWORD,
        listener=MockedS3ConnectorGetImageListener()
    )

@pytest.fixture()
def get_image_reply_conn() -> stomp.connect.StompConnection11:
    return ActiveMqConnectionFactory.create_connection(
        broker_host=config.ACTIVEMQ_HOST,
        broker_port=int(config.ACTIVEMQ_PORT),
        broker_username=config.ACTIVEMQ_USERNAME,
        broker_password=config.ACTIVEMQ_PASSWORD,
        listener=GetImageReplyListener()
    )

@pytest.fixture()
def mock_store_image_msg(message_factory: MessageFactory) -> StoreImageMsg:
    return message_factory.create_store_image_message(
        filename='mocked_filename.png',
        image_data=...,
        correlation_id='mocked_correlation_id'
    )

@pytest.fixture()
def mock_get_image_msg(message_factory: MessageFactory) -> GetImageMsg:
    return message_factory.create_get_image_message()

def test_store_image(
    activemq_dispatcher: ActivemqDispatcher, 
    activemq_worker_manager: ActivemqWorkerManager,
    mocked_convert_image_msg: ConvertImageMsg,
    mocked_convert_image_reply_msg: ConvertImageReplyMsg,
    activemq_cache_manager: ActivemqCacheManager
    ):
    assert type(activemq_dispatcher) == ActivemqDispatcher
    assert type(activemq_worker_manager) == ActivemqWorkerManager
    assert type(mocked_convert_image_msg) == ConvertImageMsg
    assert type(mocked_convert_image_reply_msg) == ConvertImageReplyMsg
    assert type(activemq_cache_manager) == ActivemqCacheManager
    
    activemq_worker_manager.submit_threadpool()

    activemq_dispatcher.send_convert_image_message(
        msg=mocked_convert_image_msg
        )
    
    assert activemq_cache_manager.await_reply_message(
        correlation_id=mocked_convert_image_msg.correlation_id
        ) == mocked_convert_image_reply_msg
    
    activemq_worker_manager.stop_threadpool()