import binascii
import os
import random
import string

from django.utils.text import slugify


def generate_code():
    return binascii.hexlify(os.urandom(20)).decode('utf-8')


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, attr='title', new_slug=None):
    slug = new_slug or slugify(getattr(instance, attr), slugify)

    Class: object = instance.__class__
    qs_exists = Class.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug
