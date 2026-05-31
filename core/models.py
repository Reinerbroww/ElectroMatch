from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.name

class Criteria(models.Model):
    name = models.CharField(max_length=100)

    TYPE_CHOICES = (
        ('benefit', 'Benefit'),
        ('cost', 'Cost'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    weight = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-weight']

class ProductValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    value = models.FloatField()