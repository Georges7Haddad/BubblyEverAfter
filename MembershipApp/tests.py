from django.test import TestCase

from .models import BubblyMember


def member_and_leader_factory(self):
    self.member = BubblyMember.objects.create(
        username="member_username",
        is_leadership=False,
        birthday="2020-04-05",
        country="Lebanon",
        city="Beirut",
        phone_number="+12125552368",
        paypal_email="test@gmail.com",
        burning_man_profile_email="test@gmail.com",
        is_superuser=True,
    )
    self.member.set_password("testing")
    self.member.save()

    self.leader = BubblyMember.objects.create(
        username="leader_username",
        is_leadership=True,
        birthday="2020-04-05",
        country="Lebanon",
        city="Beirut",
        phone_number="+12125552368",
        paypal_email="test@gmail.com",
        burning_man_profile_email="test@gmail.com",
    )
    self.leader.set_password("testing")
    self.leader.save()

    return self.member, self.leader


class LoginTest(TestCase):
    def setUp(self):
        self.member, self.leader = member_and_leader_factory(self)
        self.member_credentials = {"username": "member_username", "password": "testing"}
        self.leader_credentials = {"username": "leader_username", "password": "testing"}

    def test_member_login(self):
        logged_in = self.client.post("/member/login/", self.member_credentials, follow=True)
        self.assertRedirects(
            response=logged_in, status_code=302, target_status_code=200, expected_url="/member/profile/"
        )

    def test_leader_login(self):
        logged_in = self.client.post("/member/login/", self.leader_credentials, follow=True)
        self.assertRedirects(
            response=logged_in, status_code=302, target_status_code=200, expected_url="/leader/dashboard/"
        )

    def test_login_already_logged_in(self):
        """
        If the user tries to log in and is already logged in, he returns to his profile
        """
        logged_in = self.client.post("/member/login/", self.member_credentials, follow=True)
        self.assertRedirects(
            response=logged_in, status_code=302, target_status_code=200, expected_url="/member/profile/"
        )
        response = self.client.get("/member/login/")
        self.assertRedirects(
            response=response, status_code=302, target_status_code=200, expected_url="/member/profile/"
        )


class InvalidLoginTest(TestCase):
    def setUp(self):
        self.member, self.leader = member_and_leader_factory(self)
        self.invalid_username = {"username": "os", "password": "testing"}
        self.invalid_password = {"username": "member_username", "password": "os"}

    def test_wrong_username(self):
        logged_in = self.client.login(**self.invalid_username)
        self.assertFalse(logged_in)

    def test_wrong_password(self):
        logged_in = self.client.login(**self.invalid_password)
        self.assertFalse(logged_in)


class LogoutTest(TestCase):
    def setUp(self):
        self.member, self.leader = member_and_leader_factory(self)
        self.member_credentials = {"username": "member_username", "password": "testing"}
        self.leader_credentials = {"username": "leader_username", "password": "testing"}

    def test_logout_member(self):
        """
        Member cannot access his profile after logout
        """
        self.client.login(**self.member_credentials)
        self.client.get("/member/logout/")
        response = self.client.get("/member/profile/")
        self.assertRedirects(
            response=response,
            status_code=302,
            target_status_code=200,
            expected_url="/member/login/?next=%2Fmember%2Fprofile%2F",
        )

    def test_logout_leader(self):
        """
        Leader cannot access his dashboard or his profile after logout
        """
        self.client.login(**self.leader_credentials)
        self.client.get("/member/logout/")
        response = self.client.get("/leader/dashboard/")
        self.assertRedirects(
            response=response,
            status_code=302,
            target_status_code=200,
            expected_url="/member/login/?next=%2Fleader%2Fdashboard%2F",
        )
        response2 = self.client.get("/member/profile/")
        self.assertRedirects(
            response=response2,
            status_code=302,
            target_status_code=200,
            expected_url="/member/login/?next=%2Fmember%2Fprofile%2F",
        )


class LoginRequiredTest(TestCase):
    def setUp(self):
        self.member, self.leader = member_and_leader_factory(self)
        self.member_credentials = {"username": "member_username", "password": "testing"}

    def test_anonymous_permissions(self):
        """
        If the user is not logged in, he cannot access a member or leader's page
        """
        response = self.client.get("/member/profile/")
        self.assertRedirects(
            response=response,
            status_code=302,
            target_status_code=200,
            expected_url="/member/login/?next=%2Fmember%2Fprofile%2F",
        )
        response = self.client.get("/leader/dashboard/")
        self.assertRedirects(
            response=response,
            status_code=302,
            target_status_code=200,
            expected_url="/member/login/?next=%2Fleader%2Fdashboard%2F",
        )

    def test_member_permissions(self):
        """
        If the user is logged as a member, he cannot access a leader's page
        """
        logged_in = self.client.post("/member/login/", self.member_credentials, follow=True)
        self.assertRedirects(
            response=logged_in, status_code=302, target_status_code=200, expected_url="/member/profile/"
        )
        response = self.client.get("/leader/dashboard/")
        self.assertRedirects(
            response=response,
            status_code=302,
            target_status_code=302,
            expected_url="/member/login/?next=%2Fleader%2Fdashboard%2F",
        )
