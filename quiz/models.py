# quiz/models.py
from django.db import models

class Question(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=255, blank=True)
    option_b = models.CharField(max_length=255, blank=True)
    option_c = models.CharField(max_length=255, blank=True)
    option_d = models.CharField(max_length=255, blank=True)

    # store which option is correct as one of 'a','b','c','d'
    CORRECT_CHOICES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ]
    correct_option = models.CharField(
        max_length=1,
        choices=CORRECT_CHOICES,
        help_text="Choose which option (A/B/C/D) is correct",
        default='a'
    )

    def options_list(self):
        """Return options in order [A, B, C, D] — filter out empty strings if any."""
        return [o for o in [self.option_a, self.option_b, self.option_c, self.option_d] if o.strip()]

    def correct_value(self):
        mapping = {'a': self.option_a, 'b': self.option_b, 'c': self.option_c, 'd': self.option_d}
        return mapping.get(self.correct_option)

    def __str__(self):
        return self.question_text[:80]

