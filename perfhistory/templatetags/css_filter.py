from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
	return field.as_widget(attrs={"class":css})

@register.filter(name='addplaceholder')
def addplaceholder(field, something):
	return field.as_widget(attrs={"placeholder":something})