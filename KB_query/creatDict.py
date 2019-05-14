# encoding=utf-8
import pymysql

posAptitudeName = 'pan'
posAptitudeCategory = 'pac'
posAptitudeFrom = 'paf'
posCompanyName='pcn'
posCompanyCategory='pcc'
posPeopleName='ppn'
posPeopleCategory='ppc'
posPeopleMajor='ppm'
posProjectCatgory='pqc'
posProjectWhom='pqw'
posProjectName='pqn'

def deletePunctuate(strT):
    ls=0
    for loc,p in enumerate(strT):
        try:
            p=str(p.encode('raw_unicode_escape'))
        except:
            continue
        if p<"b\'\\\\u4e00\'"or p>"b\'\\\\u9fa5\'":
            strT=strT[0:loc-ls]+strT[loc-ls+1:]
            ls=ls+1
    return strT

def creatDict(target, database, cate):
    db = pymysql.connect("localhost", "root", "root", "kg4company_2", charset="utf8")
    cur = db.cursor()
    sqlR=u"select {target} from {database} group by {target}"
    sql=sqlR.format(target=target,database=database)
    cur.execute(sql)
    relts = cur.fetchall()
    listDict=[]
    for relt in relts:
        if relt[0]==' ':
            continue
        listDict.append(deletePunctuate(relt[0])+' '+cate+'\n')
    return listDict

if __name__=='__main__':
    listD=[]
    listT=[
        ['name_','aptitude',posAptitudeName], ['category','aptitude',posAptitudeCategory], ['fromWhere', 'aptitude', posAptitudeFrom],
        ['name_', 'company',posCompanyName], ['category','company',posCompanyCategory],
        ['name_','people',posPeopleName],['category','people',posPeopleCategory],['major','people',posPeopleMajor],
        ['category','project',posProjectCatgory],['whom_','project',posProjectWhom],['name_','project',posProjectName]
    ]
    f1 = open('./externalDict/Dict.txt', 'w', encoding='UTF-8')
    for ioi in range(0,len(listT)):
        listD=creatDict(listT[ioi][0], listT[ioi][1], listT[ioi][2])
        for ld in listD:
            f1.write(ld)
            print(ld)
