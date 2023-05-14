import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace YOUR_BOT_TOKEN with your bot token obtained from BotFather
bot = telegram.Bot(token='5973486244:AAHULwsMWBiGfu0wXI64zb4IkfpBxLx27B0')

# Define a dictionary of menu items and their descriptions and prices
menu = {
    "peanuts": {"description": "BB Popular Peanuts/Kadalekayi - Raw, 200 g Pouch \n ", "price": 35},
    "sugar": {"description": "Madhur Sugar - Pure & Hygienic, Fine Grain, Natural, Sulphur Free, 5 kg", "price": 236},
    "atta": {"description": "Aashirvaad Atta/Godihittu - Whole Wheat, 10 kg", "price": 480},
    "poha" : {"description": "Tata Sampann High In Fibre Thick Poha - Flattened & Beaten Rice, Makes Breakfast & Teatime Snack, 500 g ", "price": 42},
    "almonds": {"description": "BB Popular Almond/Badam - Californian, Giri, 500 g Pouch \n", "price": 371},
    "maida": {"description": "BB Super Saver Maida, 1 kg", "price": 42},
    "tea": {"description": "Red Label Tea, 1 Kg ", "price": 512.5},
    "salt": {"description": "Tata Salt Vacuum Evaporated Iodised Salt - Helps Mental Development, 1 kg Pouch ", "price": 25.5},
    "perfume": {"description": "Versace Mens Dylan Blue Eau De Toilette 100 ml ", "price": 7100},
    "soap": {"description": "Kama Ayurveda Sugar Tamarind cleansing Soap - 125gm", "price": 650},
    "toothpaste": {"description": "Colgate Strong Teeth Cavity Protection with Calcium Boost (500gm x 2), India's No.1 Toothpaste  (1000 g, Pack of 2)", "price": 399},
}

def start(update, context):
    """Send a welcome message when the command /start is issued."""
    message = "Welcome to the General Store. \n Here is our inventory:\n \n Soap \n Toothpaste \n Perfume \n Atta \n Peanuts \n Sugar \n Poha \n Almond \n Maida \n Tea \n Salt \n \nPlease select an item from the inventory to place an order.\n type menu for more description"
    update.message.reply_text(message)

def show_menu(update, context):
    """Show the menu items when the user types 'menu'."""
    message = "Here are our menu items:\n\n"
    for item, details in menu.items():
        description = details['description']
        price = details['price']
        message += f"{item}: \n {description} (Price: {price} Rs.)\n \n"
    update.message.reply_text(message)

def order_food(update, context):
    """Take the user's order and send a confirmation message."""
    food = update.message.text.lower()
    if food == "menu":
        show_menu(update, context)
    elif food in menu:
        context.user_data['item'] = food
        message = f"You selected {menu[food]['description']}. The price is {menu[food]['price']} Rs. Please enter the quantity you want to order."
        update.message.reply_text(message)
    elif 'item' in context.user_data and context.user_data['item']:
        try:
            quantity = int(food)
            if quantity > 0:
                price = quantity * menu[context.user_data['item']]['price']
                context.user_data['quantity'] = quantity
                message = f"You ordered {quantity} {menu[context.user_data['item']]['description']}. The total price is {price} Rs. Do you want to confirm the order? Please answer with y or n."
            else:
                message = "Please enter a valid quantity (a positive integer)."
        except ValueError:
            message = "Please enter a valid quantity (a positive integer)."
        update.message.reply_text(message)
    elif 'quantity' in context.user_data and context.user_data['quantity']:
        if food.lower() == "y":
            price = context.user_data['quantity'] * menu[context.user_data['item']]['price']
            message = f"Thank you for your order! Your total amount is {price} Rs."
        else:
            message = "Order cancelled."
        update.message.reply_text(message)
        context.user_data.clear()
    else:
        message = "Sorry, I didn't understand your request. Please type 'menu' to see the menu items, or select an item from the menu to order."
        update.message.reply_text(message)

updater = Updater(token='5973486244:AAHULwsMWBiGfu0wXI64zb4IkfpBxLx27B0', use_context=True)
dispatcher = updater.dispatcher

# Set up command handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Set up message handlers
order_food_handler = MessageHandler(Filters.text & (~Filters.command), order_food)
dispatcher.add_handler(order_food_handler)

# Start the bot
updater.start_polling()
updater.idle()
