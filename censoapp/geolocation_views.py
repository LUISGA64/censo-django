# Geolocation Views - Mapas y Visualizaciones
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
import folium
from folium import plugins
import json

from censoapp.models import Sidewalks, FamilyCard, Person, Organizations


@login_required
def map_view(request):
    """Vista principal del mapa con todas las veredas"""
    # Obtener organización del usuario
    organization = None
    if hasattr(request.user, 'profile'):
        if not request.user.profile.can_view_all_organizations:
            organization = request.user.profile.organization

    # Filtrar veredas
    if organization:
        sidewalks = Sidewalks.objects.filter(organization_id=organization)
    else:
        sidewalks = Sidewalks.objects.all()

    # Contar estadísticas
    total_veredas = sidewalks.count()
    veredas_con_ubicacion = sidewalks.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).count()

    context = {
        'total_veredas': total_veredas,
        'veredas_con_ubicacion': veredas_con_ubicacion,
        'organization': organization,
    }

    return render(request, 'maps/map_view.html', context)


@login_required
def map_sidewalks_data(request):
    """API JSON con datos de veredas para el mapa"""
    organization = None
    if hasattr(request.user, 'profile'):
        if not request.user.profile.can_view_all_organizations:
            organization = request.user.profile.organization

    # Filtrar veredas
    if organization:
        sidewalks = Sidewalks.objects.filter(organization_id=organization)
    else:
        sidewalks = Sidewalks.objects.all()

    # Preparar datos GeoJSON
    features = []

    for sidewalk in sidewalks.filter(latitude__isnull=False, longitude__isnull=False):
        # Contar fichas y personas
        fichas_count = FamilyCard.objects.filter(
            sidewalk_home=sidewalk
        ).count()

        personas_count = Person.objects.filter(
            family_card__sidewalk_home=sidewalk
        ).count()

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(sidewalk.longitude), float(sidewalk.latitude)]
            },
            'properties': {
                'id': sidewalk.id,
                'name': sidewalk.sidewalk_name,
                'fichas': fichas_count,
                'personas': personas_count,
                'description': sidewalk.description or '',
            }
        }
        features.append(feature)

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    return JsonResponse(geojson, safe=False)


@login_required
def map_heatmap(request):
    """Vista de mapa de calor de densidad poblacional"""
    organization = None
    if hasattr(request.user, 'profile'):
        if not request.user.profile.can_view_all_organizations:
            organization = request.user.profile.organization

    # Crear mapa base
    m = folium.Map(
        location=[4.5709, -74.2973],  # Colombia center
        zoom_start=6,
        tiles='OpenStreetMap'
    )

    # Obtener datos para heatmap
    heat_data = []

    if organization:
        sidewalks = Sidewalks.objects.filter(organization_id=organization)
    else:
        sidewalks = Sidewalks.objects.all()

    for sidewalk in sidewalks.filter(latitude__isnull=False, longitude__isnull=False):
        personas_count = Person.objects.filter(
            family_card__sidewalk_home=sidewalk
        ).count()

        if personas_count > 0:
            heat_data.append([
                float(sidewalk.latitude),
                float(sidewalk.longitude),
                personas_count
            ])

    # Agregar capa de calor
    if heat_data:
        plugins.HeatMap(
            heat_data,
            min_opacity=0.3,
            max_opacity=0.8,
            radius=25,
            blur=20,
            gradient={
                '0.0': 'blue',
                '0.5': 'lime',
                '0.7': 'yellow',
                '1.0': 'red'
            }
        ).add_to(m)

    # Obtener HTML del mapa
    map_html = m._repr_html_()

    context = {
        'map_html': map_html,
        'organization': organization,
    }

    return render(request, 'maps/heatmap.html', context)


@login_required
def map_clusters(request):
    """Vista de mapa con clusters de marcadores"""
    organization = None
    if hasattr(request.user, 'profile'):
        if not request.user.profile.can_view_all_organizations:
            organization = request.user.profile.organization

    # Crear mapa base
    m = folium.Map(
        location=[4.5709, -74.2973],
        zoom_start=6,
        tiles='OpenStreetMap'
    )

    # Crear cluster de marcadores con estilos personalizados (azul en lugar de verde)
    marker_cluster = plugins.MarkerCluster(
        name='Clusters',
        overlay=True,
        control=False,
        icon_create_function="""
        function(cluster) {
            var childCount = cluster.getChildCount();
            var c = ' marker-cluster-';
            if (childCount < 10) {
                c += 'small';
            } else if (childCount < 100) {
                c += 'medium';
            } else {
                c += 'large';
            }
            return new L.DivIcon({ 
                html: '<div><span>' + childCount + '</span></div>', 
                className: 'marker-cluster' + c, 
                iconSize: new L.Point(40, 40) 
            });
        }
        """
    ).add_to(m)

    # Agregar CSS personalizado para clusters azules
    cluster_css = """
    <style>
    .marker-cluster-small {
        background-color: rgba(33, 150, 243, 0.6);
    }
    .marker-cluster-small div {
        background-color: rgba(33, 150, 243, 0.8);
    }
    .marker-cluster-medium {
        background-color: rgba(25, 118, 210, 0.6);
    }
    .marker-cluster-medium div {
        background-color: rgba(25, 118, 210, 0.8);
    }
    .marker-cluster-large {
        background-color: rgba(21, 101, 192, 0.6);
    }
    .marker-cluster-large div {
        background-color: rgba(21, 101, 192, 0.8);
    }
    .marker-cluster {
        background-clip: padding-box;
        border-radius: 20px;
    }
    .marker-cluster div {
        width: 30px;
        height: 30px;
        margin-left: 5px;
        margin-top: 5px;
        text-align: center;
        border-radius: 15px;
        font: 12px "Helvetica Neue", Arial, Helvetica, sans-serif;
    }
    .marker-cluster span {
        line-height: 30px;
        color: white;
        font-weight: bold;
    }
    </style>
    """
    m.get_root().html.add_child(folium.Element(cluster_css))

    # Obtener veredas
    if organization:
        sidewalks = Sidewalks.objects.filter(organization_id=organization)
    else:
        sidewalks = Sidewalks.objects.all()

    for sidewalk in sidewalks.filter(latitude__isnull=False, longitude__isnull=False):
        fichas_count = FamilyCard.objects.filter(
            sidewalk_home=sidewalk
        ).count()

        personas_count = Person.objects.filter(
            family_card__sidewalk_home=sidewalk
        ).count()

        # Crear popup
        popup_html = f"""
        <div style="font-family: Arial; min-width: 200px;">
            <h5 style="color: #2196F3; margin-bottom: 10px;">
                <i class="fas fa-map-marker-alt"></i> {sidewalk.sidewalk_name}
            </h5>
            <p style="margin: 5px 0;">
                <strong>Fichas Familiares:</strong> {fichas_count}
            </p>
            <p style="margin: 5px 0;">
                <strong>Personas:</strong> {personas_count}
            </p>
            <a href="/familyCard/index?sidewalk={sidewalk.id}" 
               target="_blank" 
               style="color: #2196F3; text-decoration: none;">
                Ver fichas <i class="fas fa-external-link-alt"></i>
            </a>
        </div>
        """

        # Determinar color del ícono según población
        # Colores que contrastan bien con el fondo verde del mapa
        if personas_count > 100:
            icon_color = 'red'  # Rojo para alta densidad
        elif personas_count > 50:
            icon_color = 'orange'  # Naranja para media-alta
        elif personas_count > 20:
            icon_color = 'purple'  # Púrpura para media (contrasta con verde)
        else:
            icon_color = 'blue'  # Azul para baja densidad

        folium.Marker(
            location=[float(sidewalk.latitude), float(sidewalk.longitude)],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{sidewalk.sidewalk_name} ({personas_count} personas)",
            icon=folium.Icon(color=icon_color, icon='home', prefix='fa')
        ).add_to(marker_cluster)

    # Agregar control de capas
    folium.LayerControl().add_to(m)

    # Obtener HTML del mapa
    map_html = m._repr_html_()

    context = {
        'map_html': map_html,
        'organization': organization,
    }

    return render(request, 'maps/clusters.html', context)


@login_required
def sidewalk_detail_map(request, sidewalk_id):
    """Mapa detallado de una vereda específica"""
    try:
        sidewalk = Sidewalks.objects.get(id=sidewalk_id)
    except Sidewalks.DoesNotExist:
        return render(request, '404.html', status=404)

    # Verificar permisos
    if hasattr(request.user, 'profile'):
        if not request.user.profile.can_view_all_organizations:
            if sidewalk.organization != request.user.profile.organization:
                return render(request, '403.html', status=403)

    # Estadísticas
    fichas = FamilyCard.objects.filter(sidewalk_home=sidewalk)
    fichas_count = fichas.count()
    personas_count = Person.objects.filter(
        family_card__sidewalk_home=sidewalk
    ).count()

    context = {
        'sidewalk': sidewalk,
        'fichas_count': fichas_count,
        'personas_count': personas_count,
        'has_location': sidewalk.latitude and sidewalk.longitude,
    }

    return render(request, 'maps/sidewalk_detail.html', context)


@login_required
def update_sidewalk_location(request, sidewalk_id):
    """Actualizar coordenadas de una vereda"""
    if request.method == 'POST':
        try:
            sidewalk = Sidewalks.objects.get(id=sidewalk_id)

            # Verificar permisos
            if hasattr(request.user, 'profile'):
                if not request.user.profile.can_view_all_organizations:
                    if sidewalk.organization != request.user.profile.organization:
                        return JsonResponse({'error': 'Sin permisos'}, status=403)

            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude and longitude:
                sidewalk.latitude = latitude
                sidewalk.longitude = longitude
                sidewalk.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Ubicación actualizada correctamente'
                })
            else:
                return JsonResponse({'error': 'Datos incompletos'}, status=400)

        except Sidewalks.DoesNotExist:
            return JsonResponse({'error': 'Vereda no encontrada'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
