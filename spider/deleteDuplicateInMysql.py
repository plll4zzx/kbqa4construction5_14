import pymysql

def doSql(sql):
    db = pymysql.connect("localhost","root","root","kg4company_2", charset="utf8")
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    #db.close()

def ddim(table,coloums):
    sqls={
        'sqlRename':u"ALTER TABLE tmp RENAME TO {tableName};",
        'sqlDrop':u'DROP TABLE {tableName};',
        'sqlCreateNew':u'CREATE TABLE tmp SELECT * FROM {tableName}  GROUP BY {coloums};'
    }
    sqls['sqlCreateNew']=sqls['sqlCreateNew'].format(tableName=table,coloums=coloums)
    sqls['sqlDrop']=sqls['sqlDrop'].format(tableName=table)
    sqls['sqlRename']=sqls['sqlDrop'].format(tableName=table)

    doSql(sqls['sqlCreateNew'])
    doSql(sqls['sqlDrop'])
    doSql(sqls['sqlRename'])

if __name__=='__main__':
    #ddim('compinfo','name_')
    #ddim('peopleinfo','No_,compName')
    #ddim('projectinfo','No_, compName')
    ddim('compaptitude','No_, compName')
