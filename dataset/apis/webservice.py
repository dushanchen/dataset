import suds
import hashlib
import json
import time
import pymongo
from suds.client import Client

 
mongo = pymongo.MongoClient('127.0.0.1:27017')
schema = mongo['shanghai']['schema']
api = mongo['shanghai']['api']

def hash(dict_):
    return hashlib.sha256('&'.join([_+'='+str(dict_[_]) for _ in sorted(dict_)]).encode('utf8')).hexdigest()

def add_table(**kwargs):
    if not schema.find_one({'item': kwargs['item']}):
        schema.insert_one(kwargs)


def insert_schema(**dkwargs):
    def wrapper(func):
        def fun(*args, **kwargs):
            dkwargs['name'] = func.__name__
            add_table(**dkwargs)
            func(*args, **kwargs)
        return fun
    return wrapper

def batch_insert(records, table):
    
    if records:
        db = mongo['shanghai'][table]
      
        try:
           
            q = db.insert_many(records, ordered=False)
            
        except pymongo.errors.BulkWriteError as e:
            if e.details and 'writeErrors' in e.details:
                print('重复数据 %s条' % len(e.details['writeErrors']))
    
    return

def get(url, method, *kw):

    try:
        client = Client(url)
        if hasattr(client.service, method):
            func = getattr(client.service, method, '')

            if func:
                result = func(*kw)
                result = json.loads(result)
                return result 
        return []
    except Exception as e:
        print(url, '调用失败!!!!')
        return []

@insert_schema(item='行政处罚信息', 
    fields=['WSH', 'AJMC', 'FR', 'YJ','XDRSHXYM', 'JG', 'SXQ', 'SY', 'XZJG'],
    names=['处罚决定书文号', '处罚名称', '法定代表人', '处罚依据', '统一社会信用代码', '金额', '时间', '原因', '处罚机关']
)
def xzcf(cfwsh=''):
    '''
        行政处罚信息
        cfwsh, 行政许可决定书文号, 如果参数为空，则返回近30天的处罚数据。
        接口说明地址: http://data.sh.gov.cn/query!queryGdsInterfaceInfoById.action?dataId=2c90e4f357d7581401580965afcf022d
    '''
 
    url = 'http://sjkf.swj.sh.gov.cn:81/services/getXZCF?wsdl'
    result = get(url, 'getXZCF', cfwsh)
    if 'DB_DEFAULT_ROOT' in result:
        if result['DB_DEFAULT_ROOT']:
            if 'record' in result['DB_DEFAULT_ROOT']:
                print('行政处罚 %s条' % len(result['DB_DEFAULT_ROOT']['record']))
                records = result['DB_DEFAULT_ROOT']['record']

                for i, v in enumerate(records):
                    if 'WSH' in records[i]:
                        records[i]['WSH'] = str(records[i]['WSH'])
                    if 'XDRSHXYM' in records[i]:
                        records[i]['XDRSHXYM'] = str(records[i]['XDRSHXYM']) 
                    records[i]['_id'] = hash(records[i])
                    records[i]['create_time'] = int(time.time())
                 
                batch_insert(records, 'xzcf')

    return 


def get_xml():
    pass

def jlktjxx(month):
    url = 'http://180.168.211.29:8080/jxwjk/services/JXWJK?wsdl'

    c = Client(url)
    pass


if __name__ == '__main__':
    print('ss')
    xzcf()



