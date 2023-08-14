from django.db import models

from main.models import Member

# Create your models here.
class File(models.Model):
    file_no = models.IntegerField(primary_key= True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    file_name = models.CharField(max_length=50)
    file_date = models.CharField(max_length=1000)
    file_root = models.FileField()
    
    class Meta:
        db_table = 'file'
        app_label = 'dobby'
        unique_together = (('file_no', 'member_id'),)
        managed = False
        
        
class Inputfile(models.Model):
    # input_name = models.CharField(max_length=255)
    input_file = models.FileField()
    # def __str__(self):
    #     return self.input_name