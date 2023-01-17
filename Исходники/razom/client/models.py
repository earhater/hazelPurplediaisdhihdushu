import hashlib

from tortoise import fields
from tortoise.models import Model


class Client(Model):
    """Base model for client"""
    telegram_username = fields.CharField(
        max_length=255, null=True)
    telegram_id = fields.BigIntField(pk=True, unique=True)
    register_data = fields.DatetimeField(auto_now_add=True)
    is_blocked = fields.BooleanField(default=False)
    is_participating = fields.BooleanField(
        default=False, description="Участвует ли в розыгрыше")
    personal_number = fields.CharField(max_length=12, null=True)
    moderation_accept = fields.BooleanField(default=False)

    def generate_personal_number(self):
        ids = str(self.telegram_id)
        self.personal_number = int(hashlib.sha1(
            ids.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    class Meta:
        table = "client"


class Moderation(Model):
    user = fields.OneToOneField(
        'models.Client', related_name="moderations", on_delete=fields.CASCADE)
    image = fields.CharField(max_length=1024)
    accepted = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "on_moderation"
