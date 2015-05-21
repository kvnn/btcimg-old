from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify as django_slugify

from unidecode import unidecode


def slugify(value, max_length=128, usable=None, max_retries=1000):
    """
    Normalizes string, removing non-ascii characters, converts to lowercase,
    converts underscores and spaces to hyphens, removes all other non-alphanumeric
    characters.

    Providing an exists function will result in conflict resolution. Conflicts
    will have a suffix appended to indicate the index. e.g. samsung, samsung~1
    ... samsung~10

    If the appending the suffix exceeds maxlen then the original slug will be
    truncated to fit exactly maxlen. e.g. samsung, samsun~1, samsun~2 ... samsu~10

    The usable function takes a single value `slug` and returns True or False.
    The algorithm will continue to try new slugs, until the usable method
    returns True.

    To prevent an infinate loop condition, the max_retries variable limits how
    many different slugs to try before raising a RuntimeError.

        def valid_slug(self, slug):
            parent = self.parent or self.parent_id
            return not MyModel.objects.filter(parent=parent, slug=slug).exists()

        def save(self, *args, **kwargs):
            if not self.slug is None and self.name:
                self.slug = slugify(self.name, exists=self.valid_slug)

    :param value: string to normalize
    :param maxlen: maximum length for string, default is 128. If evaluates
        False then no max length will be enforced
    :param exists: a function that returns True if the slug already exists,
        False otherwise.
    :param max_retries: limit the number of times to retry slug creation
        before giving up.
    :return: slugified value
    """
    if usable and not callable(usable):
        raise TypeError('usable argument must be a callable')

    if isinstance(value, unicode):
        # if the value is currently unicode, convert it back to a ascii
        # traslating any special chars to similar ones in ascii.
        value = unidecode(value)
    slug = django_slugify(unicode(value)).replace('_', '-')

    if max_length:
        slug = slug[:max_length]

    # decide whether to resolve conflicts
    if usable is None:
        return slug

    # conflict detection/resolution
    copy = slug
    count = 0
    # TODO: need a better slug collision algorithm, as this can be expensive
    while not usable(slug):
        count += 1
        if max_retries and count > max_retries:
            raise RuntimeError('slugify surpassed its max_retries limit of %s'
                    % max_retries)
        suffix = '~%d' % count
        slug = copy[:max_length - len(suffix)] if max_length else copy
        slug = '%s%s' % (slug, suffix)
    return slug


class SlugModel(models.Model):
    """
    A base class for any model that wants to implement an auto generated slug
    field.
    """
    # how many times we'll retry creating a slug before giving up
    MAX_RETRIES = 1000
    regenerate_slug_on_save = False
    slug = models.SlugField(_('slug'), max_length=255, unique=True,
            editable=False)

    class Meta:
        abstract = True

    @classmethod
    def is_valid_slug(cls, slug):
        """Convenience method to check if the given slug already exists."""
        manager = getattr(cls, 'all_objects', cls.objects)
        return not manager.filter(slug=slug).exists()

    @classmethod
    def get_by_slug(cls, slug, **extra):
        """
        Return the :class:`nauman.libs.common.models.SlugModel` for the given
        slug.  If the slug dosen't exist, return None.

        :param slug: the slug value to search for
        """
        try:
            return cls.objects.get(slug=slug, **extra)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_pk_or_slug(cls, value):
        """
        Return the :class:`nauman.libs.common.models.SlugModel` for the given
        slug or primary key. If either value doesn't exist, return None.

        :param value: the slug or id value to search for
        """
        try:
            return cls.objects.get(Q(slug=value) | Q(pk__iexact=value))
        except cls.DoesNotExist:
            return None

    def base_slug_value(self):
        """
        As a subclass of :class:`nauman.libs.common.models.SlugModel` one must
        implement the :method:`nauman.libs.common.models.SlugModel.base_slug_value`
        which returns a unicode value that is used as the basis of the slug value.
        """
        raise NotImplementedError

    def generate_slug(self):
        """
        Create a slug based on the value of
        :method:`nauman.libs.common.models.SlugModel.base_slug_value`, ensure
        that the slug is unique by comparing it to existing slugs.
        """
        value = self.base_slug_value()
        field = self._meta.get_field('slug')
        return slugify(value, max_length=field.max_length,
                usable=self.is_valid_slug, max_retries=self.MAX_RETRIES)

    def save(self, *args, **kwargs):
        """
        Right before a model is saved, check to see if the slug field has yet
        to be defined.  If so, generate and set the
        :attr:`nauman.libs.common.models.SlugModel.slug`.
        """
        if not self.slug or self.regenerate_slug_on_save:
            # a slug has not yet been defined, or updates are requested, generate one
            self.slug = self.generate_slug()
        return super(SlugModel, self).save(*args, **kwargs)

    def pusher_channel(self):
        return self.slug.replace('-', '')