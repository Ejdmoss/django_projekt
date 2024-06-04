import os
import shutil
from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.utils import timezone


class Vyrobce(models.Model):
    def logo_upload_path(self, filename):
        return os.path.join('vyrobci', str(self.id), filename)

    nazev = models.CharField(max_length=100, verbose_name='Název', help_text='Zadejte název výrobce')
    telefon = models.CharField(max_length=20, verbose_name='Telefon',
                               help_text='Zadejte telefonní číslo výrobce (včetně předvolby)',
                               validators=[RegexValidator(regex='^(\\+420)? ?[1-9][0-9]{2}( ?[0-9]{3}){2}$',
                                                          message='Zadejte prosím platné telefonní číslo.'
                                                          )])
    email = models.EmailField(max_length=254, verbose_name='E-mail', help_text='Zadejte e-mailovou adresu výrobce',
                              validators=[EmailValidator('Neplatný e-mail.')])
    logo = models.ImageField(upload_to=logo_upload_path, blank=True, null=True, verbose_name='Logo',
                             help_text='Nahrajte logo výrobce')

    class Meta:
        verbose_name = 'Výrobce'
        verbose_name_plural = 'Výrobci'
        ordering = ['nazev']

    def __str__(self):
        return self.nazev

    def delete(self, *args, **kwargs):
        if self.logo:
            logo_path = os.path.join('media', 'vyrobci', str(self.id))
            shutil.rmtree(logo_path)
        super().delete(*args, **kwargs)


class VyrobniZavod(models.Model):
    nazev = models.CharField(max_length=100, verbose_name='Název', help_text='Zadejte název výrobního závodu')
    adresa = models.CharField(max_length=200, verbose_name='Adresa', help_text='Zadejte adresu výrobního závodu')
    vyrobce = models.ForeignKey('Vyrobce', verbose_name='Výrobce', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Továrna'
        verbose_name_plural = 'Továrny'
        ordering = ['nazev']

    def __str__(self):
        return self.nazev


class Auto(models.Model):
    MAX_DELKA_MODELU = 50
    DELKA_SPZ = 8
    MIN_ROK_VYROBY = 2000
    MAX_ROK_VYROBY = timezone.now().year

    DRUH_PREVODOVKY = [
        ('manuální', 'Manuální'),
        ('automatická', 'Automatická'),
    ]

    DRUH_PALIVA = [
        ('benzín', 'Benzín'),
        ('nafta', 'Nafta'),
        ('elektrika', 'Elektrika'),
    ]

    MODELY = [
        ('brabus 500', 'Brabus 500'),
        ('brabus 800', 'Brabus 800'),
        ('brabus 900', 'Brabus 900'),
        ('mercedes G63', 'Mercedes G63'),
        ('mercedes G65', 'Mercedes G65'),
        ('mercedes-AMG EQE', 'Mercedes-AMG EQE'),
    ]

    model = models.CharField(verbose_name='Typ modelu', default='Brabus 900', max_length=45,
                                  choices=MODELY)
    spz = models.CharField(max_length=DELKA_SPZ, verbose_name='SPZ', help_text='SPZ',
                           validators=[RegexValidator(r'^[A-Z0-9]{8}$')])
    rok_vyroby = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Rok výroby',
                                                  help_text='Zadej rok výroby',
                                                  validators=[MinValueValidator(MIN_ROK_VYROBY),
                                                              MaxValueValidator(MAX_ROK_VYROBY)])
    prevodovka = models.CharField(verbose_name='Typ převodovky', default='manuální', max_length=15,
                                  choices=DRUH_PREVODOVKY)
    palivo = models.CharField(verbose_name='Typ paliva', default='benzín', max_length=10, choices=DRUH_PALIVA)
    zavod = models.ForeignKey('VyrobniZavod', verbose_name='Výrobní závod', on_delete=models.CASCADE)



    class Meta:
        verbose_name = 'Auto'
        verbose_name_plural = 'Auta'
        ordering = ['zavod', '-rok_vyroby']

    def __str__(self):
        return f'{self.model}, ({self.spz})'


@receiver(models.signals.post_save, sender=Vyrobce)
def vyrobce_post_save(sender, instance, created, **kwargs):
    if created:
        directory_path = os.path.join('media', 'vyrobci', str(instance.id))
        old_directory_path = os.path.join('media', 'vyrobci', 'None')
        if os.path.exists(old_directory_path):
            os.rename(old_directory_path, directory_path)
            instance.logo.name = instance.logo.name.replace('None', str(instance.id))
            instance.save()
