import os
from django.core.exceptions import ValidationError
from django.conf import settings

def result_file(value):
	if not value.name.endswith(tuple(settings.RESULT_FILE)):
		raise ValidationError('This file is not appropiate')
