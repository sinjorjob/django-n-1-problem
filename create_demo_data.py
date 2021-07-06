import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

import random
from faker import Factory
from kakeibo.models import Category, Kakeibo


fakegen = Factory.create('ja_JP')
categories = ['食費', '交通費', '書籍', '雑費', '電話代', '各種アプリ利用費']


def add_category():
    # カテゴリを自動生成する関数
    category = Category.objects.get_or_create(category_name=random.choice(categories))[0]

    return category


def auto_gen_demo_data(num):

    for _ in range(num):
        # カテゴリ名の作成
        category_name = add_category()

        # ダミーデータの作成
        date = fakegen.date()
        amount = fakegen.port_number()
        memo = fakegen.text(max_nb_chars=20)

        # 新しい家計簿ダミーデータの作成
        kakeibo_data = Kakeibo.objects.get_or_create(
                category=category_name, date=date, amount=amount, memo=memo)

# コードの実行
if __name__ == "__main__":
    print('Start create demo data ...')
    auto_gen_demo_data(100000)
    print('Demo data generation is complete.')
