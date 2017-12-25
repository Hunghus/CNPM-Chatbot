
#########################################################
##                                                     ##
##                                                     ##
#########################################################




from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot

chatterbot = ChatBot("Training Example")
chatterbot.set_trainer(ChatterBotCorpusTrainer)

chatterbot.train([
    # "chatterbot.corpus.english",
    # "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
    ]
)

#########################################################
##                                                     ##
##                                                     ##
#########################################################

from flask import Flask, request
import json
import os
import requests

app = Flask(__name__)

token = "EAACwhRBVJUwBAJDJngHNjeOd3kzTUkbagFLZA0ARspZAIziVzEVZAKW7FdlRCh3aHKyZBkyqaDeXeijKNlndYVhHUJBOjeQlxoS2m9qkoDeC9BPI40cUzEfnZBwOknARvStCFVaAndC6gIjc7Ng8IgJBTZBJ9hnWzErpCymXeiBLZBaHYjkDSFZC"
very_token = "12345"


########################################################


@app.route('/', methods=['GET'])
def handle_verification():
  if request.args.get('hub.verify_token', '') == very_token:
    return request.args.get('hub.challenge', '')
  else:
    return 'Error, wrong validation token'


########################################################


@app.route('/webhook', methods=['POST'])
def handle_messages():
  payload = request.get_data()
  for sender, message in messaging_events(payload):
    # message = chatterbot.get_response(message)
    # print("=====================")
    print(message)
    send_message(token, sender, "hi")
  return "ok"


########################################################


def messaging_events(payload):
  
  data = json.loads(payload)

  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      print ("NULL")


def send_message(token, recipient, text):
  
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})


#########################################################
##                                                     ##
##                                                     ##
#########################################################

if __name__ == '__main__':
  app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))