"""Unit and integration tests for the Missions App"""
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission

from .models import Mission, Employee, SecurityClearance


class MissionTestCase(TestCase):
    """Test cases in the Missions App"""

    def setUp(self):
        """Set up the client and environment"""
        self.client = Client()

        User.objects.create_superuser('admin', 'admin@test.com', 'password')

        iss_admins = Group.objects.create(name='ISS_Admin_User')
        nasa_admins = Group.objects.create(name='NASA_Admin_User')

        iss_admins.permissions.add(*[
            Permission.objects.get(codename='add_mission'),
            Permission.objects.get(codename='change_mission'),
            Permission.objects.get(codename='delete_mission'),
            Permission.objects.get(codename='view_mission'),

            Permission.objects.get(codename='add_missionreport'),
            Permission.objects.get(codename='change_missionreport'),
            Permission.objects.get(codename='delete_missionreport'),
            Permission.objects.get(codename='view_missionreport')
        ])

        nasa_admins.permissions.add(*[
            Permission.objects.get(codename='view_missionreport')
        ])

        juan = User.objects.create_user('juan.mortyme', 'juan@iss.com', 'password')
        juan.groups.add(iss_admins)
        juan.save()

        ella = User.objects.create_user('ella.vader', 'ella@nasa.com', 'password')
        ella.groups.add(nasa_admins)
        ella.save()

    def test_should_redirect_to_login_unless_logged_in(self):
        """Test for redirecting to login if not logged in"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login?next=/')

    def test_should_display_index_when_logged_in(self):
        """Test for displaying index page when logged in"""
        self.client.login(username='admin', password='password')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_should_not_display_mission_details_when_logged_out(self):
        """Test for denied access to mission details when logged out"""
        supervisor = Employee.objects.create(
            user=User.objects.get(username='admin'),
            security_clearance=SecurityClearance.TOP_SECRET
        )

        mission = Mission.objects.create(
            name='Mission 1',
            description='Description 1',
            supervisor=supervisor,
            security_clearance=SecurityClearance.TOP_SECRET
        )

        response = self.client.get(f"/mission/{mission.pk}")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/login?next=/mission/{mission.pk}")

    def test_should_display_mission_details_when_logged_in(self):
        """Test for display of mission details when logged in"""
        supervisor = Employee.objects.create(
            user=User.objects.get(username='admin'),
            security_clearance=SecurityClearance.TOP_SECRET
        )

        mission = Mission.objects.create(
            name='Mission 1',
            description='Description 1',
            supervisor=supervisor,
            security_clearance=SecurityClearance.TOP_SECRET
        )

        self.client.login(username='admin', password='password')

        response = self.client.get(f"/mission/{mission.pk}")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mission.html')

    def test_should_not_allow_mission_creation_when_logged_out(self):
        """Test for function security (unable to create mission) when logged out"""
        response = self.client.get('/mission/create')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login?next=/mission/create')

    def test_should_allow_mission_creation_when_logged_in(self):
        """Test for function to create mission when logged in"""
        self.client.login(username='admin', password='password')

        response = self.client.get('/mission/create')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mission-create.html')

    def test_should_not_allow_mission_update_when_logged_out(self):
        """Test for function security (unable to update mission) when logged out"""
        supervisor = Employee.objects.create(
            user=User.objects.get(username='admin'),
            security_clearance=SecurityClearance.TOP_SECRET
        )

        mission = Mission.objects.create(
            name='Mission 1',
            description='Description 1',
            supervisor=supervisor,
            security_clearance=SecurityClearance.TOP_SECRET
        )

        response = self.client.get(f"/mission/{mission.pk}/update")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/login?next=/mission/{mission.pk}/update")

    def test_should_allow_mission_update_when_logged_in(self):
        """Test for update of mission details when logged in"""
        supervisor = Employee.objects.create(
            user=User.objects.get(username='admin'),
            security_clearance=SecurityClearance.TOP_SECRET
        )

        mission = Mission.objects.create(
            name='Mission 1',
            description='Description 1',
            supervisor=supervisor,
            security_clearance=SecurityClearance.TOP_SECRET
        )

        self.client.login(username='admin', password='password')

        response = self.client.get(f"/mission/{mission.pk}/update")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mission-update.html')

    def test_should_not_allow_mission_delete_when_logged_out(self):
        """Test for function security (unable to delete mission) when logged out"""
        supervisor = Employee.objects.create(
            user=User.objects.get(username='admin'),
            security_clearance=SecurityClearance.TOP_SECRET
        )

        mission = Mission.objects.create(
            name='Mission 1',
            description='Description 1',
            supervisor=supervisor,
            security_clearance=SecurityClearance.TOP_SECRET
        )

        response = self.client.get(f"/mission/{mission.pk}/delete")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/login?next=/mission/{mission.pk}/delete")

    def test_should_allow_mission_delete_when_logged_in(self):
        """Test for deletion of mission when logged in"""
        supervisor = Employee.objects.create(
            user=User.objects.get(username='admin'),
            security_clearance=SecurityClearance.TOP_SECRET
        )

        mission = Mission.objects.create(
            name='Mission 1',
            description='Description 1',
            supervisor=supervisor,
            security_clearance=SecurityClearance.TOP_SECRET
        )

        self.client.login(username='admin', password='password')

        response = self.client.get(f"/mission/{mission.pk}/delete")

        self.assertEqual(response.status_code, 302)

        missions = Mission.objects.filter(pk=mission.pk).count()

        self.assertEqual(missions, 0)

    def test_should_not_allow_mission_creation_without_supervisor(self):
        """Test for mission creation database model requirements"""
        self.client.login(username='admin', password='password')

        response = self.client.post('/mission/create', {
            'name': 'Mission 1',
            'description': 'Description 1',
            'security_clearance': SecurityClearance.TOP_SECRET
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mission-create.html')

    def test_should_not_allow_mission_creation_when_user_is_not_iss_admin(self):
        """Test for role based access control deny mission creation"""
        supervisor = Employee.objects.create(
            user=User.objects.get(username='admin'),
            security_clearance=SecurityClearance.TOP_SECRET
        )

        self.client.login(username='ella.vader', password='password')

        response = self.client.post('/mission/create', {
            'name': 'Mission 1',
            'description': 'Description 1',
            'supervisor': supervisor,
            'security_clearance': SecurityClearance.TOP_SECRET
        })

        self.assertEqual(response.status_code, 403)

    def test_should_allow_mission_creation_when_user_is_iss_admin(self):
        """Test for role based access control allow mission creation"""
        supervisor = Employee.objects.create(
            user=User.objects.get(username='juan.mortyme'),
            security_clearance=SecurityClearance.TOP_SECRET
        )

        self.client.login(username='juan.mortyme', password='password')

        response = self.client.post('/mission/create', {
            'name': 'Mission 1',
            'description': 'Description 1',
            'supervisor': supervisor,
            'security_clearance': SecurityClearance.TOP_SECRET
        })

        self.assertEqual(response.status_code, 200)
