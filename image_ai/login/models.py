from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.username


class Record(models.Model):
    record_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    handImg = models.ImageField(upload_to='./upload/')
    imgDetect = models.ImageField(null=True)
    imgPredict_res = models.CharField(max_length=2000, null=True)
    imgPredict_sqz = models.CharField(max_length=2000, null=True)


# there is only one administrator account in this project
# stored in database, read the doc for more info
class Admin(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.username
