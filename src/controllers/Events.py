from urllib.error import HTTPError
from flask import request, jsonify, Blueprint
from httplib2 import Http
from marshmallow import Schema, fields, ValidationError, validate

def EventsBluePrint(calendar):

    Events = Blueprint('Events',__name__)
    
    class CreateEventAttendee_Request_Schema(Schema):
        DisplayName = fields.String(required=True)
        Email = fields.Email(required=False)
    
    class CreateEvent_Request_Schema(Schema):
        Title = fields.String(required=True)
        Location = fields.String()
        Category = fields.String(validate=validate.OneOf(['Team Meeting', 'Lecture']), required = True)
        Period = fields.String(validate=validate.OneOf(['Semester', 'Break']), required = True)
        Start = fields.DateTime(required = True)
        End = fields.DateTime(required = True)
        Attendees = fields.List(fields.Nested(CreateEventAttendee_Request_Schema()))
        
        
    @Events.route("/event/create", methods=["POST"])
    def CreateEvent():
        request_data = request.json
        
        try:
            result = CreateEvent_Request_Schema().load(request_data)
            eventAttendees = []
            event = {
                'summary': result['Title'],
                'location': result['Location'],
                'extendedProperties': { 
                    'private': {
                    'period': result['Period'], 
                    'category': result['Category']
                    #'attendees': eventAttendees
                    }
                },
                'start': {
                    "dateTime": result['Start'].strftime("%Y-%m-%dT%H:%M:%S"),
                    "timeZone": "Europe/Dublin"
                },
                'end': {
                    "dateTime": result['End'].strftime("%Y-%m-%dT%H:%M:%S"),
                    "timeZone": "Europe/Dublin"
                }
            }
            for i, result_attendee in enumerate(result['Attendees']):
                event['extendedProperties']['private'][f'attendee{i}'] = f"{result_attendee['DisplayName']}-{result_attendee['Email']}"
                # attendee = {
                #     'displayName': result_attendee['DisplayName'],
                #     'email': result_attendee['Email']
                # }
                #eventAttendees.append(attendee)
            if calendar.create_event(event):
                return jsonify({"message": "Success"}), 200
            else:
                return jsonify({"message": "error"}), 400
        except ValidationError as err:
            return jsonify(err.messages), 400
        except Exception as err:
            return jsonify(err), 400
            

    @Events.route("/event/read_all", methods=["GET"])
    def ReadAlLEvents():
        events = calendar.read()
        
        events_response = []
        for event in events:
            event_attendees = []
            # current_event_attendees = getValueFromDictKey(event, 'extendedProperties', 'private', 'attendees')
            # if current_event_attendees != None:
            #     for event_attendee in current_event_attendees:
            #         attendee = {
            #             "DisplayName": getValueFromDictKey(event_attendee, 'displayName'),
            #             "Email": getValueFromDictKey(event_attendee, 'email')
            #         }
            #         event_attendees.append(attendee)
            current_event_private_variables = getValueFromDictKey(event, 'extendedProperties', 'private')
            for private_variable in current_event_private_variables:
                if private_variable not in ['period', 'category']:
                    attendee_variable = current_event_private_variables[private_variable].split('-')
                    attendee = {
                        "DisplayName": attendee_variable[0],
                        "Email": attendee_variable[1]
                    }
                    event_attendees.append(attendee)
            event_resp = {
                "Title": getValueFromDictKey(event, 'summary'),
                "Location": getValueFromDictKey(event, 'location'),
                "Category": getValueFromDictKey(event, 'extendedProperties', 'private', 'category'),
                "Period": getValueFromDictKey(event, 'extendedProperties', 'private', 'period'),
                "Start": getValueFromDictKey(event, 'start', 'dateTime'),
                "End": getValueFromDictKey(event, 'end', 'dateTime'),
                "Attendees": event_attendees
            }
            events_response.append(event_resp)
                
        return jsonify(events_response)
        
    def getValueFromDictKey(dictionary, a, b = None, c = None):
        try:
            if b == None and c == None:
                return dictionary[a]
            elif c == None:
                return dictionary[a][b]
            else:
                return dictionary[a][b][c]
        except KeyError as err:
            print(f"KeyError: {err}")
            return None
            
    
    return Events
        
    '''
    event = {
  'summary': 'Distributed Systems',
  'location': 'LB01 Lloyd Institute',
  'extendedProperties': { 
    'private': {
      'period': 'Semester', 
      'category': 'Team Meeting'
    }
  },
  "start": {
    "dateTime": "2022-02-22T14:00:00Z",
    "timeZone": "Europe/Dublin"
  },
  "end": {
    "dateTime": "2022-02-22T16:00:00Z",
    "timeZone": "Europe/Dublin"
  },
  'attendees': [
    {
      'displayName': 'L Page',
      'email': 'lpage@example.com'
    },
    {
      'displayName': 'S Brin',
      'email': 'sbrin@example.com'
    },
  ]
}

    
    

    class TimeRange(Schema):
        StartTime = fields.Time(required=True)
        EndTime = fields.Time(required=True)

    # Payload Schema for Store Initial Model API
    class StoreInitialModelSchema(Schema):
        UserId = fields.Integer(required=True)
        WorkingHours = fields.Nested(TimeRange(), required=True)
        BreakTime = fields.Nested(TimeRange(), required=True)
        TimePreference = fields.String(validate=validate.OneOf(['morning', 'afternoon', 'evening']), required=True)
        WeatherPreference = fields.String(validate=validate.OneOf(['sunny', 'none']), required=True)

    @UserModel.route("/store-initial-model", methods=["POST"])
    def StoreInitialModel():
        # Unmarshal Payload
        request_data = request.json

        try:
            result = StoreInitialModelSchema().load(request_data)
            result["WorkingHours"]["StartTime"] = result["WorkingHours"]["StartTime"].isoformat()
            result["WorkingHours"]["EndTime"] = result["WorkingHours"]["EndTime"].isoformat()
            result["BreakTime"]["StartTime"] = result["BreakTime"]["StartTime"].isoformat()
            result["BreakTime"]["EndTime"] = result["BreakTime"]["EndTime"].isoformat()
        except ValidationError as err:
            return jsonify(err.messages), 400

        try:
            database["userModel"].insert_one(result)
            return jsonify({"message": "Success"}), 200
        except Exception as e:
            return jsonify({"main_message": "Something went wrong!!", "detail_message": str(e)}), 500
    
    return UserModel

'''