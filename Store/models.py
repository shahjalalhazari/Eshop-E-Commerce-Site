from django.db import models
from django.shortcuts import reverse
from django.conf import settings


# CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"


LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller'),
)


# PRODUCT MODEL
class Item(models.Model):
    item_name = models.CharField(max_length=264)
    main_image = models.ImageField(upload_to="ItemImage")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    description = models.TextField()
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    label = models.CharField(choices=LABEL, max_length=2, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.item_name
    class Meta:
        ordering = ['-created']
    def get_absolute_url(self):
        return reverse("store:product", kwargs={"pk" : self.pk})
    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={"pk" : self.pk})
    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={"pk" : self.pk})