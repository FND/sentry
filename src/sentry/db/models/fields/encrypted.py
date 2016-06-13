from __future__ import absolute_import

__all__ = (
    'EncryptedCharField',
    'EncryptedJsonField',
    'EncryptedPickledObjectField',
)

import six

from django.db.models import CharField
from jsonfield import JSONField
from picklefield.fields import PickledObjectField
from sentry.utils.encryption import decrypt, encrypt


class EncryptedCharField(CharField):
    def get_db_prep_value(self, value, *args, **kwargs):
        value = super(EncryptedCharField, self).get_db_prep_value(
            value, *args, **kwargs)
        return encrypt(value)

    def to_python(self, value):
        if value is not None and isinstance(value, six.string_types):
            value = decrypt(value)
        return super(EncryptedCharField, self).to_python(value)

    def get_prep_lookup(self, lookup_type, value):
        raise NotImplementedError('{!r} lookup type for {!r} is not supported'.format(
            lookup_type,
            self,
        ))


class EncryptedJsonField(JSONField):
    def get_db_prep_value(self, value, *args, **kwargs):
        value = super(EncryptedJsonField, self).get_db_prep_value(
            value, *args, **kwargs)
        return encrypt(value)

    def to_python(self, value):
        if value is not None and isinstance(value, six.string_types):
            value = decrypt(value)
        return super(EncryptedJsonField, self).to_python(value)

    def get_prep_lookup(self, lookup_type, value):
        raise NotImplementedError('{!r} lookup type for {!r} is not supported'.format(
            lookup_type,
            self,
        ))


class EncryptedPickledObjectField(PickledObjectField):
    def get_db_prep_value(self, value, *args, **kwargs):
        if isinstance(value, six.binary_type):
            value = value.decode('utf-8')
        value = super(EncryptedPickledObjectField, self).get_db_prep_value(
            value, *args, **kwargs)
        return encrypt(value)

    def to_python(self, value):
        if value is not None and isinstance(value, six.string_types):
            value = decrypt(value)
        return super(EncryptedPickledObjectField, self).to_python(value)

    def get_prep_lookup(self, lookup_type, value):
        raise NotImplementedError('{!r} lookup type for {!r} is not supported'.format(
            lookup_type,
            self,
        ))
