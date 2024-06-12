from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup

# Your Telegram Bot token
TOKEN = '7477703109:AAF8cUweBG32SXT95tj9xVNp1JeW21_R_-M'

# Function to scrape Quickler value
def get_quickler():
    url = 'https://olymptrade.com/platforms'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    quickler = soup.find('span', class_='header-trading-ticker__value').text
    return float(quickler)

# Function to check Quickler value and notify prediction
def check_quickler_prediction(context):
    current_quickler = get_quickler()
    if 'previous_quickler' not in context.bot_data:
        context.bot_data['previous_quickler'] = 0
        context.bot_data['direction'] = None
    else:
        previous_quickler = context.bot_data['previous_quickler']
        direction = context.bot_data['direction']
        if current_quickler > previous_quickler:
            new_direction = "up"
        elif current_quickler < previous_quickler:
            new_direction = "down"
        else:
            new_direction = direction
        if new_direction != direction:
            context.bot.send_message(context.job.context, text=f'Quickler is expected to go {new_direction}!')
            context.bot_data['direction'] = new_direction
    context.bot_data['previous_quickler'] = current_quickler

def start(update, context):
    update.message.reply_text('Hi! I am your Olymp Trade Quickler bot. I will predict whether Quickler will go up or down after 5 seconds.')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Schedule job to check Quickler value every 5 seconds
    job_queue = updater.job_queue
    job_queue.run_repeating(check_quickler_prediction, interval=5, context=None)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
