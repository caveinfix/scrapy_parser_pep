import csv
from collections import defaultdict
from datetime import datetime as dt

from scrapy.exceptions import DropItem

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.all_status = defaultdict(int)

    def process_item(self, item, spider):
        if "status" not in item:
            raise DropItem("Статус отсутствует!")
        self.all_status[item["status"]] += 1
        return item

    def close_spider(self, spider):
        date = dt.now().strftime("%Y-%m-%dT%H-%M-%S")
        filename = BASE_DIR / "results" / f"status_summary_{date}.csv"
        with open(filename, "w", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Статус", "Количество"])
            w.writerows(self.all_status.items())
            w.writerow(["Total", sum(self.all_status.values())])
