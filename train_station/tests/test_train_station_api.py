from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from train_station.models import (
    Train,
    Journey,
    Station,
    Route,
    Crew,
    TrainType,
)
from train_station.serializers import JourneyListSerializer


JOURNEY_URL = reverse("train_station:journey-list")


def sample_type(**params):
    defaults = {
        "name": "Type",
    }
    defaults.update(params)

    return TrainType.objects.create(**defaults)


def sample_train(**params):
    train_type = sample_type(name="Type1")
    defaults = {
        "name": "Train",
        "cargo_num": 6,
        "places_in_cargo": 50,
        "train_type": train_type,
    }
    defaults.update(params)

    return Train.objects.create(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "Name",
        "last_name": "Last name"
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


def sample_station(**params):
    defaults = {
        "name": "Station",
        "latitude": 15645.14455,
        "longitude": 555553.4444
    }
    defaults.update(params)

    return Station.objects.create(**defaults)


def sample_route(**params):
    station1 = sample_station(name="Station1")
    station2 = sample_station(name="Station2")
    defaults = {
        "source": station1,
        "destination": station2,
        "distance": 720,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_journey(**params):
    route = sample_route()
    train = sample_train()
    crew1 = sample_crew()
    crew2 = sample_crew(first_name="Name2", last_name="Last Name2")

    defaults = {
        "route": route,
        "train": train,
        "departure_time": "2023-11-11",
        "arrival_time": "2023-11-12"
    }

    defaults.update(params)
    journey = Journey.objects.create(**defaults)
    journey.crews.set([crew1, crew2])

    return journey


def detail_url(journey_id):
    return reverse("train_station:journey-detail", args=[journey_id])


class UnauthenticatedJourneyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(JOURNEY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedJourneyAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@gmail.com",
            "userpassword",
        )
        self.client.force_authenticate(self.user)

    def test_journey_list(self):
        journey = sample_journey()
        journey.save()
        response = self.client.get(JOURNEY_URL)

        journeys = Journey.objects.all()
        serializer = JourneyListSerializer(journeys, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_journey_detail(self):
        journey = sample_journey()
        journey.save()
        url = detail_url(journey.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_journey_create_forbidden(self):
        route = sample_route()
        train = sample_train()
        crew1 = sample_crew()
        crew2 = sample_crew(first_name="Name2", last_name="Last Name2")

        crew1.save()
        crew2.save()

        payload = {
            "route": route.id,
            "train": train.id,
            "crews": [crew1.id, crew2.id],
            "departure_time": "2023-11-11",
            "arrival_time": "2023-11-12",
        }

        response = self.client.post(JOURNEY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "1122Admin",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_journey(self):
        route = sample_route()
        train = sample_train()
        crew1 = sample_crew()
        crew2 = sample_crew(first_name="Name2", last_name="Last Name2")

        crew1.save()
        crew2.save()

        payload = {
            "route": route.id,
            "train": train.id,
            "crews": [crew1.id, crew2.id],
            "departure_time": "2023-11-11",
            "arrival_time": "2023-11-12",
        }

        response = self.client.post(JOURNEY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_journey_allowed(self):
        journey = sample_journey()
        journey.save()
        url = detail_url(journey.id)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
