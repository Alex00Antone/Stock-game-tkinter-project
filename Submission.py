#Michael Dickinson
#CSCI 128 K
#Final Project: Stock Simulator Game 
#Group: Tyler Frost, Alex Antone 
#Time: 20 hours
import tkinter as tk
from tkinter import simpledialog
import random

from stock_class import Stock

from stock_simulator import Game

class Game_part2(Game):
    def __init__(self):
        super().__init__()

    def create_graph(self, stock):
        if self.canvas:
            frame = tk.Frame(self.root)
            frame.pack(pady=10)
            self.canvas = tk.Canvas(frame, width=400, height=200)
            self.canvas.pack()
        
        self.canvas.delete("all")
        self.lines.clear()
        self.draw_graph(stock)
        
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

        

    # Alex wrote buy option, had to add in game class
    def buy_option(self, option):
        
        strike_price = simpledialog.askfloat("Strike price", "Enter the strike price:", minvalue=1)
        if strike_price is not None:
            option.update_strike_price(strike_price)
            index1 = self.options.index(option)
            stock1 = self.stocks[index1]
            call_price = option.call_price(stock1)
            calls_to_buy = simpledialog.askfloat("calls to buy", f"Price per call: {call_price:.2f} Enter the amount of calls:", minvalue=1)
            
            total_cost = calls_to_buy * option.call_price(stock1)
            if self.player_money >= total_cost:
                self.player_money -= total_cost
                if option.name in self.player_options:
                    self.player_options[option.name] += calls_to_buy
                    self.player_stocks_price[stock1.name] = stock1.price
                else:
                    self.player_options[option.name] = calls_to_buy
                    self.player_stocks_price[stock1.name] = stock1.price
                tk.messagebox.showinfo("Purchase Successful", f"You bought {calls_to_buy} options of {option.name}!")
            else:
                tk.messagebox.showerror("Purchase Failed", "You do not have enough money to buy this stock.")
        else:
            tk.messagebox.showwarning("Input Cancelled", "Purchase cancelled.")
        
        

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

    def sell_option(self, option):
        if option.name in self.player_options:
            shares_owned = self.player_options[option.name]
            calls_to_sell = simpledialog.askinteger("Sell Options", "Enter the number of options to sell:", minvalue=1, maxvalue=shares_owned)
            if calls_to_sell is not None:
                if calls_to_sell <= shares_owned:
                    self.player_options[option.name] -= calls_to_sell
                    index1 = self.options.index(option)
                    stock1 = self.stocks[index1]
                    price = self.player_stocks_price[stock1.name]
                    self.player_money += ((calls_to_sell *price)-(calls_to_sell*stock1.price))
                    tk.messagebox.showinfo("Sale Successful", f"You exercised {calls_to_sell} calls of {option.name}!")
                else:
                    tk.messagebox.showerror("Sale Failed", "You do not own enough calls to exercise this amount.")
            else:
                tk.messagebox.showwarning("Input Cancelled", "Sale cancelled.")
        else:
            tk.messagebox.showerror("Sale Failed", "You do not own any calls of this stock.")

        self.create_stock_page()


    

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Start the game
if __name__ == "__main__":
    Game_part2()


