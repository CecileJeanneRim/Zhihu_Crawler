# -*- coding:utf-8 -*-
import MySQLdb


class Database:
    def __init__(self, error_logger, message_logger, utils):
        self.message_logger = message_logger
        self.utils = utils
        self.error_logger = error_logger
        try:
            self.db = MySQLdb.connect('localhost', 'zhihu', 'crawler', 'zhihu')
            self.cur = self.db.cursor()
            self.db.set_character_set('utf8')
        except MySQLdb.Error, e:
            self.utils.mysqldb_error_handle(exception=e)
        self.message_logger.event(u"Database Built")

    def insert_data(self, data_dict, table):
        try:
            sql = self.insert_sql_construct(data_dict, table)
            self.execute_insert(sql)
        except MySQLdb.Error, e:
            self.utils.mysqldb_error_handle(e)

    def insert_sql_construct(self, data_dict, table):
        cols = ', '.join(data_dict.keys())
        values = '"," '.join(data_dict.values())
        return "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"' + values + '"')

    def execute_insert(self, sql):
        try:
            result = self.cur.execute(sql)
            insert_id = self.db.insert_id()
            self.db.commit()
            if result:
                return insert_id
            else:
                return -1
        except MySQLdb.Error, e:
            self.db.rollback()
            self.utils.mysqldb_error_handle(e)

    def users(self, contents):
        for content in contents:
            # print "Love"
            # print content[1]
            sql = 'INSERT INTO users (%s) VALUES (%s)' % ("user_url", '"' + content[1] + '"')
            self.execute_insert(sql)
