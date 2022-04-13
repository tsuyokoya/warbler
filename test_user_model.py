"""User model tests."""

import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ["DATABASE_URL"] = "postgresql:///warbler-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.user_one = User.signup(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            image_url=None,
        )
        self.user_two = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            image_url=None,
        )

        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(email="test@test.com", username="testuser", password="HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        # User should have no messages, no followers, no likes
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.likes), 0)

        # Test __repr__
        self.assertEqual(f"{u}", f"<User #{u.id}: {u.username}, {u.email}>")

    def test_user_is_following(self):
        """Is user followed by another user?"""
        self.assertFalse(self.user_one.is_following(self.user_two))
        self.user_one.following.append(self.user_two)
        self.assertTrue(self.user_one.is_following(self.user_two))

    def test_user_is_followed(self):
        """Is user followed by another user?"""
        self.assertFalse(self.user_one.is_followed_by(self.user_two))
        self.user_one.followers.append(self.user_two)
        self.assertTrue(self.user_one.is_followed_by(self.user_two))

    def test_user_signup(self):
        """Can user signup?"""
        u = User.signup(
            email="test3@test.com",
            username="testuser3",
            password="secret",
            image_url=None,
        )
        db.session.commit()

        self.assertTrue(User.query.get(u.id))
        self.assertNotEqual(u.password, "secret")

    def test_user_authentication(self):
        """Can user be authenticated?"""
        username = self.user_one.username
        password = "HASHED_PASSWORD"
        can_authenticate = User.authenticate(username, password)

        self.assertTrue(can_authenticate)

        username = "wrong_user"
        can_authenticate = User.authenticate(username, password)
        self.assertFalse(can_authenticate)

        password = "HASHED_PASSWORDDD"
        can_authenticate = User.authenticate(username, password)
        self.assertFalse(can_authenticate)
