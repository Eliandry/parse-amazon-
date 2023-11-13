# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter




class CsvExportPipeline:
    def __init__(self):
        # Открывает файл на запись и создает объект csv.writer
        self.file = open('output123.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

    def open_spider(self, spider):
        # Записывает заголовок файла CSV
        self.writer.writerow(['star', 'comment'])

    def close_spider(self, spider):
        # Закрывает файл при завершении работы паука
        self.file.close()

    def process_item(self, item, spider):
        # Записывает строки в файл CSV, если значение star не равно 5
        self.writer.writerow([item['star'], item['comment']])
        return item
