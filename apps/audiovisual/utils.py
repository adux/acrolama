from PIL import Image
from django.db.models.fields.files import ImageFieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile

def _create_thumbnail(image_field: ImageFieldFile, thumbnail_image_field: ImageFieldFile, size: tuple):
    image = Image.open(image_field.file.file)
    image.thumbnail(size=size)
    image_file = BytesIO()
    image.save(image_file, image.format)
    thumbnail_image_field.save(
        image_field.name,
        InMemoryUploadedFile(
            image_file,
            None, '',
            image_field.file.content_type,
            image.size,
            image_field.file.charset,
        ),
        save=False
    )

