#Alex Antone
import tkinter as tk
from tkinter import simpledialog
import random

from stock_class import Stock

from stock_simulator import Game

class Game_part2(Game):
    def __init__(self):
        super().__init__()

    
    def draw_graph(self, stock):
        if not self.canvas: 
            return

        if len(stock.history) < 2:
            return

        max_price = max(stock.history)
        min_price = min(stock.history)

        for i in range(len(stock.history) - 1):
            x1 = (i / (len(stock.history) - 1)) * 400 
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
            self.canvas.delete('all') 
            self.draw_graph(stock)  
            self.root.after(1000, update)
        
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
    Game_part2()

    # add main loop functionality
