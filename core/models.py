from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='image_users/', null=True, blank=True)
    bio = models.TextField()
    social_network = models.ManyToManyField('SocialNetwork', through='SocialNetworkUser', related_name='networks')
    level = models.ManyToManyField('Level', through='GetLevel', related_name='levels')

    def __str__(self):
        return f'{self.username}'
    

class SocialNetwork(models.Model):
    name = models.CharField(max_length=15, unique=True)
    website = models.URLField()
    image = models.ImageField(upload_to='logos_socialnetworks')

    def __str__(self):
        return f'{self.name}'

class SocialNetworkUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    username = models.CharField(max_length=15)
    url = models.URLField()

    def __str__(self):
        return f'{self.user} - {self.social_network} ({self.username})'

class Level(models.Model):
    name = models.CharField(max_length=25)
    number = models.IntegerField()
    colour = models.CharField(max_length=16, null=True, blank=True) #Hexadecimal irá aquí esto luego habrá que validarlo
    emblem = models.ImageField(upload_to='emblem/', null=True, blank=True)

    def __str__(self):
        return f'Lvl: {self.number}:{self.name}'

class GetLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    datetime_get = models.DateTimeField()

    def __str__(self):
        return f'{self.user} obtuvo el nivel {self.level} a las {self.datetime_get}'

class Keyboard(models.Model):
    name = models.CharField(max_length=35)
    colours = models.CharField(max_length=48) #En teoria va a ver 3 colores entonces 16 x 3 = 48 digitos en hexadecimal
    price = models.DecimalField(max_digits=9, decimal_places=2) #Un teclado puede costar máximo 1M€
    stars = models.DecimalField(max_digits=2, decimal_places=1) # Para las estrellas del 1 al 5
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    component = models.ManyToManyField('Component', through='KeyboardComponent', related_name='components')

    def __str__(self):
        return f'{self.name} ({self.price}€)'

class Component(models.Model):
    brand = models.CharField(max_length=25)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    shopping_website = models.URLField()
    keycaps = models.OneToOneField('Keycaps', on_delete=models.CASCADE, null=True, blank=True)
    case = models.OneToOneField('Case', on_delete=models.CASCADE, null=True, blank=True)
    plate = models.OneToOneField('Plate', on_delete=models.CASCADE, null=True, blank=True)
    pcb = models.OneToOneField('Pcb', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.brand}: {self.model} {self.price}'

class KeyboardComponent(models.Model):
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    date_modification = models.DateField()

    def __str__(self):
        return f'{self.component} se modifico en {self.keyboard} a las {self.date_modification}'

class Keycaps(models.Model):
    material = models.CharField(max_length=15, null=True, blank=True)
    layaut = models.CharField(max_length=6, null=True, blank=True)
    colours = models.CharField(max_length=48, null=True, blank=True)
    profile = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.material}'

class Case(models.Model):
    material = models.CharField(max_length=15, null=True, blank=True)
    colours = models.CharField(max_length=48, null=True, blank=True)
    measures = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.material}'

class Plate(models.Model):
    material = models.CharField(max_length=15, null=True, blank=True)
    measures = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.material}'

class Pcb(models.Model):
    connectivity = models.CharField(max_length=50, null=True, blank=True) #Esto cambiarlo por un TEXTCHOICES
    measures = models.CharField(max_length=30, null=True, blank=True)
    layaut = models.CharField(max_length=10, null=True, blank=True)
    rgb = models.BooleanField(default=True)
    hotswap = models.BooleanField(default=True)
    firmware = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'RGB: {self.rgb} Hotswap: {self.hotswap}'

class Switch(models.Model):
    type = models.CharField(max_length=25) #Esto será un textchoices
    force = models.DecimalField(max_digits=5, decimal_places=2)
    point = models.DecimalField(max_digits=5, decimal_places=2)
    route = models.DecimalField(max_digits=5, decimal_places=2)
    useful_life = models.IntegerField()
    pin_number = models.IntegerField() #Esto podria ser un integer choices 

    def __str__(self):
        return f'{self.type}'