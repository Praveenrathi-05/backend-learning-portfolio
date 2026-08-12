import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Product:

    def __init__(self, name, quantity, price, reorder_threshold=10):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.reorder_threshold = reorder_threshold

    def is_low_stock(self):
        return self.quantity <= self.reorder_threshold

    def __str__(self):
        status = " - LOW STOCK" if self.is_low_stock() else ""
        return f"{self.name}: {self.quantity} units @ ₹{self.price}{status}"

    def __lt__(self, other):
        return self.quantity < other.quantity

    def to_line(self):
        return f"{self.name},{self.quantity},{self.price},{self.reorder_threshold}"


class PerishableProduct(Product):

    def __init__(self, name, quantity, price, expiry_date, reorder_threshold=10):
        super().__init__(name, quantity, price, reorder_threshold)
        self.expiry_date = expiry_date

    def __str__(self):
        product_str = super().__str__()
        return product_str + f" expires on {self.expiry_date}"

    def to_line(self):
        return super().to_line() + f",{self.expiry_date}"


def log_action(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Action: {func.__name__} - {args[1]} x{args[2]}")
        return result
    return wrapper


class Shop:

    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    @log_action
    def restock(self, name, amount):
        is_found = False
        for product in self.products:
            if product.name.lower() == name.lower():
                product.quantity += amount
                is_found = True
                print("Product restocked")
                break
        if not is_found:
            print("Product not found")

    @log_action
    def sell(self, name, amount):
        is_found = False
        for product in self.products:
            if product.name.lower() == name.lower():
                if product.quantity >= amount:
                    product.quantity -= amount
                else:
                    print("We don't have that much in stock")
                is_found = True
                break
        if not is_found:
            print("Product not found")

    def low_stock_items(self):
        i = 0
        while i < len(self.products):
            if self.products[i].is_low_stock():
                yield self.products[i]
            i += 1

    def total_inventory_value(self):
        return sum(product.quantity * product.price for product in self.products)

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            for product in self.products:
                file.write(product.to_line() + "\n")

    def load_from_file(self, filename):
        self.products = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    name, quantity, price, reorder_threshold, *extra = line.split(",")
                    if len(extra) != 0:
                        self.products.append(PerishableProduct(
                            name, int(quantity), float(price), extra[0], int(reorder_threshold)))
                    else:
                        self.products.append(Product(
                            name, int(quantity), float(price), int(reorder_threshold)))
        except FileNotFoundError:
            print("Shop is empty, Starting with empty Product list")


shop = Shop()
filename = "shop.txt"
shop.load_from_file(filename)


def add_new_product(number):
    name = input("Enter Product Name: ").strip()

    if name == "":
        print("Product name can't be empty.")
        return

    quantity = input("Enter Product Quantity: ")

    try:
        quantity = int(quantity)
    except ValueError:
        print("Product Quantity should be a integer")
        return

    if quantity <= 0:
        print("Product Quantity must be greater than zero.")
        return

    price = input("Enter Product Amount: ")

    try:
        price = float(price)
    except ValueError:
        print("Product Price should be a decimal or integer")
        return

    if price <= 0:
        print("Product Price must be greater than zero.")
        return

    reorder_threshold = input("Enter Product Reorder Threshold: ")

    try:
        reorder_threshold = int(reorder_threshold)
    except ValueError:
        print("Product Reorder Threshold should be a integer")
        return

    if reorder_threshold <= 0:
        print("Product Reorder Threshold must be greater than zero.")
        return

    if number == 2:
        expiry_date = input("Enter Product Expiry Date: ").strip()

        if expiry_date == "":
            print("Product Expiry date can't be empty.")
            return

        shop.add_product(PerishableProduct(name, quantity, price, expiry_date, reorder_threshold))
    else:
        shop.add_product(Product(name, quantity, price, reorder_threshold))

    print(f"{name} is Added to Inventory")


def restock_product():

    name = input("Enter Product Name: ").strip()

    if name == "":
        print("Product name can't be empty.")
        return

    quantity = input("Enter Product Quantity: ")

    try:
        quantity = int(quantity)
    except ValueError:
        print("Product Quantity should be a integer")
        return

    if quantity <= 0:
        print("Product Quantity must be greater than zero.")
        return

    shop.restock(name, quantity)


def sell_product():

    name = input("Enter Product Name: ").strip()

    if name == "":
        print("Product name can't be empty.")
        return

    quantity = input("Enter Product Quantity: ")

    try:
        quantity = int(quantity)
    except ValueError:
        print("Product Quantity should be a integer")
        return

    if quantity <= 0:
        print("Product Quantity must be greater than zero.")
        return

    shop.sell(name, quantity)


while True:
    print("1.Add Product (regular or perishable)\n2.Restock a Product\n3.Sell / Reduce Stock\n"
          "4.View Low-Stock Alerts\n5.View Total Inventory Value\n6.Save\n0.Exit (auto-saves before exiting)")
    try:
        task = int(input("Enter Task Number: "))
    except ValueError:
        print("Type a Number")
    else:
        if task == 1:
            print("1.Regular Product\n2.Perishable Product")
            try:
                product_type = int(input("Enter Type of Product: "))
            except ValueError:
                print("Type a number")
            else:
                if product_type in [1, 2]:
                    add_new_product(product_type)
                else:
                    print("Enter a valid product type")
        elif task == 2:
            restock_product()
        elif task == 3:
            sell_product()
        elif task == 4:
            found = False
            for product in shop.low_stock_items():
                print(product)
                found = True
            if not found:
                print("No low-stock products.")
        elif task == 5:
            print(f"₹{shop.total_inventory_value():.2f}")
        elif task == 6:
            shop.save_to_file(filename)
        elif task == 0:
            shop.save_to_file(filename)
            break
        else:
            print("Not a valid task")
