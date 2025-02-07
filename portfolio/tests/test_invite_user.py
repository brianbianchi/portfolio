from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import LeagueUserForm
from ..models import League, LeagueUser, Portfolio


class InviteTest(TestCase):

    def setUp(self):
        self.user1 = User(username="exampleuser1", email="exampleuser1@gmail.com")
        self.user1.save()
        self.general_league = League(
            name="General",
            description="Site-wide League",
            start_value=1000,
            author=self.user1,
        )
        self.general_league.save()
        self.user2 = User(username="exampleuser2", email="exampleuser2@gmail.com")
        self.user2.save()
        self.league = League(
            name="Test League",
            description="Description of the Test League",
            start_value=1000,
            author=self.user1,
        )
        self.league.save()
        self.portfolio = Portfolio(
            name="Test Portfolio",
            user=self.user1,
            league=self.league,
            value=self.league.start_value,
        )
        self.portfolio.save()

    def test_user_invited_valid(self):
        form_data = {
            "username": self.user2.username,
            "league": self.league.id,
        }
        form = LeagueUserForm(data=form_data, user=self.user1)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_user_invited_invalid(self):
        form_data = {
            "quantity": "fakeusername",
            "league": self.league.id,
        }
        form = LeagueUserForm(data=form_data, user=self.user1)

        self.assertNotEqual(self.user2.username, form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_invited_from_nonmember_invalid(self):
        form_data = {
            "quantity": self.user2,
            "league": self.league.id,
        }
        form = LeagueUserForm(data=form_data, user=self.user2)

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("league"))
        self.assertIn("Select a valid choice", form.errors["league"][0])

    def test_invited_when_user_registers(self):
        user = User(username="exampleuser3", email="exampleuser3@gmail.com")
        user.save()
        league_users = LeagueUser.objects.filter(league=self.general_league, user=user)

        self.assertEqual(league_users.count(), 1)
