from django.db import models

from django.contrib.auth.models import User 

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()
def get_current_user():
    return getattr(_thread_locals, 'user', None)


class Task(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()

#class ReviewPass(models.Model):
#    
#    task = models.ForeignKey(Task)
#    
#    pass_order = models.IntegerField()
#    
#    name = models.CharField(max_length=255)
#    description = models.TextField()
#    
#    def status(self):
#        
#        user = get_current_user()
#        
#        items = taks.item_set.all().count()
#        
#        items_voted = Vote.objects.filter(user=user, review_pass=self).count()
#        
#        return '%d/%d complete' % (items_voted, items)
    
    
class Tag(models.Model):
    
    task = models.ForeignKey(Task) 
    
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

    

class Item(models.Model):
    
    task = models.ForeignKey(Task)
    
    name = models.CharField(max_length=255)
    description = models.TextField()    
    unique_id = models.CharField(max_length=255)
    url = models.URLField()  
    
    def sumVotes(self):
        
        votes = {}
        
        for vote in self.vote_set.all():  
            
            if vote.decision:
                
                if not votes.has_key(vote.decision):
                    votes[vote.decision] = 0
    
                votes[vote.decision] += 1
        
        summary = ''
                
        for decision in votes:
            
            summary += '%s: %d ' % (decision, votes[decision])
            
        return summary
    
    

class Vote(models.Model):
    
    user = models.ForeignKey(User, editable=False)
    
    item = models.ForeignKey(Item, editable=False)
    
    DECISION_CHOICES = (
        ('yes','Yes'),
        ('no','No'),
        ('maybe', 'Maybe'), 
        ('dont-know', 'Don\'t Know')
    )
    
    decision = models.CharField(verbose_name="Subsidy", max_length=25, choices=DECISION_CHOICES, blank=True, null=True)
    
    comments = models.TextField(blank=True)
    
    tags = models.ManyToManyField(Tag, blank=True)
