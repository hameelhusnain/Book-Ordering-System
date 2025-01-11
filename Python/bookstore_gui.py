import tkinter as tk
from tkinter import ttk, messagebox
from bookstore_core_inher import Customer, Stock, Order, Shipping, Invoice, BookStore
import datetime
import csv

class BookOrderingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Ordering System")
        self.root.geometry("500x500")

        self.customers = []
        self.books = []
        self.orders = []
        self.bookstore = BookStore()

        self.create_home_window()

    def create_home_window(self):
        """Create the home window with two buttons."""
        tk.Button(self.root, text="Add Details", command=self.open_add_details_window).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.root, text="View All Invoices", command=self.open_view_invoices_window).grid(row=0, column=1, padx=10, pady=10)

    def open_add_details_window(self):
        """Open a new window for adding details."""
        add_details_window = tk.Toplevel(self.root)
        add_details_window.title("Add Details")
        add_details_window.geometry("500x500")  # Set window size to 500x500
        self.create_gui(add_details_window)

    def open_view_invoices_window(self):
        """Open a new window to view all invoices."""
        view_invoices_window = tk.Toplevel(self.root)
        view_invoices_window.title("View All Invoices")
        view_invoices_window.geometry("500x500")  # Set window size to 500x500

        if not self.bookstore.invoices:
            tk.Label(view_invoices_window, text="No invoices found.").pack(pady=20)
            return

        invoices = "\n".join([
            f"Invoice {inv.invoice_nbr}: {inv.customer.name} bought {inv.stock.name} - Total: £{inv.invoice():.2f}"
            for inv in self.bookstore.invoices
        ])
        tk.Label(view_invoices_window, text=invoices, justify="left").pack(pady=20)

    def create_gui(self, window):
        """Create the GUI for adding details."""
        padx, pady = 5, 5

        # Customer input form
        tk.Label(window, text="Customer Name").grid(row=0, column=0, padx=padx, pady=pady, sticky="w")
        self.customer_name_entry = tk.Entry(window)
        self.customer_name_entry.grid(row=0, column=1, padx=padx, pady=pady)

        tk.Label(window, text="Phone Number").grid(row=1, column=0, padx=padx, pady=pady, sticky="w")
        self.customer_phone_entry = tk.Entry(window)
        self.customer_phone_entry.grid(row=1, column=1, padx=padx, pady=pady)

        tk.Label(window, text="Email").grid(row=2, column=0, padx=padx, pady=pady, sticky="w")
        self.customer_email_entry = tk.Entry(window)
        self.customer_email_entry.grid(row=2, column=1, padx=padx, pady=pady)

        tk.Button(window, text="Add Customer", command=self.add_customer).grid(row=3, column=1, padx=padx, pady=pady, sticky="e")

        # Bookstore input form
        tk.Label(window, text="Book Name").grid(row=4, column=0, padx=padx, pady=pady, sticky="w")
        self.book_name_entry = tk.Entry(window)
        self.book_name_entry.grid(row=4, column=1, padx=padx, pady=pady)

        tk.Label(window, text="Author").grid(row=5, column=0, padx=padx, pady=pady, sticky="w")
        self.book_author_entry = tk.Entry(window)
        self.book_author_entry.grid(row=5, column=1, padx=padx, pady=pady)

        tk.Label(window, text="Price").grid(row=6, column=0, padx=padx, pady=pady, sticky="w")
        self.book_price_entry = tk.Entry(window)
        self.book_price_entry.grid(row=6, column=1, padx=padx, pady=pady)

        tk.Button(window, text="Add Book", command=self.add_book).grid(row=7, column=1, padx=padx, pady=pady, sticky="e")

        # Order placement
        tk.Label(window, text="Select Customer").grid(row=8, column=0, padx=padx, pady=pady, sticky="w")
        self.customer_dropdown = ttk.Combobox(window)
        self.customer_dropdown.grid(row=8, column=1, padx=padx, pady=pady)

        tk.Label(window, text="Select Book").grid(row=9, column=0, padx=padx, pady=pady, sticky="w")
        self.book_dropdown = ttk.Combobox(window)
        self.book_dropdown.grid(row=9, column=1, padx=padx, pady=pady)

        tk.Button(window, text="Place Order", command=self.place_order).grid(row=10, column=1, padx=padx, pady=pady, sticky="e")

        # Shipping options
        self.urgent_shipping_var = tk.BooleanVar()
        tk.Checkbutton(window, text="Urgent Shipping", variable=self.urgent_shipping_var).grid(row=11, column=0, padx=padx, pady=pady, sticky="w")
        tk.Button(window, text="Calculate Shipping", command=self.calculate_shipping).grid(row=11, column=1, padx=padx, pady=pady, sticky="e")

        # Generate Invoice Button
        tk.Button(window, text="Generate Invoice", command=self.generate_invoice).grid(row=12, column=1, padx=padx, pady=pady, sticky="e")

    def add_customer(self):
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        if name and phone and email:
            customer = Customer(name, phone, email)
            self.customers.append(customer)
            self.update_customer_dropdown()
            messagebox.showinfo("Success", "Customer added successfully!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def add_book(self):
        name = self.book_name_entry.get()
        author = self.book_author_entry.get()
        price = self.book_price_entry.get()
        if name and author and price:
            try:
                price = float(price)
                book = Stock(name, author, price)
                self.books.append(book)
                self.update_book_dropdown()
                messagebox.showinfo("Success", "Book added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Price must be a valid number!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def update_customer_dropdown(self):
        self.customer_dropdown["values"] = [c.name for c in self.customers]

    def update_book_dropdown(self):
        self.book_dropdown["values"] = [b.name for b in self.books]

    def place_order(self):
        customer_name = self.customer_dropdown.get()
        book_name = self.book_dropdown.get()

        customer = next((c for c in self.customers if c.name == customer_name), None)
        book = next((b for b in self.books if b.name == book_name), None)

        if customer and book:
            order = Order(customer, book)
            self.orders.append(order)
            messagebox.showinfo("Success", "Order placed successfully!")
        else:
            messagebox.showerror("Error", "Select both a customer and a book!")

    def calculate_shipping(self):
        if not self.orders:
            messagebox.showerror("Error", "No orders to calculate shipping for!")
            return

        is_urgent = self.urgent_shipping_var.get()
        order = self.orders[-1]
        shipping = Shipping(order, datetime.date.today())
        cost = shipping.calc_ship_cost(is_urgent)
        shipping.set_ship_cost(cost)
        messagebox.showinfo("Success", f"Shipping cost calculated: £{cost:.2f}")

    def generate_invoice(self):
        if not self.orders:
            messagebox.showerror("Error", "No orders placed to generate an invoice!")
            return

        order = self.orders[-1]
        is_urgent = self.urgent_shipping_var.get()
        shipping = Shipping(order, datetime.date.today())
        shipping_cost = shipping.calc_ship_cost(is_urgent)

        total_cost = order.stock.price + shipping_cost

        invoice = Invoice(order.customer, order.stock, shipping_cost, total_cost)
        self.bookstore.invoices.append(invoice)

        # Save invoice to CSV
        print("Debug: Saving invoice to CSV")  # Debug statement
        with open("invoices.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                invoice.invoice_nbr,
                invoice.customer.name,
                invoice.customer.phone,
                invoice.customer.email,
                invoice.stock.name,
                invoice.stock.price,
                invoice.shipping_cost,
                invoice.invoice()
            ])

        messagebox.showinfo("Success", f"Invoice generated successfully! Total: £{invoice.invoice():.2f}")
        print("Debug: Invoice generated successfully!")  # Debug statement

        print("Debug: Checking invoices...")  # Debug statement
        if not self.bookstore.invoices:
            print("Debug: No invoices found.")  # Debug statement
            return

        invoices = "\n".join([
            f"Invoice {inv.invoice_nbr}: {inv.customer.name} bought {inv.stock.name} - Total: £{inv.invoice():.2f}"
            for inv in self.bookstore.invoices
        ])
        tk.Label(view_invoices_window, text=invoices, justify="left").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookOrderingApp(root)
    root.mainloop()
