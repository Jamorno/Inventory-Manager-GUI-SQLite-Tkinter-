import tkinter as tk
from inventory_db import InventoryDB

inventory = InventoryDB()

root = tk.Tk()
root.title("Inventory System")
root.geometry("350x280")

#entry field
input_frame = tk.Frame(root)
input_frame.pack(pady=(15, 5))

tk.Label(input_frame, text="Product name:").grid(row=0, column=0, sticky="e", padx=5)
product_name_entry = tk.Entry(input_frame, width=8)
product_name_entry.grid(row=0, column=1, padx=5)
product_name_entry.focus_set()

tk.Label(input_frame, text="Quantity:").grid(row=0, column=2, sticky="e", padx=5)
qty_entry = tk.Entry(input_frame, width=3)
qty_entry.grid(row=0, column=3, padx=5)

#output area(fixed size)
output = tk.Text(root, height=10, width=45)
output.pack(pady=5)
output.configure(state="disabled")

#action funtion
def update_output():
    output.configure(state="normal")
    output.delete(1.0, tk.END)
    output.insert(tk.END, inventory.show_stock())
    output.configure(state="disabled")

def add(event=None):
    product = product_name_entry.get().strip()
    qty = qty_entry.get().strip()

    if not product:
        return

    try:
        quantity = int(qty) if qty else 1
    except ValueError:
        quantity = 1

    inventory.add_item(product, quantity)
    product_name_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    update_output()
    product_name_entry.focus_set()

def remove():
    product = product_name_entry.get().strip()
    qty = qty_entry.get().strip()

    if not product:
        return
    
    try:
        quantity = int(qty) if qty else 1
    except ValueError:
        quantity = 1

    inventory.remove_item(product, quantity)
    product_name_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    update_output()

#button
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Add", width=6, command=add).pack(side="left", padx=5)
tk.Button(button_frame, text="Remove", width=6, command=remove).pack(side="left", padx=5)
tk.Button(button_frame, text="Show Stock", width=6, command=update_output).pack(side="left", padx=5)

#keyboard blinding
product_name_entry.bind("<Return>", lambda e:qty_entry.focus_set())
qty_entry.bind("<Return>", add)

#start GUI
root.mainloop()
