from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.username

    
class Session1(models.Model):
    session_id = models.IntegerField()
    user = models.ForeignKey(User)
    session_valid = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.session_id)

class Session2(models.Model):
    session_id = models.IntegerField()
    user = models.ForeignKey(User)
    session_valid = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.session_id)
    
class Session3(models.Model):
    session_id = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    session_valid = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.session_id)    

class Session4(models.Model):
    session_id = models.IntegerField()
    session_id_hash = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    session_valid = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.session_id)  
    
class XSSData(models.Model):
    data = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "XSS Data " + str(self.id) 
    
class XSSData2(models.Model):
    data = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "XSS Data " + str(self.id) 
    
class SensitiveData(models.Model):
    data = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "Sensitive Data " + str(self.id)   