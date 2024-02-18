from src.orders.models import Order, OrderTotal

def calculate_total_orders(orders: "list[Order]") -> OrderTotal:
    total_us = 0
    total_bs = 0

    for order in orders:
        total = order.price * order.quantity
        total_with_discount = total * (1 - (order.discount / 100))
        total_us += total_with_discount
        total_bs += total_with_discount * order.rate

    return OrderTotal(
        total=total_us,
        bs=total_bs,
        us=total_us
    )