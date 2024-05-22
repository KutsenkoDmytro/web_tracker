from django.db import models
from django.urls import reverse


class Campaign(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name="Кампанія")
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name="Slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кампанія"
        verbose_name_plural = "Кампанії"

    def get_absolute_url(self):
        return reverse('campaign', kwargs={'camp_slug': self.slug})


class Offer(models.Model):
    title = models.CharField(max_length=100, verbose_name="Офер")

    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name="Slug")
    content = models.TextField(blank=True, verbose_name='Додатково')
    cost_per_click = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name="Ціна за клік")
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Час створення')
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Час зміни')
    campaign = models.ForeignKey(Campaign, related_name='offers',
                                 on_delete=models.CASCADE,
                                 verbose_name="Кампанія")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Офер"
        verbose_name_plural = "Офери"

    def total_clicks(self):
        return self.rel_click.count()

    def total_leads(self):
        return self.rel_click.filter(rel_lead__isnull=False).count()


class Click(models.Model):
    offer = models.ForeignKey(Offer, related_name='rel_click',
                              on_delete=models.CASCADE, verbose_name="Офер")
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Часова мітка")

    def __str__(self):
        return f"Click on {self.offer.title} at {self.timestamp}"

    class Meta:
        verbose_name = "Клік"
        verbose_name_plural = "Кліки"


class Lead(models.Model):
    click = models.OneToOneField(Click, related_name='rel_lead',
                                 on_delete=models.CASCADE, verbose_name="Клік")
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Часова мітка")
    ip_address = models.GenericIPAddressField(verbose_name="IP адреса")
    operating_system = models.CharField(null=True, blank=True, max_length=100,
                                        verbose_name="Система")
    user_agent = models.CharField(max_length=255, verbose_name="User-Agent")
    geolocation = models.TextField(null=True, blank=True,
                                   verbose_name="Геолокація")
    referrer = models.URLField(null=True, blank=True, verbose_name="Реферер")

    # Оптримання інформації (ел. адреси), як приклад цільової дії реклами.
    email = models.EmailField(verbose_name="Електронна пошта")
    phone_number = models.CharField(max_length=20,
                                    verbose_name="Номер телефону")

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = "Лід"
        verbose_name_plural = "Ліди"
