from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

class UserModuleManager(BaseUserManager):
    use_in_migrations = True 

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The username must be set')
        
        # email = self.normalize_email(email)
        # user = self.model(email=email, **extra_fields)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Properly set the password
        user.save(using=self._db)  # Ensure the correct database is used
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)        
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'user_management'

    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)    
    date_activated = models.DateTimeField(auto_now_add=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True) 
    email = models.EmailField(max_length=255, blank=True, null=True)   
    address = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    identification_document = models.CharField(max_length=255, blank=True, null=True)
    identification_document_number = models.CharField(max_length=255, blank=True, null=True)

    username = models.CharField(max_length=255, blank=False, null=False, unique=True)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserModuleManager()

# class Student(models.Model):    
#     admitted_on = models.DateField(blank=True, null=True)
#     admission_number = models.CharField(max_length=255, blank=True, null=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_user')
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_created_by')
    
    
# class Staff(models.Model):
#     date_joined = models.DateField(blank=True, null=True)
#     id_number = models.CharField(max_length=255, blank=True, null=True)
#     staff_type = models.CharField(max_length=255, blank=True, null=True)    
#     staff_number = models.CharField(max_length=255, blank=True, null=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_user')
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_created_by')

# class Parent(models.Model):
#     children = models.ManyToManyField(Student, related_name='parents')
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_user')
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_created_by')