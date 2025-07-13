from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name=models.CharField(max_length=20,unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=8,decimal_places=2)



    def get_review(self):
        reviews=self.reviews.all()
        if reviews:
            rating= sum([review.rating  for review in reviews])/reviews.count()
            result=round(rating,1)
            return result
        return 0


    def __str__(self):
        return self.name



RATES=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reviews=models.TextField(blank=True)
    rating=models.IntegerField(choices=RATES)

    class Meta:
        constraints=[models.UniqueConstraint(fields=['product','user'],name='one review for one user')]


    def __str__(self):
        return f'{self.user.username}: {self.product.name} :{self.rating}'




