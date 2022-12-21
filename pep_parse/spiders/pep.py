import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        pep_links = response.css("section#numerical-index a::attr(href)")
        for pep in pep_links:
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_name = response.css("h1.page-title::text").get()
        data = {
            "number": pep_name.split(" ")[1],
            "name": pep_name.split(" – ")[1],
            "status": response.css(
                'dt:contains("Status") + dd abbr::text').get(),
        }
        yield PepParseItem(data)
