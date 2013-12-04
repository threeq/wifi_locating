
# -*- coding: utf-8 -*-

import ConfigParser;

########################################################################
# 系统配置文件
class Config:
    """"""
    _instance = None;
    _config = ConfigParser.ConfigParser();
    _config.readfp(open("config.ini","rb"));
    
    @classmethod
    def get(cls, group, item):
        return cls._config.get(group, item);
    
    def __new__(cls,*args,**kwargs):
        if not cls._instance:
            cls._instance=super(Singleton,cls).__new__(cls,*args, **kwargs)
        return cls._instance;
    
########################################################################
# 扩展配置文件
class ExtendConfig:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, path):
        """Constructor"""
        self._config = ConfigParser.ConfigParser();
        self._config.readfp(open(path,"rb"));
        
    def get(self, group, item):
        return self._config.get(group, item);