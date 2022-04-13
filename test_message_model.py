"""Message model tests."""

from datetime import datetime
import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ["DATABASE_URL"] = "postgresql:///warbler-test"

from app import app

db.create_all()


class MessageModelTestCase(TestCase):
    """Test model for message."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.user_one = User.signup(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            image_url=None,
        )

        db.session.commit()

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(text="This is a test", user_id=self.user_one.id)

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.user_one.messages), 1)
        self.assertEqual(
            Message.query.filter_by(user_id=self.user_one.id).one().text,
            "This is a test",
        )
        self.assertIsInstance(
            Message.query.filter_by(user_id=self.user_one.id).one().timestamp, datetime
        )
