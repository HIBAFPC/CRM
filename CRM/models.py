from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("sales_rep", "Sales Representative"),
        ("support", "Support Staff"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="sales_rep")

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="customers_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("converted", "Converted"),
        ("lost", "Lost"),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="leads")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="leads")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead: {self.customer.name} ({self.status})"
    
    
class Deal(models.Model):
    STAGE_CHOICES = [
        ("prospecting", "Prospecting"),
        ("qualification", "Qualification"),
        ("proposal", "Proposal Sent"),
        ("negotiation", "Negotiation/Review"),
        ("closed_won", "Closed Won"),
        ("closed_lost", "Closed Lost"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="deals")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="deals")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="prospecting")
    expected_close_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Deal with {self.customer.name} - {self.stage}"
    
class Activity(models.Model):
    ACTIVITY_TYPES = [
        ("call", "Call"),
        ("email", "Email"),
        ("meeting", "Meeting"),
        ("demo", "Demo"),
        ("followup", "Follow-up"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="activities")
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="activities", blank=True, null=True)
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="activities")

    def __str__(self):
        return f"{self.type} with {self.customer.name} on {self.date.date()}"

    