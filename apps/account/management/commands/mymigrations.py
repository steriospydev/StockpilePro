from django.core.management.base import BaseCommand
from django.apps import apps
import subprocess

class Command(BaseCommand):
    help = 'Runs makemigrations for all apps in the apps/ directory'

    def handle(self, *args, **options):
        apps_directory = 'apps'

        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            app_name = app_config.name
            # Extract the app name without the "apps." prefix
            app_name_without_prefix = app_name[len(apps_directory)+1:]

            if app_name.startswith(apps_directory):
                command = ['python', 'manage.py', 'makemigrations', app_name_without_prefix]

                self.stdout.write(f"Running 'python manage.py makemigrations {app_name}'...")
                subprocess.run(command)
                self.stdout.write(self.style.SUCCESS(f"Successfully ran 'python manage.py makemigrations {app_name}'\n"))

        self.stdout.write(self.style.SUCCESS("Migration creation complete!"))
