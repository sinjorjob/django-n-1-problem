import os
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from kakeibo.models import Category, Kakeibo
from django.db import connection, reset_queries
import time
import functools


def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        reset_queries()
        
        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"実行されたQuery数 : {end_queries - start_queries}")
        print(f"実行時間 : {(end - start):.2f}s")
        return result

    return inner_func

@query_debugger
def case1():
    item_list =[]
    kakeibo_items = Kakeibo.objects.all()
    for item in kakeibo_items:
        item_list.append(item.memo)

@query_debugger
def case2():
    item_list =[]
    kakeibo_items = Kakeibo.objects.all()
    for item in kakeibo_items:
        item_list.append([item.category, item.memo])

@query_debugger
def case3():
    item_list =[]
    kakeibo_items = Kakeibo.objects.all().select_related('category') #改修箇所
    for item in kakeibo_items:
        item_list.append([item.category, item.memo])

@query_debugger
def case4():
    item_list =[]
    for category in Category.objects.all():
        item_list.append([category.category_name, Category.objects.get(pk=category.pk).kakeibo_set.all().count()])
        

@query_debugger
def case5():
    item_list =[]
    for category in Category.objects.all().prefetch_related("kakeibo_set"):
        item_list.append([category.category_name, category.kakeibo_set.all().count()])


# コードの実行
if __name__ == "__main__":
    print('計測開始')
    case1()
    case2()
    case3() 
    case4()
    case5()
    print('計測終了')
