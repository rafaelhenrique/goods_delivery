from django.contrib import admin
from .models import Map, Route


class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_routes')

    def get_routes(self, obj):
        routes = [str(route) for route in obj.routes.all()]
        return "</br>".join(routes)

    get_routes.allow_tags = True
    get_routes.short_description = 'Rotas'


class RouteAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'distance')


admin.site.register(Map, MapAdmin)
admin.site.register(Route, RouteAdmin)
