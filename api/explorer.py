import datetime
import json
import urllib2
from services.cache import cache
import config
import logging
from logging.handlers import TimedRotatingFileHandler
from pymongo import MongoClient
import json,zmq
from bson import json_util
from bson.objectid import ObjectId
import q,traceback

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='mydebug.log',
                filemode='w')
logHandler = TimedRotatingFileHandler(filename = 'mydebug.log',
                when = 'D', interval = 1, encoding='utf-8'
)
logger = logging.getLogger('pubAdmin')
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

context = zmq.Context()
socket = context.socket(zmq.PUB)
# port = socket.bind_to_random_port("tcp://127.0.0.1")
socket.bind("tcp://127.0.0.1:"+ str(config.Port))
logger.info('binding to port '+ str(config.Port))

regtable = {}
# post
def unregister_topic(topic):
    key = ':'.join((topic['service'],topic['name'],topic['ttype'],topic['ext']))
    try:
        regtable.pop(key)
        return True
    except:
        logger.error('fail to unregister '+ key)
        return False
# post
def register_topic(topic, slot):
    key = ':'.join((topic['service'],topic['name'],topic['ttype'],topic['ext']))
    if key in regtable:
        logger.error('already exist '+ key)
        return False
    regtable[key] = {'slot':slot, 'time':datetime.datetime.now()}
    return True

# post
def modify_topic(topic, new_slot):
    key = ':'.join((topic['service'],topic['name'],topic['ttype'],topic['ext']))
    if key not in regtable:
        logger.error('cant find '+ key)
        return False
    regtable[key] = {'slot':new_slot, 'time':datetime.datetime.now()}
    return True
# get
def getRegTable(topic):
    key = ':'.join((topic['service'],topic['name'],topic['ttype'],topic['ext']))
    if key not in regtable:
        logger.error('cant find '+ key)
        return False
    return regtable[key]
# post
def pub(topic, content):
    key = ':'.join((topic['service'],topic['name'],topic['ttype'],topic['ext']))
    if key not in regtable:
        logger.error('cant find '+ key)
        return False
    _now = datetime.datetime.now()
    if _now < datetime.timedelta(seconds = regtable[key]['slot'] ) + regtable[key]['time']:
        logger.warn('wait, slot is ' +  str(regtable[key]['slot']))
        return False
    try:
        socket.send_string("%s %s"%(key, content))
        regtable[key]['time'] = _now
        logger.info('to topic : ' +key)
        return True
    except:
        logger.error('failed to pub content '+ content + ' with key '+ key)
        return False





