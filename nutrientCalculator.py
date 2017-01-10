import server
import login

db = server.get_db()

def convert_height(feet, inches):
    """
    Converts height given in feet and inches into height in centimeters
    :param feet: number of feet
    :param inches: number of inches
    :return: height in centimeters
    """
    total_inches = feet*12 + inches
    centimeters = total_inches*2.54
    return centimeters

def convert_weight(pounds):
    """
    Converts weight given in pounds into weight in kilograms
    :param pounds: number of pounds
    :return: weight in kilograms
    """
    kilograms = pounds*0.453592
    return kilograms

def get_activity_factor(activity):
    """
    Converts activity level into an activity factor
    :param activity: string describing activity level
    :return: activity factor
    """
    activity_level_map = {"bmr": 1, "sedentary": 1.2, "mild": 1.375, "moderate": 1.55, "heavy": 1.7, "extreme": 1.9}
    activity_factor = activity_level_map[activity]
    return activity_factor

def calculate_calories(username, gender, age, height, weight, activity_factor):
    """
    Calculates the number of calories an individual should consume in a day
    :param username: username of individual
    :param gender: gender of individual
    :param age: age of individual
    :param height: height of individual in centimeters
    :param weight: weight of individual in kilograms
    :param activity_factor: the factor by which the BMR is multiplied
    :return: the number of calories to consume
    """
    BMR = 0
    #Mifflin - St Jeor equation
    if (gender == "male"):
        BMR = 10*weight + 6.25*height - 5*age + 5
    else:
        BMR = 10 * weight + 6.25 * height - 5 * age - 161

    calories = round(BMR*activity_factor)

    db.users.update(
        {"username":username},
        {"$set":{
            "calories":calories
        }}
    )

    return calories

def calculate_daily_values(username, calories):
    """
    Calculates the recommended daily values for each nutrient based on the number of calories to consume
    :param username: username of individual
    :param calories: number of calories the individual should consume
    :return: dictionary containing the recommended daily values where the key is the nutrient
    """
    daily_value_2000 = {"total_fat": 65, "saturated_fat": 20, "cholesterol": 300, "sodium": 2400, "carbohydrate": 300,
                        "dietary_fiber": 25, "protein": 50, "sugar": 25, "vitaminA": 1.5, "vitaminC": 60,
                        "calcium": 1000, "iron": 18}
    daily_values = {}
    for nutrient in daily_value_2000:
        amount = round(daily_value_2000[nutrient]*calories/2000)
        daily_values[nutrient] = amount
        db.users.update(
            {"username": username},
            {"$set": {nutrient: amount}}
        )
    return daily_values

def write_info(username, gender_string, age_string, height_feet, height_inches, weight_string, activity_level, restrictions):
    """
    Writes the information about the individual to the database
    :param username: username of inidividual
    :param gender_string: gender of individual
    :param age_string: age of individual
    :param height_feet: feet component of height of individual
    :param height_inches: inches component of height of individual
    :param weight_string: weight of individual in pounds
    :param activity_level: activity level of individual
    :param restrictions: dietary restrictions of individual
    :return: none
    """
    gender = gender_string.lower()
    age = int(age_string)
    height = convert_height(int(height_feet), int(height_inches))
    weight = convert_weight(int(weight_string))
    activity_level2 = (activity_level.split(' ')[0]).lower()
    activity_factor = get_activity_factor(activity_level2)
    calories = calculate_calories(username, gender, age, height, weight, activity_factor)
    daily_values = calculate_daily_values(username, calories)

    print activity_level
    db.users.update(
        {"username": username},
        {"$set": {
            "gender": gender,
            "age": age,
            "height_ft": height_feet,
            "height_in": height_inches,
            "weight": weight_string,
            "activity": activity_level,
            "restrictions": restrictions}}
    )

    return {"calories":calories, "daily_values":daily_values}

def get_info(username):
    doc = db.users.find({"username": username})[0]
    entries = {}
    print doc["activity"]
    entries["gender"] = doc["gender"]
    entries["age"] = doc["age"]
    entries["height_ft"] = doc["height_ft"]
    entries["height_in"] = doc["height_in"]
    entries["weight"] = doc["weight"]
    entries["activity"] = doc["activity"]
    entries["restrictions"] = doc["restrictions"]
    return entries

print(login.create_account("amanocha", "password"))
write_info("amanocha", "female", 19, 5, 2, 120, "moderate", [])
