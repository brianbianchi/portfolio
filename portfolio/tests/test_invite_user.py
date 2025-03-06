from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from ..forms import LeagueUserForm
from ..models import League, LeagueUser, Portfolio


class InviteTest(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username="admin")
        call_command("init")
        self.default_league = League.objects.get(is_default=True)
        self.user1 = User.objects.create(
            username="exampleuser1", email="exampleuser1@gmail.com"
        )
        self.user2 = User.objects.create(
            username="exampleuser2", email="exampleuser2@gmail.com"
        )
        self.league = League.objects.create(
            name="Test League",
            description="Description of the Test League",
            start_value=1000,
            author=self.user1,
        )
        self.portfolio = Portfolio.objects.create(
            name="Test Portfolio",
            user=self.user1,
            league=self.league,
            value=self.league.start_value,
        )

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

    def test_new_user(self):
        user = User.objects.create(
            username="exampleuser3", email="exampleuser3@gmail.com"
        )
        league_users = LeagueUser.objects.filter(league=self.default_league, user=user)
        portfolios = Portfolio.objects.filter(league=self.default_league, user=user)

        self.assertEqual(league_users.count(), 1)
        self.assertEqual(portfolios.count(), 1)
        self.assertEqual(portfolios.first().name, user.username)
        self.assertEqual(portfolios.first().value, self.default_league.start_value)
