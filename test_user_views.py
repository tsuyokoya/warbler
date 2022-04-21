"""User View tests."""

import os
from unittest import TestCase, main

from models import db, connect_db, Message, User

os.environ["DATABASE_URL"] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config["WTF_CSRF_ENABLED"] = False


class UserViewTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser_one = User.signup(
            username="testuser",
            email="test@test.com",
            password="testuser",
            image_url=None,
        )

        db.session.commit()

    def test_show_profile(self):
        """Can user see profile?"""

        with self.client as c:
            # when not logged in
            resp = c.get(f"/users/{self.testuser_one.id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("Access unauthorized.", html)

            # when logged in
            with self.client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_one.id
            resp = c.get(f"/users/{self.testuser_one.id}")
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn(f"{self.testuser_one.username}", html)

    def test_add_follow(self):
        """Can user follow another user?"""

        # app_context is needed for the correct functioning of sqlalchemy
        # else client.post closes all sessions.
        with app.app_context():
            # signup already adds the user to db.session
            testuser_two = User.signup(
                username="testuser2",
                email="test2@test.com",
                password="testuser2",
                image_url=None,
            )
            db.session.commit()

            with self.client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_one.id

            resp = self.client.post(
                f"/users/follow/{testuser_two.id}", follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn(f"{testuser_two.username}", html)

    def test_remove_follow(self):
        """Can user stop following a user?"""

        with app.app_context():
            testuser_two = User.signup(
                username="testuser2",
                email="test2@test.com",
                password="testuser2",
                image_url=None,
            )
            db.session.commit()

            with self.client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_one.id
            # add a testuser to follow
            resp = self.client.post(
                f"/users/follow/{testuser_two.id}", follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)

            # remove follow
            resp = self.client.post(
                f"/users/stop-following/{testuser_two.id}", follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertNotIn(f"{testuser_two.username}", html)


if __name__ == "__main__":
    main(verbosity=3)
