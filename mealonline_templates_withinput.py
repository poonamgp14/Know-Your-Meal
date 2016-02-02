import webapp2
import jinja2
import os
from google.appengine.api import users
import mealdatastore
import re


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Handler(webapp2.RequestHandler):
	"""This is the handler class for handling jinja2 template"""
	
	def write(self,*a,**kw):
		"""This will write response back to our browser(client)"""
		self.response.out.write(*a,**kw)   

	#functions for rendering basic templates
	def render_str(self,template,**params):
		"""This calls jinja template we specify and 
		returns template in form of a string.
		render_str() will return a HTML string based off on the 
		params which will be a dictionary of all of our keywords
		"""

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self,template, **kw):
		"""Main method to call from get methods"""
	
		self.write(self.render_str(template,**kw))
	

class MainPage(Handler):
	def get(self):
		self.render("meal_htmlform_withinput.html" , output_str = '')

		
class Testhandler(Handler):
	def get(self):
		self.render("meal_htmlform_withinput.html" , output_str = '')
		
	def post (self):
		post_values = self.request.POST.items()
		self.output = mealdatastore.main(post_values)

		#Checks for active Google account session
		user = users.get_current_user()
		if user:
			self.current_user= user.nickname()
			self.output_ds = mealdatastore.Output_DS(content=self.output,username=user.nickname())#,date_created=datetime.datetime.now())
			donot_put_in_flag = self.output_ds.content
		
			self.output_ds.put() #this writes to the datastore
			self.render("meal_htmlform_withinput.html" ,output_str = self.output)


		#this is for previously selected meal if user would like to compare meals!
			q = mealdatastore.Output_DS.all()
			self.query_for_current_user = q.filter("username =",self.current_user)
			if self.query_for_current_user:
			#if q:


			# flag is list of all those meal details which are unique.
				flag = []


				#for self.output_ds in self.query:
				for self.output_ds in self.query_for_current_user:
				

				#this will avoid putting the current selected meal under previous selected meal section
					if donot_put_in_flag == self.output_ds.content:
						continue
					elif self.output_ds.content != 'None' and self.output_ds.content not in flag:
						x = self.output_ds.content
						flag.append(x)
						self.response.write('<p>Your previously selected meal details are:<br> %s </p>' % self.output_ds.content)
		else:
			self.redirect(users.create_login_url(self.request.uri))



#this is for feedback
class HandlerFeedback(Handler):
	def get(self):
		self.render("meal_feedback_page.html")

	def post(self):		
		missing_item_value_from_get = self.request.get("missingItem")
		if missing_item_value_from_get:

		#checks for any number
			validation_num_value =validate_for_number(missing_item_value_from_get)
		#checks for any special character
			validation_sp_char_value = validate_for_special_char(missing_item_value_from_get)

			#checks for both number and special character
			if (validation_num_value and validation_sp_char_value):
				self.render("meal_feedback_page.html",
					feedback_str = "Error: Please enter a valid food item.",
					missingItemValue = missing_item_value_from_get)


			#checks for number only	
			elif validation_num_value:
				self.render("meal_feedback_page.html",
					feedback_str = "Error: Please enter a valid food item.",
					missingItemValue = missing_item_value_from_get)


			#checks for special character only	
			elif validation_sp_char_value:
				self.render("meal_feedback_page.html",
					feedback_str = "Error: Please enter a valid food item.",
					missingItemValue = missing_item_value_from_get)	

			else:
				self.feedbackds = mealdatastore.FeedbackDS(input_from_user = missing_item_value_from_get)
				self.feedbackds.put()
				self.render("meal_feedback_page.html",
					feedback_str = "Thanks for your input. We will add the food item to our database shortly.",
					missingItemValue = missing_item_value_from_get)


		# when input is left blank		
		else:
			self.render("meal_feedback_page.html",
					feedback_str = "Error: Please enter a food item.")
					


				
			
app = webapp2.WSGIApplication([
    ('/', MainPage),('/testform',Testhandler)
    ,('/feedback',HandlerFeedback)
], debug=True)


def validate_for_number(any_string):
	string_to_search = any_string
	search_obj = re.search(r'\d',string_to_search)
	if search_obj:
		return search_obj.group()

def validate_for_special_char(any_string):
	string_to_search = any_string
	#the below mentioned regrex considered space as special character
	#this if statement would replace space with no space
	if ' ' in string_to_search:
		string_to_search = string_to_search.replace(' ','')
	#excluding numbers and alphabets, everything else is special character
	#I know Steve in class videos used a built-in function for escaping HTML
	# This regrex mentioned below escapes HTML too.!!!!!
	#source of this regrex is stackflow.com	
	search_obj = re.search(r"[^A-Za-z0-9]",string_to_search)
	if search_obj:
		return search_obj.group()





















