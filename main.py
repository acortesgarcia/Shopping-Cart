import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QFormLayout, QWidget, QMessageBox


class ShoppingCartApp(QMainWindow):
    def __init__(self):
        """
        Initialize the main window of the shopping cart app
        """
        super().__init__()
        self.setWindowTitle("Shopping Cart App")

        self.item_cost = {'cookie': 1.50, 'sandwich': 4.00, 'water': 1.00}
        self.shopping_cart = {}
        self.total_cost = 0

        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface of the shopping cart app
        """

        main_layout = QVBoxLayout()

        item_button_layout = QHBoxLayout()

        for item_name in self.item_cost.keys():
            item_button = QPushButton(item_name.capitalize())
            item_button.clicked.connect(lambda checked, item=item_name: self.add_to_cart(item))
            item_button_layout.addWidget(item_button)

        main_layout.addLayout(item_button_layout)

        self.quantity_input = QLineEdit()
        main_layout.addWidget(QLabel("Quantity:"))
        main_layout.addWidget(self.quantity_input)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        main_layout.addWidget(self.clear_button)

        tax_label = QLabel("Note: There is a 7% tax applied at checkout.")
        main_layout.addWidget(tax_label)

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(3)
        self.cart_table.setHorizontalHeaderLabels(["Item", "Quantity", "Price/Item"])
        self.cart_table.horizontalHeader().setStretchLastSection(True)
        self.cart_table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.cart_table)

        checkout_layout = QHBoxLayout()

        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout)
        checkout_layout.addWidget(self.checkout_button)

        main_layout.addLayout(checkout_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_to_cart(self, item):
        """
        Add an item to the shopping cart with the specified quantity

        Args:
            item (str): The name of the item to add to the shopping cart

        Raises:
            QMessageBox.warning: If an invalid quantity is entered
        """

        quantity = self.quantity_input.text().strip()

        if not quantity:
            quantity = 1
        elif not quantity.isdigit():
            QMessageBox.warning(self, "Invalid Quantity", "Invalid input. Please enter a number.")
            return
        else:
            quantity = int(quantity)

        if item in self.shopping_cart:
            self.shopping_cart[item] += quantity
        else:
            self.shopping_cart[item] = quantity

        self.total_cost += self.item_cost[item] * quantity

        self.update_cart_table()

    def update_cart_table(self):
        """
        Update the table displaying the items in the shopping cart
        """
        self.cart_table.setRowCount(0)
        for item, quantity in self.shopping_cart.items():
            price = self.item_cost[item]
            row_position = self.cart_table.rowCount()
            self.cart_table.insertRow(row_position)
            self.cart_table.setItem(row_position, 0, QTableWidgetItem(item))
            self.cart_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
            self.cart_table.setItem(row_position, 2, QTableWidgetItem(f"${price:.2f}"))

    def checkout(self):
        """
        Calculates the total cost of the items in the shopping cart with tax and display it in a message box
        """
        total_cost_with_tax = self.total_cost * 1.07
        QMessageBox.information(self, "Total Cost", f"Your total cost is ${total_cost_with_tax:.2f}")
        self.close()

    def clear_form(self):
        """
        Clear the form inputs and reset the shopping cart
        """
        self.quantity_input.clear()
        self.shopping_cart.clear()
        self.total_cost = 0
        self.update_cart_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    shopping_cart_app = ShoppingCartApp()
    shopping_cart_app.show()
    sys.exit(app.exec_())