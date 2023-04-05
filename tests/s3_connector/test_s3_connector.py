import pytest
import stomp
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
        def on_message(self, message):
            logging.info(f'new store image message: {message}')
    
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

def test_get_image(
    activemq_dispatcher: ActivemqDispatcher, 
    get_image_reply_conn: stomp.connect.StompConnection11,
    mock_store_image_msg: StoreImageMsg
    ):
    assert type(activemq_dispatcher) == ActivemqDispatcher
    assert type(get_image_reply_conn) == stomp.connect.StompConnection11
    assert type(mock_store_image_msg) == StoreImageMsg
    # activemq_dispatcher.send_store_image_message(msg=mock_store_image_msg)
    