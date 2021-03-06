# services/users/project/tests/test_users.py

import json
import unittest

from project.tests.base import BaseTestCase

from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests para el servicio Users."""

    def test_users(self):
        """Asegurando que la ruta /ping se comporta correctamente."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "abel.huanca", "email": "abel.huanca@upeu.edu.pe"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("abel.huanca@upeu.edu.pe was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Asegurese de que se produzca un error si el objeto JSON esta vacio"""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """
        Asegurese de que se produzca un error si el objeto JSON no tiene una clave
        de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "abel.huanca@upeu.edu.pe"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Asegurese de que se arroje un error si el correo electronico ya
        existe."""
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "abel.huanca", "email": "abel.huanca@upeu.edu.pe"}
                ),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "abel.huanca", "email": "abel.huanca@upeu.edu.pe"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That email already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user("abel.huanca", "abel.huanca@upeu.edu.pe")
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("abel.huanca", data["data"]["username"])
            self.assertIn("abel.huanca@upeu.edu.pe", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Asegurese de que se produzca un error si no se proporciona un id."""
        with self.client:
            response = self.client.get("/users/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Aseg�rese de que se produzca un error si el id no existe."""
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Asegúrese de que todos los usuarios se comporten correctamente."""
        add_user("abel.huanca", "abel.huanca@upeu.edu.pe")
        add_user("abelthf", "abelthf@gmail.com")
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("abel.huanca", data["data"]["users"][0]["username"])
            self.assertIn("abel.huanca@upeu.edu.pe", data["data"]["users"][0]["email"])
            self.assertIn("abelthf", data["data"]["users"][1]["username"])
            self.assertIn("abelthf@gmail.com", data["data"]["users"][1]["email"])
            self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main()
