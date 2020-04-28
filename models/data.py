import pandas as pd


class ReportGenerator:

    """
    Takes in date in format 'YYYY-MM-DD' and generates the report attribute to be returned in response.
    This assumes all data files are present in the data folder
    """

    def __init__(self, date, folder='data'):
        self.date = date
        self.commissions = pd.read_csv(f'{folder}/commissions.csv', parse_dates=['date'], index_col=['date', 'vendor_id'])
        self.order_lines = pd.read_csv(f'{folder}/order_lines.csv', index_col=['order_id', 'product_id'])
        self.orders = pd.read_csv(f'{folder}/orders.csv', parse_dates=['created_at'], index_col='id')
        self.products = pd.read_csv(f'{folder}/products.csv', index_col='id')
        self.promotions = pd.read_csv(f'{folder}/promotions.csv', index_col='id')
        self.product_promotions = pd.read_csv(
            f'{folder}/product_promotions.csv',
            parse_dates=['date'],
            index_col=['date', 'product_id'])
        self.report = {}

    def calculate_metrics(self):

        """
        Analysis of data to generate the report metrics
        """

        order_products = self.order_lines.merge(self.orders, left_on='order_id', right_index=True)\
            .merge(self.products, left_on='product_id', right_index=True)

        # 1. Total number of items sold on a day
        day_orders = order_products[order_products['created_at'].dt.strftime('%Y-%m-%d') == self.date].sort_values(
            by=['order_id', 'product_id'])
        self.report['items'] = day_orders['quantity'].sum().item()

        # 2. Total number of customers
        unique_customers = pd.unique(day_orders['customer_id'])
        self.report['customers'] = len(unique_customers)

        # 3. Total amount of discount given on day
        day_orders['discount_value'] = day_orders['full_price_amount'] - day_orders['discounted_amount']
        total_discount = day_orders['discount_value'].sum()
        self.report['total_discount_amount'] = round(total_discount.item(), 2)

        # 4. Average discount rate applied to items sold
        average_discount = day_orders.loc[day_orders['discount_rate'] > 0, 'discount_rate'].mean()
        self.report['discount_rate_avg'] = round(average_discount, 2)

        # 5. Average order total for that day
        total_day_revenue = day_orders['total_amount'].sum()
        num_orders_for_day = len(day_orders.index.get_level_values(0).unique())
        print('Total orders: {total_day_revenue}, Num orders: {num_orders_for_day}')
        average_day_revenue = total_day_revenue / num_orders_for_day
        self.report['order_total_average'] = round(average_day_revenue, 2)

        # 6. Total amount of commissions for that day
        day_prod_promos = self.product_promotions[self.product_promotions.index.get_level_values('date') == self.date].reset_index()
        day_commissions = self.commissions[self.commissions.index.get_level_values('date') == self.date].reset_index()

        day_orders_commissions = day_orders.reset_index()
        day_orders_commissions = day_orders_commissions.merge(day_commissions, how='left', left_on='vendor_id',
                                                              right_on='vendor_id', suffixes=('', '_commissions'))
        day_orders_commissions['commission_amount'] = day_orders_commissions['total_amount'] \
                                                        * day_orders_commissions['rate']
        total_commissions_for_day = day_orders_commissions['commission_amount'].sum()
        self.report['commissions'] = {}

        self.report['commissions']['total'] = round(total_commissions_for_day, 2)

        # 7. Average amount of commission per order
        average_commissions = day_orders_commissions[['order_id', 'commission_amount']].groupby(
            'order_id').sum().mean()
        self.report['commissions']['order_average'] = round(average_commissions.item(), 2)

        # 8. Total amount of commissions earned per promotion
        commissions_per_promo = day_orders_commissions.merge(day_prod_promos, how='inner', left_on='product_id',
                                                             right_on='product_id', suffixes=('', '_promos'))
        commissions_per_promo = commissions_per_promo[['commission_amount', 'promotion_id', ]].groupby('promotion_id').sum()

        commissions_per_promo.index = commissions_per_promo.index.map(str)
        commissions_dict = commissions_per_promo.to_dict('dict')['commission_amount']
        commissions_dict = {k: round(v, 2) for k, v in commissions_dict.items()}
        self.report['commissions']['promotions'] = commissions_dict

        return

