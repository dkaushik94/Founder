'''-------------------------------------------------------------------------------------'''

#Django imports.
from django.db import models

'''-------------------------------------------------------------------------------------'''



'''-------------------------------------------------------------------------------------'''


'''Database model for Resources.'''
class Resource(models.Model):
    TYPE = (
            ('legal' , 'Legal'),
            ('hr' , 'Human Resource'),
            ('finance' , 'Finanace'),
            ('partnership' , 'Partnerships'),
        )

    name_of_file = models.CharField(max_length = 75)
    data = models.FileField(upload_to = 'resources/')
    type_of_doc = models.CharField(max_length = 100 , choices = TYPE)

    def __str__(self):
        return self.name_of_file
