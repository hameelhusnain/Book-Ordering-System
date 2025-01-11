import datetime
#Rhis is Base class: represent the base classs person name email.
class Person:
    def __init__(self, name: str, phone: str, email: str):
        self._name = name
        self._phone = phone
        self._email = email
    @property
    def name(self):
        return self._name
    @property
    def phone(self):
        return self._phone
    @property
    def email(self):
        return self._email
# Custmer classs **inheriting Person**
class Customer(Person):
    """Represents a customer, inheriting from Person."""
    def __init__(self, name: str, phone: str, email: str):
        super().__init__(name, phone, email)
# Base Class: for product
class Product:
    """Represents a product with name and price."""
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price
    @property
    def name(self):
        return self._name
    @property
    def price(self):
        return self._price
# this is stock class which representing a inherting book 
class Stock(Product):
    def __init__(self, name: str, author: str, price: float):
        super().__init__(name, price)
        self._author = author
    @property
    def author(self):
        return self._author
# this is order classs which represent an order and a book
class Order:
    def __init__(self, customer: Customer, stock: Stock):
        self._customer = customer
        self._stock = stock
    @property
    def customer(self):
        return self._customer
    @property
    def stock(self):
        return self._stock
# this is shipping classs which handels shipping cost and class
class Shipping:
    count_urgent = 0
    def __init__(self, order: Order, ship_date: datetime.date):
        self._order = order
        self._ship_date = ship_date
        self._ship_cost = 0.0
    @property
    def ship_date(self):
        return self._ship_date
    @property
    def ship_cost(self):
        return self._ship_cost
    def set_ship_cost(self, cost: float):
#Sets the shipping cost
        self._ship_cost = cost
    def calc_ship_cost(self, is_urgent: bool):
#Calculates the shipping cost
        if is_urgent:
            Shipping.count_urgent += 1
            return 5.45
        return 3.95
# invoice generate here for orders
class Invoice:
    def __init__(self, invoice_nbr: str, stock: Stock, ship_order: Shipping):
        self._invoice_nbr = invoice_nbr
        self._stock = stock
        self._ship_order = ship_order
    @property
    def invoice_nbr(self):
        return self._invoice_nbr
    def invoice(self):
        return self._stock.price + self._ship_order.ship_cost
# BookStore Class stores and search invoice
class BookStore:
    def __init__(self):
        self._invoices = []
    @property
    def invoices(self):
        return self._invoices
    def search_invoice(self, nbr: str):
        for invoice in self._invoices:
            if invoice.invoice_nbr == nbr:
                return invoice
        print("Invoice not found")
# Test Class
class Test:
#Tests all component
    @staticmethod
    def main():

        customer1 = Customer("Alice", "1234567890", "alice@example.com")
        customer2 = Customer("Bob", "0987654321", "bob@example.com")
        customer3 = Customer("Charlie", "5555555555", "charlie@example.com")

        stock1 = Stock("Book1", "Author1", 20.0)
        stock2 = Stock("Book2", "Author2", 15.0)
        stock3 = Stock("Book3", "Author3", 25.0)

        order1 = Order(customer1, stock1)
        order2 = Order(customer2, stock2)
        order3 = Order(customer3, stock3)

        shipping1 = Shipping(order1, datetime.date.today())
        shipping2 = Shipping(order2, datetime.date.today())
        shipping3 = Shipping(order3, datetime.date.today())

        shipping1.set_ship_cost(shipping1.calc_ship_cost(True))
        shipping2.set_ship_cost(shipping2.calc_ship_cost(False))
        shipping3.set_ship_cost(shipping3.calc_ship_cost(True))

        invoice1 = Invoice("INV0001", stock1, shipping1)
        invoice2 = Invoice("INV0002", stock2, shipping2)
        invoice3 = Invoice("INV0003", stock3, shipping3)

        bookstore = BookStore()
        bookstore.invoices.append(invoice1)
        bookstore.invoices.append(invoice2)
        bookstore.invoices.append(invoice3)

        print(f"Number of urgent shipments: {Shipping.count_urgent}")
        print(f"Invoice 1 total cost: {invoice1.invoice():.2f}")
        print(f"Invoice 2 total cost: {invoice2.invoice():.2f}")
        print(f"Invoice 3 total cost: {invoice3.invoice():.2f}")

        bookstore.search_invoice("INV0004")

if __name__ == "__main__":
    Test.main()
