from django.contrib import admin

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


admin.site.register(Train)
admin.site.register(Journey)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(TrainType)
admin.site.register(Crew)
admin.site.register(Order)
admin.site.register(Ticket)
