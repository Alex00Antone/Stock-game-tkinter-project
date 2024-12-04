#Alex Antone
#CSCI 128 G
#Final Project: Stock Simulator Game
#Group: Tyler Frost, Michael Dickinson
#Time: 20 hours
import random
import numpy as np 
from math import *

class Stock:
    def __init__(self, name, sector, description, price):
        self.name = name
        self.sector = sector
        self.description = description
        self.price = price
        self.history =self.generate_initial_history(20)
    
    def generate_initial_history(self, length):
        
        price_range = 0.1 * self.price  
        return [round(random.uniform(self.price - price_range, self.price + price_range), 2) for _ in range(length)] + [self.price]
    
    def update_price(self):
        change_percent = random.uniform(-0.05, 0.05)  
        self.price = max(0, self.price * (1 + change_percent))
        self.history.append(self.price)



class Option():
    def __init__(self, name, price, strike_price, rate, dividend_yield, sigma):
        self.name = name
        self.price = price
        self.strike_price= strike_price
        self.rate = rate 
        self.dividend_yield = dividend_yield
        self.sigma = sigma
        self.time = 1

    # used documentation to change algorithm, originally used black-scholez but didn't work properly so changed to longstaff-schwartz
    def call_price(self, stock, n_paths=1000, n_steps= 1000, degree=2):
        dt = 1/n_steps
        discount_factor = np.exp(-self.rate * dt)

        
        S = np.zeros((n_paths, n_steps + 1))
        S[:, 0] = stock.price
        for t in range(1, n_steps + 1):
            Z = np.random.standard_normal(n_paths)
            S[:, t] = S[:, t - 1] * np.exp((self.rate - 0.5 * self.sigma**2) * dt + self.sigma * np.sqrt(dt) * Z)

        
        V = np.maximum(self.strike_price - S, 0)

        
        for t in range(n_steps - 1, 0, -1):
            
            itm = S[:, t] < self.strike_price

            
            if np.sum(itm) > 0:
                X = np.vander(S[itm, t], degree + 1)
                Y = V[itm, t + 1] * discount_factor
                beta = np.linalg.lstsq(X, Y, rcond=None)[0]

                # Calculate continuation value
                CV = np.dot(X, beta)

                # Update the value matrix
                V[itm, t] = np.maximum(V[itm, t], CV)


        option_price = np.mean(V[:, 1] * discount_factor)
        return option_price
    
    def update_strike_price(self, strike_price):
        self.strike_price = strike_price
