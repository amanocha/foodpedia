from nutritionix import Nutritionix


nix = Nutritionix(app_id="7f770e5d", api_key="dae4065c600b6b161789a27471167ccd") #make these env variables later


def canAdd(item, oneMealPlan, max_total_fat, max_cholesterol, max_saturated_fat, max_sodium, max_sugar):
  #print "Saturated fat-----------"
  #print oneMealPlan['saturated_fat']
  #print item['saturated_fat']
  #print "----------------------"
  if item['saturated_fat'] is None:
    item['saturated_fat'] = 0
  if item['sugar'] is None:
    item['sugar'] = 0
  if item['total_fat'] is None:
    item['total_fat']=0
  return ((oneMealPlan['total_fat'] + item['total_fat'] <= max_total_fat) and
  (oneMealPlan['saturated_fat'] + item['saturated_fat'] <= max_saturated_fat) and
  (oneMealPlan['cholesterol'] + item['cholesterol'] <= max_cholesterol) and
  (oneMealPlan['sodium'] + item['sodium'] <= max_sodium) and
  (oneMealPlan['sugar'] + item['sugar'] <= max_sugar)) 




# restriction should be the array of food restrictions, each element would be the string name
# calories_max is from the profile 
# limit number should be 10 for getting 10 meal suggestion
# if getting 10 more, have offset_value = 10, otherwise 0 
def getMealPlan(restrictions, calories_min, limit_number, offset_value, food_type, 
  max_total_fat, max_cholesterol, max_saturated_fat, max_sodium, max_sugar):
  fields = ["allergen_contains_"+food for food in restrictions]
  fields = fields + ["item_name", "nf_calories",'nf_vitamin_a_dv', 'nf_vitamin_c_dv',
   'nf_total_fat', 'nf_total_carbohydrate', 'nf_saturated_fat', 'nf_sodium', 'nf_sugars', 'nf_cholesterol', 
   'nf_dietary_fiber','nf_protein','nf_calcium_dv', 'nf_iron_dv']
  response = nix.search().nxql(
    filters={
    "nf_sodium": {
    "lte": max_sodium,
    },
    "nf_sugars": {
    "lte": max_sugar,
    },
    "nf_total_fat": {
    "lte": max_total_fat,
    },
    "nf_saturated_fat": {
    "lte": max_saturated_fat,
    },
    "nf_cholesterol": {
    "lte": max_cholesterol,
    },
    "not":{
     "item_type":1, #not from restaurant
     "nf_serving_weight_grams":None
    }
  },
  sort = {
    "field":"nf_protein",
    "order":"desc"
    },
  offset = offset_value,
  limit = limit_number,
  fields = fields
  ).json()

  allFood = []  
  #print response
  #print"length"
  #print len(response['hits'])
  for i in response['hits']:
    tel = {}  
    item_i = i['fields']
    tel['name']=item_i['item_name']
    tel['calories'] = item_i['nf_calories']
    tel['name'] = item_i['item_name']
    tel['vitamin_a'] = item_i['nf_vitamin_a_dv']
    tel['vitamin_c'] = item_i['nf_vitamin_c_dv']
    tel['total_fat'] = item_i['nf_total_fat']
    tel['carbs'] = item_i['nf_total_carbohydrate']
    tel['saturated_fat'] = item_i['nf_saturated_fat']
    tel['sodium'] = item_i['nf_sodium']
    tel['sugar'] = item_i['nf_sugars']
    tel['cholesterol'] = item_i['nf_cholesterol']
    tel['fiber'] = item_i['nf_dietary_fiber']
    tel['protein'] = item_i['nf_protein']
    tel['calcium'] = item_i['nf_calcium_dv']
    tel['iron'] = item_i['nf_iron_dv']
    allFood.append(tel)

  # this should a list of 8 mea; plans, and each is represented as a dictionary  
  
  allFood = allFood + allFood + allFood + allFood

  allMealPlans = []
  
  #while loop each time getting a meal plan, so loop 8 times
  i = 0
  while (i < 8):
    oneMealPlan = {}
    oneMealPlan['meal_plan'] = []

    #each mean plan dictionary of meal plan will have those values calculated
    # names are all the food in this meal plan
    allIngredients = ['calories','vitamin_c', 'total_fat','carbs','saturated_fat','sodium', 'sugar','fiber','cholesterol','calcium','iron']

    for x in allIngredients:
      oneMealPlan[x] = 0

    oneMealPlan['counttest']=i
    #oneMealPlan['item_name']=allFood[i]['name']
    #print allFood[i]['name']

    for item in range(i * 7, len(allFood)):
      if (canAdd(allFood[item], oneMealPlan, max_total_fat, max_cholesterol, max_saturated_fat, max_sodium, max_sugar)):
        oneMealPlan['meal_plan'].append(allFood[item]['name'])
        #print "i value"
        #print i * 5
        for j in allIngredients:
          #this if check to see if some variable is none does not work, need Debug
          if isinstance(allFood[item][j], basestring):
            y = 0
          else:
            y = allFood[item][j]
          if oneMealPlan[j] is None:
            oneMealPlan[j]=0
          if y is None:
            y = 0
          oneMealPlan[j] = oneMealPlan[j]+ y
    #print "++++++++++each meal plan+++++++++++++++"
    #for w in oneMealPlan['meal_plan']:
    #  print w 
    allMealPlans.append(oneMealPlan)
    i = i + 1

  #print len(allMealPlans)
  return allMealPlans

#value = response["food"]