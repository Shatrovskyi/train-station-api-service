from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from train_station.models import (
    Train,
    Journey,
    Station,
    Route,
    TrainType,
    Crew,
    Order,
    Ticket,
)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    source = StationSerializer(many=False, read_only=True)
    destination = StationSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "capacity",
            "train_type",
        )


class TrainDetailSerializer(TrainSerializer):
    train_type = TrainTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "capacity",
            "train_type",
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ("id", "route", "train", "crews", "departure_time", "arrival_time")


class JourneyListSerializer(JourneySerializer):
    crews = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    train_name = serializers.CharField(source="train.name")
    train_type = serializers.CharField(source="train.train_type")
    train_cargo_num = serializers.IntegerField(source="train.cargo_num")
    places_in_cargo = serializers.IntegerField(source="train.places_in_cargo")

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train_name",
            "train_type",
            "train_cargo_num",
            "places_in_cargo",
            "crews",
            "departure_time",
            "arrival_time",
        )


class JourneyDetailSerializer(JourneySerializer):
    crews = CrewSerializer(many=True, read_only=True)
    train = TrainDetailSerializer(many=False, read_only=True)
    route = RouteSerializer(many=False, read_only=True)
    taken_seats = serializers.SlugRelatedField(
        source="tickets", many=True, read_only=True, slug_field="seat"
    )
    taken_cargo = serializers.SlugRelatedField(
        source="tickets", many=True, read_only=True, slug_field="cargo"
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "crews",
            "taken_cargo",
            "taken_seats",
            "departure_time",
            "arrival_time",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["cargo"], attrs["seat"], attrs["journey"].train, ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")


class TicketListSerializer(TicketSerializer):
    journey = JourneyListSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("cargo", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)
        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
