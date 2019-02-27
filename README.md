大作业实验报告

# 项目描述

这是一个资料齐全的香水搜索网站。用户通过输入自己所期待的香水的各类信息，检索到期望的香水，并通过网站的购买链接直接购买。

---

# 项目目的

市面上的香水搜索引擎都是与购买相分离的，香水购物网站并没有提供较详细的商品信息，比如：关心的前中后调、调香师、香调等元素都未被容纳在购物网站，市面上并没有专门的香水购物网站，给大家的购买带来了许多麻烦。因此我们打算设计开发出一个资料齐全、且能满足用户个性化的购买需求的香水搜索小站。

---

# 任务分工

- 顾钰仪：爬虫、图片搜索
- 李聆嘉：文字搜索、整合
- 马菁晖：界面、整合
- 王琢：爬虫、测试、实验报告、PPT

---

# 项目实现

1. 界面(含整合)
   - 页面构架：
     网页的结构和中期整合时提供的思路一致，渲染模版html文件，其中包括搜索主页与搜索结果展示页面。为不同搜索功能的实现制作多个搜索主页，结果展示基本不作区分。使用页面主要实现了菜单栏的设计，网页间的转换以及结果的排列展示，详细资料。展示网页的设计主要采用了css的格式和JavaScript添加动态效果。
   - 实现方法
     1. 菜单栏
     菜单栏的设计主要是为了实现页面之前的切换。通过页面右上角的button实现菜单栏的弹出和隐藏，具体方式是将菜单的初始位置设为负数，即在页面左侧之外；单击菜单按钮使菜单向右移动至合适位置出现，通过js函数（classie.js）使弹出收回过程平滑。菜单栏本体为标签为nav的框架，具体格式设计在component.css文件中实现。
     2. 首页设计
        - 文字搜索
          文字搜索页面采用统一的格式：标题栏/按钮/搜索框，其中搜索框按照搜索的不同功能区别，如文字单一特征搜索仅一文字输入框，交叉搜索多项输入。关键词由input传入搜索系统，再将结果以列表的形式传入结果页面。
                  user_data = web.input()
                  a = func(user_data.keyword)
        - 图片搜索
          图片搜索的输入框为文件导入，通过JavaScript函数实现了图片预览功能：
              function imgPreview(fileDom){
                      //判断是否支持FileReader
                      if (window.FileReader) {
                          var reader = new FileReader();
                      } else {
                          alert("您的设备不支持图片预览功能，如需该功能请升级您的设备");
                      }
                      //获取文件
                      var file = fileDom.files[0];
                      var imageType = /^image\//;
                      //是否是图片
                      if (!imageType.test(file.type)) {
                          alert("请选择图片格式文件");
                          return;
                      }
                      //读取完成
                      reader.onload = function(e) {
                          //获取图片dom
                          var img = document.getElementById("preview");
                          //图片路径设置为读取的图片
                          img.src = e.target.result;
                      };
                      reader.readAsDataURL(file);
                  }
          另外通过函数upload（code.py 47）将图片保存至本地，以进行图片搜索数据的读取。
     3. 搜索结果展示
        搜索结果通过$def with(form)的形式传入html文件中，由于每个结果商品特征过多不方便在页面同时展示，我们仅在结果页面展示相关关键特征（如商品名字和价格等），再设计详细展示模块，展示具体信息并提供商品链接。格式设置主要是通过标签的class信息在css文件中具体控制，结果格式设计见rescomponent.css
        - 结果排列
          商品采用小图+标题的形式展示，控制商品宽度一致，高度按原图比例实现每行四个block叠加排列。
        - 详细信息
          为实现用户打开结果展示，结果展示默认属性hidden，当商品状态转化为active后出现；通过div标签划分左右文字/图片区域，文字部分提供名称/品牌/香调/气味/购买链接等具体信息，图片部分展示完整大图，控制max-width，max-height，align="center"使其居中至适宜尺寸，另加入结果切换效果，详细见cbpGridGallery.js
              .slideshow nav span.nav-prev,
              .slideshow nav span.nav-next {
              	top: 50%;
              	-webkit-transform: translateY(-50%);
              	transform: translateY(-50%);
              }
     4. 其他
        除以上内容外我们还具体加入了背景图片，字体，指针悬浮/选中效果等，尽可能优化用户体验。
   
   
   
   1. 爬虫
   - 目标网站：
     	由于我们小组做的是香水品类搜索引擎，因此也就不需要大范围无差爬虫，可以将目标简单的定为商品内容和商品详细资料两部分进行爬取。
     	商品内容部分我们主要以淘宝网作为目标网站，而商品详细资料的来源较为广泛，但是主要的参考网站还是香水时代网站。
   - 实现方法：
     - 淘宝网站有较强反爬虫策略，又加上我们并不需要大量不同品类商品的信息，因此我设计了一个模仿用户行为的爬虫，简单的来说就是爬取关键词搜索后得到的网站中的商品信息。
       1.设置headers
           def url_open(url):
               headers=("user-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
               opener=urllib2.build_opener()
               opener.addheaders=[headers]
               urllib2.install_opener(opener)
               response=urllib2.Request(url)
               data=urllib2.urlopen(response).read().decode("utf-8","ignore")
               return data
       2.通过keyword进行检索
           keywords=urllib.quote(keywd)
           url="https://s.taobao.com/search?q="+keywords+"&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s="+str(i*44)
       3.通过分析淘宝的API.CustomizedApi类，定义各个字段正则匹配规则
       	由于淘宝网显示的html代码都经过加密等处理，直接用其爬取是无法得到任何信息的，所以只能分析json的列表信息。很容易就可以知道商品Url的匹配时detail_url等等，按照类似规则就可以进行正则匹配。
       
     - 香水时代等网站的结构较为简单，可以直接通过BeautifulSoup进行爬取。
   - 结果：所有结果都以列表形式提供
     	perfumer_pic.txt:提供调香师姓名和图片URL（38.1kB）
     	taobao.txt:提供商品的URL链接、图片链接、购买人数、评价人数、邮费、店铺名、店铺所在地 （18.8MB）
     	scent.txt:提供商品的气味、香调归属、香水时代评分、评价数、图片URL(1.62MB)
     	perfumer.txt:提供调香师名字及调香师香水作品名字、图片URL、香水前中后调(3.01MB)
     	materials文件:提供香水时代中的所有香水图片(127.9MB)
   1. 文字搜索
      1. 建立索引
         索引关键词信息的来源：原始爬虫资料+处理后的爬虫资料（分组整理）
         问题难点：
         1. 怎么把爬取到的商品和香水资料整合到一起？ - 因为每个香水的购买信息和资料信息是独立爬取 的，而我们的网站需要对这两类信息加以整合，这就要求我们的索引必须是既包含购买信息又包含详细资料的。因此，这就需要我们对不同类别的资料进行预处理和匹配，从而建立可靠的完整商品索引。
            我们首先对每一件商品的商品信息在单纯根据香水资料建立的索引里根据名字、热度、评论数等可靠信息的相似度进行第一次预搜索，每次通过找到最佳商品与资料的对应关系来不断更新原来的基础索引，从而建立起完整的。
         2. 怎么根据不同香水的资料完整度分别建立索引- 因为爬取香水资料的网站多样性，导致各类香水的原始资料参差不齐。所以不可能对所有爬虫资料使用同一种建立索引的方式，也不可能单纯使用不同的建立索引的方式遍历一篇原始爬虫资料。解决方法是：先对所有爬取到的香水信息进行分类，分别整合入各自不同的新的txt文件里进行文本处理，不断迭代更新，最后生成一个完整的资料汇总whole.txt并使用它来建立索引。
         结果：
         处理原始爬虫文件生成适合所需索引的文本文件，然后进行预搜索处理，最后建立最终索引。建成大小为20M，涵盖65853条商品，每条包含20个字段（香水名、调香师、前中后调、销量、店铺、价格、邮费、图片、链接等各种所需信息）的index索引文件。索引的使用搜索效果也十分理想——同一款式的香水都能对应5到6个不同店铺的购买链接，这为后续结果处理（价格、销量的排序）提供了便利。
      2. 关键词搜索
         前八次实验中我们学习了pylucene库，但是只用了单字段的文本搜索，然后根据默认的相关度排序。我们在中期学习lucene的基础上深入学习了pylucene提供的接口，结合具体的商品情况实现了组合搜索等更丰富的功能，满足各种个性化的商品需求。
         结果：在实现了根据品牌、气味（可单独分前中后调或是综合搜索）、调香师等有用信息检索香水的功能的基础上，实现了品牌|气味|香调的多元素组合搜索。
         - 交叉搜索包括：品牌+气味 / 前中后调交叉搜索
         - 这是我们的亮点。因为香水有各种信息都可以作为特征来进行搜索，对不同特征有不同需求的用户可以通过使用组合特征搜索这项功能，进而找到最适合自己的商品。
         - BooleanClause - 用于表示布尔查询子句关系的类
         - MultiFieldQueryParser - 对单个表的索引进行多字段同时搜索
         - 另外，此处在搜索时用列表来存储目标输入，使得用户可以自由地输入前中后调（可以为空，也可以单个香调的多重输入），增强了搜索的鲁棒性。
             fields = ["brand", "scents"]
             clauses=[BooleanClause.Occur.SHOULD,BooleanClause.Occur.SHOULD,BooleanClause.Occur.SHOULD]
             parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, fields, analyzer)
             parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
             query = MultiFieldQueryParser.parse(parser, query)     
      3. 结果处理
      在SortField里面有很多静态常量来提供给排序器作为排序的依据：
   1.       SortField里的属性    	    Sort里的属性    	      含义      
         SortField.FIELD_DOC 	Sort.INDEXORDER 	 按照索引的顺序进行排序  
        SortField.FIELD_SCORE	 Sort.RELEVANCE 	 按照关联性评分进行排序  
         SortField.Type.INT  	 Sort.Type.INT  	 按照int型的字段排序  
        SortField.Type.DOUBLE	Sort.Type.DOUBLE	按照double型的字段排序
      	- 综合排序：使用按各个字段设定的权重boost对结果排序
      	- 价格区间：使用numeric range query对价格关键词进行筛选
      	- 由于对于pylucene各种接口的调用网上更多的是c++调用方法，没有官方和详细的教程与示例代码，即使找到也是对应不同lucene版本的，最后我通过在github上找到pylucene apache java源码，以及参考stackoverflow上的问题尝试出了正确调用方法，实现了预期效果。
      - 效果：实现了价格升序、销量降序、评分降序、综合排序和价格区间筛选的功能，优化了用户的搜索体验。
      一些题外话：在网上查阅资料的时候发现有个lupyne的库，它的介绍如下：
      > Lupyne first provides a unified search interface.The search method allows lucene Sort parameters to be passed through, since that's still optimal.Additionally the hits themselves can be sorted afterwards with any python callable key.The IndexSearcher.comparator method is convenient for creating a sort key table from indexed fields.The upshot is custom sorting and sorting large results are both easier and faster.
      因为lucene虽然有它的优点，但不足仍然不可忽视，比如：必须设置最大结果显示数，如果过大会由于它是预先分配，再排序，而造成结果不准确；比较算法中调用VM的时间复杂度是O(nlogn)，比scoredocs的迭代要复杂得多。最后我安装了lupyne库，并尝试使用它搜索和排序：
          hits = indexer.search(sort='price')
          comparator = indexer.comparator('price')	#建立关于价格排序的比较器
          hits = indexer.search().sorted(comparator.__getitem__)	#根据该比较器进行排序
      效果很不错，但是由于与已经建立的index商品索引很难对接，没有继续使用下去这个方法。如果后续有时间，会继续对其进行研究和应用。
   1. 图像搜索
   - 实现方法：
     1. 图片整体特征提取
        由于在香水时代匹配的都是特征较好的、没有干扰特征的图片、所以可以从整体上进行特征把握，所以我建立颜色直方图，并将结果进行差分哈希映射，并把预处理结果保存pkl文件。
     2. 目标图片特征提取
        首先像预处理一样对于图片整体特征进行提取，然后在预处理哈希及图片的词典中进行匹配，对于映射在同一图片中的图片再进行传统的特征点提取，在提取方面，为了追求检索速度，我选择了ORB特征，但是由于ORB是二进制串，所以会有较高的误匹配率，所以为了追求较好的结果，在匹配器部分选择了暴力匹配匹配器。
   - 理论支持：
     1. orb特征子是速度和性能都较好的特征描述算法
     ORB（Oriented FAST and Rotated BRIEF）是一种快速特征点提取和描述的算法。
     这个算法是由Ethan Rublee, Vincent Rabaud, Kurt Konolige以及Gary R.Bradski在2011年一篇名为“ORB：An Efficient Alternative to SIFTor SURF”的文章中提出。ORB算法分为两部分，分别是特征点提取和特征点描述。
     特征提取是由FAST（Features from  Accelerated Segment Test）算法发展来的，特征点描述是根据BRIEF（Binary Robust IndependentElementary Features）特征描述算法改进的。
     ORB特征是将FAST特征点的检测方法与BRIEF特征描述子结合起来，并在它们原来的基础上做了改进与优化。ORB算法的速度是sift的100倍，是surf的10倍。
   1. 差异哈希是速度较快的哈希映射
      由于通过异或来进行匹配，因此在速度上有着非常好的提升，但是这个哈希可能太过严格，因此在尺度不一致的情况下，搜索的结果不甚理想，可以进一步的优化。

---

# 有待改进之处和未来展望

- 哈希算法可以更进一步优化（加上图片整体特征，而不是仅仅使用颜色特征）以进一步提升图片搜索准确性。
- 增加根据用户的搜索历史提供个性化推荐的功能。
- 建立商品之间的联系，提供同类商品推荐功能。
- 模糊搜索 - 错别字，模糊信息识别功能。
- 不只从香水信息角度出发去检索，可以进一步增加根据顾客的性别、年龄、职业、性格等个性化信息来检索适合特定类别顾客的某类香水产品，使搜索网站更加有温度和人性化。

---

# 其他

项目的github主页：[点此进入](https://github.com/LiPGa/JiaoDaXunXun)
