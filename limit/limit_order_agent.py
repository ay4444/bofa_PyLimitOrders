from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
import json

class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        self.execution_client = execution_client
        super().__init__()

    def execute_orders(self, flag: str,product_id: str, amount: int, limit: int):
        order_details = {"flag": flag,"product_id": product_id, "amount": amount, "limit": limit}

        if product_id == self.price_tick_data.get('product_id'):
            if self.price_tick_data.get('cmp_price')<=limit and flag=="BUY":
                self.execution_client.buy(self, product_id=product_id, amount=amount)
                result = {'order_detail': order_details, "order_status": 'Executed'}
                return result
            elif self.price_tick_data.get('cmp_price')>=limit and flag=="SELL":
                self.execution_client.sell(self, product_id=product_id, amount=amount)
                result = {'order_detail': order_details, "order_status": 'Executed'}
                return result
        else:
            return None

    def execute_pending_orders(self):
        with open('pending_orders.json') as po:
            po_dict = json.load(po)        

        pending_order_list = po_dict['pending_orders_list']
        executed_orders_list = []
        for order in po_dict['pending_orders_list']:
            pending_order_status = self.execute_orders(order.get('flag'), order.get('product_id'), order.get('amount'), order.get('limit'))
            if pending_order_status:
                pending_order_list.remove(order)
                executed_orders_list.append(order)
        po_dict['pending_orders_list'] = pending_order_list
        with open('pending_orders.json', 'w') as po:
            json.dump(po_dict, po, indent=6)
        print(f'\n pending orders executed : {executed_orders_list} \n')
        return 0

    def on_price_tick(self, product_id: str, price: float):
        self.price_tick_data = {"product_id": product_id, "cmp_price": price}
        return self.execute_pending_orders() 
     

class ExecuteOrders(LimitOrderAgent):
    def __init__(self, execution_client: ExecutionClient) -> None:
        super().__init__(execution_client)

    def add_order(self, flag: str,product_id: str, amount: int, limit: int):
        order_details = {"flag": flag,"product_id": product_id, "amount": amount, "limit": limit}
        with open('pending_orders.json') as po:
            po_dict = json.load(po)
        if len(po_dict['pending_orders_list'])>0:
            order_details['order_id'] = po_dict['pending_orders_list'][-1].get('order_id') + 1
        else:
            order_details['order_id'] = 0
        po_dict['pending_orders_list'].append(order_details)
        with open('pending_orders.json', 'w') as po:
            json.dump(po_dict, po, indent=6)
        return 'Order placed'
