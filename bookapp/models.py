from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200,blank=False,null=False)
    author = models.CharField(max_length=100,blank=False,null=False)
    price=models.IntegerField(default=0)
    published_date = models.DateField(blank=True, null=True)
    gmail=models.EmailField(blank=True,null=True)
    quantity = models.PositiveIntegerField(default=0)      # total stock available
    copies_sold = models.PositiveIntegerField(default=0) 
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
 
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='unique_book_title_author')
        ]
        # unique_together = ('title', 'author')
    def __str__(self):
        return self.title
    

class Study(models.Model):
    min_price= models.IntegerField(default=0)
    max_profit=models.IntegerField(default=0)

