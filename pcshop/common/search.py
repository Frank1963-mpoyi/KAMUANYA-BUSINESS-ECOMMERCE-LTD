from django.db                                                      import models
from django.db.models                                               import Q


class ProductQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query =="":
            return self.none()
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(discount_price__icontains=query) |
                Q(top_featured__icontains=query) |
                Q(best_seller__icontains=query)
        )
        return self.filter(lookups)

class ProductsManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


