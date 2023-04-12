import time
import pytest
import stomp
import stomp.utils
from src.activemq.utils import SubIdGenerator
from src.activemq.worker import ActiveMqWorker
from src.activemq.manager import ActivemqWorkerManager
from src.s3_connector.message import DeleteImageMsg, GetImageMsg, GetImageReplyMsg, StoreImageMsg, StoreImageReplyMsg
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, ActivemqWorkerFactory, MessageFactory
from src.s3_connector.listener import GetImageReplyListener, StoreImageReplyListener
import src.config as config
import logging
from tests.test_base import *
