# encoding=utf-8
import matplotlib
import networkx as nx
import matplotlib.pyplot as plt

#添加边

F = nx.Graph() # 创建无向图
F.add_edge('嘿嘿嘿',12)   #一次添加一条边

#等价于
e=(13,14)        #e是一个元组
F.add_edge(*e) #这是python中解包裹的过程

F.add_edges_from([(1,2),(1,3)],attr2 = 'this_is_a_edge_attribute' )     #通过添加list来添加多条边

#通过添加任何ebunch来添加边
#F.add_edges_from(H.edges()) #不能写作F.add_edges_from(H)

nx.draw(F, with_labels=True,width=6,node_size=700,node_color='r')
plt.show()