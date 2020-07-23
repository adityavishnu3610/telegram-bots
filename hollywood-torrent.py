from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import re
from bs4 import BeautifulSoup
import json


def echo(bot, update):

    film_name = update.message.text

    film_name = film_name.replace(' ','+').lower()
    api_req = requests.get("http://www.omdbapi.com/?t="+film_name+"&apikey=YOURAPIKEY")

    api_response = BeautifulSoup(api_req.content, 'html5lib')

    api_json = json.loads(api_response.text)

    search_keyword = api_json['Title']
    year = api_json['Year']
    search_keyword = search_keyword.replace(' ','-').lower()
    search_keyword = search_keyword.replace(":","")
    search_keyword = search_keyword.replace(".","")
    search_keyword = search_keyword.replace("?","")
    search_keyword = search_keyword.replace("'","")
    search_keyword = search_keyword + '-' + year
    search_keyword = search_keyword.lower()

    URL = 'https://THESITEYOUARESCRAPING.COM/PATH/'+search_keyword+''

    r = requests.get(URL) 
      
    soup = BeautifulSoup(r.content, 'html5lib')

    link_dict = {}

    link_index = 0

    for a in soup.find_all('a',attrs = {'class':'CLASS-NAME-IN-WHICH-YOUR-LINK-RESIDES'}, href=True):
        link_dict [link_index] = a['href']
        link_index += 1


    resolution_dict = {}

    resolution_index = 0

    for i, p_tag in enumerate(soup.find_all('a', text=True)): 
        if '.' in p_tag.get_text():
            resolution_dict [resolution_index] = p_tag.get_text()
            resolution_index += 1

    for (k,v), (k2,v2) in zip(link_dict.items(), resolution_dict.items()):
        bot.send_message(chat_id=update.message.chat_id, text=link_dict[k] + "\nResolution: " + resolution_dict[k2])


def main():
    updater = Updater('YOUR-TELEGRAM-BOT-TOKEN')
    dispatcher = updater.dispatcher
    user_message_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(user_message_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
