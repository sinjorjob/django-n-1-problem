from django.db import models
from datetime import datetime

class Category(models.Model):

	# カテゴリー名の定義
	category_name = models.CharField(max_length=255,unique=True, verbose_name="カテゴリ")
		
	# 管理サイトの表示名を読み込む定義
	def __str__(self):
		return self.category_name
	

class Kakeibo(models.Model):

	# 家計簿レコード列の定義	
    category = models.ForeignKey(Category, verbose_name ="カテゴリ", on_delete = models.PROTECT)
    amount = models.IntegerField(verbose_name = "金額", help_text = "単位は日本円")
    date = models.DateField(verbose_name = "日付",default=datetime.now)
    memo = models.CharField(verbose_name = "メモ", max_length=500)

	# 管理サイトの表示名を読み込む定義
    def __str__(self):
        return self.memo
