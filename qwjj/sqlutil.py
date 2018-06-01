import pymysql
from qwjj import settings
class SqlUtil:

    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect(host=settings.MYSQL_HOSTS, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWORD,
                                  db=settings.MYSQL_DB, use_unicode=True, charset="utf8")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    # 插入表数据
    def insert_data(self, table, item):
        sql = "INSERT INTO " + table + " ({fields}) VALUES ({values})"
        fields = ''
        values = ''
        value = []
        for field in item.fields:
            if field in item and item[field]:
                fields += '`' + field +'`, '
                values += '%s, '
                value.append(item[field])
        fields = fields[0:-2]
        values = values[0:-2]
        fdict = {'fields': fields, 'values': values}
        sql = sql.format(**fdict)
        self.cursor.execute(sql, value)
        self.db.commit()

    # 修改表数据
    def update_data(self, table, item):
        sql = "INSERT INTO " + table + " ({fields}) VALUES ({values})"
        fields = ''
        values = ''
        value = []
        for field in item.fields:
            if field in item and item[field]:
                fields += '`' + field + '`, '
                values += '%s, '
                value.append(item[field])
        fields = fields[0:-2]
        values = values[0:-2]
        fdict = {'fields': fields, 'values': values}
        sql = sql.format(**fdict)
        self.cursor.execute(sql, value)
        self.db.commit()
