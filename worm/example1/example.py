import requests
from lxml import etree

#http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-1
class Dangdang(object):
    def __init__(self):
        self.header = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Cookie":"ddscreen=2; dest_area=country_id%3D9000%26province_id%3D111%26city_id%20%3D0%26district_id%3D0%26town_id%3D0; __permanent_id=20210505164819616363853155952382710; __visit_id=20210505164819619368706834681754458; __out_refer=; __trace_id=20210505164819621274593890361828304",
            "Host":"bang.dangdang.com",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }

    def get_dangdang(self, page):
        """send requests to obtain data"""
        url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-%s" % page
        #send requests
        response = requests.get(url = url, headers = self.header)
        if response:
            #HTML DATA concrete
            html = etree.HTML(response.text)
            items = html.xpath("//ul[@class='bang_list clearfix bang_list_mode']/li")
            return items

    def join_list(self, item):
        """handle list to string"""
        return "".join(item)

    def parse_item(self, items):
        """understand content"""
        #save data before putting into database 
        result_list = []
        for item in items:
            title = item.xpath(".//div[@class='name']/a/text()")
            author = item.xpath(".//div[@class='publisher_info'][1]/a/text()")
            publisher = item.xpath(".//div[@class='publisher_info'][2]/a/text()")
            price_n = item.xpath(".//div[@class='price']/p[1]/span[1]/text()")
            price_r = item.xpath(".//div[@class='price']/p[1]/span[2]/text()")
            account = item.xpath(".//div[@class='price']/p[1]/span[3]/text()")
            price_e = item.xpath(".//div[@class='price']/p[2]/span/text()")

            result_list.append(
                {
                    "title": self.join_list(title),
                    "author": self.join_list(author),
                    "publisher": self.join_list(publisher),
                    "price_n": self.join_list(price_n),
                    "price_r": self.join_list(price_r),
                    "account": self.join_list(account),
                    "price_e": self.join_list(price_e)
                }
            )

        return result_list

def main():
    f = open('save_data.txt', 'w')
    import json
    d = Dangdang()
    for page in range(1, 26):
        items = d.get_dangdang(page = page)
        result = d.parse_item(items = items)
        json_sight = json.dumps(result)
        f.write(json_sight)
        f.write('\n')

    f.close()

if __name__ == '__main__':
    main()