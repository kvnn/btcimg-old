import os
import random
from math import fabs
from PIL import Image, ImageFilter
from StringIO import StringIO

from django.db import models
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as storage

from btcimg.libs.common.models import SlugModel


class Asset(SlugModel, models.Model):
    owner = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=255)
    unlock_value = models.DecimalField(max_digits=19, decimal_places=2, default=1.0)
    btc_address = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    public_image = models.ImageField(max_length=255, blank=True, upload_to='public_images')
    public_image_blur_ratio = models.FloatField(null=True, blank=True)
    private_image = models.ImageField(max_length=255, upload_to='private_images')

    blocked = models.BooleanField(default=False)
    edit_hash = models.CharField(max_length=255, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def base_slug_value(self):
        return unicode(self.name)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('locker:asset-detail', kwargs={'slug': self.slug})

    def _determine_blur_radius(self, image):
        return 0.25 * image.size[0] * self.public_image_blur_ratio

    def _generate_public_image(self):
        private_file = storage.open(self.private_image.name, 'r')
        private_file = Image.open(private_file)
        image = private_file.filter(ImageFilter.GaussianBlur(self._determine_blur_radius(private_file)))
        private_file.close()

        # Path to save to, name, and extension
        image_name, image_extension = os.path.splitext(self.private_image.name)
        image_extension = image_extension.lower()

        image_filename = image_name + '_public' + image_extension

        if image_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif image_extension == '.gif':
            FTYPE = 'GIF'
        elif image_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_image = StringIO()
        image.save(temp_image, FTYPE)
        temp_image.seek(0)

        # Load a ContentFile into the thumbnail field so it gets saved
        self.public_image.save(image_filename, ContentFile(temp_image.read()), save=True)
        temp_image.close()

    def get_public_image(self, btc_received):
        if btc_received >= self.unlock_value:
            self.public_image_blur_ratio = 0
            self.public_image = self.private_image
            self.save()
            return self.private_image

        current_blur_ratio = self.public_image_blur_ratio
        actual_blur_ratio = float(1.0) - float(btc_received) / self.unlock_value.__float__()
        if not current_blur_ratio or fabs(1 - actual_blur_ratio / current_blur_ratio) > 0.1:
            # If there is a >10% difference, update the image & the ratio
            # This means that images are comprised of 10 steps, 1 being "most blurry"
            # and 10 being "completely clear".
            self.public_image_blur_ratio = actual_blur_ratio
            self.save()
            self._generate_public_image()
        return self.public_image

    class Meta:
        ordering = ['-name']


@receiver(post_save, sender=Asset)
def add_edit_hash(sender, **kwargs):
    obj = kwargs['instance']
    if not len(obj.edit_hash):
        obj.edit_hash = '%d%s%d' % (random.randint(99999, 9999999999), obj.btc_address, obj.pk)
        obj.save()
