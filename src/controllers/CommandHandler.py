from flask import request, jsonify, Blueprint
from marshmallow import Schema, fields, ValidationError, validate
from dialogflow_fulfillment import WebhookClient
import datetime
from src.services.models.model import PredictionModel
import json

def CommandBluePrint(database):

    command_handler = Blueprint('command_handler',__name__)

    def checkOverlap(record, solution):
        
        solution["StartTime"] = solution["Start"]
        solution["EndTime"] = datetime.datetime.strptime(solution["StartTime"], "%H:%M:%SZ") + datetime.timedelta(hours=int(float(solution["End"])))
        solution["EndTime"] = solution["EndTime"].strftime("%H:%M:%S")
        
        x = [int(record['StartTime'].replace(':','')), int(record["EndTime"].replace(':',''))]
        y = [int(solution['StartTime'].replace(':','').replace('Z','')), int(solution["EndTime"].replace(':','').replace('Z',''))]
        
        # print(x, flush=True)
        # print(y, flush=True)

        if x[0] == y[0]:
            return True
        elif x[1] == y[1]:
            return True
        elif (x[1]>y[0] and x[0]<y[1]):
            return True
        return False

    @command_handler.route("/command-handler", methods=["POST"])
    def CommandHandler():
        # Parse Payload
        req = request.get_json(force=True)
        action = req.get('queryResult').get('intent')
        
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
            
            solutions = model.findSolutions(userSolution)

            record = database["userModel"].find_one()

            finalSolutions = []
            for sol in solutions:
                isOverlap = checkOverlap(record["BreakTime"], sol)
                # print(isOverlap, flush=True)
                if not isOverlap:
                    sol['date'] = startdate
                    finalSolutions.append(sol)
            print("final sol -> ",finalSolutions, flush=True)

            # Create an instance of the WebhookClient
            agent = WebhookClient(req)
            agent.add(json.dumps(finalSolutions))
            
        return agent.response
    return command_handler