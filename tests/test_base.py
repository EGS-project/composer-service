import io
from fastapi import UploadFile
import pytest
import stomp
from src.conversion.schemas import ConversionCreate
from src.conversion.message import ConvertImageMsg, ConvertImageReplyMsg
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, MessageFactory
from src.conversion.listener import ConvertImageReplyListener
import src.config as config
import logging


@pytest.fixture()
def send_conn() -> stomp.connect.StompConnection11:
    return ActiveMqConnectionFactory.create_connection()

@pytest.fixture()
def activemq_dispatcher(send_conn: stomp.connect.StompConnection11):
    return ActivemqDispatcher(conn=send_conn)

@pytest.fixture()
def message_factory() -> MessageFactory:
    return MessageFactory()

@pytest.fixture()
def mocked_upload_file() -> UploadFile:
    with open('sample_images/raccoon.jpg', 'rb') as f:
        return UploadFile(
            filename='raccoon.jpg',
            file=io.BytesIO(f.read()),
            headers={"content-type": "image/jpeg"}
            )
