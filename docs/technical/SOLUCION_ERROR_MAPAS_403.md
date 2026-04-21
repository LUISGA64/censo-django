# Solución Error 403 en Mapas OpenStreetMap

## Problema
Al visualizar los mapas en la aplicación, aparecían errores 403r "Access blocked" con el mensaje:
> "Referer is required by tile usage policy of OpenStreetMap's volunteer-run servers: osm.wiki/Blocked"

## Causa
OpenStreetMap (OSM) requiere que las aplicaciones que usan sus tiles establezcan un referer HTTP válido para prevenir abuso de sus servidores voluntarios. Este es un requisito de su política de uso justo.

## Solución Implementada

### Opción 1: Usar CartoDB Tiles (Implementada)
Reemplazamos los tiles de OpenStreetMap con tiles de **CartoDB**, que no requieren configuración de referer y son gratuitos para uso normal:

#### En Leaflet (JavaScript):
```javascript
// ANTES (causaba error 403)
const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap',
    maxZoom: 19
});

// DESPUÉS (funciona correctamente)
const osmLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 20
});
```

#### En Folium (Python):
```python
# ANTES
m = folium.Map(
    location=[4.5709, -74.2973],
    zoom_start=6,
    tiles='OpenStreetMap'
)

# DESPUÉS
m = folium.Map(
    location=[4.5709, -74.2973],
    zoom_start=6,
    tiles='CartoDB positron',
    attr='&copy; OpenStreetMap contributors &copy; CARTO'
)
```

## Archivos Modificados

1. **templates/maps/map_view.html**
   - Reemplazado tiles de OSM con CartoDB Voyager
   - Actualizada configuración de capas topográficas

2. **censoapp/geolocation_views.py**
   - Función `map_heatmap()`: tiles='CartoDB positron'
   - Función `map_clusters()`: tiles='CartoDB positron'

## Alternativas de Tiles Gratuitos

### CartoDB (Usado en la solución)
- **Voyager**: `https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png`
- **Positron**: `https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png`
- **Dark Matter**: `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`

### Otras Alternativas
- **Stamen Terrain**: `http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg`
- **Esri World Street Map**: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}`
- **OpenTopoMap**: `https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png` (también puede tener restricciones)

## Ventajas de CartoDB
✅ No requiere API key para uso básico
✅ No requiere configuración de referer
✅ Buena calidad visual
✅ Múltiples estilos disponibles
✅ Buen rendimiento
✅ Límite generoso de peticiones
✅ Usa datos de OpenStreetMap

## Solución Alternativa (No implementada)
Si se quisiera seguir usando tiles de OSM directamente, habría que:

1. Configurar el referer correctamente en el servidor web (nginx/apache)
2. O usar un proxy inverso para las peticiones de tiles
3. Respetar estrictamente la política de uso de OSM

Sin embargo, la solución con CartoDB es más simple y no tiene estos requisitos.

## Verificación
Para verificar que funciona:
1. Acceder a cualquier vista de mapas en la aplicación
2. Verificar que los tiles se cargan correctamente
3. No deberían aparecer errores 403

## Referencias
- [Tile Usage Policy de OSM](https://operations.osmfoundation.org/policies/tiles/)
- [CartoDB Basemaps](https://carto.com/basemaps/)
- [Leaflet Documentation](https://leafletjs.com/)
- [Folium Documentation](https://python-visualization.github.io/folium/)

## Fecha de Implementación
2026-04-20

## Notas Adicionales
- Los tiles de CartoDB son completamente gratuitos para uso normal
- CartoDB usa datos de © OpenStreetMap contributors
- Si en el futuro se necesita más customización, se puede considerar Mapbox (requiere API key)

