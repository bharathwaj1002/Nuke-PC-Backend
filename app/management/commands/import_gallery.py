import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from app.models import Gallery  # Change 'app' to your app's name

class Command(BaseCommand):
    help = "Import images from a folder into the Gallery model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=str,
            help="Absolute or relative path to folder containing images",
            default=os.path.join(settings.MEDIA_ROOT, "gallery"),
        )

    def handle(self, *args, **options):
        folder_path = options['source']

        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f"Folder not found: {folder_path}"))
            return

        files = os.listdir(folder_path)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))]

        if not image_files:
            self.stdout.write(self.style.WARNING("No images found."))
            return

        for filename in image_files:
            full_path = os.path.join(folder_path, filename)
            alt_text = filename  # or: os.path.splitext(filename)[0]

            if Gallery.objects.filter(alt=alt_text).exists():
                self.stdout.write(self.style.WARNING(f"Skipped (already exists): {filename}"))
                continue

            with open(full_path, 'rb') as f:
                gallery = Gallery(alt=alt_text)
                gallery.image.save(filename, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"Imported: {filename}"))

        self.stdout.write(self.style.SUCCESS("✅ All images processed."))
