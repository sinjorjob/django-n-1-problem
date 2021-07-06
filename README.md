# Reproducing and solving the Django N+1 problem

Test the effect of prefetch_related and select_related by reproducing the N+1 problem with the following kakeibo and category tables

```python
class Category(models.Model):

	category_name = models.CharField(max_length=255,unique=True, verbose_name="カテゴリ")
		
	def __str__(self):
		return self.category_name
	

class Kakeibo(models.Model):

    category = models.ForeignKey(Category, verbose_name ="カテゴリ", on_delete = models.PROTECT)
    amount = models.IntegerField(verbose_name = "金額", help_text = "単位は日本円")
    date = models.DateField(verbose_name = "日付",default=datetime.now)
    memo = models.CharField(verbose_name = "メモ", max_length=500)

    def __str__(self):
        return self.memo
```

## generate test data

Generate 100,000 data using the following procedure.

```console
python create_demo_data.py
```

## execute test case(1～5)

```console
python measure_processing_time.py
```

## case1

Looping with reference to own table only

```python
    item_list =[]
    kakeibo_items = Kakeibo.objects.all()
    for item in kakeibo_items:
        item_list.append(item.memo)
```

## case2

Looping over external table references

```python
    item_list =[]
    kakeibo_items = Kakeibo.objects.all()
    for item in kakeibo_items:
        item_list.append([item.category, item.memo])
```

## case3

Improved looping of external table references using select_related

```python
    item_list =[]
    kakeibo_items = Kakeibo.objects.all().select_related('category') #fixed
    for item in kakeibo_items:
        item_list.append([item.category, item.memo])
```


## case4

Simple reverse reference

```python
    item_list =[]
    for category in Category.objects.all():
        item_list.append([category.category_name, Category.objects.get(pk=category.pk).kakeibo_set.all().count()])
```
## case5

Reverse reference using prefetch_related

```python
    item_list =[]
    for category in Category.objects.all().prefetch_related("kakeibo_set"):
        item_list.append([category.category_name, category.kakeibo_set.all().count()])
```

## Execution result

```console
計測開始
Function : case1
実行されたQuery数 : 1
実行時間 : 1.60s
...django-n+1-problem\venv\djang-n+1-problem\lib\site-packages\django\db\backends\base\base.py:159: UserWarning: Limit for query logging exceeded, only the last 9000 queries will be returned.
  warnings.warn(
Function : case2
実行されたQuery数 : 9000
実行時間 : 60.77s
Function : case3
実行されたQuery数 : 1
実行時間 : 2.33s
Function : case4
実行されたQuery数 : 13
実行時間 : 0.02s
Function : case5
実行されたQuery数 : 2
実行時間 : 1.81s
計測終了
```