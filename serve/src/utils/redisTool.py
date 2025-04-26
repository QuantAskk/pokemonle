# -*-coding: utf-8 -*-
# @Time    : 2025/4/21 15:42
# @Author  : TyranitarX
import redis


class RedisTool(object):
    def __init__(self, host, port):
        self.conn = redis.Redis(host=host, port=port, db=0)

    def set(self, key, value):
        self.conn.set(key, value)

    def get(self, key):
        return self.conn.get(key)

    def clean(self, key):
        self.conn.delete(key)

    def hset(self, h, key, value):
        self.conn.hset(h, key, value)

    def hget(self, h, key):
        return self.conn.hget(h, key)
