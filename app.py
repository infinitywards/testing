import os

from flask import Flask, Response, request, render_template
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

# Pull in configuration from system environment variables
TWILIO_ACCOUNT_SID = "AC947d59f1edf12eeb95a35920a8186762"
TWILIO_AUTH_TOKEN = "5e3c96bdc7ed66bc9d0320ea15be1136"
TWILIO_PHONE_NUMBER = "+12022171993"

# create an authenticated client that can make requests to Twilio for your
# account.
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Create a Flask web app
app = Flask(__name__)


# Render the home page
@app.route('/')
def index():
    return render_template('index.html')


# Handle a POST request to send a text message. This is called via ajax
# on our web page
@app.route('/message', methods=['POST'])
def message():
    # Send a text message to the number provided
    client.messages.create(
        to=request.form['to'],
        from_=TWILIO_PHONE_NUMBER,
        body='Good luck on your Twilio quest!'
    )

    # Return a message indicating the text message is enroute
    return 'Message on the way!'


# Handle a POST request to make an outbound call. This is called via ajax
# on our web page
@app.route('/call', methods=['POST'])
def call():
    # Make an outbound call to the provided number from your Twilio number
    client.calls.create(
        to=request.form['to'],
        from_=TWILIO_PHONE_NUMBER,
        url='http://demo.twilio.com/docs/voice.xml'
    )

    # Return a message indicating the call is coming
    return 'Call inbound!'


# Generate TwiML instructions for an outbound call
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    response = VoiceResponse()
    response.say('Hello there! You have successfully configured a web hook.')
    response.say('Good luck on your Twilio quest!', voice='woman')
    return Response(str(response), mimetype='text/xml')


if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)
