from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise


class Whitelisted(Model):
    address = fields.TextField(primary_key=True)
    unwhitelist_at = fields.IntField()


class Timedout(Model):
    address = fields.TextField(primary_key=True)
    untimeout_at = fields.IntField()


def register_database(app):
    register_tortoise(
        app=app,
        
        generate_schemas=True,
        add_exception_handlers=True,
        
        config={
            "connections": {
                "default": "sqlite://db.sqlite3"
            },
                
            "apps": {
                "models": {
                    "models": ["gate.model"],
                    "default_connection": "default"
                }
            }
        }
    )