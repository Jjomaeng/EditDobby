from django.db import models

class Member(models.Model):
    member_id = models.CharField(primary_key= True, max_length=20)
    member_email = models.CharField(max_length=50)
    member_password = models.CharField(max_length=20)
    member_joindate = models.DateTimeField()
    member_status = models.IntegerField()
    member_nick = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'member'
        app_label = 'main'
        managed = False