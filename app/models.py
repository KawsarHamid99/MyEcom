from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.
from django.core.mail import EmailMessage
from django.conf import settings
""""
from django.db import models
from PIL import Image
class FixedSizeImage(models.Model):
    image = models.ImageField(upload_to='fixed_images/')
    fixed_width = 300  # Set your desired fixed width
    fixed_height = 200  # Set your desired fixed height

    def save(self, *args, **kwargs):
        # Open the uploaded image using PIL
        img = Image.open(self.image)
        
        # Resize the image to the fixed dimensions
        resized_img = img.resize((self.fixed_width, self.fixed_height), Image.ANTIALIAS)
        
        # Create a temporary file to save the resized image
        temp_img_path = f"temp_{self.image.name}"
        resized_img.save(temp_img_path)
        
        # Open the resized image and save it to the database
        with open(temp_img_path, 'rb') as temp_img:
            self.image.save(self.image.name, temp_img, save=False)
        
        # Clean up the temporary file
        import os
        os.remove(temp_img_path)
        
        super(FixedSizeImage, self).save(*args, **kwargs)
"""


kamlaSTATE_CHOICE=(
    ("dhaka","Dhaka"),
    ("khulna","Khulna"),
    ('rajsahi','Rajsahi'),
    ('barishal','Barishal'),
    ('mymansing',"Mymansing"),
    ('chittagong',"Chittagong"),
    ('Chandpur',"Chandpur"),
    ('noakhali','Noakhali')
)


STATUS_CHOICE=(
    ('Placed','Placed'),
    ('Accepted','Accepted'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class StateSelect(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    zipcode=models.PositiveIntegerField(null=True,blank=True)
    shippingcost=models.PositiveIntegerField(null=True,blank=True,default=20)

class StateList(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    zipcode=models.PositiveIntegerField(null=True,blank=True)
    shippingcost=models.PositiveIntegerField(null=True,blank=True,default=20)

class ProductSize(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True,unique=True)
    shortform=models.CharField(max_length=100,null=True,blank=True,unique=True)

    def __str__(self):
        return str(self.name)

class Productcolor(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True,unique=True)
    color_code=models.CharField(max_length=100,null=True,blank=True,unique=True)

    def __str__(self):
        return str(self.name)



class Category(MPTTModel):
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to="category",null=True,blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        if self.parent:
            return str(self.parent)+"_"+str(self.name)
        else:
            return str(self.name)
        
    def get_root_parent(self):
        # Recursively find the root parent (top-level ancestor) for this category.
        if self.parent is None:
            return self
        return self.parent.get_root_parent()

    def get_all_children(self):
        # Get all children of this category, including itself.
        return self.get_descendants(include_self=True)
    
    def get_path_to_last_child(self):
        path = [self]
        current_category = self

        while current_category.parent:
            path.append(current_category.parent)
            current_category = current_category.parent

        # Reverse the path to get the correct order (from root to last child).
        path.reverse()

        return path
    

    @classmethod
    def find_children_by_parent_pk(cls, parent_pk):
        try:
            parent_category = cls.objects.get(pk=parent_pk)
        except cls.DoesNotExist:
            return []

        return cls.objects.filter(parent=parent_category)


class Brand(models.Model):
    name=models.CharField(max_length=100)
    category=models.ManyToManyField(Category,blank=True)
    image=models.ImageField(upload_to="brand",null=True,blank=True)

    def Category_list(self):
        return ",".join(str(p.name) for p in self.category.all())

    def __str__(self):
        return str(self.name)
    


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    zipcode=models.IntegerField()
    state=models.CharField(choices=kamlaSTATE_CHOICE,max_length=100,null=True,blank=True)
    #state=models.ForeignKey(States_choice,on_delete=models.DO_NOTHING,null=True,blank=True)


    def __str__(self):
        return str(self.name)
    
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField(null=True,blank=True)
    description=models.TextField()
    brand=models.ForeignKey(Brand,on_delete=models.DO_NOTHING,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,null=True,blank=True)
    size=models.ManyToManyField(ProductSize,blank=True)
    color=models.ManyToManyField(Productcolor,blank=True)
    product_image=models.ImageField(upload_to="productimg")
    key_word=models.CharField(max_length=1000,null=True,blank=True)

    

    class Meta:
        ordering = ('title',)

    def size_list(self):
        return ",".join([str(p) for p in self.size.all()])
    
    def color_list(self):
        return ",".join([str(p) for p in self.color.all()])

    def __str__(self):
        return str(self.title)
    
class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    size=models.ForeignKey(ProductSize,on_delete=models.CASCADE,blank=True,null=True)
    color=models.ForeignKey(Productcolor,on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.PositiveIntegerField(default=1)
    
    def total_cost(self):
        if self.product.discounted_price:
            return self.quantity * self.product.discounted_price
        else:
            return self.quantity * self.product.selling_price

    def __str__(self):
        return str(self.id)
    
class OrderPlaced(models.Model):
    orderid=models.CharField(max_length=10000,null=True,blank=True)
    trcking_id=models.CharField(max_length=100,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    customer=models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    price_per_unit=models.FloatField(blank=True,null=True)
    quantity=models.PositiveIntegerField()
    address=models.CharField(max_length=500,null=True,blank=True)
    orderd_date=models.DateTimeField(auto_now_add=True)
    size=models.ForeignKey(ProductSize,on_delete=models.DO_NOTHING,null=True,blank=True)
    color=models.ForeignKey(Productcolor,on_delete=models.DO_NOTHING,null=True,blank=True)
    status=models.CharField(choices=STATUS_CHOICE,max_length=100,default="orderd_date")

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        OrderPlaced.objects.filter(orderid=self.orderid).update(status=self.status,trcking_id=self.trcking_id)

    @property
    def total_cost(self):
        return self.price_per_unit * self.quantity

@receiver(pre_save, sender=OrderPlaced)
def my_model_updated(sender, instance, **kwargs):
    if instance.pk:
        old_instance = OrderPlaced.objects.get(pk=instance.pk)
        if instance.status != old_instance.status or instance.trcking_id != old_instance.trcking_id:
            
            message='''
                hello {},
                Here is update of your order.

                order id: {}
                Current order status: {}
                Tracking id : {}


                Thanks,
                Garbleddeals
                '''.format(instance.user.username,instance.orderid,instance.status,instance.trcking_id)
            mail=EmailMessage("Updated Order Information",message,settings.EMAIL_HOST_USER,[instance.user.email])
            mail.send()
# Connect the pre_save signal
pre_save.connect(my_model_updated, sender=OrderPlaced)
