import time
import json
import hashlib
import pymongo
import requests


mongo = pymongo.MongoClient('127.0.0.1:27017')
schema = mongo['shanghai']['schema']
headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:68.0) Gecko/20100101 Firefox/68.0'
    }

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

@insert_schema(item='结婚登记预约机构',
    filter={'orgid': '区县id'},
    fields=['orgName', 'isSw', 'boroughName', 'orgAddress', 'amStart', 'amEnd', 'pmStart', 'pmEnd', 'orgBus', 'yyTel', 'rgTel', 'orgSpecial', 'orgRemark'],
    names=['机构名称', '是否涉外（是、否）', '机构所属区县名称', '机构地址', '上午接待开始时间', '上午接待结束时间', '下午接待开始时间', '下午接待结束时间', '乘车路线', '语音咨询电话', '人工咨询电话', '特色服务描述', '备注']
    )
def jhyydjjg(orgid=''):
    '''
        结婚登记预约机构信息的接口

        000310999 上海市婚姻（收养）登记中心
        1010     黄浦区婚姻（收养）登记处
        1040     徐汇区婚姻收养登记中心
        1050     上海市长宁区婚姻（收养）登记中心
        1060     上海市静安区婚姻（收养）登记中心
        1070     上海市普陀区婚姻收养登记中心
        1080     闸北区婚姻登记处
        1090     上海市虹口区民政局
        1100     杨浦区婚姻（收养）登记中心
        1120     闵行区婚姻（收养）登记中心
        1130     宝山区婚姻登记管理所
        1140     上海市嘉定区民政局
        115A     上海市浦东新区婚姻管理所（合欢路）
        1260     上海市奉贤区婚姻（收养）登记中心
        1270     松江区民政局婚姻登记处
        128A     金山区婚姻管理所
        1290     上海市青浦区婚姻登记管理中心
        1300     崇明县婚姻收养登记中心
    '''
    #     ??????????  orgid 无用,返回值都一样, 只有一条数据
    
    url = 'http://marry.mzj.sh.gov.cn/minz-app-front/f/getOrgInfo?orgid=%s' % orgid
    result = requests.get(url, headers=headers).text
    records = []
    if result:
        print(result)
        record = json.loads(result)
        # for i,v in enumerate(records):
        if 'orgName' in record:
            record['_id'] = hash(record)
            record['create_time'] = int(time.time())
            records.append(record)

    batch_insert(records, 'jhyydjjg')
    return 


@insert_schema(item='上海市研发公共服务平台两类平台信息',
    fields=['platformSeries', 'platformName', 'leadUnit', 'unitNature', 'chargeDept', 'district', 'serviceIndustry', 'industryType', 'serviceTypes', 'majorServiceType', 'keyDomain', 'memberUnit', 'buildDateFormatted', 'passDateFormatted', 'authorizeDateFormatted', 'assessNumber', 'lastEvaluateDateFormatted', 'lastEvaluateGrade', 'platformIntro', 'orgnName', 'address', 'chargePerson', 'chargePost', 'chargeTitle', 'chargeTel', 'chargeMobile', 'chargeEmail', 'contactPerson', 'contactDeptPost', 'contactFax', 'contactTel', 'contactMobile', 'contactEmail', 'servicePerson', 'serviceDeptPost', 'serviceTel', 'serviceMobile', 'serviceEmail', 'hotlineTel', 'website'],
    names=['平台系列', '平台名称', '平台依托单位', '单位性质', '上级主管部门', '注册区县', '主要服务产业', '七大战略性新兴产业', '服务类别', '主要服务类别', '平台定位及主要服务特点', '主要参建单位', '开始建设年月', '建设项目验收年月', '评定授牌年月', '评估次数', '上次评估年月', '上次评估成绩', '平台简介', '平台日常管理服务机构名称', '平台日常管理服务机构地址', '平台负责人姓名', '平台负责人职务', '平台负责人职称', '平台负责人电话', '平台负责人手机', '平台负责人邮箱', '平台联系人姓名', '平台联系人部门/职务', '平台联系人传真', '平台联系人电话', '平台联系人手机', '平台联系人邮箱', '平台服务联系人姓名', '平台服务联系人部门/职务', '平台服务联系人电话', '平台服务联系人手机', '平台服务联系人邮箱', '服务热线', '平台网址']
    )
def yfggfwptxx():
    '''
        上海市研发公共服务平台两类平台信息
    '''

    url = 'http://api.sstir.cn/platform?username=test&password=test&size=20&number=%s'

    try:
        number = 1
        while True: 
            rq = url % number
            number += 1
            result = requests.get(rq)
            if result and result.text:
                result = json.loads(result.text)

                if 'content' in result and result['content']:
                    res = result['content']
                    for i, v in enumerate(res):
                        res[i]['_id'] = hash(res[i])
                        res[i]['create_time'] = int(time.time())
                    batch_insert(res, 'yfggfwptxx')
                    continue
            break
    except Exception as e:
        print(e)
    return 


@insert_schema(item='上海市研发公共服务平台大型仪器信息',
        fields=['name', 'engName', 'mergeStatus', 'ownerName', 'belongsFacilities', 'belongsCenter', 'belongsItem', 'yqsize', 'newcode', 'propMngNum', 'assetCode', 'equipSource', 'instruProp', 'nation', 'factory', 'instrSupervise', 'photoid', 'accessory', 'insideDepart', 'instruArea', 'location', 'relName', 'relEmail', 'relAddress', 'relNumber', 'relFax', 'relPost', 'bDate', 'useDate', 'centralFinancialAid', 'localFinancialAid', 'areaFinancialAid', 'selfFinancialAid', 'unitSelfAid', 'otherHelpAid', 'tRmb', 'useStatus', 'equipType'],
        names=['仪器中文全称', '仪器英文全称', '仪器状态', '所有权单位', '所属大型科学装置', '所属仪器中心', '所属服务单元', '规格型号', '仪器分类编码', '单位资产管理号', '固定资产分类代码', '仪器设备来源', '进口/国产', '生产国别（地区）', '制造商', '海关监管情况', '图片信息', '主要附件', '所属单位内部门', '仪器安置所在区县', '仪器安放地址', '仪器设施联系人', '仪器设施联系人电子邮箱', '仪器设施联系人通讯地址', '仪器设施联系人联系电话', '仪器设施联系人传真', '仪器设施联系人邮政编码', '购置日期', '启用日期', '经费来源-政府拨款-中央财政', '经费来源-政府拨款-上海市财政', '经费来源-政府拨款-区县财政', '经费来源-联合国、国际组织或者外国政府援助', '经费来源-单位自有资金', '经费来源-其他', '仪器原值', '运行状态', '仪器设备类别'] 
    )
def yfggfwdxyqxx():
    ''' 
        上海市研发公共服务平台大型仪器信息
    '''
    url = 'http://api.sstir.cn/instrument?username=test&password=test&size=20&number=%s'

    try:
        j = 1
        while True:
            req = url % j
            j += 1
            result = requests.get(req)
            print(j)
            if result and result.text:
                result = json.loads(result.text)

                if 'content' in result and result['content']:
                    records = result['content']
                    for i, v in enumerate(records):
                        records[i]['_id'] = hash(records[i])
                        records[i]['create_time'] = int(time.time())
                    
                    batch_insert(records, 'yfggfwdxyqxx')
                    continue
            break
    except Exception as e:
            print(e)


@insert_schema(item='上海市研发公共服务平台重点实验室信息',
    fields=['syjdName', 'syjdSeriers', 'syjdKind', 'syjdType', 'subjectDomain', 'syjdDomain', 'otherPlaceBase', 'syjdOrient', 'syjdAdmit', 'syjdPermit', 'startbuildTime', 'endbuildTime', 'syjdEvaluate', 'evaluateTime', 'syjdResult', 'syjdArea', 'syjdLinkman', 'syjdLinkphone', 'syjdLinkfax', 'syjdWww', 'syjdEmail', 'address', 'syjdPostcode', 'chargeName', 'chargeBirth', 'chargeMobile', 'chargeFunction', 'chargePosition', 'chargeEmail', 'scienceName', 'scienceBirth', 'scienceFunction', 'sciencePosition', 'syjdRootunit', 'rootunitKind', 'rootunitFlag', 'rootunitRegDistrict'],
    names=['全称', '系列', '性质', '类别', '学科领域', '涉及领域', '是否其他省部级以上基地', '定位', '实验室认可', '建设批准部门', '开始建设年月', '通过验收年月', '已评估次数', '上次评估年月', '上次评估成绩', '面积（平方米）', '联系人姓名', '联系人电话', '联系人传真', '联系人网址', '联系人电子邮箱', '联系人地址', '联系人邮编', '负责人姓名', '负责人出生年月', '负责人联系电话', '负责人职称', '负责人职务', '负责人电子邮箱', '实验室学术委员会负责人姓名', '实验室学术委员会负责人出生年月', '实验室学术委员会负责人职称', '实验室学术委员会负责人职务', '依托单位情况名称', '依托单位情况性质', '研发公共服务平台加盟单位', '注册地所在区县']
)
def yfggfwzdsysxx():
    ''' 
        上海市研发公共服务平台重点实验室信息
    '''
    url = 'http://api.sstir.cn/laboratory?username=test&password=test&size=20&number=%s'

    try:
        j = 1
        while True:
            req = url % j
            j += 1
            result = requests.get(req)
            print(j)
            if result and result.text:
                result = json.loads(result.text)

                if 'content' in result and result['content']:
                    records = result['content']
                    for i, v in enumerate(records):
                        records[i]['_id'] = hash(records[i])
                        records[i]['create_time'] = int(time.time())
                    
                    batch_insert(records, 'yfggfwzdsysxx')
                    continue
            break
    except Exception as e:
            print(e)      


@insert_schema(item=' 上海市研发公共服务平台工程技术中心信息',
    fields=['syjdName', 'syjdWww', 'ifSgstMember', 'syjdArea', 'totalAsset', 'startbuildTime', 'endbuildTime', 'evaluateTime', 'syjdResult', 'subjectDomain', 'syjdIndustry', 'chKeywords', 'enKeywords', 'orgForm', 'address', 'syjdLinkman', 'syjdLinkphone', 'ext1', 'syjdEmail', 'syjdLinkfax', 'syjdPostcode', 'chargeName', 'chargeBirth', 'chargeSex', 'chargeEntryTime', 'chargeFunction', 'chargePosition', 'chargeStudy', 'chargeDegree', 'otherPlaceBase', 'majorSupportInfoName', 'majorSupportInfoRegDistrict', 'majorSupportInfoOrgCode', 'majorSupportInfoEmail', 'majorSupportInfoRegAddress', 'majorSupportInfoPostcode', 'majorSupportInfoLawName', 'majorSupportInfoLawSex', 'majorSupportInfoLawDegree', 'majorSupportInfoLawServiceTime', 'majorSupportInfoLawTel', 'majorSupportInfoSciLinkMan', 'majorSupportInfoSciLinkEmail', 'majorSupportInfoFincLinkMan', 'majorSupportInfoFincLinkEmail', 'majorSupportInfoUnitBelong', 'majorSupportInfoRegType', 'majorSupportInfoWorkerNum', 'majorSupportInfoJuniorUpper', 'majorSupportInfoDevNum', 'majorSupportInfoManagerNum', 'majorSupportInfoManagerUniverUpper', 'majorSupportInfoCharacter', 'majorSupportInfoComments'],
    names=['全称', '网址', '研发平台加盟加盟机构', '面积（平方米）', '总资产（万元）', '开始建设年月', '规定的验收年月', '上次评估年月', '上次评估成绩', '所属学科', '所属产业', '中文技术关键词', '英文技术关键词', '依托单位情况组织形式', '通讯地址', '联系人', '办公电话', '手机', '电子邮箱', '传真', '邮编', '工程中心主任姓名', '工程中心主任出生年月', '工程中心主任性别', '工程中心主任聘任日期', '工程中心主任职称', '工程中心主任职务', '工程中心主任学科专长', '工程中心主任最后学位', '是否同时是其他省部级及以上的研发基地', '主要依托单位名称', '主要依托单位注册区县', '主要依托单位单位代码', '主要依托单位电子邮件', '主要依托单位注册地址', '主要依托单位邮编', '主要依托单位法人姓名', '主要依托单位法人性别', '主要依托单位法人最高学历', '主要依托单位法人现任职时间', '主要依托单位法人电话', '主要依托单位科研部门联系人', '主要依托单位电子邮件', '主要依托单位财务部门联系人', '主要依托单位电子邮件', '主要依托单位单位隶属', '主要依托单位注册登记类型', '主要依托单位单位职工总数', '主要依托单位大专以上', '主要依托单位研究开发', '主要依托单位单位中层以上管理人员总数', '主要依托单位其中大学本科以上人员数', '主要依托单位企业特性', '主要依托单位单位需要说明的问题']
)
def yfggfwgcjszxxx():
    ''' 
        上海市研发公共服务平台重点实验室信息
    '''
    url = 'http://api.sstir.cn/engineering?username=test&password=test&size=20&number=%s'

    try:
        j = 1
        while True:
            req = url % j
            j += 1
            result = requests.get(req)
            print(j)
            if result and result.text:
                result = json.loads(result.text)

                if 'content' in result and result['content']:
                    records = result['content']
                    for i, v in enumerate(records):
                        records[i]['_id'] = hash(records[i])
                        records[i]['create_time'] = int(time.time())
                    
                    batch_insert(records, 'yfggfwgcjszxxx')
                    continue
            break
    except Exception as e:
            print(e) 


@insert_schema(item='技术进出口供需企业',
    fields=['Account', 'CompanyName', 'Email', 'Contact', 'Phone', 'Mobile', 'CNExhibitionName', 'UserName', 'CompanyNameE', 'Address', 'CName', 'Provinces', 'City', 'Zip', 'ManagingDirector', 'Fax', 'Type', 'Website', 'Product', 'BoothNo', 'EAres', 'ToIDCard', 'Exhibits', 'CategoryName', 'Bookingbooth', 'State', 'WhetherExhibitors', 'Massage'],
    names=['账号名', '公司名', '邮箱', '联系人', '电话', '手机号', '所属展会', '所属业务员', '单位英文名称', '单位地址', '国家', '省', '市', '邮编', '董事长或经理', '传真', '职务', '网站', '展品名称', '展位号', '参展面积', '参展证数量', '展品范围', '公司性质', '预订展位', '1表示成功，2表示失败', 'True：本届参展，2不参展', '说明']
    )
def jsjckgxqy(QueryWhere=''):
    '''技术进出口供需企业'''

    url = 'http://csitf.echaokj.cn/API/Exhibitorsto/GetBusinessman'
    params =  {'TokenName':'EChaokj'}
    if QueryWhere:
        params['QueryWhere'] = QueryWhere
    try:
        result = requests.post(url, data=params)
        if result and result.text:
            result = json.loads(result.text)

            if 'LUserModel' in result:
                records = result['LUserModel']
                for i, v in enumerate(records):
                    records[i]['_id'] = hash(records[i])
                    records[i]['create_time'] = int(time.time())
                print(len(records))
            
                batch_insert(records, 'jsjckgxqy')
                 
    except Exception as e:
            print(e) 


if __name__ == '__main__':

    # jhyydjjg()
    # yfggfwptxx()
    # yfggfwdxyqxx()
    # yfggfwgcjszxxx()
    jsjckgxqy()








