from django import template
from Order.models import Order

register = template.Library()

@register.filter
def item_total(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].orderitems.count()
    else:
        return 0