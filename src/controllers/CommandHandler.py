from flask import request, jsonify, Blueprint
from marshmallow import Schema, fields, ValidationError, validate
from dialogflow_fulfillment import WebhookClient
import datetime
from src.services.models.model import PredictionModel
import json

def CommandBluePrint(database):

    command_handler = Blueprint('command_handler',__name__)

    @command_handler.route("/command-handler", methods=["POST"])
    def CommandHandler():
        # Parse Payload
        req = request.get_json(force=True)
        action = req.get('queryResult').get('intent')
        print(action['displayName'], flush=True)
        if action['displayName'].lower() == "schedule":
            params = req.get('queryResult').get('parameters')
            print(params, flush=True)
            date  = params['date-time']
            weekdate  = params['date-period']
            if date:
                startdate = date.split('T')[0]
            else:
                startdate = weekdate['startDate'].split('T')[0]
            
            meet  = params['meeting-type']

            date_time_obj = datetime.datetime.strptime(startdate, "%Y-%m-%d")
            weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
            day = weekDays[date_time_obj.weekday()]

            meet = meet.lower()
            if meet == "ase":
                meet = "ASE GROUP MEETING"
            if meet == "adaptive":
                meet == "Adaptive Apps Meeting"

            model = PredictionModel(database)
            userSolution = {'Title': meet,'Category':'Team Meeting', 'Period': 'Semester', 'Day' : day}
            print(userSolution, flush=True)
            solutions = model.findSolutions(userSolution)
            for sol in solutions:
                print("sol -> ",sol, flush=True)

            # Create an instance of the WebhookClient
            agent = WebhookClient(req)
            agent.add(json.dumps(solutions))
            
        return agent.response
    
    return command_handler