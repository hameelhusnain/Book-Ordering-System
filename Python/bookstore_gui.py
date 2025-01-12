import tkinter as tk
from tkinter import messagebox
import csv
import datetime
from bookstore_core import Customer, Stock, Order, Shipping, Invoice, BookStore

class BookOrderingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Ordering System")
        self.root.geometry("600x600")
        self.root.configure(bg="#d4a373")
        self.bookstore = BookStore()
        self.orders = []

        self.customer_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.book_name_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.price_var = tk.DoubleVar()
        self.urgent_shipping_var = tk.BooleanVar()

        self.current_customer = None
        self.current_book = None

        self.setup_ui()

    def setup_ui(self):
        tk.Button(self.root, text="Add Details", command=self.add_details_window, bg="#fefae0", fg="black", width=20, height=2).pack(pady=20)
        tk.Button(self.root, text="View All Invoices", command=self.view_invoices_window, bg="#fefae0", fg="black", width=20, height=2).pack(pady=20)

    def add_details_window(self):
        details_window = tk.Toplevel(self.root)
        details_window.title("Add Details")
        details_window.geometry("800x800")
        details_window.configure(bg="#d4a373")

        tk.Label(details_window, text="Customer Name:", bg="#d4a373", fg="white").pack(pady=5)
        tk.Entry(details_window, textvariable=self.customer_var, bg="#fefae0", fg="black", width=40).pack(pady=5)

        tk.Label(details_window, text="Phone Number:", bg="#d4a373", fg="white").pack(pady=5)
        tk.Entry(details_window, textvariable=self.phone_var, bg="#fefae0", fg="black", width=40).pack(pady=5)

        tk.Label(details_window, text="Email:", bg="#d4a373", fg="white").pack(pady=5)
        tk.Entry(details_window, textvariable=self.email_var, bg="#fefae0", fg="black", width=40).pack(pady=5)

        tk.Button(details_window, text="Add Customer", command=self.add_customer, bg="#fefae0", fg="black").pack(pady=10)

        tk.Label(details_window, text="Book Name:", bg="#d4a373", fg="white").pack(pady=5)
        tk.Entry(details_window, textvariable=self.book_name_var, bg="#fefae0", fg="black", width=40).pack(pady=5)

        tk.Label(details_window, text="Author:", bg="#d4a373", fg="white").pack(pady=5)
        tk.Entry(details_window, textvariable=self.author_var, bg="#fefae0", fg="black", width=40).pack(pady=5)

        tk.Label(details_window, text="Price:", bg="#d4a373", fg="white").pack(pady=5)
        tk.Entry(details_window, textvariable=self.price_var, bg="#fefae0", fg="black", width=40).pack(pady=5)

        tk.Button(details_window, text="Add Book", command=self.add_book, bg="#fefae0", fg="black").pack(pady=10)

        tk.Checkbutton(details_window, text="Urgent Shipping", variable=self.urgent_shipping_var, bg="#d4a373", fg="white").pack(pady=5)

        tk.Button(details_window, text="Calculate Shipping", command=self.calculate_shipping, bg="#fefae0", fg="black").pack(pady=10)
        tk.Button(details_window, text="Place Order", command=self.place_order, bg="#fefae0", fg="black").pack(pady=10)
        tk.Button(details_window, text="Generate Invoice", command=self.generate_invoice, bg="#fefae0", fg="black").pack(pady=10)

    def add_customer(self):
        customer_name = self.customer_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()

        if customer_name and phone and email:
            if not self.current_customer or (self.current_customer.name != customer_name or self.current_customer.phone != phone or self.current_customer.email != email):
                self.current_customer = Customer(customer_name, phone, email)
                messagebox.showinfo("Success", "Customer details added successfully!")
            else:
                messagebox.showinfo("Info", "Customer details already added!")
        else:
            messagebox.showerror("Error", "Please fill all the customer details!")

    def add_book(self):
        book_name = self.book_name_var.get()
        author = self.author_var.get()
        price = self.price_var.get()

        if book_name and author and price:
            if not self.current_book or (self.current_book.name != book_name or self.current_book.author != author or self.current_book.price != price):
                self.current_book = Stock(book_name, author, price)
                messagebox.showinfo("Success", "Book details added successfully!")
            else:
                messagebox.showinfo("Info", "Book details already added!")
        else:
            messagebox.showerror("Error", "Please fill all the book details!")

    def place_order(self):
        if self.current_customer and self.current_book:
            order = Order(self.current_customer, self.current_book)
            self.orders.append(order)
            messagebox.showinfo("Success", "Order placed successfully!")
        else:
            messagebox.showerror("Error", "Add customer and book details first!")

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

        invoice = Invoice(f"INV{len(self.bookstore.invoices) + 1:04d}", order.customer, order.stock, shipping)
        self.bookstore.invoices.append(invoice)

        # Save invoice to CSV
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

    def view_invoices_window(self):
        view_invoices_window = tk.Toplevel(self.root)
        view_invoices_window.title("View All Invoices")
        view_invoices_window.geometry("600x600")
        view_invoices_window.configure(bg="#d4a373")

        if not self.bookstore.invoices:
            tk.Label(view_invoices_window, text="No invoices found.", bg="#d4a373", fg="white").pack(pady=20)
            return

        invoices = "\n".join([
            f"Invoice {inv.invoice_nbr}: {inv.customer.name} bought {inv.stock.name} - Total: £{inv.invoice():.2f}"
            for inv in self.bookstore.invoices
        ])
        tk.Label(view_invoices_window, text=invoices, justify="left", bg="#d4a373", fg="white").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookOrderingApp(root)
    root.mainloop()
