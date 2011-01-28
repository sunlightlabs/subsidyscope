from django.contrib.syndication.feeds import Feed
from project_updates.models import ProjectUpdate
import datetime

class ProjectUpdatesFeed(Feed):
    title = "Subsidyscope.org Updates"
    link = "/updates/"
    description = "Updates on changes and additions to subsidyscope.org."
   
    def items(self):
        return ProjectUpdate.objects.filter(published=True).order_by('-date')[:10]
        
    def item_pubdate(self, item):
        return datetime.datetime(item.date.year, item.date.month, item.date.day, 9, 0, 0)
          
    def item_link(self, item):
        return item.link


class TransportationProjectUpdatesFeed(ProjectUpdatesFeed):

    def items(self):
        return ProjectUpdate.objects.filter(published=True).filter(sectors=2).order_by('-date')[:10]