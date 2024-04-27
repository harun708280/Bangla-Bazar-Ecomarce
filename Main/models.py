from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator,MaxValueValidator

DIVISION_CHOICES = (
    ('Dhaka','Dhaka'),
    ('Rangpur','Rangpur'),
    ('Rajshahi','Rajshahi'),
    ('Khulna','Khulna'),
    ('Barishal','Barishal'),
    ('Chattogram','Chattogram'),
    ('Mymenshing','Mymenshing'),
    ('Sylhet','Sylhet'),
)

class customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField( max_length=200)
    division=models.CharField(choices=DIVISION_CHOICES, max_length=50)
    district=models.CharField( max_length=50)
    thana=models.CharField( max_length=50)
    vllorroad=models.CharField( max_length=50)
    zipcode=models.IntegerField()

    def __str__(self):
        return str(self.id)
    
DIVISIONS_CHOICES = (
    ('Dhaka','Dhaka'),
    ('Rangpur','Rangpur'),
    ('Rajshahi','Rajshahi'),
    ('Khulna','Khulna'),
    ('Barishal','Barishal'),
    ('Chattogram','Chattogram'),
    ('Mymenshing','Mymenshing'),
    ('Sylhet','Sylhet'),
)

class customers(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField( max_length=50)
    last_name=models.CharField(max_length=50)
    Contract_Number=models.IntegerField()
    email=models.EmailField( max_length=254)
    division=models.CharField(choices=DIVISIONS_CHOICES, max_length=50)
    district=models.CharField( max_length=50)
    thana=models.CharField( max_length=50)
    Union=models.CharField( max_length=50)
    

    def __str__(self):
        return str(self.id)

#hero
class hero(models.Model):
    img=models.ImageField( upload_to='imges', height_field=None, width_field=None, max_length=None)
    name=models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)
    
    #PRODUCT ADD
PRODUCT_CETAGROY=(
    ('vegetables','vegetable'),
    ('fruits','fruits'),
    ('bread','bread'),
    ('meat','meat'),

)
class Product(models.Model):
    name=models.CharField( max_length=50)
    item=models.CharField(choices=PRODUCT_CETAGROY, max_length=50)
    img=models.ImageField( upload_to='imges', height_field=None, width_field=None, max_length=None)
    price=models.FloatField()
    discription=models.TextField()

    def __str__(self):
        return self.name
    


PRODUCT_CETAGROYS=(
    ('vegetables','vegetable'),
    ('fruits','fruits'),
    ('bread','bread'),
    ('meat','meat'),

)
class Products(models.Model):
    name=models.CharField( max_length=50)
    item=models.CharField(choices=PRODUCT_CETAGROYS, max_length=50)
    img=models.ImageField( upload_to='imges', height_field=183, width_field=265, max_length=None)
    price=models.FloatField()
    discription=models.TextField()

    def __str__(self):
        return str(self.id)
    
class bestsel(models.Model):
    name=models.CharField( max_length=50)
    price=models.FloatField()
    discription=models.TextField()
    img=models.ImageField( upload_to='imges', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return str(self.id)



class Customer_Reivew(models.Model):
    name=models.CharField( max_length=50)
    profesion=models.CharField( max_length=50)
    rating=models.IntegerField()
    comments=models.TextField()
    img=models.ImageField( upload_to=None, height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return str (self.id)
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    product=models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    def line_total(self):
        return self.product.price * self.quantity
    

class SpacialOffer(models.Model):
    
    OFFER_TYPE=(
        ('20percentoff',20),
        ('30percentoff',30),
        ('10percentoff',10),
        ('freedelivery',100),
    )

    discount_type = models.CharField(choices=OFFER_TYPE, max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Customer_Contract_From(models.Model):
    name=models.CharField( max_length=50)
    email=models.EmailField( max_length=254)
    message=models.TextField()
    
    def __str__(self):
        return self.name
    
class onlyOne_Special_Product(models.Model):
    items=(
        ('Fruit','Fruit'),
        ('Vegetable','Vegetable'),
        ('Meat','Meat')
    )
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    item=models.CharField(choices=items, max_length=50)
    
class OrderPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(default='Pending', max_length=50)
    name=models.CharField( max_length=50)
    company_name=models.CharField( max_length=50)
    address=models.CharField( max_length=50)
    town=models.CharField( max_length=50)
    upozila=models.CharField( max_length=50)
    postcode=models.CharField( max_length=50)
    mobile=models.CharField( max_length=50)
    email=models.EmailField( max_length=254)
    
    def __str__(self):
        return str(self.user)
    
class Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField( max_length=50)
    email=models.EmailField( max_length=254)
    comment=models.TextField()
    rating=models.FloatField(default=0)
    date=models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return (self.id)
class Reviews(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.TextField()
    rating=models.FloatField(default=0)
    date=models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
class Cupon(models.Model):
    code = models.CharField( max_length=50,unique=True)
    valid_from=models.DateField()
    valid_to=models.DateTimeField()
    discaunt=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(70)])
    active=models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.code
     
    
    










