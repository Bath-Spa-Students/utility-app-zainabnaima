import tkinter as tk
from tkinter import simpledialog, messagebox

class VendingMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Vending Machine")
        self.root.geometry("1200x800")
        self.cart = []
        self.total_amount = 0
        self.items = {
            "Snacks": {"Pretzels": ("$1.75", 12), "Trail Mix": ("$2.50", 7), "Potato Chips": ("$1.50", 10),
                       "Popcorn": ("$2.25", 10), "Chocolate Bars": ("$2.00", 8)},
            "Beverages": {"Iced Tea": ("$1.75", 12), "Coffee": ("$2.50", 8), "Soda": ("$1.25", 15),
                          "Juice": ("$2.00", 10), "Water": ("$1.00", 20)},
            "Candy": {"M&Ms": ("$1.75", 10), "Twix": ("$2.00", 8), "Snickers": ("$1.50", 12),
                      "Skittles": ("$1.50", 10), "Gummy Bears": ("$1.25", 15)},
            "Microwavable Meals": {"Mac 'n Cheese": ("$2.50", 8), "Frozen Pizza": ("$4.00", 6),
                                   "Instant Ramen": ("$3.00", 5), "Chicken Nuggets": ("$3.50", 7),
                                   "Hot Pockets": ("$2.75", 10)},
            "Desserts": {"Ice Cream Sandwich": ("$2.50", 8), "Brownies": ("$2.00", 10),
                         "Cheesecake": ("$3.00", 7), "Cupcakes": ("$2.25", 10), "Cookies": ("$1.75", 12)},
            "Sandwiches and Wraps": {"Chicken Wrap": ("$3.50", 7), "BLT Sandwich": ("$3.00", 8),
                                     "Veggie Wrap": ("$4.50", 5), "Turkey Sandwich": ("$4.00", 6),
                                     "Ham and Cheese Sandwich": ("$3.75", 6)}
        }

        self.root.configure(bg='#34495e')

        # Start with the category selection page
        self.create_category_page()

    def create_category_page(self):
        # Clear the screen
        self.clear_screen()

        # Display the title
        tk.Label(self.root, text="Vending Machine", font=("Verdana", 48, "bold"), bg='#34495e', fg='#ecf0f1').pack(pady=25)

        # Display category buttons
        categories = ["Snacks", "Beverages", "Candy", "Microwavable Meals", "Desserts", "Sandwiches and Wraps"]
        for category in categories:
            tk.Button(self.root, text=category, command=lambda c=category: self.select_category(c),
                      bg='#2c3e50', fg='#ecf0f1', font=("Verdana", 18)).pack(pady=15)

    def select_category(self, category):
        # Set the selected category and create the items page
        self.selected_category = category
        self.create_items_page()

    def create_items_page(self):
        # Clear the screen
        self.clear_screen()

        # Display category title
        tk.Label(self.root, text=f"Select {self.selected_category}", font=("Verdana", 32, "bold"), bg='#34495e', fg='#ecf0f1').pack(pady=20)

        # Display buttons for each item in the category
        for item, (price, quantity) in self.items[self.selected_category].items():
            tk.Button(self.root, text=f"{item} - {price} - Quantity: {quantity}",
                      command=lambda i=item, p=price, q=quantity: self.add_to_cart(i, p, q),
                      bg='#2c3e50', fg='#ecf0f1', font=("Verdana", 16)).pack(pady=18)

    def add_to_cart(self, item, price, quantity):
        # Update the cart based on user selection
        for i, (cart_item, _, cart_quantity) in enumerate(self.cart):
            if cart_item == item:
                # If the item is already in the cart, increase the quantity
                self.cart[i] = (item, price, cart_quantity + 1)
                messagebox.showinfo("Vending Machine", f"{item} quantity increased in the cart.")
                break
        else:
            # If the item is not in the cart, add it
            self.cart.append((item, price, 1))
            messagebox.showinfo("Vending Machine", f"{item} added to the cart.")

            # Decrease the quantity in stock by one
            self.decrease_stock(item)

        # Decrease the quantity by one
        quantity -= 1

        if quantity > 0:
            response = messagebox.askquestion("Vending Machine", "Do you want anything else?")
            if response == 'yes':
                # If the user wants more items, go back to category selection
                self.create_category_page()
            else:
                # If not, show the cart page
                self.show_cart_page()
        else:
            # If the item is out of stock, show a message and go back to category selection
            messagebox.showinfo("Vending Machine", "Sorry, this item is out of stock.")
            self.create_category_page()

    def show_cart_page(self):
        # Clear the screen
        self.clear_screen()

        # Display cart contents and total amount
        tk.Label(self.root, text="Your Cart", font=("Verdana", 30, "bold"), bg='#34495e', fg='#ecf0f1').pack(pady=20)
        self.total_amount = 0
        for item, price, quantity in self.cart:
            tk.Label(self.root, text=f"{item} | {price} | Quantity: {quantity}",
                     bg='#34495e', fg='#ecf0f1', font=("Verdana", 18)).pack()
            self.total_amount += float(price[1:]) * quantity

        tk.Label(self.root, text=f"Total Amount: ${self.total_amount:.2f}", font=("Verdana", 28,"bold"), bg='#34495e', fg='#ecf0f1').pack(pady=10)

        tk.Button(self.root, text="Proceed to Payment", command=self.show_payment_page,
                  bg='#2c3e50', fg='#ecf0f1', font=("Verdana", 18)).pack(pady=20)  # Dark blue button

    def show_payment_page(self):
        # Clear the screen
        self.clear_screen()

        # Display payment information
        tk.Label(self.root, text="Payment", font=("Verdana", 50, "bold"), bg='#34495e', fg='#ecf0f1').pack(pady=20)

        # Prompt user to insert money
        amount = simpledialog.askfloat("INSERT MONEY", "Enter the amount you want to insert:")
        if amount is not None:
            if amount >= self.total_amount:
                # Calculate change and display it
                change = amount - self.total_amount
                tk.Label(self.root, text=f"Change: ${change:.2f}", font=("Verdana", 30), bg='#34496e', fg='#ecf0f1').pack(pady=10)

                # List of dispensed items
                dispensed_items = [item[0] for item in self.cart]

                # Display dispensed items
                tk.Label(self.root, text="Items Dispensed:", font=("Verdana", 28, "bold"), bg='#34495e', fg='#ecf0f1').pack(pady=15)
                
                for dispensed_item in dispensed_items:
                    tk.Label(self.root, text=f"{dispensed_item}", font=("Verdana", 18), bg='#34495e', fg='#ecf0f1').pack()

                # Update stock based on the dispensed items (reduce quantity by 1)
                for dispensed_item in dispensed_items:
                    self.decrease_stock(dispensed_item)

                # Display thank you message
                tk.Label(self.root, text="Thank You for Your Purchase! Come Again!", font=("Verdana", 18, "bold"),
                        bg='#34495e', fg='#ecf0f1').pack(pady=50)

                # Reset the page after 8 seconds
                self.root.after(8000, self.root.destroy)
            
            else:
                # If not enough money, show a message and go back to category selection
                messagebox.showinfo("Vending Machine", "Insufficient funds. Please insert more money.")
                self.create_category_page()

    def decrease_stock(self, item):
        # Decrease the quantity of the selected item in stock by one
        for category, items in self.items.items():
            if item in items:
                items[item] = (items[item][0], items[item][1] - 1)

    def clear_screen(self):
        # Clear all widgets on the screen
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    # Create and run the VendingMachine application
    root = tk.Tk()
    vending_machine = VendingMachine(root)
    root.mainloop()
