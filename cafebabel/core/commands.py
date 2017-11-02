import click
from peewee import create_model_tables, drop_model_tables

from .. import app, db
from ..users.models import Role, User, UserProfile, UserRoles, user_datastore

tables = [User, UserProfile, Role, UserRoles]


def _initdb():
    _dropdb()
    create_model_tables(tables, fail_silently=True)
    Role.create(name='editor')
    admin_role = Role.create(name='admin')
    admin_user = user_datastore.create_user(
        email='admin@example.com', password='password',
        firstname='Admin', lastname='Admin')
    user_datastore.add_role_to_user(admin_user, admin_role)
    if not db.database.is_closed():
        db.close_db(None)
    click.echo('DB intialized.')


def _dropdb():
    drop_model_tables(tables, fail_silently=True)
    if not db.database.is_closed():
        db.close_db(None)
    click.echo('DB dropped.')


@app.cli.command()
def initdb():
    _initdb()