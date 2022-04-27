from flask import request, jsonify, Blueprint
from marshmallow import Schema, fields, ValidationError, validate
from dialogflow_fulfillment import WebhookClient

command_handler = Blueprint('command_handler',__name__)

@command_handler.route("/command-handler", methods=["POST"])
def CommandHandler():
    # Parse Payload
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    params = req.get('queryResult').get('parameters')
    date  = params['date-time']
    weekdate  = params['date-period']
    if date:
        startdate = date.split('T')[0]
    else:
        startdate = weekdate['startDate'].split('T')[0]
    duration = params['duration']
    meet  = params['meeting-type']
    print(params, flush=True)
    # Create an instance of the WebhookClient
    agent = WebhookClient(req)
    agent.add('Sure I will book appointment for '+meet+' in the week starting from '+startdate)
    
    return agent.response
    