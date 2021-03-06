# 基于建筑企业知识图谱的问答系统

这个是我本科毕业时的毕业设计，主要是想先构建一个有关于建筑企业的知识图谱，在基于这个知识图谱做点事情，就用图谱可视化的形式做了这么一个问答系统。

先简单介绍一下知识图谱吧，当然了，这些都是我自己的理解，未必准确。

在介绍知识图谱之前呢，先简单介绍一下什么是数据。在传统的关系型数据库中，数据就是标签和相对应的值，比如：姓名：张三，性别：男……数据的结构虽然看起来很简单，但是已经可以解决很多问题了，比如最常见的增删改查，但是这种结构无法进行推理。那什么是推理呢？举例子来讲：苹果是水果，水果都可以吃，所以苹果可以吃。当然了也不是完全不能进行推理，（其实有很多图数据库就是在sql数据库的基础上搭建的），但至少很麻烦，尤其是涉及到多表多属性联合查找的时候。

为了实现推理，我们就引入了“知识”这个概念，希望“知识”可以解决这个问题。实现“知识”的方法有很多种，其中一种就是“知识图谱”，简单说就是用图的方式来表示知识：用结点表示实体，用边表示实体间的关系。“知识图谱”这个概念最近是由Google重新提出的，它并不是Google的首创。

随着知识图谱技术的不断发展，其应用范围也越来越广泛，在通用知识图谱方面已经诞生了许多杰出的成果，但是在领域知识图谱方面的研究还尚显不足。随着建筑市场的不断发展，政府部门对于应用新的技术方法管理建筑企业数据，描述企业综合情况的需求越来越迫切。因此本文提出了一种建筑企业知识图谱的构建方案，以及在此图谱的基础上的可视化问答系统的实现方案。本文主要贡献如下：

（1）提出了建筑企业知识图谱的构建方案、总体框架、技术路线。

（2）通过建立建筑企业知识图谱的本体，详细描述了图谱中各实体的属性以及实体间的关系。

（3）通过编写网络爬虫，从开放网站爬取了多种数据来源的建筑企业的相关信息；通过实体对齐解决异构数据源的所导致的数据重叠、歧义；通过知识抽取得到RDF三元组。最后将所得RDF数据存储在图数据库中并完成建筑企业知识图谱的构建。

（4）在构建完成的建筑企业知识图谱的基础上，通过自然语言处理、可视化技术构建可视化问答系统。基于自然语言处理技术实现问题与图谱查询语言间的转换，基于可视化技术实现图谱查询结果集的图形化展示。

更多见知乎文章https://zhuanlan.zhihu.com/p/144548736
