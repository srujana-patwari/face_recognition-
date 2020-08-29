from tkinter import *
from tkinter import messagebox,Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("My Crypto Portpolio")
pycrypto.iconbitmap("favicon.ico")   #to add logo to our title

con = sqlite3.connect("coin.db")  #connecting to DATABASE
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY,symbol TEXT,amount INTEGER,price REAL)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():  #it cointain all the windows that we have here
        cell.destroy()

    app_nav()
    app_header()
    my_portfolio()

def app_nav():          #navigating the files loke file, edit,view
    def clear_all():
        cursorObj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo("Portfolio Notification","Portfolio Cleared - Add New Coins")
        reset()

    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label='File',menu=file_item)
    pycrypto.config(menu=menu)


def my_portfolio():
    api_request = requests.get(
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=22ff4501-289c-44b0-9cfb-d3e57b2ec10f")
    api = json.loads(api_request.content)

    cursorObj.execute("SELECT * FROM coin")
    coins = cursorObj.fetchall()

    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cursorObj.execute("INSERT INTO coin(symbol,price,amount) VALUES(?,?,?)",(symbol_txt.get(),price_txt.get(),amount_txt.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notification","Coin ADDED to Portfolio successfully!")
        reset()

    def update_coin():
        cursorObj.execute("UPDATE coin SET symbol=?, price=? amount=? WHERE id=?",symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get())
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin UPDATED successfully!")
        reset()

    def delete_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?",(portid_delete.get(),))
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin DELETED from Portfolio")
        reset()

    total_pl = 0  # tatal profit or loss
    coin_row = 1  # row start with 1 bcz 0 occupies headings
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0, 300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] * coin[3]
                total_pl_coin = pl_percoin * coin[2]

                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid

                portfolio_id = Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black", font="Lato 12",borderwidth=2, relief="groove", padx="2", pady="2")
                portfolio_id.grid(row=coin_row, column=0, sticky=N + S + E + W)

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="2",pady="2")
                name.grid(row=coin_row, column=1, sticky=N + S + E + W)

                price = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6", fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="2",pady="2")
                price.grid(row=coin_row, column=2, sticky=N + S + E + W)

                no_coins = Label(pycrypto, text=coin[2], bg="#F3F4F6", fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="2",pady="2")
                no_coins.grid(row=coin_row, column=3, sticky=N + S + E + W)

                amount_paid = Label(pycrypto, text="${0:.2f}".format(total_paid), bg="#F3F4F6", fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="2",pady="2")
                amount_paid.grid(row=coin_row, column=4, sticky=N + S + E + W)

                current_val = Label(pycrypto, text="${0:.2f}".format(current_value), bg="#F3F4F6", fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="2",pady="2")
                current_val.grid(row=coin_row, column=5, sticky=N + S + E + W)

                pl_coin = Label(pycrypto, text="${0:.2f}".format(pl_percoin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(pl_percoin))),font="Lato 12",borderwidth=2,relief="groove",padx="2",pady="2")
                pl_coin.grid(row=coin_row, column=6, sticky=N + S + E + W)

                totalpl = Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(total_pl_coin))),font="Lato 12",borderwidth=2,relief="groove",padx="2",pady="2")
                totalpl.grid(row=coin_row, column=7, sticky=N + S + E + W)

                coin_row += 1

    #insert data
    symbol_txt = Entry(pycrypto, borderwidth=2,relief="groove")
    symbol_txt.grid(row=coin_row+1, column=1)

    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row + 1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row + 1, column=3)

    add_coin = Button(pycrypto, text="Add coin", bg="#142E54", fg="white", command=insert_coin, font="Lato 12",borderwidth=2, relief="groove", padx="2", pady="2")
    add_coin.grid(row=coin_row+1, column=4, sticky=N + S + E + W)

    #update coin
    portid_update = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_update.grid(row=coin_row + 2, column=0)

    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row + 2, column=1)

    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row + 2, column=2)

    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row + 2, column=3)

    update_coin_txt = Button(pycrypto, text="update coin", bg="#142E54", fg="white", command=update_coin, font="Lato 12",borderwidth=2, relief="groove", padx="2", pady="2")
    update_coin_txt.grid(row=coin_row + 2, column=4, sticky=N + S + E + W)

    #Delete coin
    portid_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_delete.grid(row=coin_row + 3, column=0)

    delete_coin_txt = Button(pycrypto, text="Delete coin", bg="#142E54", fg="white", command=delete_coin,font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    delete_coin_txt.grid(row=coin_row + 3, column=4, sticky=N + S + E + W)

    totalap = Label(pycrypto, text="${0:.2f}".format(total_amount_paid), bg="#F3F4F6", fg="black", font="Lato 12",borderwidth=2, relief="groove", padx="2", pady="2")
    totalap.grid(row=coin_row, column=4, sticky=N + S + E + W)

    totalcv = Label(pycrypto, text="${0:.2f}".format(total_current_value), bg="#F3F4F6", fg="black",font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    totalcv.grid(row=coin_row, column=5, sticky=N + S + E + W)

    totalpl = Label(pycrypto, text="${0:.2f}".format(total_pl), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(total_pl))), font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    totalpl.grid(row=coin_row, column=7, sticky=N + S + E + W)

    api = ""

    refresh = Button(pycrypto, text= "Refresh", bg="#142E54",fg="white",command=reset , font="Lato 12", borderwidth=2,relief="groove", padx="2", pady="2")
    refresh.grid(row=coin_row+1, column=7, sticky=N + S + E + W)

def app_header():
    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N + S + E + W)

    name = Label(pycrypto,text="coin name",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    name.grid(row=0,column=1,sticky=N+S+E+W)

    price = Label(pycrypto,text="price",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    price.grid(row=0,column=2,sticky=N+S+E+W)

    no_coins = Label(pycrypto,text="no_coins",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    no_coins.grid(row=0,column=3,sticky=N+S+E+W)

    amount_paid = Label(pycrypto,text="total amount paid",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    amount_paid.grid(row=0,column=4,sticky=N+S+E+W)

    current_val = Label(pycrypto,text="current value",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    current_val.grid(row=0,column=5,sticky=N+S+E+W)

    pl_coin = Label(pycrypto,text="P/L per coin",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    pl_coin.grid(row=0,column=6,sticky=N+S+E+W)

    totalpl = Label(pycrypto,text="total P/L per coin",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    totalpl.grid(row=0,column=7,sticky=N+S+E+W)

app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()

cursorObj.close()
con.close()

print("Program Completed")