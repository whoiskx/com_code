# -*- coding:utf-8 -*-
import time

import datetime

from aliyun.log.logclient import LogClient
from aliyun.log.logitem import LogItem
from aliyun.log.putlogsrequest import PutLogsRequest

from comm.basic_tools import pyobj2json, base64_to_string, string_to_base64, json2pyobj, get_md5, is_aliyun

loghub_endpoint = "cn-shenzhen.log.aliyuncs.com"
loghub_endpoint_aliyun = "cn-shenzhen-intranet.log.aliyuncs.com"
loghub_accessKeyId = 'LTAISVhnEaVSx7Lj'
loghub_accessKey = 'MPP1DhADcUyeXOVDDKmMk2gCgfWg47'
loghub_project = 'mokiwi'
loghub_logstore = 'pykafka'


def get_loghub_client():
    if is_aliyun():
        endpoint = loghub_endpoint_aliyun
    else:
        endpoint = loghub_endpoint
    access_key_id = loghub_accessKeyId
    access_key = loghub_accessKey
    return LogClient(endpoint, access_key_id, access_key)


def get_mongo_client():
    from pymongo import MongoClient
    return MongoClient("mongodb://10.169.222.251:27017", maxPoolSize=100, socketKeepAlive=True)


class Producer(object):
    def __init__(self, project=None, logstore=None, source=None):
        self.client = get_loghub_client()
        self.project = project or loghub_project
        self.logstore = logstore or loghub_logstore
        self._key = "log"
        self.source = source

    def _put_logs(self, topic, source, logitem_list):
        req = PutLogsRequest(self.project, self.logstore, topic, source, logitem_list)
        return self.client.put_logs(req)

    def send(self, topic, value, key=None, source=None):
        log_item = LogItem()
        log_item.set_time(int(time.time()))
        log_item.set_contents([(self._key, Producer._value_to_string(key, value))])
        if source is None:
            log_info = (topic, self.source, [log_item])
        else:
            log_info = (topic, source, [log_item])

        self._put_logs(*log_info)

    @staticmethod
    def _value_to_string(key, value):
        dict_value = {'v': value}
        if key:
            dict_value['k'] = key
        return pyobj2json(dict_value)


class BufferedProdecer(Producer):
    def __init__(self, project=None, logstore=None):
        super(BufferedProdecer, self).__init__(project=project, logstore=logstore)
        self._log_item_list = []

    def send(self, topic, value, key=None, source=None):
        # todo not finish
        log_item = LogItem()
        log_item.set_time(int(time.time()))
        log_item.set_contents([(self._key, Producer._value_to_string(key, value))])
        if source is None:
            log_info = (topic, self.source, [log_item])
        else:
            log_info = (topic, source, [log_item])

        self._put_logs(*log_info)


class CheckpointManager(object):
    def __init__(self, mongo=None, project=None, logstore=None, client_name=None):
        self.mongo = mongo or get_mongo_client()
        self.cp_collection = self.mongo["LOG"]["checkpoint"]
        self.project = project or loghub_project
        self.logstore = logstore or loghub_logstore
        self.client_name = client_name or "log"
        self._key = self.project + "-" + self.logstore + "-" + self.client_name
        self.cache = {}

    def save(self, shard_id, checkpoint):
        """
        :param shard_id: 分片id
        :param checkpoint: 未消费的最早的cp
        :return:
        """
        self.cp_collection.update({"_id": self._key + "-" + str(shard_id)}, {'$set': {"cp": checkpoint}}, upsert=True)

    def __setitem__(self, shard_id, checkpoint):
        old_cp = None
        if shard_id in self.cache:
            old_cp = self.cache.pop(shard_id)

        if old_cp != checkpoint:
            self.save(shard_id, checkpoint)
        self.cache[shard_id] = checkpoint

    def __getitem__(self, key):
        return self.cache[key]

    def keys(self):
        return self.cache.keys()

    def get(self, shard_id):
        if shard_id not in self.cache:
            info = self.cp_collection.find_one({"_id": self._key + "-" + str(shard_id)})
            if info:
                self.cache[shard_id] = info.get("cp")
        return self.cache.get(shard_id)


class Consumer(object):
    def __init__(self, project=None, logstore=None, mongo=None):
        self.loghub_client = get_loghub_client()
        self.mongo = mongo or get_mongo_client()
        self.project = project or loghub_project
        self.logstore = logstore or loghub_logstore
        self._key = "log"
        self.topic = "error"
        self.log_mongo = self.mongo["LOG"]["error_log"]
        self.log_record = []
        self._cursors = CheckpointManager(mongo=self.mongo, project=self.project, logstore=self.logstore)
        self.init_order()

    def run(self):
        while True:
            try:
                time.sleep(5)
                self.consume()
            except KeyboardInterrupt:
                self.save_in_mongo()
            except Exception as e:
                print e

    def save_in_mongo(self):
        if self.log_record:
            try:
                self.log_mongo.insert(self.log_record)
            except Exception as e:
                print e
                for log in self.log_record:
                    try:
                        self.log_mongo.insert(log)
                    except Exception as ex:
                        print ex
            self.log_record = []

    def consume(self):
        for shard_id in self._cursors.keys():
            start_cursor = string_to_base64(self._cursors[shard_id])

            end_time = int(time.time())
            res = self.loghub_client.get_cursor(self.project, self.logstore, shard_id, end_time)
            end_cursor = res.get_cursor()

            while start_cursor != end_cursor:
                loggroup_count = 100
                res = self.loghub_client.pull_logs(self.project, self.logstore, shard_id, start_cursor,
                                                   loggroup_count, end_cursor)

                self.log_record.extend(self.get_record_list(shard_id, start_cursor, res.get_loggroup_json_list()))

                self.save_in_mongo()
                next_cursor = res.get_next_cursor()
                self._cursors[shard_id] = base64_to_string(next_cursor)

                if next_cursor == start_cursor:
                    break
                start_cursor = next_cursor

    def get_record_list(self, shard_id, start_cursor, json_list):
        result = []
        num_cursor = int(base64_to_string(start_cursor))
        for i, log in enumerate(json_list):
            result.extend(self.loghub_log_to_dict(shard_id, num_cursor + i, log))
        return result

    def loghub_log_to_dict(self, shard_id, num_cursor, log):
        topic = log.get('topic')
        if topic == "error":
            result = []
            source = log.get("source")
            temp = log.get("logs")
            log_content = temp[0]
            dict_temp = json2pyobj(log_content["log"])
            dict_log = dict_temp.get('v')
            dict_log["key"] = dict_temp.get('k')
            dict_log["topic"] = topic
            dict_log["source"] = source
            dict_log["_id"] = str(shard_id) + "-" + str(num_cursor)
            dict_log["cursor_id"] = num_cursor
            try:
                dict_log["asctime"] = datetime.datetime.strptime(dict_log["asctime"], '%Y-%m-%d %H:%M:%S,%f')
            except Exception:
                pass

            try:
                exception = dict_log["exception"]["stackTrace"]
                dict_log["md5"] = get_md5(exception)
            except Exception:
                pass
            result.append(dict(dict_log))
            return result
        else:
            return []

    def init_order(self):
        listShardRes = self.loghub_client.list_shards(self.project, self.logstore)

        for shard in listShardRes.get_shards_info():
            shard_id = shard["shardID"]
            start_cursor = self._cursors.get(shard_id)
            if start_cursor is None:
                res = self.loghub_client.get_cursor(self.project, self.logstore, shard_id, 0)
                start_cursor = base64_to_string(res.get_cursor())
                self._cursors[shard_id] = start_cursor
            else:
                self._cursors[shard_id] = start_cursor

            cursor = self._cursors[shard_id]
            if self._exists(shard_id, cursor):
                int_cursor = int(cursor)
                count = 100
                temp_cursor = None
                while count > 0:
                    count += 1
                    int_cursor += 1
                    str_cursor = str(int_cursor)
                    if not self._exists(shard_id, str_cursor):
                        temp_cursor = str_cursor
                        break

                if temp_cursor is None:
                    raise Exception("unexpected cursor!")

                self._cursors[shard_id] = temp_cursor
            else:
                int_cursor = int(cursor)
                count = 100
                temp_cursor = cursor
                while count > 0:
                    count -= 1
                    int_cursor -= 1
                    str_cursor = str(int_cursor)
                    if self._exists(shard_id, str_cursor):
                        break
                    temp_cursor = str_cursor

                if self._exists(shard_id, temp_cursor):
                    raise Exception("unexpected cursor!")

                self._cursors[shard_id] = temp_cursor

    def _exists(self, shard_id, str_cursor):
        info = self.log_mongo.find_one({"_id": str(shard_id) + "-" + str_cursor})
        if info:
            return True
        return False

    def update_history_record(self):
        for record in self.log_mongo.find({"cursor_id": {"$exists": False}}):
            _id = record["_id"]
            _dict = {"cursor_id": int(_id.split("-")[1])}
            try:
                _dict["asctime"] = datetime.datetime.strptime(record["asctime"], '%Y-%m-%d %H:%M:%S,%f')
            except Exception:
                pass
            self.log_mongo.update_one({"_id": _id}, {"$set": _dict})
