from django import template
import datetime
register = template.Library()

@register.filter(name='add_time')
def add_time(input_time, offset_minutes):
	# print input_time, offset_minutes
	if not input_time:
		return ""
	if not offset_minutes:
		return input_time

	return  input_time + datetime.timedelta(minutes=offset_minutes)