class PaymentsResume:
    def __init__(self, date: str, bs: float, us: float, total_us: float) -> None:
        self.date = date
        self.bs = bs
        self.us = us
        self.total_us = total_us
