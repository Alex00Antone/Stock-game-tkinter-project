#Tyler Frost
#CSCI 128 L
#Final Project: Stock Simulator Game
#Group: Alex Antone, Michael Dickinson 
#Time: 20 hours
import tkinter as tk
from tkinter import simpledialog
import random

from stock_class import Stock
from stock_class import Option

class Game:
    def __init__(self):
        self.player_money = 100
        self.player_stocks = {}
        self.canvas = None
        self.lines = []
        self.stocks = [
            # Stock names and descripitons written by AI to change later
            # Penny stocks
            Stock("FinCorp", "Finance", "A low-cost finance stock.", random.uniform(1, 10)),
            Stock("TechNova", "Tech", "A tech penny stock.", random.uniform(1, 10)),
            Stock("HealthFirst", "Healthcare", "A healthcare penny stock.", random.uniform(1, 10)),
            Stock("EnergyPlus", "Energy", "An energy penny stock.", random.uniform(1, 10)),
            Stock("RetailX", "Retail", "A retail penny stock.", random.uniform(1, 10)),
            Stock("TransLogistics", "Transportation", "A transport penny stock.", random.uniform(1, 10)),
            Stock("MediaHub", "Media", "A media penny stock.", random.uniform(1, 10)),
            # Cheap stocks
            Stock("FinSavvy", "Finance", "A cheap finance stock.", random.uniform(11, 60)),
            Stock("TechWave", "Tech", "A tech cheap stock.", random.uniform(11, 60)),
            Stock("CareMed", "Healthcare", "A healthcare cheap stock.", random.uniform(11, 60)),
            Stock("GreenEnergy", "Energy", "An energy cheap stock.", random.uniform(11, 60)),
            Stock("ShopSmart", "Retail", "A retail cheap stock.", random.uniform(11, 60)),
            Stock("LogiTrans", "Transportation", "A transport cheap stock.", random.uniform(11, 60)),
            Stock("MediaConnect", "Media", "A media cheap stock.", random.uniform(11, 60)),
            # Medium stocks
            Stock("FinGroup", "Finance", "A medium finance stock.", random.uniform(61, 100)),
            Stock("TechFusion", "Tech", "A tech medium stock.", random.uniform(61, 100)),
            Stock("HealthNet", "Healthcare", "A healthcare medium stock.", random.uniform(61, 100)),
            Stock("EnergyTech", "Energy", "An energy medium stock.", random.uniform(61, 100)),
            Stock("RetailDynamics", "Retail", "A retail medium stock.", random.uniform(61, 100)),
            Stock("TransGlobal", "Transportation", "A transport medium stock.", random.uniform(61, 100)),
            Stock("MediaWorld", "Media", "A media medium stock.", random.uniform(61, 100)),
            # High stocks
            Stock("FinInvest", "Finance", "A high finance stock.", random.uniform(101, 200)),
            Stock("TechGiant", "Tech", "A tech high stock.", random.uniform(101, 200)),
            Stock("HealthCorp", "Healthcare", "A healthcare high stock.", random.uniform(101, 200)),
            Stock("EnergyInnovations", "Energy", "An energy high stock.", random.uniform(101, 200)),
            Stock("RetailEmpire", "Retail", "A retail high stock.", random.uniform(101, 200)),
            Stock("TransSolutions", "Transportation", "A transport high stock.", random.uniform(101, 200)),
            Stock("MediaVision", "Media", "A media high stock.", random.uniform(101, 200)),
            # Expensive stocks
            Stock("FinElite", "Finance", "An expensive finance stock.", random.uniform(201, 500)),
            Stock("TechSavants", "Tech", "A tech expensive stock.", random.uniform(201, 500)),
            Stock("HealthAdvantage", "Healthcare", "A healthcare expensive stock.", random.uniform(201, 500)),
            Stock("EnergyExperts", "Energy", "An energy expensive stock.", random.uniform(201, 500)),
            Stock("RetailMasters", "Retail", "A retail expensive stock.", random.uniform(201, 500)),
            # Crazy expensive stocks
            Stock("FinPrestige", "Finance", "A crazy expensive finance stock.", random.uniform(501, 1000)),
            Stock("TechPioneers", "Tech", "A tech crazy expensive stock.", random.uniform(501, 1000)),
            Stock("HealthLeaders", "Healthcare", "A healthcare crazy expensive stock.", random.uniform(501, 1000)),
            Stock("EnergyTitan", "Energy", "An energy crazy expensive stock.", random.uniform(501, 1000)),
            # Super stocks
            Stock("FinFuture", "Finance", "A super finance stock.", random.uniform(1001, 10000)),
            Stock("TechMasters", "Tech", "A tech super stock.", random.uniform(1001, 10000)),
            Stock("HealthInnovators", "Healthcare", "A healthcare super stock.", random.uniform(1001, 10000)),
            # Ultra stocks
            Stock("FinExcellence", "Finance", "An ultra finance stock.", random.uniform(10001, 100000)),
            Stock("TechExcellence", "Tech", "A tech ultra stock.", random.uniform(10001, 100000)),
        ]

        # Alex wrote this, had to add in game class
        self.player_options = {}
        self.strike_price = 10
        self.rate = random.randrange(1, 10, 1)
        self.dividend_yield = random.randrange(0, 5, 1)
        self.sigma = 7
        self.player_stocks_price = {}
        
        self.options = [Option(stock.name, stock.price, self.strike_price, self.rate, self.dividend_yield, self.sigma) for stock in self.stocks]
        self.create_main_menu()

    def create_main_menu(self):
        self.root = tk.Tk()
        self.root.title("Stock Trader Simulator")
        tk.Label(self.root, text="Welcome to the Stock Trader Simulator!").pack(pady=10)
        tk.Button(self.root, text="Start New Game", command=self.create_stock_page).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)
        self.root.mainloop()

    def create_stock_page(self):
        self.clear_window()
        tk.Label(self.root, text="Stocks").pack(pady=10)

        money_label = tk.Label(self.root, text=f"Available Money: ${self.player_money:.2f}")
        money_label.pack(pady=5)

        
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.stock_frames = {}
        for stock in self.stocks:
            if stock.name in self.player_stocks:
                shares_owned = self.player_stocks[stock.name]
            else:
                shares_owned = 0

            index1 = self.stocks.index(stock)

            frame = tk.Frame(self.scrollable_frame)
            frame.pack(pady=5)
            self.stock_frames[stock.name] = tk.Label(frame, text=f"{stock.name}: ${stock.price:.2f}  Owned: {shares_owned}")
            self.stock_frames[stock.name].pack(side=tk.LEFT)
            tk.Button(frame, text="View", command=lambda s=stock, o= self.options[index1]: self.view_stock(s, o)).pack(side=tk.LEFT)
            

        self.update_stock_prices()
        self.root.after(5000, self.update_stock_prices)

    def update_stock_prices(self):
        for stock in self.stocks:
            if stock.name in self.player_stocks:
                shares_owned = self.player_stocks[stock.name]
            else:
                shares_owned = 0
            stock.update_price()
            self.stock_frames[stock.name].config(text=f"{stock.name}: ${stock.price:.2f}  Owned: {shares_owned}")
        self.root.after(5000, self.update_stock_prices)

    def view_stock(self, stock, option):
        self.clear_window()
        if stock.name in self.player_stocks:
            shares_owned = self.player_stocks[stock.name]
        else:
            shares_owned = 0

        tk.Label(self.root, text=f"{stock.name} ({stock.sector})").pack(pady=10)
        tk.Label(self.root, text=stock.description).pack(pady=5)
        self.price_label = tk.Label(self.root, text=f"Current Price: ${stock.price:.2f}")
        self.owned_label = tk.Label(self.root, text=f"Stocks Owned: {shares_owned}")
        self.price_label.pack(pady=5)
        self.owned_label.pack(pady= 5)
        self.create_graph(stock)
        tk.Button(self.root, text="Buy", command=lambda s=stock: self.buy_stock(s)).pack(side=tk.LEFT)
        tk.Button(self.root, text="Sell", command=lambda s=stock: self.sell_stock(s)).pack(side=tk.LEFT)
        tk.Button(self.root, text="Buy option", command=lambda o=option: self.buy_option(o)).pack(side=tk.LEFT)
        tk.Button(self.root, text="Sell option", command=lambda o=option: self.sell_option(o)).pack(side=tk.LEFT)
        tk.Button(self.root, text="Back to Stocks", command=self.create_stock_page).pack(pady=5)
        
        self.start_price_update_view(stock)
