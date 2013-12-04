
# -*- coding: utf-8 -*-

import pymongo;
import string;
from config import Config;
import sys;

########################################################################
# 数据库操作封装
class DBConnector:
    """"""

    # 单例实现
    _instance = None;
    def __new__(cls,*args,**kwargs):
        if not cls._instance:
            cls._instance=super(Singleton,cls).__new__(cls,*args, **kwargs)
        return cls._instance;    
    
    # 构造方法
    def __init__(self):  

        host = Config.get('db','db.host');
        port = string.atoi(Config.get('db','db.port'));
        db = Config.get('db','db.database');
        
        self.connection=pymongo.Connection(host, port);
        self.db = self.connection[db];
    
    #########################################
    # 保存数据
    def save(self, tab, dataList):
        self.db[tab].insert(dataList);
    
    #########################################
    #查询数据
    def find(self, tab, query, sort=None):
        return self.db[tab].find(query_if, sort=sort);
    
    def find_one(self, tab, query_if):
        return self.db[tab].find_one(query_if);
    
    #########################################
    # 更新数据
    def update(self, tab, up_if, up_data):
        return self.db[tab].update(up_if, up_data);
    
    #########################################
    # 删除数据
    def delete(self, tab, del_if):
        self.db[tab].remove(del_if);
    
    #########################################
    # 删除集合
    def drop(self, tab):
        self.db[tab].drop();
    
    #########################################
    # 统计总数
    def count(self, tab, count_if=None):
        if None==count_if:
            return self.db[tab].count();
        else:
            return self.db[tab].find(count_if).count()