import random

class Stock:
    def __init__(self, name, sector, description, price):
        self.name = name
        self.sector = sector
        self.description = description
        self.price = price
        self.history =self.generate_initial_history(20)
    
    def generate_initial_history(self, length):
        # Generate initial prices based on the stock's initial price
        price_range = 0.1 * self.price  # 10% of the initial price for variation
        return [round(random.uniform(self.price - price_range, self.price + price_range), 2) for _ in range(length)] + [self.price]
    
    def update_price(self):
        change_percent = random.uniform(-0.05, 0.05)  # Price can change by ±5%
        self.price = max(0, self.price * (1 + change_percent))
        self.history.append(self.price)



    # add options class