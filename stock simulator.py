import tkinter as tk
from tkinter import simpledialog
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


class Game:
    def __init__(self):
        self.player_money = 100
        self.player_stocks = {}
        self.canvas = None
        self.lines = []
        self.stocks = [
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

        # Display player money
        money_label = tk.Label(self.root, text=f"Available Money: ${self.player_money:.2f}")
        money_label.pack(pady=5)

        # Create a Canvas and Frame for scrolling
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the Canvas and Scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.stock_frames = {}
        for stock in self.stocks:
            frame = tk.Frame(self.scrollable_frame)
            frame.pack(pady=5)
            self.stock_frames[stock.name] = tk.Label(frame, text=f"{stock.name}: ${stock.price:.2f}")
            self.stock_frames[stock.name].pack(side=tk.LEFT)
            tk.Button(frame, text="View", command=lambda s=stock: self.view_stock(s)).pack(side=tk.LEFT)
            

        self.update_stock_prices()
        self.root.after(5000, self.update_stock_prices)

    def update_stock_prices(self):
        for stock in self.stocks:
            stock.update_price()
            self.stock_frames[stock.name].config(text=f"{stock.name}: ${stock.price:.2f}")
        self.root.after(5000, self.update_stock_prices)

    def view_stock(self, stock):
        self.clear_window()
        tk.Label(self.root, text=f"{stock.name} ({stock.sector})").pack(pady=10)
        tk.Label(self.root, text=stock.description).pack(pady=5)
        self.price_label = tk.Label(self.root, text=f"Current Price: ${stock.price:.2f}")
        self.price_label.pack(pady=5)
        self.create_graph(stock)
        tk.Button(self.root, text="Buy", command=lambda s=stock: self.buy_stock(s)).pack(side=tk.LEFT)
        tk.Button(self.root, text="Sell", command=lambda s=stock: self.sell_stock(s)).pack(side=tk.LEFT)
        tk.Button(self.root, text="Back to Stocks", command=self.create_stock_page).pack(pady=5)
        self.start_price_update_view(stock)

    def create_graph(self, stock):
         # Check if the canvas exists, create it if not
        if self.canvas:
            frame = tk.Frame(self.root)
            frame.pack(pady=10)
            self.canvas = tk.Canvas(frame, width=400, height=200)
            self.canvas.pack()
        
        # Clear previous graph lines
        self.canvas.delete("all")  # Clear all items from the canvas

    # Clear the lines list for new graph
        self.lines.clear()
        # Create a new canvas for the graph
        

        # Use the stock's history for the graph
        self.draw_graph(stock)

    def draw_graph(self, stock):
        if not self.canvas:  # If the canvas is not set, do nothing
            return

        if len(stock.history) < 2:
            return

        max_price = max(stock.history)
        min_price = min(stock.history)

        for i in range(len(stock.history) - 1):
            x1 = (i / (len(stock.history) - 1)) * 400  # Adjust for current history length
            y1 = 200 - ((stock.history[i] - min_price) / (max_price - min_price) * 200)
            x2 = ((i + 1) / (len(stock.history) - 1)) * 400
            y2 = 200 - ((stock.history[i + 1] - min_price) / (max_price - min_price) * 200)

            line = self.canvas.create_line(x1, y1, x2, y2, fill="blue")
            self.lines.append(line)

    def start_price_update_view(self, stock):
        def update():
            stock.update_price()
            self.price_label.config(text=f"Current Price: ${stock.price:.2f}")
            stock.history.append(stock.price)
            stock.history.pop(0)
            self.canvas.delete('all')  # Add the new price to history
            self.draw_graph(stock)  # Update the graph
            self.root.after(1000, update)  # Update every second
        
        update()

    def buy_stock(self, stock):
        shares_to_buy = simpledialog.askinteger("Buy Shares", "Enter the number of shares to buy:", minvalue=1)
        if shares_to_buy is not None:
            total_cost = shares_to_buy * stock.price
            if self.player_money >= total_cost:
                self.player_money -= total_cost
                if stock.name in self.player_stocks:
                    self.player_stocks[stock.name] += shares_to_buy
                else:
                    self.player_stocks[stock.name] = shares_to_buy
                tk.messagebox.showinfo("Purchase Successful", f"You bought {shares_to_buy} shares of {stock.name}!")
            else:
                tk.messagebox.showerror("Purchase Failed", "You do not have enough money to buy this stock.")
        else:
            tk.messagebox.showwarning("Input Cancelled", "Purchase cancelled.")

        self.create_stock_page()

    def sell_stock(self, stock):
        if stock.name in self.player_stocks:
            shares_owned = self.player_stocks[stock.name]
            shares_to_sell = simpledialog.askinteger("Sell Shares", "Enter the number of shares to sell:", minvalue=1, maxvalue=shares_owned)
            if shares_to_sell is not None:
                if shares_to_sell <= shares_owned:
                    self.player_stocks[stock.name] -= shares_to_sell
                    self.player_money += shares_to_sell * stock.price
                    tk.messagebox.showinfo("Sale Successful", f"You sold {shares_to_sell} shares of {stock.name}!")
                else:
                    tk.messagebox.showerror("Sale Failed", "You do not own enough shares to sell this amount.")
            else:
                tk.messagebox.showwarning("Input Cancelled", "Sale cancelled.")
        else:
            tk.messagebox.showerror("Sale Failed", "You do not own any shares of this stock.")

        self.create_stock_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Start the game
if __name__ == "__main__":
    Game()