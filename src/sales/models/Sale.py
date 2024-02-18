from datetime import datetime
from typing import Optional, Union

from src.clients.models import Client


class Sale:
    def __init__(
        self,
        date: datetime = datetime.now(),
        is_finished: bool = False,
        finished_date: Optional[datetime] = None,
        description: Optional[str] = None,
        client: Optional[Client] = None,
        id: Optional[Union[str, int]] = None,
    ) -> None:
        self.date = date
        self.is_finished = is_finished
        self.finished_date = finished_date
        self.description = description
        self.client = client
        self.id = id
