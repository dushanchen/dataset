from django.core.management import BaseCommand

from apis.models import *

import csv
import xlrd


class Command(BaseCommand):

    def handle(self, **kwargs):
        # args = ('categery', 'categery', 'name', 'leader', 'address', 'mail', 'phone')
        # self.read_csv('/Users/dsc/Downloads/粮食批发市场信息1.csv', Lungis, *args)

        # args = ('categery', 'categery', 'name', 'address', 'mail', 'phone')
        # self.read_csv('/Users/dsc/Downloads/粮食批发市场信息2.csv', Lungis, *args)

        # args = ('categery', 'categery', 'name', 'leader', 'address', 'mail', 'phone')
        # self.read_excel('/Users/dsc/Downloads/粮食批发市场信息3.xls', Lungis, *args)

        # args = ('categery', 'categery', 'name', 'address', 'mail', 'phone')
        # self.read_excel('/Users/dsc/Downloads/粮食批发市场信息4.xls', Lungis, *args)

        # args = ('categery','address', 'name')
        # self.read_csv('/Users/dsc/Downloads/上海猪肉流通安全信息追溯流通节点基本信息.csv', PorkMarket, *args)

        # args = ('number', 'name')
        # self.read_csv('/Users/dsc/Downloads/上海猪肉流通安全信息追溯品牌信息.csv', PorkBrand, *args)

        # args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        # self.read_excel('/Users/dsc/Downloads/食品抽样1.xls', FoodSample, *args)
        args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        self.read_excel('/Users/dsc/Downloads/食品抽样2.xls', FoodSample, *args)
        args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        self.read_excel('/Users/dsc/Downloads/食品抽样3.xls', FoodSample, *args)
        args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        self.read_excel('/Users/dsc/Downloads/食品抽样4.xls', FoodSample, *args)
        args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        self.read_excel('/Users/dsc/Downloads/食品抽样5.xls', FoodSample, *args)
        args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        self.read_excel('/Users/dsc/Downloads/食品抽样6.xls', FoodSample, *args)
        args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        self.read_excel('/Users/dsc/Downloads/食品抽样7.xls', FoodSample, *args)
        args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        self.read_excel('/Users/dsc/Downloads/食品抽样8.xls', FoodSample, *args)
        args = ('producer', 'address', 'seller', 'categery', 'food_name', 'volume', 'product_date', 'organization', 'detail')
        self.read_excel('/Users/dsc/Downloads/食品抽样9.xls', FoodSample, *args)


    def insert_by_key(self):
        pass


    def insert_by_index(self, rows, model, *args):
        records = []
        
        for line in rows:
            
            a = model()

            blank = True
            try:
                for i, v in enumerate(args):
                    if str(line[i]).strip():
                        setattr(a, v, line[i])
                        blank = False
            except Exception as e:
                print(e)

            if not blank:
                records.append(a)

            if(len(records) == 200):
                model.objects.bulk_create(records)
                records = []

        model.objects.bulk_create(records)


    def read_csv(self, path, model, *args):

        try:
            with open(path, 'r') as file:
                rows = csv.reader(file)
                
                self.insert_by_index(rows, model, *args)

        except UnicodeDecodeError:
            with open(path, 'r', encoding="GB2312") as file:
                rows = csv.reader(file)
                
                self.insert_by_index(rows, model, *args)

    def read_excel(self, path, model, *args):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        rows = []
        for i in range(sheet.nrows):
            rows.append(sheet.row_values(i))
        print(rows[1])
        self.insert_by_index(rows[1:], model, *args)
 




     