# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CNKIPipeline:
    def process_item(self, item, spider):
        item["期刊名称"] = item["期刊名称"].strip()
        item["收录数据库"] = ";".join([i.strip() for i in item["收录数据库"]])
        item["语种"] = item["语种"].strip(";")
        if item["专辑名称"] is not None:
            item["专辑名称"] = item["专辑名称"].replace("；", ";")
        if item["专题名称"] is not None:
            item["专题名称"] = item["专题名称"].replace("；", ";")
        item["出版文献量"] = item["出版文献量"].replace("篇", "")
        item["总下载次数"] = item["总下载次数"].replace("次", "")
        item["总被引次数"] = item["总被引次数"].replace("次", "")
        return item