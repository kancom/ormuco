#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2019 andrey <andrey@andrey-UX330UAR>
#  

import sys
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


from model import DBase

__author__ = "Andrey Kashrin <kas@sysqual.net>"
__copyright__ = "Copyright (C) 2019 by Andrey Kashrin"
__license__ = "proprietary"


dbhost = "localhost"
db_user = "ormuco"
db_name = "ormuco"
db_passwd = "ormuco"

class App(object):

    def __init__(self):
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
        
        self.app = Flask(__name__)
        app.config.from_object(__name__+'.ConfigClass')
        db = SQLAlchemy(app)

if __name__ == '__main__':
    app = App()
    app.main(sys.argv[1:])
    app.run(host='0.0.0.0', port=5000, debug=True)
