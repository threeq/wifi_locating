
# -*- coding: utf-8 -*-


#枚举定义
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

#枚举定义
def enum2(**enums):
    return type('Enum', (), enums)