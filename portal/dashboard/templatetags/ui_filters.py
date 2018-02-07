from django import template

import json

register = template.Library()

def str2json(str_data):
    return json.loads(str_data)


register.filter('str2json', str2json)