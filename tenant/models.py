from django.db import models
from authentication.models import Tenant
from landlord.models import House

import uuid

# Create your models here.

class Swipe(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant')
    partner = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='partner', null=True, blank=True)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        from .utils import update_match
        update_match(self)
        return super(Swipe, self).save(*args, **kwargs)

    def __str__(self):
        rep = 'Active' if self.active else 'Inactive'
        return rep + f' swipe of {self.tenant} to {self.partner}'
    

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    tenant1 = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant1', blank=True, null=True)
    tenant2 = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant2', blank=True, null=True)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # match housing
    budget = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        rep = 'Active' if self.status else 'Inactive'
        return rep + f' match between {self.tenant1} and {self.tenant2}'

    def save(self, *args, **kwargs):
        from .utils import update_housing
        update_housing(self)

        if not self.tenant2: 
            self.budget = self.tenant1.budget
            self.city = self.tenant1.desiredCity
            self.district = self.tenant1.desiredDistrict
            return super(Match, self).save(*args, **kwargs)

        self.budget = self.tenant1.budget + self.tenant2.budget

        if self.tenant1.desiredCity == self.tenant2.desiredCity:
            self.city = self.tenant1.desiredCity
            if self.tenant1.desiredDistrict == self.tenant2.desiredDistrict:
                self.district = self.tenant1.desiredDistrict
            else: 
                self.district = f"{self.tenant1.desiredDistrict} and {self.tenant2.desiredDistrict}"
        else: 
            self.city = f"{self.tenant1.desiredCity} and {self.tenant2.desiredCity}"
            self.district = ""

        return super(Match, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Matches"

class Shortlist(models.Model):
    user = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'house')
        