# encoding=utf-8

"""
@desc:main函数，整合整个处理流程。
"""
from KB_query.jenaSparqlEndpoint import JenaFuseki
from KB_query.question2sparql import Question2Sparql
import KB_query.creatDict
def query_function(question):
    print(question)
    adrs='D:\graduation_design\Demo\kbqa4construction5_13\KB_query\externalDict\\'
    q2s = Question2Sparql([adrs+'Dict.txt', adrs+'Dict1.txt'])
    fuseki = JenaFuseki()
    sparql = q2s.getSparqlAuto(question.encode('utf-8'))
    #listR=[question]
    if sparql != {}:
        result = fuseki.get_sparql_result(sparql)
        return fuseki.result2RDF(result)
    else:
        return []

if __name__ == '__main__':
    #question = input('请输入你的问题：')
    question =[ '一片绿园林工程有限公司有哪些注册人员',
                '一片绿园林工程有限公司有哪些工程',
                '三河市华玉建筑工程有限公司有哪些资质?',
                '哪些企业参与了舒迪安细胞治疗技术车间装修工程',
                '哪些企业拥有工程设计建筑行业（建筑工程）甲级的资质？',
                '参与舒迪安细胞治疗技术车间装修工程且有注册造价工程师的公司有哪些资质？'
            ]
    listR=query_function(question[5])
    if listR!=[]:
        print(listR[0])
        for object in listR[1:]:
            print(object)
    else:
        print('Sorry')

