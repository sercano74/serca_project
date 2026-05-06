from django.db import models


class HomeNewsBadge(models.Model):
    text = models.CharField(max_length=160)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Badge de noticia"
        verbose_name_plural = "Badges de noticias"
        ordering = ["-updated_at"]

    def __str__(self):
        state = "activo" if self.is_active else "inactivo"
        return f"{self.text} ({state})"
