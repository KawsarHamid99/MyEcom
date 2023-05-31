from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

STATE_CHOICE=(
    ("dhaka","Dhaka"),
    ("khulna","Khulna"),
    ('rajsahi','Rajsahi'),
    ('barishal','Barishal'),
    ('mymansing',"Mymansing"),
    ('chittagong',"Chittagong"),
    ('Chandpur',"Chandpur"),
    ('noakhali','Noakhali')
)
CATEGORY_CHOICE=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Ware'),
    ('BW','Bottom Wear'),
)

STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICE,max_length= 50)


    def __str__(self):
        return str(self.name)
    
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICE,max_length=2)
    product_image=models.ImageField(upload_to="productimg")

    def __str__(self):
        return str(self.title)
    
class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return str(self.id)
    
class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    orderd_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=STATUS_CHOICE,max_length=100,default="pending")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
