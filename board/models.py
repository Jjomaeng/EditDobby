from django.db import models

from main.models import Member

# Create your models here.
class Post(models.Model):
    post_no= models.IntegerField(primary_key = True)  
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    post_title = models.CharField(max_length=50)
    post_detail = models.CharField(max_length=1000)
    post_update = models.DateField()

    class Meta:
        db_table = 'post'
        app_label = 'board'
        unique_together = (('post_no', 'member_id'),)
        managed = False
        


class Comment(models.Model):
    comment_no = models.IntegerField(primary_key= True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    post_no = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_no')
    comment_detail = models.CharField(max_length=1000)
    comment_update = models.DateField()
    
    class Meta:
        db_table = 'comment'
        app_label = 'board'
        unique_together = (('comment_no', 'member_id', 'post_no'),)
        managed = False
    
    
    
class Postfile(models.Model):
    postfile_no = models.IntegerField(primary_key= True)
    post_no = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_no')
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    postfile_name = models.CharField(max_length=50)
    postfile_root = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'postfile'
        app_label = 'board'
        unique_together = (('postfile_no', 'post_no', 'member_id'),)
        managed = False