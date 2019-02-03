#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2019 andrey <andrey@andrey-UX330UAR>
#  

import sys
import argparse

from flask_wtf import FlaskForm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, request, render_template, flash, redirect



from model import DBase, Ormuco
from form import RegistrationForm

__author__ = "Andrey Kashrin <kas@sysqual.net>"
__copyright__ = "Copyright (C) 2019 by Andrey Kashrin"
__license__ = "proprietary"


dbhost = "dbhost"
db_user = "ormuco"
db_name = "ormuco"
db_passwd = "ormuco"
application = None


class EndpointAction(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        return self.action()

class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)
        self.app.config['SECRET_KEY'] = 'some-key'

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), **kwargs)

class App(object):

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            description=__doc__,
            epilog="Report bugs to %s" % __author__
        )
        self.parser.add_argument(
            "--dbhost", metavar="DBCONFIG", type=str, default=dbhost,
            help="IP address MySQL server for db(default: dbhost)"
        )
        self.parser.add_argument(
            "-u", "--user", metavar="USER", type=str, default=db_user,
            help="MySQL user (default: ormuco)"
        )
        self.parser.add_argument(
            "-p", "--passwd", metavar="PASSWORD", default=db_passwd,
            help="MySQL password"
        )


    def register(self):
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            user = Ormuco(form.name.data, form.color.data,
                        form.pet.data)
            try:
                self.dbsession.add(user)
                self.dbsession.commit()
                flash('Thanks for registering')
                return redirect('/')
            except:
                self.dbsession.rollback()
                flash('Duplicate name. Choose another')
        return render_template('base.html', form=form)


    def main(self, cli_args):
        self.args = self.parser.parse_args(cli_args)
        self.engine = create_engine("mysql://{}:{}@{}/ormuco".format(
                                         self.args.user,
                                         self.args.passwd,
                                         self.args.dbhost
                                     ),
                                    encoding='utf8',
                                    echo=True
                                        )
        smaker = scoped_session(sessionmaker(bind=self.engine))
        self.dbsession = smaker()
        DBase.metadata.create_all(bind=self.engine)
        self.app = FlaskAppWrapper(__name__)
        self.app.add_endpoint(endpoint='/',
                                    endpoint_name='root',
                                    handler=self.register,
                                    methods=['POST', 'GET']
                                    )
        global application
        application = self.app.app

    def run(self):
        self.app.run(host='0.0.0.0', port=5000, debug=True)
        

if __name__ == '__main__':
    app = App()
    app.main(sys.argv[1:])
    app.run()
