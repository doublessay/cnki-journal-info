import csv
import json
import math
import scrapy


class JournalSpider(scrapy.Spider):
    name = "journal"

    with open("dataset/2023-11-30.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        journal_codes = {row[-2] for row in reader}

    def start_requests(self):
        data = {"productcode": "JOURNAL", "index": ""}
        yield scrapy.FormRequest(
            url="https://navi.cnki.net/knavi/journals/categories", formdata=data, callback=self.parse
        )

    def parse(self, response):
        category_count_list = response.xpath("//li/span/a/i/following-sibling::em/text()").getall()
        assert len(category_count_list) == 10
        category_count_list = [int(i.strip("()")) for i in category_count_list]
        category_page_count_list = [math.ceil(i / 21) for i in category_count_list]

        search_state_json = {
            "StateID": "",
            "Platfrom": "",
            "QueryTime": "",
            "Account": "knavi",
            "ClientToken": "",
            "Language": "",
            "CNode": {"PCode": "JOURNAL", "SMode": "", "OperateT": ""},
            "QNode": {
                "SelectT": "",
                "Select_Fields": "",
                "S_DBCodes": "",
                "QGroup": [
                    {
                        "Key": "Navi",
                        "Logic": 1,
                        "Items": [],
                        "ChildItems": [
                            {
                                "Key": "journals",
                                "Logic": 1,
                                "Items": [
                                    {
                                        "Key": "subject",
                                        "Title": "",
                                        "Logic": 1,
                                        "Name": "CCL",
                                        "Operate": "",
                                        "Value": "A?",
                                        "ExtendType": 0,
                                        "ExtendValue": "",
                                        "Value2": "",
                                    }
                                ],
                                "ChildItems": [],
                            }
                        ],
                    }
                ],
                "OrderBy": "OTA|DESC",
                "GroupBy": "",
                "Additon": "",
            },
        }
        for category, category_page_count in zip("ABCDEFGHIJ", category_page_count_list):
            search_state_json["QNode"]["QGroup"][0]["ChildItems"][0]["Items"][0]["Value"] = category + "?"
            data = {
                "searchStateJson": json.dumps(search_state_json),
                "displaymode": "1",
                "pageindex": "1",
                "pagecount": "21",
                "index": "subject",
                "searchType": "刊名(曾用刊名)",
                "clickName": "",
                "switchdata": "",
            }
            for i in range(1, category_page_count + 1):
                data["pageindex"] = str(i)
                yield scrapy.FormRequest(
                    url="https://navi.cnki.net/knavi/journals/searchbaseinfo", formdata=data, callback=self.parse_page
                )

    def parse_page(self, response):
        if not response.text.startswith("<script>"):
            for href in response.xpath("//a[@target='_blank']/@href").getall():
                journal_code = href.split("=")[-1]
                if journal_code not in self.journal_codes:
                    yield scrapy.Request(
                        url=f"https://navi.cnki.net/knavi/journals/{journal_code}/detail?uniplatform=NZKPT",
                        callback=self.parse_detail,
                    )

    def parse_detail(self, response):
        if not response.text.startswith("<script>"):
            yield {
                "期刊名称": response.xpath("//h3[@class='titbox titbox1']/text()").get(),
                "出版类型": response.xpath("//p[@class='journalType journalType1']/span/text()").getall(),
                "收录信息": response.xpath("//p[@class='journalType journalType2']/span//text()").getall(),
                "收录信息详细": response.xpath("//h4/following-sibling::p//text()").getall(),
                "目前状态": response.xpath("//label[text()='目前状态']/following-sibling::span/text()").get(),
                "曾用刊名": response.xpath("//label[text()='曾用刊名']/following-sibling::span/text()").get(),
                "主办单位": response.xpath("//label[text()='主办单位']/following-sibling::span/text()").get(),
                "出版周期": response.xpath("//label[text()='出版周期']/following-sibling::span/text()").get(),
                "ISSN": response.xpath("//label[text()='ISSN']/following-sibling::span/text()").get(),
                "CN": response.xpath("//label[text()='CN']/following-sibling::span/text()").get(),
                "出版地": response.xpath("//label[text()='出版地']/following-sibling::span/text()").get(),
                "语种": response.xpath("//label[text()='语种']/following-sibling::span/text()").get(),
                "开本": response.xpath("//label[text()='开本']/following-sibling::span/text()").get(),
                "邮发代号": response.xpath("//label[text()='邮发代号']/following-sibling::span/text()").get(),
                "创刊时间": response.xpath("//label[text()='创刊时间']/following-sibling::span/text()").get(),
                "专辑名称": response.xpath("//span[@id='jiName']/text()").get(),
                "专题名称": response.xpath("//span[@id='tiName']/text()").get(),
                "出版文献量": response.xpath("//label[text()='出版文献量']/following-sibling::span/text()").get(),
                "总下载次数": response.xpath("//label[text()='总下载次数']/following-sibling::span/text()").get(),
                "总被引次数": response.xpath("//label[text()='总被引次数']/following-sibling::span/text()").get(),
                "复合影响因子": response.xpath("//label[contains(text(),'复合影响因子')]/following-sibling::span/text()").get(),
                "综合影响因子": response.xpath("//label[contains(text(),'综合影响因子')]/following-sibling::span/text()").get(),
                "code": response.url.split("/")[-2],
                "url": response.url.split("?")[0],
            }
