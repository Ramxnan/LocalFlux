from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os
import shutil
from django.conf import settings

class Command(BaseCommand):
    help = 'Deletes all non-admin users and their corresponding folders in media/storage'

    def handle(self, *args, **kwargs):
        for user in User.objects.filter(is_superuser=False):
            # Construct the path to the user's folder
            display_name = user.username.split('@')[0]
            user_folder = os.path.join(settings.MEDIA_ROOT, 'storage', display_name)
            
            # Check if the folder exists
            if os.path.exists(user_folder):
                # If it exists, delete the folder and all its contents
                shutil.rmtree(user_folder)
                self.stdout.write(self.style.SUCCESS(f'Deleted folder for user: {display_name}'))
            
            # Delete the user
            user.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all non-admin users and their folders'))
