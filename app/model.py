#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  model.py
#  
#  Copyright 2019 andrey <andrey@andrey-UX330UAR>
#  
#  
#  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Enum


__author__ = "Andrey Kashrin <kas@sysqual.net>"
__copyright__ = "Copyright (C) 2019 by Andrey Kashrin"
__license__ = "proprietary"

DBase = declarative_base()
schema = "ormuco"

pets = ("cat", "dog")

class Ormuco(DBase):
    __tablename__ = 'ormuco'
    __table_args__ = {'schema': schema}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    color = Column(String(50), nullable=False)
    pet = Column(Enum(*pets), default='dog')
    
    def __init__(self, name, color, cat):
        self.name = name
        self.color = color
        self.is_cat_lover = cat
    
    def __repr__(self):
        return "<(Ormuco'{}')>".format(self.name)
    
