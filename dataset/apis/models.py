from django.db import models

# Create your models here.



class Lungis(models.Model):
	class Meta:
		verbose_name = '粮食批发市场'

	categery = models.CharField(max_length=200, null=True, blank=True, verbose_name='区/县')
	name = models.CharField(max_length=200, null=True, blank=True, verbose_name='市场名称')
	address = models.CharField(max_length=200, null=True, blank=True, verbose_name='地址')
	leader = models.CharField(max_length=200, null=True, blank=True, verbose_name='负责人')
	mail = models.CharField(max_length=200, null=True, blank=True, verbose_name='邮编')
	phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='电话')

	def __str__(self):
		return self.name


class PorkBrand(models.Model):
	class Meta:
		verbose_name = '上海猪肉流通安全信息追溯品牌信息'

	name = models.CharField(max_length=200, null=True, blank=True, verbose_name='品牌名称')
	number = models.CharField(max_length=200, null=True, blank=True, verbose_name='编码')

	def __str__(self):
		return self.name


class PorkMarket(models.Model):
	class Meta:
		verbose_name = '上海猪肉流通安全信息追溯流通节点基本信息'
	
	categery = models.CharField(max_length=200, null=True, blank=True, verbose_name='区/县')
	address = models.CharField(max_length=200, null=True, blank=True, verbose_name='地址')
	name = models.CharField(max_length=200, null=True, blank=True, verbose_name='品牌名称')


	def __str__(self):
		return self.name


class FoodSample(models.Model):
	class Meta:
		verbose_name = '食品抽样'
	
	producer = models.CharField(max_length=200, null=True, blank=True, verbose_name='标称生产企业名称')
	seller = models.CharField(max_length=200, null=True, blank=True, verbose_name='销售单位地址')
	categery = models.CharField(max_length=200, null=True, blank=True, verbose_name='被抽样单位所在区域')
	address = models.CharField(max_length=200, null=True, blank=True, verbose_name='生产单位地址')
	food_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='食品名称')
	volume = models.CharField(max_length=200, null=True, blank=True, verbose_name='规格型号')
	product_date = models.CharField(max_length=200, null=True, blank=True, verbose_name='生产日期')
	organization = models.CharField(max_length=200, null=True, blank=True, verbose_name='检验机构')
	detail = models.CharField(max_length=200, null=True, blank=True, verbose_name='备注')


	def __str__(self):
		if self.seller and self.food_name:
			return self.seller + '  '  + self.food_name
		return self.food_name	


