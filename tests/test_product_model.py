from product.product_model import ProductModel


def test_product_model():
    product = ProductModel(
        name="apple seed",
        unit="kg",
        cost_per_unit=100,
        price_per_unit=150,
        quantity_in_stock=100,
        category_id=1,
    )
    assert product.name == "apple seed"
    assert product.unit == "kg"
    assert product.cost_per_unit == 100
    assert product.price_per_unit == 150
    assert product.quantity_in_stock == 100
