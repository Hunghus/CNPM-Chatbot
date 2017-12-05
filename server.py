from flask import Flask, request
import json
import requests
import os
app = Flask(__name__)


# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = ''
token = "EAACwhRBVJUwBAGy5FpUvLkax1pmOs1YWOb8F4KgVaZBSrYGyYmZBz99iPka644ny7RQfQ5rv2ZCbpyQ90nFguMlIt0rJuk31YruYWGK60JCbYBU1EcmNBNZBqU4JRPnY2AKCTLelcbuUGWM3YoO2ZAG4RDyCeZBZBVaWFP1W4lk0QZDZD"
very_token = "12345"


@app.route('/')
def handle_defaule():
  return "OK"

@app.route('/webhook', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  if request.args.get('hub.verify_token', '') == very_token :
    return request.args.get('hub.challenge','')
    # return request.args.get('hub.challenge', '')
  else:
    print "Verification failed!"
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
  print "Handling Messages"
  payload = request.get_data()
  print payload
  for sender, message in messaging_events(payload):
    print "Incoming from %s: %s" % (sender, message)
    send_message(PAT, sender, message)
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": "kkkkkkkk"}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text

if __name__ == '__main__':
  app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
