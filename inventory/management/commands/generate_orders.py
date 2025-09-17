from django.core.management.base import BaseCommand
from inventory.models import Order, Product, CustomerInfo
from inventory.serializers import OrderSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create 10000 orders using the serializer logic'

    def handle(self, *args, **options):
        customers = list(CustomerInfo.objects.all())
        products = list(Product.objects.all())
        user = User.objects.first()  # Replace with specific user if needed

        if not customers or not products or not user:
            self.stdout.write(self.style.ERROR('Missing required data: customers/products/user'))
            return

        factory = APIRequestFactory()
        dummy_request = factory.post('/api/inventory/orders/')
        request = Request(dummy_request)
        request.user = user  # simulate request.user

        success_count = 0
        fail_count = 0

        for _ in range(10000):
            customer = random.choice(customers)
            product = random.choice(products)
            quantity = random.randint(1, 5)
            unit_price = product.selling_price if hasattr(product, 'selling_price') else 3000

            data = {
                "customer": customer.id,
                "receipt": "No Receipt",
                "payment_status": "Paid",
                "paid_amount": unit_price * quantity,
                "items": [
                    {
                        "product": product.id,
                        "quantity": quantity,
                        "unit_price": unit_price
                    }
                ]
            }

            serializer = OrderSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                try:
                    serializer.save()
                    success_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Error saving order: {str(e)}"))
                    fail_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Invalid data: {serializer.errors}"))
                fail_count += 1

        self.stdout.write(self.style.SUCCESS(f"Completed: {success_count} successful orders, {fail_count} failed."))
