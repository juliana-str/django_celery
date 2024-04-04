from django.db import models

from users.models import User


class Order(models.Model):
    """Model for creating an order."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name="Покупатель",
    )
    order_number = models.CharField("Number", max_length=50, unique=True)
    ordering_date = models.DateTimeField(auto_now_add=True, verbose_name="DateTime")

    class Meta:
        ordering = ["-ordering_date"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        if self.user is not None:
            return f"Order {self.order_number} of {self.user.username}"
        return f"Order {self.order_number} of Anonymous User"
