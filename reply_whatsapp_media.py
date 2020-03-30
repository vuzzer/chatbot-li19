from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import urllib


app = Flask(__name__)


GOOD_BOY_URL = "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"

@app.route("/")
def hello():
    return "hello world"

@app.route("/depannage", methods=["GET", "POST"])
def depannage():
    response = MessagingResponse()
    response.message("Docteur Li👨🏿‍⚕️, votre informateur et assistant\nsur la situation du covid-19.\nJe serai disponible aujourd'hui.\nJe suis encore en phase d'apprentissage")
    response.message('Le coronavirus est une réalité en CI,\nprotegeons-nous en nous tenant à une\n distance d\'au moins 1 mètre les uns des autres.')

    return str(response)

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    #Grab the message of user
    user_msg = urllib.parse.quote(request.form['Body'])

    #words that initialize conversation
    init_msg = ['salut', 'hi', 'bonjour', 'bonsoir', 'hello', 'good morning', 'good afternoon', 'Salut', 'SALUT', 'BONJOUR', 'BONSOIR','HI', 'HELLO', 'GOOD MORNING', 'Salut', 'Hi', 'Bonjour', 'Bonsoir', 'Hello', 'salut Li', 'bonjour Li', 'bonsoir Li', "salut li", "bonjour li", "bonsoir li", "Salut Li", "Bonjour Li", "Bonsoir Li", "Salut li", "Bonjour li", "Bonsoir li"]

    option_msg = ['1', '2', '3', '4', '5']



    response = MessagingResponse()

    num_media = int(request.values.get("NumMedia"))

    #inbound message don't contain media file
    if not num_media:

        #Verify if the message of user is greeting
        if user_msg in init_msg and user_msg is not "1":
            response.message("Salut, je suis docteur Li👨🏿‍⚕️ ton informateur.\npour le moment je suis pas assistant médical.\ntape 0 pour recevoir les infos \nsur la situation du covid-19 en CI et dans le monde.\nBientôt je serai disponible selon des plages horaires.")

            #send information about covid to end-user
        elif user_msg == "0":
            response.message("Connaitre l'actualité sur le covid-19 en CI  et dans le monde,\n tapez \n 1: nombre de contaminés\
            en CI \n2: ville contaminés \n3: les décisions gouvernementales \n4: les fakes news \n5: info dans le monde")
            """   else:
                    msg = response.message("Oups🙊! je suis encore en phase d'apprentissage je peux ne pas comprendre ce que tu me dis.\
                    Mais on peut aller étape par étape? si oui tape juste 1") """

        elif user_msg in option_msg:
            msg = dialogflow(user_msg)
            response.message(msg)
            
        else:
            response.message("Docteur Li👨🏿‍⚕️! content de te lire.\nJe peux t'aider?.\nTape 0 pour voir mes services.\nBientôt je serai disponible selon des plages horaires.")

    else:
        response.message("Oups🙊! je suis encore en phase d'apprentissage j'arrive pas à interpréter les images ou audios.\nSi t'es daccord tape 0")
    #msg = response.message("Thanks for the image. Here's one for you!")
    #msg.media(GOOD_BOY_URL)
    return str(response)



def dialogflow(option_msg):

    switch = {
        "1": info_seek,
        "2": city_infected,
        "3": formal_decision,
        "4": fake_new,
        "5": news_world
    }

    news = switch.get(option_msg, "Oups🙊! je suis encore en phase d'apprentissage\n je peux ne pas comprendre ce que tu me dis.\
                    \nMais on peut aller étape par étape? si oui tape juste 0")        
    return news()
 
def info_seek():
    msg_seek = "La CI enregistre 25 nouveaux cas portant à 165 le nombre de cas confirmés dont 4 guéris et 1 décès\n(Officiel)"
    return msg_seek

def city_infected():
    msg_city_infected = "Desolé! pour l'instant j'ai aucune connaissances des villes contaminés a part celle Abidjan"
    return msg_city_infected

def formal_decision():
    msg_formal_decision ="Restriction de sortie du Grand Abidjan:\nException faite aux détenteurs de cartes professionnelles ou ordres de mission"
    return msg_formal_decision

def fake_new():
    msg_fake_new = "Oups🙊! pour le moment, je suis pas afféré. ça viendra."
    return msg_fake_new

def news_world():
    msg_news_world = "Trump et Poutine veulent coopérer sur le coronavirus et le pétrole.\nhhttps://www.france24.com/fr/20200330-trump-et-poutine-veulent-coop%C3%A9rer-sur-le-coronavirus-et-le-p%C3%A9trole"
    return msg_news_world





if __name__ == "__main__":
    app.run(debug = True, port="8000")
