import pygame
from pygame.locals import *
import math
import sys
import time

class VendingMachine:
    def __init__(self):
        pygame.init()

        self.width, self.height = 1000, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Vending Machine")

        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 72)
        self.title_text = "Vending Machine"
        self.title_color = (255, 0, 0)
        self.title_angle = 0

        self.items_font = pygame.font.Font(None, 36)
        self.item_width = 300
        self.item_height = 50

        self.items = {
            "A. Coke": {"p": 1.50, "c": 5},
            "B. Chips": {"p": 1.00, "c": 10},
            "C. Chocolate": {"p": 1.25, "c": 8},
            "D. Water": {"p": 1.00, "c": 7},
            "E. Snacks": {"p": 1.75, "c": 6},
            "F. Juice": {"p": 2.00, "c": 4},
            "G. Soda": {"p": 1.50, "c": 5},
            "H. Gum": {"p": 0.75, "c": 10},
            "I. Cookies": {"p": 1.50, "c": 8},
            "J. Coffee": {"p": 2.00, "c": 3},
            "K. Tea": {"p": 1.75, "c": 5},
            "L. Energy": {"p": 2.50, "c": 4},
            "M. Fruit": {"p": 1.50, "c": 6},
            "N. Sandwich": {"p": 3.00, "c": 2},
            "O. Ice Cream": {"p": 2.50, "c": 4},
            # Add more items as needed
        }

        self.cart = []
        self.cart_amount = 0
        self.cart_state = False

        self.b = 0
        self.u_a = ""
        self.u_i = ""
        self.p_m = ""
        self.p_c = False

        self.e_a = True
        self.e_i = False

        self.popup_active = False
        self.popup_selection = 0

        self.proceed_to_amount = False

        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        if self.popup_active:
                            self.handle_popup_selection()
                        elif self.e_a:
                            self.process_amount()
                        elif self.e_i:
                            self.process_item()
                        else:
                            self.p_m = "Please enter a valid item name before pressing Enter."
                    elif event.key == K_BACKSPACE:
                        self.handle_backspace()
                    elif event.key == K_LEFT or event.key == K_RIGHT:
                        if self.popup_active:
                            self.popup_selection = (self.popup_selection + 1) % 2
                elif event.type == TEXTINPUT:
                    self.handle_text_input(event.text)
                
            if self.proceed_to_amount:
                # If the flag is set, transition to the amount entry state
                self.e_a = True
                self.e_i = False
                self.proceed_to_amount = False  # Reset the flag

            pygame.display.flip()
            self.clock.tick(60)

            self.title_color = self.calc_gradient_color()

            self.screen.fill((0, 0, 0))

            title_surface = self.title_font.render(self.title_text, True, self.title_color)
            title_rect = title_surface.get_rect(center=(self.width // 2, 50))
            self.screen.blit(title_surface, title_rect)

            if self.e_a:
                self.display_instructions_amount()
                self.display_entered_amount()
            elif self.e_i:
                self.display_instructions_item()
                self.display_entered_item()

            self.display_items()

            self.display_purchase_info()

            if self.popup_active:
                self.display_popup()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def calc_gradient_color(self):
        frequency = 0.5
        red = int(abs(math.sin(frequency * self.title_angle + 0)) * 255)
        green = int(abs(math.sin(frequency * self.title_angle + 2)) * 255)
        blue = int(abs(math.sin(frequency * self.title_angle + 4)) * 255)
        self.title_angle += 0.03
        return red, green, blue

    def process_amount(self):
        if not self.u_a:
            self.b = 0
        else:
            try:
                self.b = float(self.u_a)  # Allow decimal input for more precise amounts
            except ValueError:
                self.b = 0
                self.u_a = ""
        self.u_a = ""
        self.e_a = False
        self.e_i = True
        if self.cart_state:
            # In cart state, check if funds are sufficient to complete the purchase
            if self.b >= self.cart_amount:
                # Sufficient funds, complete the purchase
                self.complete_purchase()
            elif self.b < self.cart_amount:
                # Insufficient funds, show a message
                self.p_m = f"Insufficient funds. Please insert more money. Total Amount: ${self.cart_amount:.2f}"
                # Reset the flag for the next transaction
                self.proceed_to_amount = False
                self.show_popup()
                self.popup_selection = 0
                self.popup_active = True 
                
            else:
                self.p_m = "Invalid item code. Please choose a valid item."

            if self.proceed_to_amount:
                self.e_a = True
                self.e_i = False
                self.proceed_to_amount = False

            pygame.display.flip()
            self.clock.tick(60)

    def process_item(self):
        if self.u_i:
            matching_items = [item for item in self.items if item.lower().startswith(self.u_i.lower())]

            if matching_items:
                item = matching_items[0]
                data = self.items[item]

                if data["c"] > 0 and self.b >= data["p"]:
                    price = data["p"]
                    self.b -= price
                    data["c"] -= 1
                    self.cart.append({"item": item, "price": data["p"]})
                    self.cart_amount += data["p"]
                    self.p_m = f"Added {item} to the cart. Cart total: ${self.cart_amount:.2f}"
                    self.p_c = True
                    self.u_i = ""  # Clear entered item after purchase
                    self.show_popup()
                elif data["c"] == 0:
                    self.p_m = f"Sorry, {item} is out of stock. Please choose another item."
                else:
                    self.p_m = f"Insufficient funds. Please insert more money or choose a cheaper item."
            else:
                self.p_m = "Invalid item code. Please choose a valid item."
                

        self.u_i = ""

    def handle_backspace(self):
        if self.e_a:
            self.u_a = self.u_a[:-1]
        elif self.e_i:
            self.u_i = self.u_i[:-1]

    def handle_text_input(self, text):
        if text.isdigit() and len(self.u_a) < 10 and self.e_a:
            self.u_a += text
        elif text.isalpha() and len(self.u_i) < 30 and self.e_i:
            self.u_i += text

    def show_popup(self):
        self.popup_active = True

    def handle_popup_selection(self):
        if self.popup_selection == 0:
            # User selected "Yes"
            self.popup_active = False
            self.popup_selection = 0
            if self.cart:
                # If there are items in the cart, switch to cart state
                self.cart_state = True
                self.p_m = f"Your Cart: {len(self.cart)} items, Total Amount: ${self.cart_amount:.2f}."
            else:
                # If the cart is empty, show a message
                self.p_m = "Your cart is empty. Please add items before proceeding."
                self.e_a = False
                self.e_i = True
        elif self.popup_selection == 1:
            # User selected "No"
            self.display_thank_you_message()
            time.sleep(120)  # Display thank you message for 2 minutes
            pygame.quit()
            sys.exit()

    def complete_purchase(self):
        # Simulate processing delay
        self.p_m = "Processing... Please wait."
        pygame.display.flip()
        time.sleep(2)  # Simulate processing delay for 2 seconds

        # Dispense items and show a thank you message
        self.p_m = "Items dispensed. Thank you for your purchase!"
        self.reset_states()

    def reset_states(self):
        # Reset states for the next transaction
        self.e_a = True
        self.e_i = False
        self.popup_active = False
        self.popup_selection = 0
        self.u_a = ""
        self.u_i = ""
        self.cart = []
        self.cart_amount = 0
        self.cart_state = False

    def display_thank_you_message(self):
        # Display thank you message
        self.screen.fill((0, 0, 0))
        thank_you_surface = self.items_font.render("Thank you for using the Vending Machine!", True, (255, 255, 255))
        thank_you_rect = thank_you_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(thank_you_surface, thank_you_rect)
        pygame.display.flip()

    def display_instructions_item(self):
        instructions_surface = self.items_font.render("TYPE ITEM CODE AND PRESS ENTER", True, (255, 255, 255))
        instructions_rect = instructions_surface.get_rect(center=(self.width // 2, 100))
        self.screen.blit(instructions_surface, instructions_rect)

    def display_instructions_amount(self):
        instructions_surface = self.items_font.render("TYPE AMOUNT AND PRESS ENTER", True, (255, 255, 255))
        instructions_rect = instructions_surface.get_rect(center=(self.width // 2, 100))
        self.screen.blit(instructions_surface, instructions_rect)

    def display_entered_item(self):
        entered_item_surface = self.items_font.render(f"Item Code: {self.u_i}", True, (255, 255, 255))
        entered_item_rect = entered_item_surface.get_rect(center=(self.width // 2, 130))
        self.screen.blit(entered_item_surface, entered_item_rect)
        
    def display_entered_amount(self):
        entered_amount_surface = self.items_font.render(f"Amount: ${self.u_a}", True, (255, 255, 255))
        entered_amount_rect = entered_amount_surface.get_rect(center=(self.width // 2, 130))
        self.screen.blit(entered_amount_surface, entered_amount_rect)

    def display_items(self):
        items_per_row = 3
        row_count = (len(self.items) + items_per_row - 1) // items_per_row

        for i, (item, data) in enumerate(self.items.items()):
            color = (255, 255, 255)
            row = i // items_per_row
            col = i % items_per_row

            x = col * (self.item_width + 10) + 50
            y = row * (self.item_height + 10) + 200

            pygame.draw.rect(self.screen, (50, 50, 50), (x, y, self.item_width, self.item_height))

            max_text_width = self.item_width - 20
            max_text_height = self.item_height - 20
            font_size = 20

            item_text = f"{item} ({data['c']} left): ${data['p']:.2f}"
            item_surface = None

            while True:
                item_surface = pygame.font.Font(None, font_size).render(item_text, True, color)
                text_rect = item_surface.get_rect()
                if text_rect.width <= max_text_width and text_rect.height <= max_text_height:
                    break
                font_size -= 1

            item_rect = item_surface.get_rect(center=(x + self.item_width // 2, y + self.item_height // 2))
            self.screen.blit(item_surface, item_rect)

    def display_purchase_info(self):
        balance_surface = self.items_font.render(f"Balance: ${self.b:.2f}", True, (255, 255, 255))
        balance_rect = balance_surface.get_rect(center=(self.width // 2, self.height - 80))
        self.screen.blit(balance_surface, balance_rect)

        message_surface = self.items_font.render(self.p_m, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(message_surface, message_rect)

        if self.p_c:
            thank_you_surface = self.items_font.render("Thank you!", True, (255, 255, 255))
            thank_you_rect = thank_you_surface.get_rect(center=(self.width // 2, self.height - 20))
            self.screen.blit(thank_you_surface, thank_you_rect)

    def display_popup(self):
        popup_surface = self.items_font.render("Buy anything else?", True, (0, 0, 0))
        popup_rect = popup_surface.get_rect(center=(self.width // 2, self.height // 2 - 20))

        # Calculate gradient color for the background
        background_color = self.calc_gradient_color()
        # Increase the background size and change the color to black
        background_rect = pygame.Rect(popup_rect.x - 20, popup_rect.y - 20, popup_rect.width + 40, popup_rect.height + 80)

        # Add a background color to the popup
        pygame.draw.rect(self.screen, background_color, background_rect)

        self.screen.blit(popup_surface, popup_rect)

        yes_surface = self.items_font.render("Yes", True, (255, 255, 255) if self.popup_selection == 0 else (100, 100, 100))
        yes_rect = yes_surface.get_rect(center=(self.width // 2 - 50, self.height // 2 + 20))
        self.screen.blit(yes_surface, yes_rect)

        no_surface = self.items_font.render("No", True, (255, 255, 255) if self.popup_selection == 1 else (100, 100, 100))
        no_rect = no_surface.get_rect(center=(self.width // 2 + 50, self.height // 2 + 20))
        self.screen.blit(no_surface, no_rect)

    def show_insufficient_funds_popup(self):
        self.popup_active = True
        self.popup_selection = 0  # Reset the popup selection

        while self.popup_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.popup_active = False
                    self.display_thank_you_message()
                    time.sleep(2)
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.handle_insufficient_funds_selection()

            self.screen.fill((0, 0, 0))

            popup_surface = self.items_font.render("Insufficient funds. What would you like to do?", True, (255, 255, 255))
            popup_rect = popup_surface.get_rect(center=(self.width // 20, self.height // 2 - 20))
            pygame.draw.rect(self.screen, (100, 100, 100), (popup_rect.x - 20, popup_rect.y - 20, popup_rect.width + 40, popup_rect.height + 80))
            self.screen.blit(popup_surface, popup_rect)

            insert_money_surface = self.items_font.render("Insert Money", True, (255, 255, 255) if self.popup_selection == 0 else (100, 100, 100))
            insert_money_rect = insert_money_surface.get_rect(center=(self.width // 2 - 50, self.height // 2 + 20))
            self.screen.blit(insert_money_surface, insert_money_rect)

            buy_cheaper_surface = self.items_font.render("Buy Cheaper Product", True, (255, 255, 255) if self.popup_selection == 1 else (100, 100, 100))
            buy_cheaper_rect = buy_cheaper_surface.get_rect(center=(self.width // 2 + 50, self.height // 2 + 20))
            self.screen.blit(buy_cheaper_surface, buy_cheaper_rect)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    vending_machine = VendingMachine()