import pandas as pd
import datetime
from pprint import pprint

class ReportGenerator:

    def __init__(self, date):
        self.date = date
        self.commissions = pd.read_csv('data/commissions.csv', parse_dates=['date'], index_col=['date', 'vendor_id'])
        self.order_lines = pd.read_csv('data/order_lines.csv', index_col=['order_id', 'product_id'])
        self.orders = pd.read_csv('data/orders.csv', parse_dates=['created_at'], index_col='id')
        self.products = pd.read_csv('data/products.csv', index_col='id')
        self.promotions = pd.read_csv('data/promotions.csv', index_col='id')
        self.product_promotions = pd.read_csv(
            'data/product_promotions.csv',
            parse_dates=['date'],
            index_col=['date', 'product_id'])
        self.report = {}

    def combined_order_data(self):
        order_products = self.order_lines.merge(self.orders, left_on='order_id', right_index=True)\
            .merge(self.products, left_on='product_id', right_index=True)

        # 1. Total number of items sold on a day
        day_orders = order_products[order_products['created_at'].dt.strftime('%Y-%m-%d') == self.date].sort_values(
            by=['order_id', 'product_id'])
        self.report['items'] = day_orders['quantity'].sum().item()



