import csv
from datetime import datetime

BASE_DIR = 'results'


class PepParsePipeline:
    def open_spider(self, spider):
        self.count = 0
        self.dict_status_pep = dict()

    def process_item(self, item, spider):
        self.count += 1
        self.dict_status_pep[
            item['status']] = self.dict_status_pep.get(item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        results = [('Статус', 'Количество')]
        results.extend(list(self.dict_status_pep.items()))
        results.append(('Total', self.count))
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(
            f'{BASE_DIR}/status_summary_{date}.csv', 'w',
             encoding='utf-8') as file:
            writer = csv.writer(file, dialect='unix')
            writer.writerows(results)
