
# -*- coding: utf-8 -*-

import os;
import sys;
import string;
from db import DBConnector;


def load_data(path='data/'):
    data_file_lst =  os.listdir(path);
    
    attrlist = []; # 采集数据点
    attrType = {}; # 每个数据点包含的类型
    for data_file in data_file_lst:
        position = data_file.split('.')[0];
        print position;
        for line in open(path+data_file):
            
            if line==None or line=='' or line=='\n': continue;    
            posattr = {};
            apList = line.split('$');
            for ap in apList:
                if ap!=None and ap!='' and ap!='\n':
                    ap_attr_list = ap.split('|');
                    posattr[ap_attr_list[1]] = -1*string.atoi(ap_attr_list[3]);
                    posattr['position']=position;
                    attrType[ap_attr_list[1]] = True;
                    
            attrlist.append(posattr);

    posdata = []; # 去掉重复数据点
    d = {}; # 记录数据点重复次数
    count = len(attrlist); # 数据总数
    print count;
    for attr in attrlist:
        onedata = [];
        for ap in attrType:
            try:
                onedata.append(attr[ap]);
            except:
                onedata.append(0);
        onedata.append(attr['position']);
        # 过滤掉重复数据
        k = ','.join([str(i) for i in onedata]);
        d.setdefault(k, 0)
        d[k]+=1
        if d[k]==1:
            posdata.append(onedata);   

    attrlist = attrType.keys();
    dataset = [ p[0:-1] for p in posdata];
    labels = [p[-1:] for p in posdata];

    dl=[]; # 封装到数据库
    for dp in posdata :
        objd = {};
        for i in range(len(attrlist)):
            objd[attrlist[i]] = dp[i]
        objd['position'] = dp[-1:][0];
        k = ','.join([str(i) for i in dp]);
        objd['repeat'] = d[k];
        objd['rate'] = d[k]*1.0/count;
        dl.append(objd);
        
    db = DBConnector();
    db.save('locating', dl);

    return dataset, labels, attrlist;

load_data();