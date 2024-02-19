import time
import hashlib
from typing import List, Dict
from slugify import slugify
from hashids import Hashids

from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings
from .exceptions import SlugifyFieldNotSetException


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(archived_stamp__isnull=True)

    def archived(self):
        return self.filter(archived_stamp__isnull=False)

    def archive(self, archived_by=None):
        for item in self:
            item.archive(archived_by)

    def restore(self, restored_by=None):
        for item in self:
            item.restore(restored_by)

    def ordered(self):
        return self.all().order_by('-created_stamp')


class CrmMixin(models.Model):
    created_stamp = models.DateTimeField(default=timezone.now, db_index=True)
    modified_stamp = models.DateTimeField(auto_now=timezone.now)
    archived_stamp = models.DateTimeField(null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')

    objects = ActiveQuerySet.as_manager()

    class Meta:
        abstract = True

    def archive(self, archived_by=None):
        self.archived_stamp = timezone.now()
        if archived_by:
            self.archived_by = archived_by
        self.save()

    def modify(self, modified_by=None):
        self.modified_stamp = timezone.now()
        if modified_by:
            self.modified_by = modified_by
        self.save()

    def restore(self, restored_by=None):
        self.archived_stamp = None
        self.archived_by = None
        self.modify(restored_by)

    @property
    def is_active(self) -> bool:
        return not bool(self.archived_stamp)


class SlugifyMixin(models.Model):
    SLUGIFY_FIELD = ''
    slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True)

    class Meta:
        abstract = True

    @classmethod
    def is_allowed_to_assign_slug(cls, value, instance=None):
        slug = slugify(value)
        qs = cls.objects.filter(slug=slug)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        return not qs.exists()

    def assign_slug(self):
        if not self.SLUGIFY_FIELD:
            raise SlugifyFieldNotSetException('Field for slugify not set!')

        slug = slugify(getattr(self, self.SLUGIFY_FIELD))
        self.slug = slug if len(slug) <= 255 else slug[:255]
        self.save()
        return self


class LikeMixin(models.Model):
    is_liked = models.BooleanField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True

    def like(self):
        self.is_liked = True
        self.save()

    def dislike(self):
        self.is_liked = False
        self.save()

    def deactivate(self):
        self.is_liked = None
        self.save()


class SlugifyHTMLMixin(SlugifyMixin):
    @classmethod
    def slugify_without_html(cls, value):
        return slugify(strip_tags(value))

    @classmethod
    def is_allowed_to_assign_slug(cls, value, instance=None):
        slug = cls.slugify_without_html(value)
        qs = cls.objects.exclude(slug__isnull=True, slug__exact='').filter(slug=slug)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        return not qs.exists()

    def assign_slug(self):
        if not self.SLUGIFY_FIELD:
            raise SlugifyFieldNotSetException('Field for slugify not set!')

        slug = self.slugify_without_html(getattr(self, self.SLUGIFY_FIELD))
        self.slug = slug if len(slug) <= 255 else slug[:255]
        self.save()
        return self


class ExportableMixin(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_data_to_export(cls) -> List[Dict]:
        raise NotImplementedError

    @classmethod
    def clear_previous(cls):
        raise NotImplementedError

    @classmethod
    def import_data(cls, data):
        raise NotImplementedError

    @classmethod
    def validate_data(cls, data):
        raise NotImplementedError

    @classmethod
    @transaction.atomic
    def import_from_data(cls, data):
        cls.clear_previous()
        cls.validate_data(data)
        cls.import_data(data)
        return True


class HashableMixin(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def __hashid(cls, salt=''):
        return Hashids(salt=settings.HASHID_SECRET + str(cls.__name__) + salt, min_length=8)

    def hashid_encode(self, salt='', *values):
        # accept only integers
        timestamp = int(time.time())
        return self.__hashid(salt=salt).encode(timestamp, self.id, *values)

    @classmethod
    def hashid_decode(cls, hash_id, salt=''):
        return cls.__hashid(salt=salt).decode(hash_id)

    @property
    def hash_id(self):
        return getattr(self, '_hash_id', self.hashid_encode())

    @classmethod
    def get_hashid_queryset(cls):
        return cls.objects.all()

    @classmethod
    def get_by_hash_id(cls, hash_id, salt=''):
        data = cls.hashid_decode(hash_id, salt=salt)
        if not data:
            raise cls.DoesNotExist

        try:
            obj = cls.get_hashid_queryset().get(pk=data[1])
        except IndexError:
            raise cls.DoesNotExist
        setattr(obj, '_hash_id', hash_id)
        return obj

    @classmethod
    def get_by_hash_id_safe(cls, *args, **kwargs):
        try:
            return cls.get_by_hash_id(*args, **kwargs)
        except cls.DoesNotExist:
            return None

    @classmethod
    def hash_str_to_int(cls, value: str) -> int:
        return int(hashlib.sha1(str(value).encode("utf-8")).hexdigest(), 16)
