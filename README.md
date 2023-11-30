# 使用Scrapy爬取CNKI期刊信息
- 截止到2023年11月，[CNKI 共收录11615种期刊](https://navi.cnki.net/knavi/journals/search)，由于存在跨学科期刊，最终爬取的数据量低于该值；
- 爬取的期刊信息涵盖期刊名称、主办单位、出版周期、ISSN号、CN号、所属学科、影响因子、字母标识、收录数据库等字段；

## 运行爬虫
本仓库提供 [爬取的数据集](https://github.com/doublessay/cnki-journal-info/blob/main/dataset)，可直接下载使用。如果想要自行爬取，请参考如下步骤：
```bash
git clone https://github.com/doublessay/cnki-journal-info.git
cd cnki-journal-info

# 建议使用虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate # Mac/Linux
venv\Scripts\activate.bat # Windows

# 安装依赖
pip install -r requirements.txt

# 运行爬虫
scrapy crawl journal -o dataset/2023-11-30.csv
```

## 爬取策略
1. 使用随机 User-Agent，借助 [fake-useragent](https://pypi.org/project/fake-useragent/) 库构造一个 Middleware；
2. 并发请求设置为3，下载延迟设置为1秒，禁用cookie；

## 统计分析
1. 创刊时间最早的5种期刊

|期刊名称|曾用刊名|主办单位|创刊时间|url|
|----|----|----|----|----|
|中华医学杂志(英文版)|Chinese Medical Journal|中华医学会|1887|https://navi.cnki.net/knavi/journals/ZHSS/detail|
|苏州大学学报(哲学社会科学版)|学桴(东吴月报);苏州科技学院学报(社会科学版)|苏州大学|1906|https://navi.cnki.net/knavi/journals/SZDX/detail|
|西北大学学报(自然科学版)| |西北大学|1913|https://navi.cnki.net/knavi/journals/XBDZ/detail|
|西北大学学报(哲学社会科学版)| |西北大学|1913|https://navi.cnki.net/knavi/journals/XBDS/detail|
|科学| |上海科学技术出版社有限公司|1915|https://navi.cnki.net/knavi/journals/KXZZ/detail|

2. 综合影响因子[^1]最高的5种期刊

|期刊名称|主办单位|专题名称|综合影响因子|url|
|----|----|----|----|----|
|管理世界|国务院发展研究中心|管理学|22.557|https://navi.cnki.net/knavi/journals/GLSJ/detail|
|求是|中国共产党中央委员会|政治军事法律综合|21.357|https://navi.cnki.net/knavi/journals/QUSI/detail|
|中国工业经济|中国社会科学院工业经济研究所|工业经济|18.213|https://navi.cnki.net/knavi/journals/GGYY/detail|
|经济研究|中国社会科学院经济研究所|经济与管理综合|15.382|https://navi.cnki.net/knavi/journals/JJYJ/detail|
|中国社会科学|中国社会科学院|教育综合|11.783|https://navi.cnki.net/knavi/journals/ZSHK/detail|

3. 平均下载次数最高的5种期刊

|期刊名称|主办单位|专题名称|平均下载次数|url|
|----|----|----|----|----|
|公共管理学报|哈尔滨工业大学管理学院|管理学|3084.01|https://navi.cnki.net/knavi/journals/GGGL/detail|
|经济研究|中国社会科学院经济研究所|经济与管理综合|2907.93|https://navi.cnki.net/knavi/journals/JJYJ/detail|
|经济学(季刊)|北京大学|经济理论及经济思想史|2841.92|https://navi.cnki.net/knavi/journals/JJXU/detail|
|管理世界|国务院发展研究中心|管理学|2835.96|https://navi.cnki.net/knavi/journals/GLSJ/detail|
|中国社会科学|中国社会科学院|教育综合|2743.52|https://navi.cnki.net/knavi/journals/ZSHK/detail|

4. CNKI收录的CSCD(2023-2024)期刊(1238种)

|期刊名称|主办单位|专题名称|url|
|:----|:----|:----|:----|
|Asian Herpetological Research|中国科学院成都生物研究所;中国科技出版传媒股份有限公司|生物学|https://navi.cnki.net/knavi/journals/YZLQ/detail|
|Research in Astronomy and Astrophysics|中国科学院国家天文台;中国天文学会|天文学|https://navi.cnki.net/knavi/journals/TTWL/detail|
|Journal of Oceanology and Limnology|中国海洋湖沼学会|海洋学|https://navi.cnki.net/knavi/journals/HYFW/detail|
|Theoretical and Applied Mechanics Letters|中国科学院力学研究所;中国力学学会|力学|https://navi.cnki.net/knavi/journals/LXKB/detail|
|Journal of Systems Science and Information|中国系统工程学会;中国科技出版传媒股份有限公司|非线性科学与系统科学;计算机软件及计算机应用|https://navi.cnki.net/knavi/journals/JSSI/detail|
|...| | | |

5. CNKI收录的CSSCI(2021-2022)期刊(813种)

|期刊名称|主办单位|专题名称|url|
|:----|:----|:----|:----|
|中国社会经济史研究|厦门大学历史研究所|中国通史;经济体制改革|https://navi.cnki.net/knavi/journals/ZSJY/detail|
|新疆社会科学|新疆社会科学院|经济与管理综合|https://navi.cnki.net/knavi/journals/XJSH/detail|
|印度洋经济体研究|云南财经大学|经济体制改革|https://navi.cnki.net/knavi/journals/YDYY/detail|
|地方财政研究|东北财经大学;辽宁省财政科学研究所|财政与税收|https://navi.cnki.net/knavi/journals/DFCZ/detail|
|财务研究|中国财政杂志社|会计|https://navi.cnki.net/knavi/journals/CWYJ/detail|
|...| | | |

6. CNKI收录的SCI(2023)期刊(178种)

|期刊名称|主办单位|专题名称|url|
|:----|:----|:----|:----|
|Asian Herpetological Research|中国科学院成都生物研究所;中国科技出版传媒股份有限公司|生物学|https://navi.cnki.net/knavi/journals/YZLQ/detail|
|Research in Astronomy and Astrophysics|中国科学院国家天文台;中国天文学会|天文学|https://navi.cnki.net/knavi/journals/TTWL/detail|
|Journal of Oceanology and Limnology|中国海洋湖沼学会|海洋学|https://navi.cnki.net/knavi/journals/HYFW/detail|
|China Communications|中国通信学会|电信技术;信息经济与邮政经济|https://navi.cnki.net/knavi/journals/ZGTO/detail|
|Journal of Computer Science & Technology|中国计算机学会;中国科学院计算技术研究所|电子信息科学综合|https://navi.cnki.net/knavi/journals/JSKB/detail|
|...| | | |


[^1]: 综合影响因子是指被评价期刊前两年发表的可被引文献在统计年的被引用总次数与该期刊在前两年内发表的可被引文献总量之比。复合影响因子的统计范围不仅包含期刊，还包含硕博士论文和会议论文。