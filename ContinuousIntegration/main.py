class DiningExperienceManager:
    def __init__(self):
        self.menu = {
            "Chinese Food": 10,
            "Italian Food": 12,
            "Pastries": 8,
            "Chef's Specials": 15,
        }
        self.special_category = "Especiales del Chef"
        self.max_order_quantity = 100

    def display_menu(self):
        print("======= Menu =======")
        for item, price in self.menu.items():
            print(f"{item}: ${price}")
        print("=====================")

    def validate_quantity(self, quantity):
        try:
            quantity = int(quantity)
            if quantity > 0:
                return quantity
            else:
                raise ValueError("The quantity must be a positive integer greater than zero.")
        except ValueError:
            raise ValueError("The quantity must be a positive integer greater than zero.")

    def calculate_cost(self, order):
        total_cost = 0
        for item, quantity in order.items():
            price = self.menu[item]
            total_cost += price * quantity

        if len(order) > 5:
            total_cost *= 0.9  # 10% de descuento

        if len(order) > 10:
            total_cost *= 0.8  # 20% de descuento

        return total_cost

    def apply_special_offers(self, total_cost):
        if total_cost > 100:
            total_cost -= 25
        elif total_cost > 50:
            total_cost -= 10
        return total_cost

    def apply_special_category_surcharge(self, order):
        for item in order.keys():
            if item in self.special_category:
                return True
        return False

    def validate_availability(self, order):
        for item in order.keys():
            if item not in self.menu:
                return False
        return True

    def manage_order(self):
        order = {}
        print("Welcome to our gastronomic experience!")
        self.display_menu()
        while True:
            item = input("Enter the name of the food you wish to order (or 'finish' to finalize the order):")
            if item.lower() == "finish":
                break

            if item not in self.menu:
                print("We are sorry! The selected meal is not available in our menu. Please select another one.")
                continue

            quantity = input("Enter the quantity you wish to order: ")
            try:
                quantity = self.validate_quantity(quantity)
                if quantity + sum(order.values()) > self.max_order_quantity:
                    print("We are sorry! The maximum order quantity is 100. Please adjust the quantity.")
                else:
                    order[item] = quantity
            except ValueError as e:
                print(e)

        if not order:
            print("The order has been cancelled.")
            return -1

        print("\nOrder summary:")
        for item, quantity in order.items():
            print(f"{item} x {quantity}")

        total_cost = self.calculate_cost(order)
        if self.apply_special_category_surcharge(order):
            total_cost *= 1.05  # 5% de recargo para la categoría especial

        total_cost = self.apply_special_offers(total_cost)

        print(f"\nTotal cost: ${total_cost}")
        confirm = input("Confirm the order? (Y/N): ")
        if confirm.lower() == "y":
            return total_cost
        else:
            print("The order has been cancelled.")
            return -1


if __name__ == "__main__":
    dem = DiningExperienceManager()
    total_cost = dem.manage_order()
    if total_cost != -1:
        print("Thank you for your order! Enjoy your dining experience.")
