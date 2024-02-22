from datetime import datetime
from typing import Optional, Union

from src.clients.models import Client
from src.orders.models import Order
from src.orders.utils import calculate_total_orders
from src.payments.models import Payment
from src.payments.utils import calculate_total_payments
from .SaleState import SaleState

class Sale:
    def __init__(
        self,
        date: datetime = datetime.now(),
        is_finished: bool = False,
        finished_date: Optional[datetime] = None,
        description: Optional[str] = None,
        client: Optional[Client] = None,
        id: Optional[Union[str, int]] = None,
        orders: "list[Order]" = [],
        payments: "list[Payment]" = [] 
    ) -> None:
        self.date = date
        self.is_finished = is_finished
        self.finished_date = finished_date
        self.description = description
        self.client = client
        self.id = id
        self.orders = orders
        self.payments = payments
        
    def get_total(self) -> float:
        total_orders = calculate_total_orders(self.orders)
        total_payments = calculate_total_payments(self.payments)
        
        return total_orders.total - total_payments.total
    
    def get_state(self) -> SaleState:
        epsilon = 0.01
        
        if abs(self.get_total()) <= epsilon:
             return SaleState.FINISHED
        
        if  self.get_total() > 0:
            return SaleState.CREDIT
        
        return SaleState.REFUND
    
    def __str__(self) -> str:
        return ("""  
            Sale(id={self.id}, date={self.date}, is_finished={self.is_finished}
            finished_date={self.finished_date}, description={self.description}
            client={self.client}
            orders={self.orders}
            payments={self.payments})
        """)