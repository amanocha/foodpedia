import os
import json
import requests
import server
from requests.auth import HTTPBasicAuth
from flask import Flask, request, jsonify,redirect, url_for, send_from_directory
from flask import render_template
from nutritionix import Nutritionix
from nutrientCalculator import *
from mealPlan import getMealPlan
from login import *
from journal import *

app = Flask(__name__)
username = ""
db =  server.get_db()

nix = Nutritionix(app_id='7f770e5d', api_key='dae4065c600b6b161789a27471167ccd') #make these env variables later
url = 'https://api.nutritionix.com/v1_1/search?'

def set_username(new_username):
	global username
	username = new_username

@app.route("/results")
def results():
	return render_template('results.html')

@app.route("/links")
def links():
	return render_template('links.html')

@app.route("/login",methods=['POST','GET'])
def login():
	open_account(request.json['username'], request.json['password'])
	set_username(request.json['username'])
	return render_template("home.html")


@app.route("/createaccount",methods=['POST','GET'])
def createaccount():
	return create_account(request.json['username'], request.json['password'])

@app.route("/")
def hello():
	if username is not "":
		return render_template('home.html', username = username)
	else:
		return render_template('login.html')

@app.route("/search")
def search():
	return render_template('main.html')

@app.route("/get_info",methods=['POST','GET'])
def edit_info():
	return get_info(username)

@app.route("/calendar")
def calendar():
	return render_template('calendar.html')

@app.route("/edit")
def edit():
	data = get_info(username)
	return render_template('edit.html', gender = data["gender"], age = data["age"], feet = data["height_ft"], inches = data ["height_in"], weight = data["weight"], restrictions = data["restrictions"], activity = data["activity"])

@app.route("/get_meal_plan_info",methods=['POST','GET'])
def get_meal_plan():
	return get_info(username)


@app.route("/journal")
def journal():
	return render_template('journal.html')

@app.route("/writeEmotions",methods=['POST','GET'])
def write():
	global username
	emotions = request.json['emotions']
	print emotions
	notes = request.json['notes']
	food = request.json['food']
	write_emotions(username, food, emotions, notes)

@app.route("/getCalendar",methods=['POST','GET'])
def getCalendar():
	global username
	return jsonify(result = get_calendar(username))
	
#get_info(gender_string, age_string, height_feet, height_inches, weight_string, activity_level)
#restrictions, calories_min, limit_number, offset_value, food_type, max_total_fat, max_cholesterol, max_saturated_fat, max_sodium, max_sugar):
@app.route("/getResults",methods=['POST','GET'])
def getResults():
	info = write_info(username, request.json['gender'], request.json['age'],request.json['height_ft'],request.json["height_in"],request.json['weight'],request.json['activity'], request.json['restrictions'])
	daily_values = info["daily_values"]
	plan = getMealPlan(request.json["restrictions"],float(info["calories"]), 50, 20, "vegetable",float(daily_values["total_fat"]),float(daily_values["cholesterol"]),float(daily_values["saturated_fat"]),float(daily_values["sodium"]), float(daily_values["sugar"]))
	return jsonify(result=plan)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
