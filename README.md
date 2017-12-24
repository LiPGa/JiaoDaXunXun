# searching-engine
searching for perfume
1. ``perfumer.txt``里有几个香水的前调、中调后调是空的，比如：心情巧克力系列


#####目前已经建好的索引：
1. 图片URLurl
2. 香水名name
3. 调香师姓名perfumer
4. 香调tune
5. 评分rate
6. 评价数comment
7. 气味scents/前后中调former_scents,mid_scents,last_scents

> brand索引目录其实可以不用。

**有关indexfiles.py里的几点说明：**
``scent_index()``函数：用来添加perfumer.txt里没有，scent.txt里有的香水
``perfumer_index()``函数，用来添加perfumer里所有香水（同时scent里有的追加香调）
``nosetime_index()``函数，用来添加nosetime里有但perfumer和scent都没有的香水（只有5个或者7个非空索引）
