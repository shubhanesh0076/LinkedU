from django.db import models
from accounts.models import User

# Create your models here.


class FriendRequest(models.Model):
    """
    This is the friend request model.
    
    The FriendRequest model is used to represent friend requests between users. It includes
    fields for the sending user (from_user), the receiving user (to_user), the status of the 
    request, and the timestamp when the request was created.
    """
    
    CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=CHOICES,default="pending",)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user} to {self.to_user} - {self.status}"
