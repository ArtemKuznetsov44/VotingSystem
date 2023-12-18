from django.apps import AppConfig


# This is the main class to configure our app - main app
class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    # With this param we can change the name in admin panel for our app instead of default "MAIN":
    # verbose_name = 'Система голосования'
