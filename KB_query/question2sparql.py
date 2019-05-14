# encoding=utf-8

"""
@desc: 将自然语言转为SPARQL查询语句
"""

from KB_query import word_tagging
from KB_query import creatDict as cd

# rela = '<file:///D:/graduation_design/Demo/kg4construction5_9/vocab/{tableName}_{columnName}>'
rela = ':{tableName}_{columnName}'
SPARQL_PREXIX = u"""
PREFIX :<file:///D:/graduation_design/Demo/kg4construction5_9/vocab/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""
SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

subSparqlEntity={
    'pan':"?aptitude "+rela.format(tableName='aptitude',columnName='name_')+" '{target}'.\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='name_')+" ?aptitude_name.\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='id')+" ?aptitude_id.\n",

    'pac':"?aptitude "+rela.format(tableName='aptitude',columnName='category')+" '{target}'.\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='category')+" ?aptitude_category .\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='name_')+" ?aptitude_name.\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='id')+" ?aptitude_id.\n",

    'paf':"?aptitude "+rela.format(tableName='aptitude',columnName='fromWhere')+" '{target}'.\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='fromWhere')+" ?aptitude_fromWhere .\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='name_')+" ?aptitude_name.\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='id')+" ?aptitude_id.\n",

    'pcn':"?company "+rela.format(tableName='company',columnName='name_')+" '{target}'.\n"\
            "?company "+rela.format(tableName='company',columnName='name_')+" ?company_name.\n",

    'pcc':"?company "+rela.format(tableName='company',columnName='category')+" '{target}'.\n"\
            "?company "+rela.format(tableName='company',columnName='category')+" ?company_category.\n"\
            "?company "+rela.format(tableName='company',columnName='name_')+" ?company_name.\n",

    'ppn':"?people "+rela.format(tableName='people',columnName='name_')+" '{target}'.\n"\
            "?people "+rela.format(tableName='people',columnName='name_')+"? people_name.\n"\
            "?people "+rela.format(tableName='people',columnName='id_p')+"? people_idp.\n",

    'ppc':"?people "+rela.format(tableName='people',columnName='category')+" '{target}'.\n"\
            "?people "+rela.format(tableName='people',columnName='category')+" ?people_category.\n"\
            "?people "+rela.format(tableName='people',columnName='name_')+" ?people_name.\n"\
            "?people "+rela.format(tableName='people',columnName='id_p')+" ?people_idp.\n",

    'ppm':"?people "+rela.format(tableName='people',columnName='major')+" '{target}'.\n"\
            "?people "+rela.format(tableName='people',columnName='major')+" ?people_major.\n"\
            "?people "+rela.format(tableName='people',columnName='name_')+" ?people_name.\n"\
            "?people "+rela.format(tableName='people',columnName='id_p')+" ?people_idp.\n",

    'pqc':"?project "+rela.format(tableName='project',columnName='category')+" '{target}'.\n"\
            "?project "+rela.format(tableName='project',columnName='category')+" ?project_category.\n"\
            "?project "+rela.format(tableName='project',columnName='name_')+" ?project_name.\n"\
            "?project "+rela.format(tableName='project',columnName='id')+" ?project_id.\n",

    'pqw':"?project "+rela.format(tableName='project',columnName='whom_')+" '{target}'.\n"\
            "?project "+rela.format(tableName='project',columnName='whom_')+" ?project_whom.\n"\
            "?project "+rela.format(tableName='project',columnName='name_')+" ?project_name.\n"\
            "?project "+rela.format(tableName='project',columnName='id')+" ?project_id.\n",

    'pqn':"?project "+rela.format(tableName='project',columnName='name_')+" '{target}'.\n"\
            "?project "+rela.format(tableName='project',columnName='name_')+" ?project_name.\n"\
            "?project "+rela.format(tableName='project',columnName='id')+" ?project_id.\n",
}

subSparqlKeyword={
    'kp':"?people "+rela.format(tableName='people',columnName='id_p')+" ?people_idp.\n"\
            "?people "+rela.format(tableName='people',columnName='name_')+" ?people_name.\n",

    'kc':"?company "+rela.format(tableName='company',columnName='name_')+" ?company_name.\n",

    'kq':"?project "+rela.format(tableName='project',columnName='id')+" ?project_id.\n"\
            "?project "+rela.format(tableName='project',columnName='name_')+" ?project_name.\n",

    'ka':"?aptitude "+rela.format(tableName='aptitude',columnName='id')+" ?aptitude_id.\n"\
            "?aptitude "+rela.format(tableName='aptitude',columnName='name_')+" ?aptitude_name.\n",
}

subSparqlMiddle={
    'p2c':"?peopleregistercompany "+rela.format(tableName='peopleregistercompany',columnName='id_p')+" ?people_idp.\n"\
            "?peopleregistercompany "+rela.format(tableName='peopleregistercompany',columnName='compName')+" ?company_name.\n",
    'q2c':"?companydoproject "+rela.format(tableName='companydoproject',columnName='id')+" ?project_id.\n"\
            "?companydoproject "+rela.format(tableName='companydoproject',columnName='compName')+" ?company_name.\n",
    'a2c':"?companyhasaptitude "+rela.format(tableName='companyhasaptitude',columnName='id')+" ?aptitude_id.\n"\
            "?companyhasaptitude "+rela.format(tableName='companyhasaptitude',columnName='compName')+" ?company_name.\n",
}
subSparqlMiddle['c2p'] = subSparqlMiddle['p2c']
subSparqlMiddle['c2q'] = subSparqlMiddle['q2c']
subSparqlMiddle['c2a'] = subSparqlMiddle['a2c']
subSparqlMiddle['q2p'] = subSparqlMiddle['p2c']+subSparqlMiddle['c2q']
subSparqlMiddle['p2q'] = subSparqlMiddle['q2p']
subSparqlMiddle['q2a'] = subSparqlMiddle['q2c'] + subSparqlMiddle['c2a']
subSparqlMiddle['a2q'] = subSparqlMiddle['q2a']
subSparqlMiddle['p2a'] = subSparqlMiddle['p2c'] + subSparqlMiddle['c2a']
subSparqlMiddle['a2p'] = subSparqlMiddle['p2a']

targetKeyword={
    'kp':' ?people_name ',
    'kc':' ?company_name ',
    'kq':' ?project_name ',
    'ka':' ?aptitude_name ',
    'pan':' ?aptitude_name ',
    'pac':' ?aptitude_catgory ',
    'paf':' ?aptitude_fromWhere ',
    'pcn':' ?company_name ',
    'pcc':' ?company_category ',
    'ppn':' ?people_name ',
    'ppc':' ?people_category ',
    'ppm':' ?people_major ',
    'pqc':' ?project_category ',
    'pqw':' ?project_whom ',
    'pqn':' ?project_name ',
}

class Question2Sparql:
    def __init__(self, dict_paths):
        self.tw = word_tagging.Tagger(dict_paths)

    def putIntoDict(self,word_objects):
        dictEntity = {
            'people': [],
            'company': [],
            'project': [],
            'aptitude': [],
        }
        dictKeyword = {
            'people': [],
            'company': [],
            'project': [],
            'aptitude': [],
        }
        for wo in word_objects:
            if wo.pos[0] == 'p':
                if wo.pos[1] == 'p':
                    dictEntity['people'].append(wo)
                elif wo.pos[1] == 'c':
                    dictEntity['company'].append(wo)
                elif wo.pos[1] == 'a':
                    dictEntity['aptitude'].append(wo)
                elif wo.pos[1] == 'q':
                    dictEntity['project'].append(wo)
            elif wo.pos[0] == 'k':
                if wo.pos[1] == 'p':
                    dictKeyword['people'].append(wo)
                elif wo.pos[1] == 'c':
                    dictKeyword['company'].append(wo)
                elif wo.pos[1] == 'a':
                    dictKeyword['aptitude'].append(wo)
                elif wo.pos[1] == 'q':
                    dictKeyword['project'].append(wo)
        return dictEntity, dictKeyword

    def getSparqlAuto(self, question):
        """
        进行语义解析，找到匹配的模板，返回对应的SPARQL查询语句
        :param question:
        :return:
        """
        sparqlE=''
        targetS = ''
        dictEntity,dictKeyword=self.putIntoDict(self.tw.get_word_objects(question))
        for lde in dictEntity:
            for de in dictEntity[lde]:
                sparqlE=sparqlE+subSparqlEntity[de.pos].format(target=de.token.decode('utf-8'))
                targetS = targetS + targetKeyword[de.pos]
        for ldk in dictKeyword:
            for dk in dictKeyword[ldk]:
                sparqlE=sparqlE+subSparqlKeyword[dk.pos].format(target=dk.token.decode('utf-8'))
                targetS=targetS+targetKeyword[dk.pos]

        for lde in dictEntity:
            for de in dictEntity[lde]:
                for ldk in dictKeyword:
                    for dk in dictKeyword[ldk]:
                        if de.pos[1]==dk.pos[1]:
                            pass
                        else:
                            sparqlE = sparqlE + subSparqlMiddle[de.pos[1]+'2'+dk.pos[1]]
        sparql=SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=targetS,
                                                  expression=sparqlE)
        return sparql

if __name__ == '__main__':
    q2s = Question2Sparql(['./externalDict/Dict.txt','./externalDict/Dict1.txt'])
    question = u'参与舒迪安细胞治疗技术车间装修工程且有注册造价工程师的公司有哪些注册人员和资质？'
    print(q2s.getSparqlAuto(question.encode('utf-8')))
