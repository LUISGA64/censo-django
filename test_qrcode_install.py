"""
Script para instalar qrcode y verificar su funcionamiento
"""
import subprocess
import sys

print("=" * 70)
print("INSTALANDO Y VERIFICANDO MÓDULO QRCODE")
print("=" * 70)

# Instalar qrcode
print("\n1. Instalando qrcode[pil]...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "qrcode[pil]"])
    print("✅ qrcode instalado exitosamente")
except Exception as e:
    print(f"❌ Error al instalar qrcode: {e}")
    sys.exit(1)

# Verificar importación
print("\n2. Verificando importación...")
try:
    import qrcode
    print(f"✅ qrcode importado correctamente")
    print(f"   Versión: {qrcode.__version__}")
except Exception as e:
    print(f"❌ Error al importar qrcode: {e}")
    sys.exit(1)

# Verificar QRCode class
print("\n3. Verificando clase QRCode...")
try:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    print("✅ Clase QRCode disponible")
except AttributeError as e:
    print(f"❌ Error AttributeError: {e}")
    print("\nIntentando método alternativo...")

    # Método alternativo
    try:
        qr = qrcode.make("test")
        print("✅ Método qrcode.make() funciona")
    except Exception as e2:
        print(f"❌ Error con método alternativo: {e2}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Probar generación de QR
print("\n4. Probando generación de QR...")
try:
    from io import BytesIO

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    qr.add_data("https://ejemplo.com/verificar/ABC123")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    size = len(buffer.getvalue())
    print(f"✅ QR generado exitosamente ({size} bytes)")

    # Guardar QR de prueba
    with open('test_qr.png', 'wb') as f:
        buffer.seek(0)
        f.write(buffer.read())
    print("✅ QR guardado en: test_qr.png")

except Exception as e:
    print(f"❌ Error al generar QR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ MÓDULO QRCODE FUNCIONANDO CORRECTAMENTE")
print("=" * 70)
print("\nAhora puedes intentar generar documentos PDF nuevamente.")

