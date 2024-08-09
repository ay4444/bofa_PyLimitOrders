import unittest
from trading_framework.execution_client import ExecutionClient
from limit.limit_order_agent import ExecuteOrders


ec = ExecutionClient
eo = ExecuteOrders(ec)

class LimitOrderAgentTest(unittest.TestCase):

    def test_add_buy_orders(self):
        # for 'IBM'
        self.assertEqual(eo.add_order(flag="BUY",product_id='IBM', amount=1000, limit=111), 'Order placed')
        self.assertEqual(eo.add_order(flag="BUY",product_id='IBM', amount=1000, limit=99), 'Order placed')
        self.assertEqual(eo.add_order(flag="BUY",product_id='IBM', amount=1000, limit=100), 'Order placed')
        # for 'AAPL'
        self.assertEqual(eo.add_order(flag="BUY",product_id='AAPL', amount=1000, limit=111), 'Order placed')
        self.assertEqual(eo.add_order(flag="BUY",product_id='AAPL', amount=1000, limit=99), 'Order placed')
        self.assertEqual(eo.add_order(flag="BUY",product_id='AAPL', amount=1000, limit=100), 'Order placed')

    def test_add_sell_orders(self):
        self.assertEqual(eo.add_order(flag="SELL",product_id='IBM', amount=1000, limit=111), 'Order placed')
        self.assertEqual(eo.add_order(flag="SELL",product_id='IBM', amount=1000, limit=99), 'Order placed')
        self.assertEqual(eo.add_order(flag="SELL",product_id='IBM', amount=1000, limit=100), 'Order placed')

        self.assertEqual(eo.add_order(flag="SELL",product_id='AAPL', amount=1000, limit=111), 'Order placed')
        self.assertEqual(eo.add_order(flag="SELL",product_id='AAPL', amount=1000, limit=99), 'Order placed')
        self.assertEqual(eo.add_order(flag="SELL",product_id='AAPL', amount=1000, limit=100), 'Order placed')

    def test_price_tick(self):     
        # this method will also test executing pending orders and print details of orders executed, since pending orders executed on every new price_tick 

        # for 'IBM'  
        self.assertEqual(eo.on_price_tick(product_id='IBM', price=111), 0)
        self.assertEqual(eo.on_price_tick(product_id='IBM', price=99), 0)
        self.assertEqual(eo.on_price_tick(product_id='IBM', price=100), 0)     

        # for 'AAPL'
        self.assertEqual(eo.on_price_tick(product_id='AAPL', price=111), 0)
        self.assertEqual(eo.on_price_tick(product_id='AAPL', price=99), 0)
        self.assertEqual(eo.on_price_tick(product_id='AAPL', price=100), 0)        


if __name__ == "__main__":
    unittest.main(verbosity=2)