from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50) # Example categories: 'Coffee', 'Tea', 'Pastries', 'Snacks'
    # Add the image field
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True, help_text="Optional: Upload an image for the menu item.")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Optional: method to get image URL or a placeholder
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None # Or path to a default placeholder image

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) # To mark if an admin has read it

    def __str__(self):
        return f"Message from {self.name} ({self.email}) on {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
