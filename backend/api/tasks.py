from __future__ import absolute_import, unicode_literals
import requests
import json
from backend.celery import app
from api.models import Product, Category, Company


def update_products(comp_id: int, company: object):

    response = requests.get(
        f'http://otp.spider.ru/test/companies/{str(comp_id)}/products/')

    if response.status_code == 200:
        new_products = json.loads(response.text)
        current_products = list(Product.objects.filter(company=company))
        for prod in new_products:
            prod_id = prod.get('id')
            prod_name = prod.get('name')
            prod_desc = prod.get('description')
            prod_cat = prod.get('category').get('name')
            category, _ = Category.objects.get_or_create(title=prod_cat)
            product = Product.objects.filter(ext_id=prod_id).first()
            if not product:
                Product.objects.create(title=prod_name,
                                       description=prod_desc,
                                       category=category,
                                       company=company,
                                       ext_id=prod_id)
            else:
                product.title = prod_name
                product.description = prod_desc
                product.category = category
                product.save()
                current_products.remove(product)

        for untrue_product in current_products:
            untrue_product.delete()


@app.task
def update_companies():

    response = requests.get('http://otp.spider.ru/test/companies/')

    if response.status_code == 200:
        companies = json.loads(response.text)
        for comp in companies:
            comp_id = comp.get('id')
            comp_name = comp.get('name')
            comp_desc = comp.get('description')
            company = Company.objects.filter(ext_id=comp_id).first()
            if not company:
                company = Company.objects.create(name=comp_name,
                                                 description=comp_desc,
                                                 ext_id=comp_id)
            else:
                company.name = comp_name
                company.description = comp_desc
                company.save()

            update_products(comp_id, company)
