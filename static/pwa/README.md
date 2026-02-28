# Generación de Iconos PWA
## Instrucciones Rápidas

Los iconos PWA son necesarios para que la aplicación se vea bien cuando se instala en dispositivos móviles.

## Opción 1: Generador Online (MÁS FÁCIL) ⭐

1. **Ir a:** https://www.pwabuilder.com/imageGenerator

2. **Subir tu logo:**
   - Formato: PNG
   - Tamaño mínimo: 512x512px
   - Fondo transparente o color sólido

3. **Generar iconos:**
   - Click "Generate Zip"
   - Descargar el archivo ZIP

4. **Instalar:**
   ```bash
   # Extraer el ZIP
   # Copiar todos los archivos .png a:
   static/pwa/
   ```

## Opción 2: Usar Logo Existente

Si ya tienes un logo en el proyecto:

```bash
# Ubicar tu logo actual
static/assets/img/tu-logo.png

# Copiar y renombrar para cada tamaño:
cp static/assets/img/tu-logo.png static/pwa/icon-192x192.png
cp static/assets/img/tu-logo.png static/pwa/icon-512x512.png
# etc...

# Redimensionar con herramientas:
- Photoshop
- GIMP (gratis)
- Paint.NET (Windows)
- Preview (Mac)
```

## Tamaños Necesarios

```
icon-72x72.png     → Notificaciones
icon-96x96.png     → Android
icon-128x128.png   → Chrome Web Store
icon-144x144.png   → Windows
icon-152x152.png   → iOS (iPad)
icon-192x192.png   → Android principal
icon-384x384.png   → Android splash
icon-512x512.png   → Alta resolución
```

## Opción 3: Iconos Temporales (Para Testing)

Puedes usar iconos placeholder temporalmente:

```bash
# Descargar iconos de muestra:
https://via.placeholder.com/192x192/2196F3/FFFFFF?text=CW
https://via.placeholder.com/512x512/2196F3/FFFFFF?text=CW

# Guardar como:
static/pwa/icon-192x192.png
static/pwa/icon-512x512.png
```

## Verificar Instalación

Después de copiar los iconos:

```bash
# 1. Acceder a la app
http://127.0.0.1:8000/

# 2. Abrir DevTools (F12)
# 3. Tab "Application"
# 4. Sección "Manifest"
# 5. Ver "Icons" - deben aparecer todos
```

## Colores Recomendados

Para el logo de Censo Web:

- **Color Primario:** #2196F3 (Azul corporativo)
- **Color Secundario:** #1976D2
- **Fondo:** Blanco o transparente
- **Texto:** Blanco sobre azul

## Notas

- Los iconos deben ser **cuadrados** (mismo ancho y alto)
- Formato **PNG** preferiblemente
- Fondo **transparente** se ve mejor
- Tamaño **mínimo 512x512px** para el logo original
