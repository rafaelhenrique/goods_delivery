import uuid
from decimal import Decimal
from django.db import models
import networkx as nx


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Route(BaseModel):
    start = models.CharField(max_length=32, null=False, blank=False)
    end = models.CharField(max_length=32, null=False, blank=False)
    distance = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rota'
        verbose_name_plural = 'Rotas'

    def __str__(self):
        return "{} - {} - {}".format(self.start, self.end, self.distance)

    def __repr__(self):
        representation = ('Route(start={!r}, end={!r}, distance={!r})')
        return representation.format(self.start, self.end, self.distance)


class Map(BaseModel):
    name = models.CharField(max_length=64, null=False, blank=False,
                            unique=True)
    routes = models.ManyToManyField(Route, blank=False, related_name='maps')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mapa'
        verbose_name_plural = 'Mapas'

    def __str__(self):
        return self.name

    def __repr__(self):
        representation = ('Map(name={!r}, created_at={!r}, modified_at={!r})')
        return representation.format(self.name, self.created_at,
                                     self.modified_at)

    def short_path(self, start, end):
        """
        Return short path based on start, end and lower distance.

        Paramethers:
            start: Some name of Route.start (model Route)
            end: Some name of Route.end (model Route)

        Returns:
            tuple when element 0 is a better route
                       element 1 is a length of route
        """

        # create graph
        G = nx.Graph()
        # add weighted edges
        weighted_edges = self.routes.values_list('start', 'end', 'distance')
        G.add_weighted_edges_from(weighted_edges)
        # get better route
        better_route = nx.dijkstra_path(G, start, end)
        # get length of route
        length = nx.dijkstra_path_length(G, start, end)
        return better_route, length

    def lower_cost_path(self, start, end, autonomy, fuel_price):
        """
        Return better route and better cost of route.

        Paramethers:
            start (str): Some name of Route.start (model Route)
            end (str): Some name of Route.end (model Route)
            autonomy (decimal.Decimal): Autonomy of vehicle
            fuel_price (decimal.Decimal): Value of fuel

        Returns:
            tuple when element 0 is a better route
                       element 1 is a fuel cost of route
        """
        better_route, length = self.short_path(start, end)
        quantity_of_fuel = Decimal(length) / Decimal(autonomy)
        fuel_cost_total = Decimal(fuel_price) * quantity_of_fuel
        return better_route, fuel_cost_total
