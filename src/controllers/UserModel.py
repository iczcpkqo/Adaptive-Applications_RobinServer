from flask import request, jsonify, Blueprint
from marshmallow import Schema, fields, ValidationError, validate

def UserModelBlueprint(database):

    UserModel = Blueprint('UserModel',__name__)

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
            return jsonify({"main_message": "Something went wrong!!", "detail_message": str(e)}), 400

    # Update Model Schema Payload
    class UpdateModelSchema(Schema):
        UserId = fields.Integer(required=True)
        WorkingHours = fields.Nested(TimeRange(), required=False)
        BreakTime = fields.Nested(TimeRange(), required=False)
        TimePreference = fields.String(validate=validate.OneOf(['morning', 'afternoon', 'evening']), required=False)
        WeatherPreference = fields.String(validate=validate.OneOf(['sunny', 'none']), required=False)

    @UserModel.route("/update-model", methods=["POST"])
    def UpdateModel():
        # Unmarshal Payload
        request_data = request.json

        try:
            result = UpdateModelSchema().load(request_data)
            if "WorkingHours" in result: 
                result["WorkingHours"]["StartTime"] = result["WorkingHours"]["StartTime"].isoformat()
            if "WorkingHours" in result:
                result["WorkingHours"]["EndTime"] = result["WorkingHours"]["EndTime"].isoformat()
            if "BreakTime" in result:
                result["BreakTime"]["StartTime"] = result["BreakTime"]["StartTime"].isoformat()
            if "BreakTime" in result:
                result["BreakTime"]["EndTime"] = result["BreakTime"]["EndTime"].isoformat()
            UserId = result["UserId"]
            del result["UserId"]
        except ValidationError as err:
            return jsonify(err.messages), 400

        try:
            resp = database["userModel"].update_one(
                { 'UserId': UserId }, { '$set': result }
            )
            
            if resp.matched_count > 0:
                return jsonify({"message": "Success"}), 200
            else:
                return jsonify({"main_message": "Something went wrong!!", "detail_message": "The user does not exist"}), 400
            
        except Exception as e:
            return jsonify({"main_message": "Something went wrong!!", "detail_message": str(e)}), 400
    
    return UserModel

    