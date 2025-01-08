# models.py
from django.db import models

class TranslationHistory(models.Model):
    input_text = models.TextField()
    translated_text = models.TextField()
    from_language = models.CharField(max_length=10)
    to_language = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.input_text} -> {self.translated_text} ({self.from_language} to {self.to_language})"
