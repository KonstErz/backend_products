from __future__ import absolute_import, unicode_literals
import requests
import json
from backend.celery import app
from api.models import Product, Category, Company


def update_products(comp_id: str, company):

    response = requests.get(
        f'http://otp.spider.ru/test/companies/{comp_id}/products/')

    if response.status_code == 200:
        products = json.loads(response.text)
        for prod in products:
            prod_name = prod.get('name')
            prod_desc = prod.get('description')
            prod_cat = prod.get('category').get('name')
            category, _ = Category.objects.get_or_create(title=prod_cat)
            product, _ = Product.objects.get_or_create(
                title=prod_name, company=company, category=category)
            product.update(description=prod_desc)


@app.task
def update_companies():
    response = requests.get('http://otp.spider.ru/test/companies/')

    if response.status_code == 200:
        companies = json.loads(response.text)
        for comp in companies:
            comp_id = str(comp.get('id'))
            comp_name = comp.get('name')
            comp_desc = comp.get('description')
            company = Company.objects.filter(name=comp_name).first()
            if company is None:
                company = Company.objects.create(name=comp_name,
                                                 description=comp_desc)
            else:
                company.update(description=comp_desc)

            update_products(comp_id, company)
