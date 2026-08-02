class Bill:

    def __init__(self, amount):
        self.amount = amount

    def calculate_total(self):
        return self.amount

    def __str__(self):
        return f"Amount is {self.amount}"

class ElectricityBill(Bill):

    def __init__(self, units_consumed, rate_per_unit):
        self.units_consumed = units_consumed
        self.rate_per_unit = rate_per_unit
        super().__init__(self.calculate_total())

    def calculate_total(self):
        return self.rate_per_unit * self.units_consumed

class WaterBill(Bill):

    def __init__(self, amount):
        super().__init__(amount)

class InternetBill(Bill):

    def __init__(self, amount, gst_percent):
        super().__init__(amount)
        self.gst_percent = gst_percent

    def calculate_total(self):
        return self.amount + (self.amount * self.gst_percent / 100)

class Resident:

    def __init__(self, name, room_number):
        self.name = name
        self.room_number = room_number
        self.bills = []

    def add_bill(self, bill):
        self.bills.append(bill)

    def total_due(self):
        total = 0
        for bill in self.bills:
            total += bill.calculate_total()
        return total

    def __str__(self):
        return f"Room {self.room_number} - {self.name}: ₹{self.total_due()} due"

    def __lt__(self, other):
        return self.total_due() < other.total_due()

class Hostel:
    def __init__(self):
        self.residents = []

    def add_resident(self, resident):
        self.residents.append(resident)

    def show_all_dues(self):
        for resident in self.residents:
            print(resident)

    def total_collection(self):
        total = 0
        for resident in self.residents:
            total += resident.total_due()
        return total

hostel = Hostel()

def validate_input(number):
    if number.isdigit():
        return True
    else:
        return False
    
while True:
    print("Menu:\n1.Add Resident\n2.Add Bill to a Resident\n3.View one's resident Dues\n4.View all dues\n5. View Total Collection\n0.Exit")
    task = (input("Enter Task Number: "))
    if validate_input(task):
        task = int(task)
        if task == 0:
            break
        elif task == 1:
            name = input("Enter Resident Name: ").strip()
            room_number = input("Enter Resident Room Number: ").strip()
            if validate_input(room_number):
                hostel.add_resident(Resident(name, room_number))
            else:
                print("Room number is not a number")
        elif task == 2:
            name = input("Enter Resident Name: ").strip()
            current_resident = None
            for resident in hostel.residents:
                if resident.name.lower() == name.lower():
                    current_resident = resident
            if current_resident != None:
                print("1. Electricity\n2. Water\n3. Internet")
                bill = input("Which Bill you want to Add: ")
                if validate_input(bill):
                    bill = int(bill)
                    if bill == 1:
                        units = input("Enter Units Consumed: ")
                        rate = input("Rate Per Unit: ")
                        if validate_input(units) and validate_input(rate):
                            current_resident.add_bill(ElectricityBill(int(units), float(rate)))
                        else:
                            print("Units and rate should be number")
                    elif bill == 2:
                        amount = input("Enter bill amount: ")
                        if validate_input(amount):
                            current_resident.add_bill(WaterBill(float(amount)))
                        else:
                            print("Amount should be a number")
                    elif bill == 3:
                        amount = input("Enter bill amount: ")
                        gst_percent = input("Enter Gst Percent: ")
                        if validate_input(amount) and validate_input(gst_percent):
                            current_resident.add_bill(InternetBill(float(amount), float(gst_percent)))
                    else:
                        print("Not a correct input")
                else:
                    print("Enter a Number")
            else:
                print("Resident Not found")
        elif task == 3:
            name = input("Enter Resident Name: ").strip()
            current_resident = None
            for resident in hostel.residents:
                if resident.name.lower() == name.lower():
                    current_resident = resident
            if current_resident != None:
                print(current_resident)
            else:
                print("Resident not found")  
        elif task == 4:
            if len(hostel.residents) > 0:
                hostel.show_all_dues()
            else:
                print("No residents yet")
        elif task == 5:
            print(hostel.total_collection())
        else:
            continue
    else:
        print("Enter a Number")