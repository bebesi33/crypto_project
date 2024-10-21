from django.test.runner import DiscoverRunner
from django.apps import apps
import logging

logger = logging.getLogger(__name__)
from django.core.management import call_command


class ManagedModelTestRunner(DiscoverRunner):
    """
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run, so that one doesn't need
    to execute the SQL manually to create them.
    Original idea/motivating example https://blog.devgenius.io/unit-testing-unmanaged-models-django-93648b5e6e24
    """

    def setup_test_environment(self, *args, **kwargs):
        logger.warning("ManagedModelTestRunner: setup_test_environment called")
        self.unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
        logger.warning(self.unmanaged_models)
        for model in self.unmanaged_models:
            model._meta.managed = True
        super().setup_test_environment(*args, **kwargs)

    def setup_databases(self, **kwargs):
        """Set up the test databases and apply migrations to copy the schema."""
        logger.warning("ManagedModelTestRunner: setup_databases called")
        databases = super().setup_databases(**kwargs)
        self.apply_migrations_to_databases()
        return databases

    def apply_migrations_to_databases(self):
        """
        Apply migrations to the test databases based on the model schema
        defined in models.py, ensuring that all tables are created.
        """
        for alias in self.get_test_databases():
            call_command("migrate", database=alias, verbosity=0, interactive=False)

    def get_test_databases(self):
        """Return the list of test databases to be used in tests."""
        return ["default", "factor_model_estimates"]

    def teardown_test_environment(self, *args, **kwargs):
        logger.warning("ManagedModelTestRunner: teardown_test_environment called")
        super().teardown_test_environment(*args, **kwargs)
        for model in self.unmanaged_models:
            model._meta.managed = False
