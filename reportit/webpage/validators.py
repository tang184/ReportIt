from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.core.validators import MaxValueValidator
import re
from datetime import datetime

def validateURL (value):
	url_validator = URLValidator()
	try:
		url_validator(value)
	except:
		raise ValidationError("Invalid URL for this field")
	return value

def validateEmail (value):
	try:
		validate_email(value)
	except:
		raise ValidationError("Wrong email form for this field")
	return value