# -*- coding: utf-8 -*-

from genericpath import exists
import requests as req
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import argparse

class shopify_shipping_cost():
    def __init__(
        self,
        shopify_token=os.getenv("SECRET_TOKEN"),
        store_name=os.getenv("STORE_NAME"),
        shipping_csv_path='stamps.csv',
        order_csv_path='orders.csv',
        start_date=(datetime.now() - timedelta(days=6*30)).isoformat()
        ) -> None:
            if shopify_token: 
                self.shopify_token = shopify_token
                self.H = {"X-Shopify-Access-Token": shopify_token} 
            else: raise ValueError("Token Not Found, Enter One or Check Env")
            if store_name: self.store_name = store_name
            else: raise ValueError("Store Name Not Found")
            if os.path.exists(shipping_csv_path): self.shipping_csv_path = shipping_csv_path
            else: raise ValueError(f'Invalid Path: {shipping_csv_path}')
            if os.path.exists(order_csv_path): 
                self.order_csv_path = order_csv_path
                self.stamps = pd.read_csv(self.shipping_csv_path,index_col=None)
                self.orders = pd.read_csv(self.order_csv_path)
                self.stamps.dropna(subset=['Tracking #'],inplace=True)
            else: raise ValueError(f'Invalid Path: {order_csv_path}')
            if start_date: self.start_date=start_date
            else: raise ValueError('Invalid Start Date must be ISO Format')

    
    def get_orders(self):
        '''
            param data_range: Date in ISO 8601 format
        '''
        results = []

        count = 1
        # Fixing the URL construction
        response = req.get(f'https://{self.store_name}/admin/api/2023-07/orders.json?status=any&limit=250&created_at_min={self.start_date}', headers=self.H)

        if response.status_code != 200:
            print(f"Error fetching orders: {response.text}")
            return results

        res = response.json()

        while response is not None:

            print(f"Checking page {count}")
            for item in res.get("orders", []):
                order_id = item.get('id', "N/A")
                tracking_number = item['fulfillments'][0].get('tracking_number', "N/A") if item.get('fulfillments') else "none"
                results.append([order_id,tracking_number])


            count += 1

            # Fetch next page
            next_url = response.links.get("next", {}).get("url")
            if next_url:
                time.sleep(.5)
                response = req.get(next_url, headers=self.H)
                if response.status_code != 200:
                    print(f"Error fetching orders on page {count}: {response.text}")
                    break
                res = response.json()
            else:
                break

        return results

    def prepare_map(self):
        results = self.get_orders()
        for item in results:
            if item[1] == 'none':
                item[1] = None

        self.id2tracking = {id:tracking for id,tracking in results}
        self.tracking2id = {tracking:id for id,tracking in results}

    def run(self):
        self.prepare_map()
        ordersWtracking = self.orders.copy()
        ordersWtracking['Tracking #'] = ordersWtracking['Id'].map(self.id2tracking)
        filtered_orders = ordersWtracking.dropna(subset=['Tracking #'])
        filtered_orders = filtered_orders[filtered_orders['Tracking #'] != None]
        merged = pd.merge(filtered_orders,self.stamps,on='Tracking #',suffixes=['_order','_shipping'])
        r_data = merged[['Name','Tracking #','Amount Paid','Subtotal','Shipping']]
        r_data['Amount Paid'] = r_data['Amount Paid'].apply(lambda x : float(x[1:]))
        shipping_cost = r_data['Amount Paid'].sum()
        SubTotal = r_data['Subtotal'].sum()
        Shipping_Rev = r_data['Shipping'].sum()
        print(f'Shipping Cost: {int(shipping_cost)} Shipping Income: {int(Shipping_Rev)}')
        print(f'Total Rev: {int(SubTotal)+(int(Shipping_Rev)-int(shipping_cost))}')
        print(SubTotal/(int(SubTotal)+(int(Shipping_Rev)-int(shipping_cost))))
        r_data['percent'] = (1-(r_data.Subtotal+r_data.Shipping-r_data['Amount Paid'])/r_data.Subtotal)*100
        r_data.to_csv('ShippingBreakDown.csv')



def create_arg_parser():
    parser = argparse.ArgumentParser(description="A tool to handle Shopify shipping costs.")
    
    parser.add_argument("--shopify_token", default=os.getenv("SECRET_TOKEN"), help="Shopify token. Defaults to SECRET_TOKEN environment variable.")
    parser.add_argument("--store_name", default=os.getenv("STORE_NAME"), help="Name of the store. Defaults to STORE_NAME environment variable.")
    parser.add_argument("--shipping_csv_path", default='stamps.csv', help="Path to the shipping CSV. Defaults to 'stamps.csv'.")
    parser.add_argument("--order_csv_path", default='orders.csv', help="Path to the order CSV. Defaults to 'orders.csv'.")
    
    # For start_date, convert the default value to string so it's consistent with argparse's behavior
    default_start_date = (datetime.now() - timedelta(days=6*30)).isoformat()
    parser.add_argument("--start_date", default=default_start_date, help=f"Start date in ISO format. Defaults to {default_start_date}.")
    
    return parser

if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()
    
    # Instantiate the shopify_shipping_cost class with parsed arguments
    shopify_tool = shopify_shipping_cost(
        shopify_token=args.shopify_token,
        store_name=args.store_name,
        shipping_csv_path=args.shipping_csv_path,
        order_csv_path=args.order_csv_path,
        start_date=args.start_date
    )
    
    # Run the tool
    shopify_tool.run()
