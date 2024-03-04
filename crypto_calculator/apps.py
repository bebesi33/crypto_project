from django.apps import AppConfig


class CryptoCalculatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crypto_calculator"
    verbose_name = 'The Crypto Risk Calculator'
    app_label = 'crypto_calculator'  # this is needed, as the model is defined outside the main Django stuff

