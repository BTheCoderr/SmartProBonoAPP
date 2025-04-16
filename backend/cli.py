import click
from flask.cli import with_appcontext
from alembic import command
from alembic.config import Config
import os

@click.group()
def db():
    """Database management commands."""
    pass

@db.command()
@with_appcontext
def init():
    """Initialize the database."""
    from models.database import db
    db.create_all()
    click.echo('Database initialized.')

@db.command()
@with_appcontext
def migrate():
    """Run database migrations."""
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), 'alembic.ini'))
    alembic_cfg.set_main_option('script_location', os.path.join(os.path.dirname(__file__), 'migrations'))
    command.upgrade(alembic_cfg, 'head')
    click.echo('Database migrated.') 