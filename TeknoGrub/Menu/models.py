from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class MenuItem(models.Model):
    item_id = models.AutoField(primary_key=True)

    canteen = models.ForeignKey('Canteen.Canteen', on_delete=models.DO_NOTHING, db_column='canteen_id')

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_column='category_id')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)

    # CARDINALITY: 1 Item has exactly 1 Stock Record -> OneToOneField
    item = models.OneToOneField(MenuItem, on_delete=models.DO_NOTHING, db_column='item_id', unique=True)

    current_stock = models.IntegerField(default=0)
    threshold_level = models.IntegerField(default=10)

    class Meta:
        verbose_name_plural = "Inventories"


class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    # References User App via string to avoid imports
    user = models.ForeignKey('User.Users', on_delete=models.DO_NOTHING, db_column='user_id')
    item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING, db_column='item_id')
    added_at = models.DateTimeField(auto_now_add=True)
