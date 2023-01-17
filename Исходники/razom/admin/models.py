from tortoise import fields
from tortoise.models import Model


class Admin(Model):
    """Base model for admin"""
    telegram_username = fields.CharField(max_length=255, unique=True)
    telegram_id = fields.BigIntField(pk=True, unique=True)
    register_data = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "admin"


class Present(Model):
    title = fields.CharField(max_length=30)
    link = fields.CharField(max_length=1024)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "present"


class Income(Model):
    text = fields.CharField(max_length=1024)
    from_user = fields.IntField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "income_message"


class Config(Model):
    group = fields.CharField(max_length=256)
    terms = fields.TextField()

    class Meta:
        table = "settings"


class Catalog(Model):
    link = fields.CharField(max_length=256)
    text = fields.CharField(max_length=25)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "catalog_link"
