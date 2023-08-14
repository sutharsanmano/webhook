from django.db import models

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.CharField(max_length=50, unique=True)
    account_name = models.CharField(max_length=100)
    app_secret_token = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.account_name
