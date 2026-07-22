from product.product_model import Product
from product.product_repository import ProductRepository


def test_add_product():
    test_list = ProductRepository()
    product_1 = Product(name= "Basil Plant - 4in Pot", unit = "5 kg", 
    cost_per_unit= 1.75, price_per_unit= 4.99, 
    quantity_in_stock= 40)

    product_2 = Product(name= "Apple Tree - 6in Pot", unit = "7 kg", 
    cost_per_unit= 2.25, price_per_unit= 6.99, 
    quantity_in_stock= 50)

    product_3 = Product(name= "Banana Tree - 6in Pot", unit = "6 kg", 
    cost_per_unit= 2.00, price_per_unit= 5.99, 
    quantity_in_stock= 45)

    test_list.add_product(product_1)
    test_list.add_product(product_2)
    test_list.add_product(product_3)

    assert len(test_list.products) == 3


    
    
