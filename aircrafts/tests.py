from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status

from aircrafts.models import Aircraft, Inventory
from accounts.models import Team, Profile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from aircrafts.models import Aircraft
from accounts.models import Team, Profile


class InventoryModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        team = Team.objects.create(team='WING')  # Create a team
        self.profile = Profile.objects.create(user=self.user, team=team)
        self.user.profile.team.team = 'WING'
        self.user.profile.save()

    def test_inventory_creation(self):
        inventory = Inventory.objects.create(
            inventory_type='WING',
            aircraft_type='TB2',
            produced_by=self.user
        )
        self.assertIsInstance(inventory, Inventory)
        self.assertEqual(inventory.produced_by, self.user)
        self.assertFalse(inventory.is_used)

    def test_generate_serial_number(self):
        inventory = Inventory(
            inventory_type='WING',
            aircraft_type='TB2',
            produced_by=self.user
        )
        serial_number = inventory.generate_serial_number()
        self.assertTrue(serial_number.startswith('TB2-WING-'))
        self.assertEqual(len(serial_number.split('-')), 5)

    def test_clean_method(self):
        inventory = Inventory(
            inventory_type='FUSELAGE',
            aircraft_type='TB2',
            produced_by=self.user
        )
        with self.assertRaises(ValidationError):
            inventory.clean()

    def test_save_method(self):
        inventory = Inventory(
            inventory_type='WING',
            aircraft_type='TB2',
            produced_by=self.user
        )
        inventory.save()
        self.assertIsNotNone(inventory.serial_number)
        self.assertTrue(inventory.serial_number.startswith('TB2-WING-'))

    def test_unique_serial_number(self):
        inventory1 = Inventory.objects.create(
            inventory_type='WING',
            aircraft_type='TB2',
            produced_by=self.user
        )
        inventory2 = Inventory.objects.create(
            inventory_type='WING',
            aircraft_type='TB2',
            produced_by=self.user
        )
        self.assertNotEqual(inventory1.serial_number, inventory2.serial_number)


class AircraftModelTest(TestCase):

    def setUp(self):
        # Create users and their respective teams with unique emails
        self.user_wing = get_user_model().objects.create_user(
            username='testuser_wing',
            email='testuser_wing@example.com',
            password='testpass'
        )
        team_wing = Team.objects.create(team='WING')
        self.profile_wing = Profile.objects.create(user=self.user_wing, team=team_wing)

        self.user_fuselage = get_user_model().objects.create_user(
            username='testuser_fuselage',
            email='testuser_fuselage@example.com',
            password='testpass'
        )
        team_fuselage = Team.objects.create(team='FUSELAGE')
        self.profile_fuselage = Profile.objects.create(user=self.user_fuselage, team=team_fuselage)

        self.user_tail = get_user_model().objects.create_user(
            username='testuser_tail',
            email='testuser_tail@example.com',
            password='testpass'
        )
        team_tail = Team.objects.create(team='TAIL')
        self.profile_tail = Profile.objects.create(user=self.user_tail, team=team_tail)

        self.user_avionics = get_user_model().objects.create_user(
            username='testuser_avionics',
            email='testuser_avionics@example.com',
            password='testpass'
        )
        team_avionics = Team.objects.create(team='AVIONICS')
        self.profile_avionics = Profile.objects.create(user=self.user_avionics, team=team_avionics)

    def test_inventory_creation_by_team(self):
        # User with team 'WING' can create 'WING' inventory
        wing_inventory = Inventory.objects.create(
            inventory_type='WING',
            aircraft_type='TB2',
            produced_by=self.user_wing
        )
        self.assertIsInstance(wing_inventory, Inventory)

        # User with team 'FUSELAGE' can create 'FUSELAGE' inventory
        fuselage_inventory = Inventory.objects.create(
            inventory_type='FUSELAGE',
            aircraft_type='TB2',
            produced_by=self.user_fuselage
        )
        self.assertIsInstance(fuselage_inventory, Inventory)

        # User with team 'TAIL' can create 'TAIL' inventory
        tail_inventory = Inventory.objects.create(
            inventory_type='TAIL',
            aircraft_type='TB2',
            produced_by=self.user_tail
        )
        self.assertIsInstance(tail_inventory, Inventory)

        # User with team 'AVIONICS' can create 'AVIONICS' inventory
        avionics_inventory = Inventory.objects.create(
            inventory_type='AVIONICS',
            aircraft_type='TB2',
            produced_by=self.user_avionics
        )
        self.assertIsInstance(avionics_inventory, Inventory)

    def test_inventory_creation_invalid_team(self):
        # User with team 'WING' cannot create 'FUSELAGE' inventory
        with self.assertRaises(ValidationError):
            Inventory.objects.create(
                inventory_type='FUSELAGE',
                aircraft_type='TB2',
                produced_by=self.user_wing
            )

        # User with team 'FUSELAGE' cannot create 'TAIL' inventory
        with self.assertRaises(ValidationError):
            Inventory.objects.create(
                inventory_type='TAIL',
                aircraft_type='TB2',
                produced_by=self.user_fuselage
            )

        # User with team 'TAIL' cannot create 'AVIONICS' inventory
        with self.assertRaises(ValidationError):
            Inventory.objects.create(
                inventory_type='AVIONICS',
                aircraft_type='TB2',
                produced_by=self.user_tail
            )

        # User with team 'AVIONICS' cannot create 'WING' inventory
        with self.assertRaises(ValidationError):
            Inventory.objects.create(
                inventory_type='WING',
                aircraft_type='TB2',
                produced_by=self.user_avionics
            )
