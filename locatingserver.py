
# -*- coding: utf-8 -*-
#####################################
##  读入传入数据，并且格式化
##
##
#####################################

import os;
import sys;
import string;
from numpy import *;
import operator;
import time;

def load_data(path='data/'):
    data_file_lst =  os.listdir(path);
    
    attrlist = [];
    attrType = {};
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
        
    posdata = [];
    d = {};
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

    return dataset, labels, attrlist;


# knn K紧邻分类
def classify_pos(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0];
    diffMat = tile(inX, (dataSetSize,1)) - dataSet;
    sqDiffMat = diffMat**2;
    sqDistances = sqDiffMat.sum(axis=1);
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort();
    classCount = {};
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]][0]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1;
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True);
    # print sortedClassCount;
    return sortedClassCount[0][0]
    
print "加载分类数据========================"
dataset, labels, attrList = load_data();
print len(attrList);
dataset = array(dataset);
print dataset.shape;

#----------------------------------------------------------------------
def do_locating(dataset_fl, attrList_fl):
    """"""
    # 整理验证数据
    dataset_yz_f = [];
    for dt in dataset_fl:
	dt_f = [];
	for attr in attrList:
	    index = -1;
	    for i in range(len(attrList_fl)):
		if attr==attrList_fl[i]:
		    index = i;
	    if index!=-1: dt_f.append(dt[i])
	    else: dt_f.append(0);
	dataset_yz_f.append(dt_f);
	
    # 开始验证
    k = 50;
    countLab = {};
    for i in range(len(dataset_yz_f)):
	data = dataset_yz_f[i];
	s = time.clock();
	c =  classify_pos(data, dataset, labels, k);
	e = time.clock();
	print '第',i+1 ,'次使用时间：', e-s, "ms"
	countLab.setdefault(c, 0);
	countLab[c] += 1;
	    
    sortedLab = sorted(countLab.iteritems(), key=operator.itemgetter(1), reverse=True)
    print sortedLab[0];
    print "分类结果：%s" %(sortedLab[0][0]);
    
    return sortedLab[0][0];
    


# 开启web服务器
import web

render = web.template.render('templates/loacting/');

urls = (
  "", "test",
  "/server.html", "locating",
  "/collect.do", "collector",
  "/", "test"
)

class relocating:
    def GET(self): raise web.seeother('/')

# 数据采集器
class collector:
    #----------------------------------------------------------------------
    def GET(self):
	""""""
	reqArgs = web.input(location=None);
	

# 定位服务
class locating:
    
    def GET(self):
	reqArgs = web.input(location=None);
	loc = reqArgs.location;
        
	if None==loc or loc=='':
	    return "数据输入有误"
	
	attrlist = [];
	attrType = {};	
	for line in loc.split('@'):
	    if line==None or line=='' or line=='\n': continue;    
	    posattr = {};
	    apList = line.split('$');
	    for ap in apList:
		if ap!=None and ap!='' and ap!='\n':
		    ap_attr_list = ap.split('|');
		    posattr[ap_attr_list[1]] = -1*string.atoi(ap_attr_list[3]);
		    attrType[ap_attr_list[1]] = True;
	    attrlist.append(posattr);	
	
	posdata = [];
	d = {};
	for attr in attrlist:
	    onedata = [];
	    for ap in attrType:
		try:
		    onedata.append(attr[ap]);
		except:
		    onedata.append(0);
	    # 过滤掉重复数据
	    k = ','.join([str(i) for i in onedata]);
	    d.setdefault(k, 0)
	    d[k]+=1
	    if d[k]==1:
		posdata.append(onedata);   
		
	attrlist = attrType.keys();
    
	position =  do_locating(posdata, attrlist);	
	print position;
	return position;
    

class test:
    def GET(self):
	return render.test();
app_locating = web.application(urls, locals())