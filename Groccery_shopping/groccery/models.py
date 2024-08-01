from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Category Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product Price")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Product Category", related_name="products")
    image = models.ImageField(upload_to='static/Images', verbose_name="Product Image", null=True, blank=True)

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)

    def register(self):
        try:
            self.save()
            return True
        except:
            return False

    def doesExist(self):
        return Customer.objects.filter(phone=self.phone).exists()


class Cart(models.Model):
    phone = models.CharField(max_length=12)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)

    class Meta:
        unique_together = ('phone', 'product')

    def __str__(self):
        return f"Cart({self.phone}, {self.product.name}, {self.quantity})"

   