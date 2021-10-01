from django.db import models
from django.contrib.auth                                        import get_user_model
# Create your models here.

User = get_user_model()

# Create your models here.
class Product(models.Model):

    title                   = models.CharField('TITLE' ,                max_length=120)
    #slug                    = models.SlugField('SLUG',                  unique=True, blank=True, null=True)
    digital                 = models.BooleanField("DIGITAL",                   default=False, blank=True, null=True)
    image                   = models.ImageField('PRODUCT IMAGE',        upload_to='photo/',        blank=True,     null=True)

    description             = models.TextField('DESCRIPTION',           blank=True, null=True)
    price                   = models.DecimalField('PRICE',              max_digits=19,      default=0,              decimal_places=2,  blank=True)
    discount_price          = models.DecimalField('DISCOUNTED PRICE',   max_digits=19,      default=0,              decimal_places=2,  blank=True)
    #label                   = models.CharField('LABEL',                 max_length=250,     choices=LABEL_CHOICES,  blank=True,  null=True)
    top_featured            = models.BooleanField("TOP FEATURE",        default=False,      blank=True, null=True)
    best_seller             = models.BooleanField("BEST SELLER",        default=False,      blank=True, null=True)
    #category                = models.ForeignKey('categories.Category',  on_delete=models.PROTECT, related_name='products_categories',       null=True)

    class Meta:

        app_label   = 'store'
        db_table    = 'Product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):

    user                        = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered                = models.DateTimeField(auto_now_add= True)
    complete                    = models.BooleanField(default=False)

    address                     = models.CharField(max_length=120, blank=True, null=True)
    payment                     = models.CharField(max_length=120, blank=True, null=True)
    coupon                      = models.CharField(max_length=120, blank=True, null=True)
    being_delivered             = models.CharField(max_length=120, blank=True, null=True)
    received                    = models.CharField(max_length=120, blank=True, null=True)
    refund_requested            = models.CharField(max_length=120, blank=True, null=True)
    refund_granted              = models.CharField(max_length=120, blank=True, null=True)


    class Meta:

        app_label   = 'store'
        db_table    = 'Order'
        verbose_name_plural = 'orders'

    # def __str__(self):
    #     return self.user.username

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])

        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])

        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()

        for i in orderitems:
            if i.item.digital == False:
                shipping = True

        return shipping


class OrderItem(models.Model):

    user                          = models.ForeignKey(User,             verbose_name="USER",    on_delete=models.CASCADE)
    product                       = models.ForeignKey(Product,          verbose_name="PRODUCT", on_delete=models.CASCADE)
    order                         = models.ForeignKey(Order,            verbose_name="ORDER",   on_delete=models.CASCADE)
    complete                      = models.BooleanField(default=False)
    quantity                      = models.IntegerField("QUANTITY",     default=1)
    date_added                    = models.DateTimeField("DATE ADDED",  auto_now_add= True)

    class Meta:

        app_label   = 'store'
        db_table    = 'OrderItem'
        verbose_name_plural = 'orderitems'

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    @property
    def get_total(self):
        total = self.product.price * self.quantity

        return total

    @property
    def get_total_discount_price(self):
        total = self.product.discount_price * self.quantity

        return total

class ShippingAddress(models.Model):

    user                                = models.ForeignKey(User,           verbose_name="USER", on_delete=models.CASCADE)
    order                               = models.ForeignKey(Order,          verbose_name="ORDER", on_delete=models.CASCADE)
    address                             = models.CharField("ADDRESS",       max_length=250, null=True, blank=True)
    city                                = models.CharField("CITY",          max_length=250, null=True, blank=True)
    state                               = models.CharField("STATE",         max_length=250, null=True, blank=True)
    zipcode                             = models.CharField("ZIP CODE",      max_length=250, null=True, blank=True)
    date_added                          = models.DateTimeField("DATE TIME", auto_now_add=True)