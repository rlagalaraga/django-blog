from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    use_in_migrations =True

    def create_user(self, email, password=None):
        """ Creates and saves a User with the given email and password """
        if not email:
            raise ValueError('Enter a valid email address')
        if not password:
            raise ValueError('Enter a password')
        
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """ Create and saves a superuser with the given email and password. """
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user