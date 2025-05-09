from django.db import models

class Query(models.Model):
    hadees_number = models.CharField(max_length=100)
    line_number = models.CharField(max_length=100)
    query_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query on Hadees {self.hadees_number} - Line {self.line_number}"
