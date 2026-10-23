from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=150)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization",
    )
    default_low_stock_threshold = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name


class Product(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    low_stock_threshold = models.PositiveIntegerField(
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "sku"],
                name="unique_sku_per_organization",
            )
        ]

    def effective_threshold(self):
        if self.low_stock_threshold is not None:
            return self.low_stock_threshold
        return self.organization.default_low_stock_threshold

    @property
    def is_low_stock(self):
        return self.quantity <= self.effective_threshold()

    def __str__(self):
        return self.name
