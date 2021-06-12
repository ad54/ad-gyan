from django.db import models
import re
# Create your models here.


class IndexItem(models.Model):
    index_string = models.TextField()
    search_string = models.TextField(db_index=True)
    path = models.TextField()
    gatha_num = models.CharField(max_length=100,null=True, blank=True)
    page_num = models.CharField(max_length=100)
    book_num = models.CharField(max_length=50)
    book_name = models.TextField()
    last_update_by = models.CharField(max_length=200)
    last_update_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    models.Index(fields=['search_string']),

    def __str__(self):
        return self.index_string

    # This should touch before saving
    def save(self, *args, **kwargs):
        # repalce characters for making searching faster
        replace_dict = {'ि': 'ी', 'ू': 'ु',
                        'િ': 'ી', 'ૂ': 'ુ'}
        regex = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
        self.search_string = regex.sub(lambda mo: replace_dict[mo.string[mo.start():mo.end()]], self.index_string)
        super().save(*args, **kwargs)
        print(self.search_string)


class SearchResult(models.Model):
    search_string = models.TextField()
    search_result = models.JSONField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_update_on = models.DateTimeField(auto_now=True)

class Analytics(models.Model):
    statics = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_update_on = models.DateTimeField(auto_now=True)




