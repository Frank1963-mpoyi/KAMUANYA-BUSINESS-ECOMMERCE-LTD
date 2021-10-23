from django.db.models.signals                                       import pre_save
from django.db                                                      import models
from django.contrib.auth                                            import get_user_model

from pcshop.common.upload_images                                    import upload_img_path
from pcshop.common.global_choices                                   import LABEL_CHOICES
from pcshop.common.search                                           import ProductsManager
from pcshop.core.model_mixins                                       import AuditFields, EmailFields
from pcshop.core.utils                                              import unique_slug_generator, product_randcode_gen, order_randcode_gen, orderitem_randcode_gen, \
                                                                            shipping_randcode_gen, transaction_id_randcode_gen, get_in_touch_randcode_gen

User = get_user_model()


class Product(AuditFields):

    code                    = models.CharField('CODE',      max_length=100,     blank=False, default=product_randcode_gen)

    title                   = models.CharField('TITLE' ,     max_length=120)
    slug                    = models.SlugField('SLUG',       unique=True, blank=True,   null=True)
    digital                 = models.BooleanField("DIGITAL", default=False,  blank=True, null=True)
    image                   = models.ImageField('IMAGE',     upload_to=upload_img_path, blank=True, null=True)

    description             = models.CharField('DESCRIPTION',           max_length=250 ,     blank=True, null=True )
    price                   = models.DecimalField('PRICE',              max_digits=19,      default=0,              decimal_places=2,  blank=True)
    discount_price          = models.DecimalField('DISCOUNTED PRICE',   max_digits=19,      default=0,              decimal_places=2,  blank=True)
    label                   = models.CharField('LABEL',                 max_length=250,     choices=LABEL_CHOICES,  blank=True,  null=True)
    top_featured            = models.BooleanField("TOP FEATURE",        default=False,      blank=True, null=True)
    best_seller             = models.BooleanField("BEST SELLER",        default=False,      blank=True, null=True)
    category                = models.ForeignKey('self',   on_delete=models.PROTECT, related_name='products_categories', blank=True,  null=True)

    objects                 = ProductsManager()
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


class Order(AuditFields):

    code                        = models.CharField('CODE', max_length=100, blank=False, default=order_randcode_gen)
    transaction_id              = models.CharField(max_length=120,  blank=True, default=transaction_id_randcode_gen)

    complete                    = models.BooleanField(default=False)

    customer                    = models.ForeignKey(User, on_delete=models.CASCADE)
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
            if i.product.digital == False:
                shipping = True

        return shipping


class OrderItem(AuditFields):

    code                          = models.CharField('CODE', max_length=100, blank=False, default=orderitem_randcode_gen)

    customer                      = models.ForeignKey(User,             verbose_name="USER",    on_delete=models.CASCADE, null=True, blank=True)
    product                       = models.ForeignKey(Product,          verbose_name="PRODUCT", on_delete=models.CASCADE)
    order                         = models.ForeignKey(Order,            verbose_name="ORDER",   on_delete=models.CASCADE)
    complete                      = models.BooleanField(default=False)
    quantity                      = models.IntegerField("QUANTITY",     default=0)
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


class ShippingAddress(AuditFields):

    code                                = models.CharField('CODE', max_length=100, blank=False, default=shipping_randcode_gen)

    customer                            = models.ForeignKey(User,       verbose_name="USER", on_delete=models.CASCADE)
    order                               = models.ForeignKey(Order,          verbose_name="ORDER", on_delete=models.CASCADE)
    address                             = models.CharField("ADDRESS",       max_length=250, null=True, blank=True)
    city                                = models.CharField("CITY",          max_length=250, null=True, blank=True)
    state                               = models.CharField("STATE",         max_length=250, null=True, blank=True)
    zipcode                             = models.CharField("ZIP CODE",      max_length=250, null=True, blank=True)
    date_added                          = models.DateTimeField("DATE TIME", auto_now_add=True)



class GetInTouch(EmailFields):

    code                                = models.CharField('CODE', max_length=100, blank=False, default=get_in_touch_randcode_gen)

    fullname                            = models.CharField(max_length=120)
    subject                             = models.CharField(max_length=250)
    message                             = models.TextField()

    def __str__(self):
        return self.fullname

class Staff(models.Model):
    code                                = models.CharField('CODE',      max_length=100,     blank=False, default=product_randcode_gen)

    name                                = models.CharField(max_length=250)
    job_position                        = models.CharField(max_length=250)
    image                               = models.ImageField('IMAGE', upload_to=upload_img_path, blank=True, null=True)

    def __str__(self):
        return self.name

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product)