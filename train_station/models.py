from django.db import models
from django.core.exceptions import ValidationError

from train_station_api_service import settings


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(to=Station, on_delete=models.CASCADE, related_name="source_routes")
    destination = models.ForeignKey(to=Station, on_delete=models.CASCADE, related_name="destination_routes")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"


class TrainType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(to=TrainType, on_delete=models.CASCADE, related_name="trains")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Journey(models.Model):
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name="journeys")
    train = models.ForeignKey(to=Train, on_delete=models.CASCADE, related_name="journeys")
    crews = models.ManyToManyField(to=Crew, related_name="journeys")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["-departure_time"]

    def __str__(self):
        return (f"{self.route.source} - {self.route.destination}: "
                f"{self.departure_time} - {self.arrival_time}")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(to=Journey, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="tickets")

    @staticmethod
    def validate_ticket(cargo, seat, train, error_to_raise):
        for ticket_attr_value, ticket_attr_name, train_attr_name in [
            (cargo, "cargo", "cargo_num"),
            (seat, "seat", "places_in_cargo")
        ]:
            if ticket_attr_value is not None:
                count_attrs = getattr(train, train_attr_name)
                if not (1 <= ticket_attr_value <= count_attrs):
                    raise error_to_raise(
                        {
                            ticket_attr_name: f"{ticket_attr_name} "
                                              f"number must be in available range: "
                                              f"(1, {train_attr_name}): "
                                              f"(1, {count_attrs})"
                        }
                    )

    def clean(self):
        Ticket.validate_ticket(
            self.cargo,
            self.seat,
            self.journey.train,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.journey)} (row: {self.cargo}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("journey", "cargo", "seat")
        ordering = ["cargo", "seat"]
