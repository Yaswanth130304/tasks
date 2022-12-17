import os
import telebot
import requests
import json
import csv 

global s,v,movies,elf 
elf=[]

# TODO: 1.1 Get your environment variables 
yourkey = os.getenv("f65f7e8e")
bot_id = os.getenv("5895657172:AAENz88Q8Ltl41CJX_HXJK_RCLkJtOpT67g")


bot = telebot.TeleBot("5895657172:AAENz88Q8Ltl41CJX_HXJK_RCLkJtOpT67g")
updates = bot.get_updates()
latest_update = updates[-1]
CHAT_ID = latest_update.message.chat.id

@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    bot.reply_to(
        message, 'Hello there! I am a bot that will show movie information for you and export it in a CSV file.\n\n')
    
@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    bot.reply_to(message, 'Bye!\nHave a good time')
    


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/movie MOVIE_NAME\" command to get the details of a particular movie. For eg: \"/movie The Shawshank Redemption\"\n\n2.0. You can use \"/export\" command to export all the movie data in CSV format.\n\n3.0. You can use \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['movie'])
def getMovie(message):
    bot.reply_to(message, 'Getting movie info...')
    # TODO: 1.2 Get movie information from the API
    a = format(message.text) 
    b = a.split(' ',1)
    c = b[1]
    api_url = f"http://www.omdbapi.com/?apikey=f65f7e8e&t={c}"
    params = {
        "api_key": yourkey,
        "query": c
    }
    
    response = requests.get(api_url)
    print(response.status_code)
    data=response.json()
    #print(data)
    if(response.status_code==200):
        #photo = data['Poster']
        #print(photo)
        l = data['Poster']+'\n'+'Title : '+data['Title']+'\n'+'Year : '+data['Year']+'\n'+'Certification : '+data['Rated']+'\n'+'Date of release : '+data['Released']+'\n'+'Imdb Rating : '+data['imdbRating']
        #print(data['Title']+'\n'+data['Year'])
        # for i in range (0,4):
        global s,v,movies,elf
        s=[]
        v=['Title','Year','Rated','Released','imdbRating']
        s=[data['Title'],data['Year'],data['Rated'],data['Released'],data['imdbRating']]
        elf.append(s)
        print(s)
        bot.send_photo(message.chat.id,data['Poster'],l)
        movies = 'movies_search.csv'
        with open(movies , 'w',encoding='UTF8',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(v)
            for i in elf:
                csvwriter.writerow(i)
            # csvwriter.writerow(elf)
            # csvwriter.writerow('\n')
        #     print(l[i])
    else:
        bot.reply_to(message,'Movie Not Found')
    # TODO: 1.3 Show the movie information in the chat window
    # TODO: 2.1 Create a CSV file and dump the movie information in it  
@bot.message_handler(func=lambda message: botRunning, commands=['export'])
def getList(message):
    bot.reply_to(message, 'Generating file...')
    bot.send_document(message.chat.id,document=open(movies,'rb'))
    os.remove(movies)
    #TODO: 2.2 Send downlodable CSV file to telegram chat

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')
    
bot.infinity_polling()
