from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class Users(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        STAFF="STAFF",'Staff'
        USER="USER",'User',
        WAREHOUSE="WAREHOUSE",'Warehouse'
        
    role=models.CharField(max_length=15,default='USER')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    location = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location
    
class Bus(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, blank= True, null = True)
    bus_number = models.CharField(max_length=250)
    seats = models.FloatField(max_length=5, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_number
    
class Schedule(models.Model):
    code = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE)
    depart = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='depart_location')
    destination = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='destination')
    schedule= models.DateTimeField()
    fare= models.FloatField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Cancelled')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code + ' - ' + self.bus.bus_number)


class Seat_map(models.Model):
    seat_number = models.CharField(max_length=10, primary_key=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    booked_seat = models.BooleanField(default=False)
    booked_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.seat_number} - {self.bus} - {self.schedule}"


from django.db import models

class Feedback(models.Model):
    User = models.ForeignKey(Users, on_delete=models.CASCADE)  # Assuming you have a User model
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    passenger_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.EmailField(unique=True, null=True)
    seatMap = models.ForeignKey(Seat_map, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    total_price = models.CharField(max_length=10, blank=True, null=True)  

    def __str__(self): 
        return f"Booking ID: {self.book_id} - Passenger: {self.passenger_name} - Schedule: {self.schedule}"
    
class Address(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='address')
    address = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address}, {self.street}, {self.city}, {self.state}, {self.country} - {self.postal_code}"
    



#contains suppliers
STATUS_CHOICES = (
        ('1', 'Accept'),
        ('2', 'Pending'),
        ('3', 'Reject'),
    )
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    gstin = models.CharField(max_length=15, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
	    return self.name

#contain product
BRAND_CHOICES = (
    ('QuillCraft', 'QuillCraft'),
    ('CreativeCanvas', 'CreativeCanvas'),
    ('CalinaQuetient', 'CalinaQuetient'),
    ('GastronomeGoods', 'GastronomeGoods'),
    ('HotWheelsHaven', 'Hot Wheels Haven'),
)

CATEGORY = (
    ('Toys', 'Toys'),
    ('KitchenItems', 'KitchenItems'),
    ('Stationary', 'Stationary'),
)

class Stock(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=200, choices=CATEGORY, null=True)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, null=True)
    costPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sellingPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveBigIntegerField(null=True)
    minStockLevel = models.PositiveIntegerField(null=True)
    maxStockLevel = models.PositiveIntegerField(null=True)
    reorderPoint = models.PositiveIntegerField(null=True)
    unitOfMeasurement = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='stock_images/', null=True)  # Changed field to ImageField
    description = models.TextField(null=True, blank=True)
    dateAdded = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.brand}) - {self.quantity}'
    


#contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, related_name='purchasesupplier')

    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total

#contains the purchase stocks made
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasebillno')
    stockname = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stockname.name


# warehouse model
class Warehouse(models.Model):
    STATUS_CHOICES = (
        ('1', 'Active'),
        ('2', 'Inactive'),
    )

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    total_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    available_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    contact_person_name = models.CharField(max_length=100)
    contact_person_email = models.EmailField(max_length=254)
    contact_person_phone = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return self.name


class WarehouseType(models.Model):
    SIZE_CHOICES = (
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
    )

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=SIZE_CHOICES)
    rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    capacity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    count = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.get_type_display()} - {self.warehouse.name}"
    

class StorageMapDup(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    warehouse_type = models.ForeignKey(WarehouseType, on_delete=models.CASCADE)
    selected_seats_display = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.warehouse_type.warehouse.name} ({self.warehouse_type.get_type_display()})"


class StorageUserDup(models.Model):
    STATUS_CHOICES = (
        ('1', 'False'),
        ('2', 'True'),
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE) 
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    warehouse_type = models.ForeignKey(WarehouseType, on_delete=models.CASCADE)
    productname = models.CharField(max_length=100, null=True)
    quantity = models.PositiveBigIntegerField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_paid = models.CharField(max_length=2, choices=STATUS_CHOICES, default='1')



#storage map
class StorageMap(models.Model):
    storageNumber = models.CharField(max_length=50)
    warehouse_type = models.ForeignKey(WarehouseType, on_delete=models.CASCADE)
    storage_user = models.ForeignKey(StorageUserDup, on_delete=models.CASCADE)  # Add this line

    def __str__(self):
        return f"Storage Number: {self.storageNumber} - {self.warehouse_type.warehouse.name} ({self.warehouse_type.get_type_display()})"
    

class Payment(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    warehouse_type = models.ForeignKey(WarehouseType, on_delete=models.CASCADE)
    storage_user = models.ForeignKey(StorageUserDup, on_delete=models.CASCADE)  # Foreign key to connect to StorageUserDup
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveBigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_paid = models.BooleanField()
    selected_seats_display = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.warehouse} ({self.warehouse_type})"


    
    