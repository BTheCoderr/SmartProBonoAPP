#!/usr/bin/env python
import os
import click
from flask.cli import FlaskGroup
from backend import create_app
from backend.database import db
from backend.models import User, Rights

cli = FlaskGroup(create_app=create_app)

@cli.command()
@click.argument("email")
@click.argument("password")
def create_admin(email, password):
    """Create an admin user.
    
    Args:
        email: Admin user's email
        password: Admin user's password
    """
    user = User(
        email=email,
        role='admin',
        active=True
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    click.echo(f"Created admin user: {email}")

@cli.command("init-db")
def init_db_command():
    """Initialize the database."""
    app = create_app()
    with app.app_context():
        db.create_all()
        click.echo("Initialized the database.")

@cli.command("seed-rights")
def seed_rights():
    """Seed the database with legal rights information."""
    rights_data = [
        {
            'category': 'housing',
            'title': 'Right to Habitable Housing',
            'description': 'Tenants have the right to live in housing that meets basic structural, health, and safety standards.'
        },
        {
            'category': 'housing',
            'title': 'Protection Against Unlawful Eviction',
            'description': 'Landlords must follow proper legal procedures to evict tenants and provide adequate notice.'
        },
        {
            'category': 'employment',
            'title': 'Minimum Wage',
            'description': 'Workers have the right to be paid at least the minimum wage established by law.'
        },
        {
            'category': 'employment',
            'title': 'Workplace Safety',
            'description': 'Employees have the right to work in an environment free from recognized hazards.'
        }
    ]
    
    for right_data in rights_data:
        right = Rights(**right_data)
        db.session.add(right)
    
    db.session.commit()
    click.echo("Legal rights seeded successfully.")

# Flask-Migrate commands are automatically added by the Flask CLI

if __name__ == "__main__":
    cli() 