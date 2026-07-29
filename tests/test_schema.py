from pydantic import ValidationError
from product.APIProduct import APIProduct


def test_product_rejects_empty_name():
    try:
        APIProduct(
            name="   ",
            unit="kg",
            cost_per_unit=1,
            price_per_unit=2,
            quantity_in_stock=5,
        )
        assert False, "Expected ValidationError"
    except ValidationError as e:
        assert "name" in str(e)


def test_product_rejects_invalid_unit():
    try:
        APIProduct(
            name="Basil",
            unit="invalid",
            cost_per_unit=1,
            price_per_unit=2,
            quantity_in_stock=5,
        )
        assert False
    except ValidationError:
        pass


def test_product_rejects_negative_cost():
    try:
        APIProduct(
            name="Basil",
            unit="kg",
            cost_per_unit=-1,
            price_per_unit=2,
            quantity_in_stock=5,
        )
        assert False
    except ValidationError:
        pass
