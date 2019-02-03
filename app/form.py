#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  model.py
#  
#  Copyright 2019 andrey <andrey@andrey-UX330UAR>
#  
#  

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, RadioField

__author__ = "Andrey Kashrin <kas@sysqual.net>"
__copyright__ = "Copyright (C) 2019 by Andrey Kashrin"
__license__ = "proprietary"


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired("Please enter your name")])
    color = StringField('Color', validators=[DataRequired("Plese enter your color")])
    pet = RadioField('Pets?', default='dog', choices = [('cat', 'Cat'), ('dog', 'Dog')])
    submit = SubmitField('Submit')
