# services/users/manage.py


import sys
import unittest

from flask.cli import FlaskGroup

from project import create_app, db  # nuevo
from project.api.models import User  # nuevo

app = create_app()  # nuevo
cli = FlaskGroup(create_app=create_app)  # nuevo


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Ejecutar los tests sin code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command("seed_db")
def seed_db():
    """Siembra la base de datos."""
    db.session.add(User(username="abelthf", email="abelthf@gmail.com"))
    db.session.add(User(username="abel.huanca", email="abel.huanca@upeu.edu.pe"))
    db.session.commit()


if __name__ == "__main__":
    cli()
