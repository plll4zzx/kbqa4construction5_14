# encoding=utf-8

"""
@desc:利用SOARQKWrapper向Fuseki发送SPARQL查询，解析返回的结果
"""

from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict

def find_(strR):
    for ini,s in enumerate(strR):
        if s=='_':
            return ini
    return -1

class JenaFuseki:
    def __init__(self, endpoint_url='http://localhost:3030/kg4construction/query'):
        self.sparql_conn = SPARQLWrapper(endpoint_url)
        self.company='company'
        self.people='people'
        self.project='project'
        self.aptitude='aptitude'

    def get_sparql_result(self, query):
        self.sparql_conn.setQuery(query)
        self.sparql_conn.setReturnFormat(JSON)
        return self.sparql_conn.query().convert()

    @staticmethod
    def parse_result(query_result):
        """
        解析返回的结果
        :param query_result:
        :return:
        """
        try:
            query_head = query_result['head']['vars']
            query_results = list()
            for r in query_result['results']['bindings']:
                temp_dict = OrderedDict()
                for h in query_head:
                    temp_dict[h] = r[h]['value']
                query_results.append(temp_dict)
            return query_head, query_results
        except KeyError:
            return None, query_result['boolean']

    def result2list(self, query_result):
        """
        直接打印结果，用于测试
        :param query_result:
        :return:
        """
        query_head, query_result = self.parse_result(query_result)

        if query_head is None:
            if query_result is True:
                print ('Yes')
            else:
                print ('False')
            print()
        else:
            strR=''
            listR=[]
            for qr in query_result:
                for ioi in range(0,len(query_head)):
                    listR.append(qr[query_head[ioi]])
        return listR

    def relationExt(self,str1,str2):
        str_=str1+str2
        if str_==self.company+self.people or str_==self.people+self.company:
            return '注册人员'
        elif str_==self.company+self.project or str_==self.project+self.company:
            return '承揽项目'
        elif str_==self.company+self.aptitude or str_==self.aptitude+self.company:
            return '持有资质'
        return ''

    def relationIn(self,str1,str2,str3):
        return '持有'

    def couple2RDF(self,kw1,kw2):
        loc1=find_(kw1)
        loc2=find_(kw2)
        list1=[
            kw1[0:loc1],
            kw1[loc1+1:]
        ]
        list2=[
            kw2[0:loc2],
            kw2[loc2+1:]
        ]
        if list1[1]=='name' and list2[1]=='name':
            return self.relationExt(list1[0],list2[0])
        elif list1[0]==list2[0]:
            if list1[1]=='name' or list2[1]=='name':
                return self.relationIn(list1[0],list1[1],list2[1])
        return ''
    def dcit2RDF(self,dictR):
        listR=[]
        for dr1 in dictR:
            for dr2 in dictR:
                if dr1==dr2:
                    pass
                else:
                    relation=self.couple2RDF(dr1,dr2)
                    if relation=='':
                        pass
                    else:
                        listR.append({'subject':dictR[dr1],'predicate':relation,'object':dictR[dr2]})
        return listR
    def equal_(self,lr,le):
        if lr['predicate']!=le['predicate']:
            return 0
        elif lr['subject']==le['subject'] and lr['object']==le['object']:
            return 1
        elif lr['object']==le['subject'] and lr['subject']==le['object']:
            return 1
    def exit_(self,lr,listE):
        for le in listE:
            if self.equal_(lr,le):
                return 1
        return 0
    def deleteDuplicate(self,listR):
        listE=[]
        for lr1 in listR:
            if self.exit_(lr1,listE):
                pass
            else:
                listE.append(lr1)
        return listE

    def result2RDF(self, query_result):
        """
        直接打印结果，用于测试
        :param query_result:
        :return:
        """
        listR=[]
        query_head, query_result = self.parse_result(query_result)
        if query_head is None:
            return []
        for qr in query_result:
            listR=listR+self.dcit2RDF(qr)
        return self.deleteDuplicate(listR)

# TODO 用于测试
if __name__ == '__main__':
    fuseki = JenaFuseki()
    my_query = """
        PREFIX :<file:///D:/graduation_design/Demo/kg4construction5_9/vocab/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT  ?people_category  ?project_name  ?people_name  ?company_name  ?aptitude_name  WHERE {
        ?people :people_category '注册造价工程师'.
        ?people :people_category ?people_category.
        ?people :people_name_ ?people_name.
        ?people :people_id_p ?people_idp.
        ?project :project_name_ '舒迪安细胞治疗技术车间装修工程'.
        ?project :project_name_ ?project_name.
        ?project :project_id ?project_id.
        ?people :people_id_p ?people_idp.
        ?people :people_name_ ?people_name.
        ?company :company_name_ ?company_name.
        ?aptitude :aptitude_id ?aptitude_id.
        ?aptitude :aptitude_name_ ?aptitude_name.
        ?peopleregistercompany :peopleregistercompany_id_p ?people_idp.
        ?peopleregistercompany :peopleregistercompany_compName ?company_name.
        ?peopleregistercompany :peopleregistercompany_id_p ?people_idp.
        ?peopleregistercompany :peopleregistercompany_compName ?company_name.
        ?companyhasaptitude :companyhasaptitude_id ?aptitude_id.
        ?companyhasaptitude :companyhasaptitude_compName ?company_name.
        ?peopleregistercompany :peopleregistercompany_id_p ?people_idp.
        ?peopleregistercompany :peopleregistercompany_compName ?company_name.
        ?companydoproject :companydoproject_id ?project_id.
        ?companydoproject :companydoproject_compName ?company_name.
        ?companydoproject :companydoproject_id ?project_id.
        ?companydoproject :companydoproject_compName ?company_name.
        ?companydoproject :companydoproject_id ?project_id.
        ?companydoproject :companydoproject_compName ?company_name.
        ?companyhasaptitude :companyhasaptitude_id ?aptitude_id.
        ?companyhasaptitude :companyhasaptitude_compName ?company_name.
        
        }
    """
    result = fuseki.get_sparql_result(my_query)
    print(fuseki.result2RDF(result))
    #fuseki.print_result_to_string(result)