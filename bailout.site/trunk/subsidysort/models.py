from django.db import models

from django.contrib.auth.models import User 

class Task(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()

class Tag(models.Model):
    
    task = models.ForeignKey(Task) 
    
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

    class Meta():
        ordering = ['name']
    

class Item(models.Model):
    
    task = models.ForeignKey(Task)
    
    name = models.CharField(max_length=255)
    description = models.TextField()    
    unique_id = models.CharField(max_length=255)
    url = models.URLField()  
    
    def getVotes(self):
        
        votes = {}
        
        for vote in self.vote_set.all():  
            
            if vote.decision:
                
                if not votes.has_key(vote.decision):
                    votes[vote.decision] = 0
    
                votes[vote.decision] += 1
        
        return votes
    
    
    def voteSummary(self):
        
        votes = self.getVotes()
        
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
    
    primary_purpose = models.ForeignKey(Tag, verbose_name="Primary Tag", related_name='primary_purpose', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Secondary Tags", null=True, blank=True)
    


