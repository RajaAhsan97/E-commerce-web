from django import template

register = template.Library()

@register.filter(name="index")
def indexing(mylist, iter):
    return mylist[iter]