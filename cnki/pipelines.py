# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CNKIPipeline:
    @staticmethod
    def func(x: list[str]):
        x = [i.strip(";").replace(";", ",") for i in x]
        colon_index = [i for i, j in enumerate(x) if j == "："]
        for idx in colon_index:
            x[idx - 1] = x[idx - 1] + x[idx] + x[idx + 1]
            x[idx] = None
            x[idx + 1] = None
        return ";".join([i for i in x if i is not None])

    def process_item(self, item, spider):
        item["期刊名称"] = item["期刊名称"].strip()
        item["出版类型"] = ";".join(item["出版类型"]) if item["出版类型"] else None
        item["收录信息"] = ";".join([i.strip() for i in item["收录信息"]]) if item["收录信息"] else None
        item["收录信息详细"] = self.func(item["收录信息详细"]) if item["收录信息详细"] else None
        item["语种"] = item["语种"].strip(";") if item["语种"] else None
        item["专辑名称"] = item["专辑名称"].replace("；", ";") if item["专辑名称"] else None
        item["专题名称"] = item["专题名称"].replace("；", ";") if item["专题名称"] else None
        item["出版文献量"] = item["出版文献量"].replace("篇", "")
        item["总下载次数"] = item["总下载次数"].replace("次", "") if item["总下载次数"] else None
        item["总被引次数"] = item["总被引次数"].replace("次", "") if item["总被引次数"] else None
        return item
