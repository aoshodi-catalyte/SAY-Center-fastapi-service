from product.product_model import Product

def test_product_model():
    product = Product(name="apple seed", unit="kg", cost_per_unit=100, price_per_unit=150,quantity_in_stock= 100)
    assert product.name == "apple seed"
    assert product.unit == "kg"
    assert product.cost_per_unit == 100
    assert product.price_per_unit == 150
    assert product.quantity_in_stock == 100

