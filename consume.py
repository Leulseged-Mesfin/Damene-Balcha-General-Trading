import requests

# Replace with your API endpoint and credentials
auth_url = 'http://192.168.8.169:8000/api/token/'
credentials = {
    "email": "leulsegedmesfin@gmail.com",
    "password": "Leul1992"
}

# Obtain JWT token
try:
    auth_response = requests.post(auth_url, json=credentials)
    auth_response.raise_for_status()
    token = auth_response.json().get('access')
    if not token:
        raise ValueError("No token found in the response")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    token = None

# Make authenticated request if token is obtained
if token:
    api_url = 'http://192.168.8.169:8000/api/inventory/products'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    print(token)
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Model
# order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.IntegerField(null=True, blank=True)
    
#     def __str__(self):
#         return self.name

# class Order(models.Model):
#     customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
#     order_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=100, choices=(('Pending', 'Pending'), ('Completed', 'Completed')))

#     def str(self):
#         return f"Order #{self.id} by {self.customer.name}"
#     def get_total_price(self):
#         """Calculate the total price of the entire order."""
#         return sum(item.quantity * item.product.price for item in self.order_items.all())


# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def str(self):
#         return f"{self.quantity} of {self.product.name}"
#     def get_price(self):
#         return self.product.price