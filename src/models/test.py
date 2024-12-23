import unittest
import uuid

import utils
import roles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base


class TestingEnums(unittest.TestCase):

    def test_userRole(self):
        self.assertEqual(utils.UserRole.USER, "user")
        self.assertEqual(utils.UserRole.BUYER.value, "buyer")
        self.assertEqual(utils.UserRole.SELLER.value, "seller")
        self.assertEqual(utils.UserRole.BOTH.value, "both")
        self.assertEqual(utils.UserRole.NONE.value, "none")

    def test_contentType(self):

        self.assertEqual(utils.ContentType.POST.value, "post")
        self.assertEqual(utils.ContentType.FANART.value, "fanart")
        self.assertEqual(utils.ContentType.COMMENT.value, "comment")

    def test_orderStatus(self):

        self.assertEqual(utils.OrderStatus.PENDING.value, "pending")
        self.assertEqual(utils.OrderStatus.ACCEPTED.value, "accepted")
        self.assertEqual(utils.OrderStatus.REJECTED.value, "rejected")
        self.assertEqual(utils.OrderStatus.ACCEPTED.value, "accepted")
        self.assertEqual(utils.OrderStatus.CANCELLED.value, "cancelled")
        self.assertEqual(utils.OrderStatus.INPROGRESS.value, "inprogress")

    def test_proficiency(self):

        self.assertEqual(utils.Proficiency.EXPERT.value, "expert")
        self.assertEqual(utils.Proficiency.INTERMEDIATE.value, "intermediate")
        self.assertEqual(utils.Proficiency.BEGINNER.value, "beginner")

