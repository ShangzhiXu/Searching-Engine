[![image](https://github.com/ShangzhiXu/Searching-Engine/blob/master/img/%E6%88%AA%E5%B1%8F2022-05-31%20%E4%B8%8B%E5%8D%886.11.46.png)](https://github.com/ShangzhiXu/Searching-Engine/blob/master/img/%E5%B1%8F%E5%B9%95%E5%BD%95%E5%88%B62022-08-02%20%E4%B8%8A%E5%8D%8810.38.34_.gif)
gif展示如上，点击可查看

使用django框架实现了一个搜索引擎的demo，用Selenium在Chrome中爬取100余篇新闻，随后使用tf-idf算法提取新闻中关键词，再使用NLP提取用户搜索中的关键词。用cosine相似度来匹配最好的文章返回给前端


# 程序结构

```java 
correct: （机器学习）用户输入纠错模块
News：本地存储所有新闻文件
templates：前端
File_manager:文件操作模块
InvertIndex:倒序索引构建
main：入口函数
models：数据库模型
nltk_manager:自然语言处理
Query_manager：查询模块
VSM_manager:构建空间向量模型
```


## 查询引擎数据
编程爬取了ChinaDaily中国日报网的China/innovation专栏的文章作为被检索文档
文章被爬取后存入数据库中，构成检索的数据源，索引包含文章id，题目，内容，网址和时间及作者信息。库中共存有文章100余篇

<img width="452" alt="image" src="https://user-images.githubusercontent.com/63028857/182281103-96b2d9ba-a716-4fb7-b4a9-863f3bdef625.png">

## 机器学习数据
<img width="415" alt="image" src="https://user-images.githubusercontent.com/63028857/182281160-4680aaa3-a86b-4c87-9ba9-4585748c4616.png">

从网上爬下来的用户在amazon上的食物评价以及酒水评价，在上面的截图中有显示，作为后面机器学习的训练数据。

## 爬虫模块
爬虫程序名命为Spider，含python程序main.py。程序使用selenium架构和chrome，通过定位元素xpath进行内容爬取。下为部分程序截图，完整程序详见Spider/main.py
爬的内容有文章标题、内容、url、作者、时间
爬取的内容放在dbsqlite数据库里面，sqlite是一个轻量级的数据库，能够很好的与我们后面的django框架结合，操作方便。
selenium架构是一个浏览器调试工具，这里用来爬虫，绕过了网站的反爬虫机制，成功获取内容

## 基于增量的倒序索引创新
倒序索引的构建，我们可以看到，需要对文章中每一个词都进行一次比对，这是我们构建倒序索引的主要瓶颈。这个问题在我们的数据库更新的时候更为明显。
新闻每天更新，按照传统算法，我们每次有任何新闻更新，都要重新构建一遍倒序索引表，这种方法需要每次都扫描一遍所有文件，重新构建全部的invertIndex，开销非常大，因此我们在这里提出了基于增量的倒序索引构建

步骤如下：
1.	第一次构建，按照传统的invertIndex构建，简单的遍历程序
2.	把现有的所有单词全部存在一个txt文件里面（word_all.txt）
3.	每次更新新闻，只需要扫描更新的新闻的词汇，分两种情况
3.1	如果这个词汇在word_all.txt中，不需要更新invertIndex，因为可以确定，别的文章里是否有这个词，和本次更新无关，因此不需要更新其余表项，只需要添加新的文章
3.2	如果不在word_all.txt中，表明这个单词在别的文章中出现次数是0，也不需要更新invertIndex其余表项，只要添加一项新的单词和一些新的文章就可以


我们称之为：基于增量的算法。
这样的算法，大大减小了每次更新新闻库的开销



## 向量空间检索模型
  
TF-IDF的主要思想是：如果某个单词在一篇文章中出现的频率TF高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类。算法用TF*IDF来表达文章的匹配度，TF为词频，用来反应关键词在文章中出现的频率，IDF为逆向文件频率通过横向对比来反应关键词的代表性高低，TF和IDF计算公式如下：
  
 
![image](https://user-images.githubusercontent.com/63028857/182281543-8b4b8192-1535-4bf8-ac22-cb30b6a863aa.png)

## 基于cosine匹配的查询算法

传统的线性比较算法过于简单，不能很好的匹配用户真正想要搜索的内容，这里，我们使用向量余弦相似度计算，通过计算文章向量和用户查询内容向量的夹角，夹角越小，说明用户查询与这篇文章匹配度越高。


## 自然语言处理NLTK

![image](https://user-images.githubusercontent.com/63028857/182281627-246e6e65-be39-4e03-affd-425e0d9eb057.png)

## 人工测试

![image](https://user-images.githubusercontent.com/63028857/182281976-9f07b44e-1c13-4b80-b148-2b0b5d1f5bd5.png)

其余测试，召回率大多数在70%-80%左右，对于准确率，由于实在是难以查看，但是经过人工检查的几次查询准确率都在80-90%，可以认为本系统的准确率和召回率都是比较高的。

 




