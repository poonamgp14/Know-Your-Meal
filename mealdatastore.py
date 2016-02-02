from google.appengine.ext import db


class Output_DS(db.Model):
	content = db.StringProperty(required=True,multiline=True)
	username = db.StringProperty(required=True)
	
	
class FeedbackDS(db.Model):
	input_from_user = db.StringProperty	(required=True)


class Food(db.Model):
	name_of_food = db.StringProperty(required=True)
  	unit_of_measurement = db.StringProperty(required=True)
  	carb = db.FloatProperty(required=True)
  	fat = db.FloatProperty(required=True)
  	fiber = db.FloatProperty(required=True)
  	protein = db.FloatProperty(required=True)
  	calories = db.FloatProperty(required=True)

f1 = Food(name_of_food='Egg',unit_of_measurement='1 large',carb=0.6,
		fat=5.0,fiber=0.0,protein=6.0,calories=78.0)
f2 = Food(name_of_food='Whole Grain Bread',unit_of_measurement='1 Slice',
	carb=10.1,fat=0.9,fiber=1.9,protein=3.6,calories=69.0)
f3 = Food(name_of_food='Whole Milk',unit_of_measurement='1 Cup',
	carb=12.0,fat=8.0,fiber=0.0,protein=8.0,calories=150.0)
f4 = Food(name_of_food='Apple',unit_of_measurement='1 Small',
	carb=17.4,fat=0.2,fiber=3.6,protein=0.4,calories=78.0)
		
f1.put()
f2.put()
f3.put()
f4.put()


		

				




def main (multidic_of_food_from_url):
	total_carbs = 0
	total_fat = 0
	total_fiber = 0
	total_protein = 0
	#total_calories = 0
	meal_consits_of = ''
	
	for each_tuple in multidic_of_food_from_url:
		food_value = each_tuple[1]
		if food_value == "":
			continue
		elif food_value == 'Select':
			continue
		else:	
			meal_consits_of = meal_consits_of + food_value + ', '
			q = db.GqlQuery("SELECT * FROM Food WHERE name_of_food =:1",food_value)
			for food in q.fetch(limit=1):
				if food.carb:
					total_carbs += food.carb
				if food.fat:
					total_fat += food.fat
				if food.fiber:
					total_fiber += food.fiber
				if food.protein:
					total_protein += food.protein
			#total_calories += food.calories

	total_carbs = str(total_carbs) + 'g'
	total_fat = str(total_fat) +'g'
	total_fiber = str(total_fiber) + 'g'
	total_protein = str(total_protein) + 'g'
	if meal_consits_of:
		return "The meal consists of " + meal_consits_of + "and has total carbs " + total_carbs + ", total fat " + total_fat + ", total fiber " + total_fiber + ", total protein " + total_protein
	else:
		return "None"





