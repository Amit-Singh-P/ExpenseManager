from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_company_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def get_team_size(self):
        """Returns the number of subordinates for managers"""
        if self.role == 'manager':
            return self.subordinates.count()
        return 0


class Company(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'United States Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('INR', 'Indian Rupee'),
        ('JPY', 'Japanese Yen'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
    ]
    
    name = models.CharField(max_length=200)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    admin = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_company',
        null=True,  
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']
        
    
    def __str__(self):
        return self.name
    
def get_employee_count(self):
    """Returns total employees in the company"""
    return self.employees.filter(role='employee').count()

def get_manager_count(self):
    """Returns total managers in the company"""
    return self.employees.filter(role='manager').count()

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'contact_messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.email}"