from dining_exp_manager import DiningExperienceManager
from unittest.mock import patch
import pytest

@pytest.fixture
def dem():
    return DiningExperienceManager()

def test_validate_quantity_valid(dem):
    assert dem.validate_quantity("5") == 5
    assert dem.validate_quantity("10") == 10

def test_validate_quantity_invalid(dem):
    with pytest.raises(ValueError):
        dem.validate_quantity("0")

    with pytest.raises(ValueError):
        dem.validate_quantity("-5")

    with pytest.raises(ValueError):
        dem.validate_quantity("abc")

def test_calculate_cost_no_discount(dem):
    order = {"Chinese Food": 2, "Italian Food": 3}
    expected_cost = 10 * 2 + 12 * 3
    assert dem.calculate_cost(order) == expected_cost

def test_calculate_cost_10_percent_discount(dem):
    order = {"Chinese Food": 6, "Pastries": 3}
    expected_cost = (10 * 6 + 8 * 3) * 0.9
    assert dem.calculate_cost(order) == round(expected_cost, 2)

def test_calculate_cost_20_percent_discount(dem):
    order = {"Chinese Food": 11, "Pastries": 4}
    expected_cost = (10 * 11 + 8 * 4) * 0.8
    assert dem.calculate_cost(order) == round(expected_cost, 2)

def test_apply_special_offers_no_discount(dem):
    assert dem.apply_special_offers(30) == 30

def test_apply_special_offers_10_dollars_discount(dem):
    assert dem.apply_special_offers(60) == 60 - 10

def test_apply_special_offers_25_dollars_discount(dem):
    assert dem.apply_special_offers(120) == 120 - 25

def test_apply_special_category_surcharge_with_special_category(dem):
    order = {"Chef's Specials": 2}
    assert dem.apply_special_category_surcharge(order) is True

def test_apply_special_category_surcharge_without_special_category(dem):
    order = {"Chinese Food": 2}
    assert dem.apply_special_category_surcharge(order) is False

def test_validate_availability_all_available(dem):
    order = {"Chinese Food": 2, "Italian Food": 1}
    assert dem.validate_availability(order) is True

def test_validate_availability_not_all_available(dem):
    order = {"Chinese Food": 2, "Sushi": 1}
    assert dem.validate_availability(order) is False

def test_manage_order_cancel(dem, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'finish')
    assert dem.manage_order() == -1

def test_manage_order_confirm(dem):
    # Utilizamos patch para simular las entradas del usuario y finalizar el pedido rápidamente
    with patch('builtins.input', side_effect=['Chinese Food', '2', 'finish', 'y']):
        total_cost = dem.manage_order()
    assert total_cost > 0

    # Restauramos el flujo normal de entrada del usuario
    with patch('builtins.input', input):
        pass