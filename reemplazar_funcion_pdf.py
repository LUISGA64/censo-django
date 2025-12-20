"""
Script para reemplazar la función download_document_pdf en document_views.py
"""

# Leer el archivo original
with open('censoapp/document_views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Nueva función con WeasyPrint
nueva_funcion = '''@login_required
def download_document_pdf(request, document_id):
    """
    Genera y muestra un documento en formato PDF usando WeasyPrint.
    Convierte HTML a PDF correctamente respetando todos los estilos y etiquetas.
    El PDF se muestra en el navegador (inline) para previsualización.
    """
    from weasyprint import HTML
    from django.template.loader import render_to_string
    import base64
    
    # Verificar si el documento existe
    try:
        document = GeneratedDocument.objects.get(pk=document_id)
    except GeneratedDocument.DoesNotExist:
        messages.error(
            request,
            f"El documento con ID {document_id} no existe. "
            f"Es posible que haya sido eliminado o que el enlace sea incorrecto."
        )
        return redirect('documents-stats')

    # VALIDACIÓN: Verificar permisos por organización
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if user_profile.organization != document.organization:
                messages.error(
                    request,
                    f"No tiene permisos para descargar este documento. "
                    f"El documento pertenece a {document.organization.organization_name}."
                )
                return JsonResponse({'error': 'No autorizado'}, status=403)
        except AttributeError:
            return JsonResponse({'error': 'No tiene un perfil de usuario configurado'}, status=403)

    try:
        # Generar código QR y convertirlo a base64
        qr_buffer = generate_document_qr(document)
        qr_buffer.seek(0)
        qr_base64 = base64.b64encode(qr_buffer.read()).decode()
        
        # Preparar contexto para el template HTML
        context = {
            'document': document,
            'organization': document.organization,
            'person': document.person,
            'signers': document.signers.all(),
            'qr_code': qr_base64,
            'issue_date_formatted': document.issue_date.strftime('%d de %B de %Y'),
            'expiration_date_formatted': document.expiration_date.strftime('%d de %B de %Y') if document.expiration_date else None,
        }
        
        # Renderizar HTML del documento usando el template
        html_string = render_to_string('censo/documentos/pdf_template.html', context)
        
        # Generar PDF con WeasyPrint
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf_bytes = pdf_file.write_pdf()
        
        # Determinar si es descarga o previsualización
        is_download = request.GET.get('download', 'false').lower() == 'true'
        
        # Crear respuesta HTTP con el PDF
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Length'] = len(pdf_bytes)
        response['Accept-Ranges'] = 'bytes'
        
        # Cabeceras CORS para permitir la carga desde PDF.js
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type'
        
        if is_download:
            # Forzar descarga
            response['Content-Disposition'] = f'attachment; filename="Documento_{document.document_number}.pdf"'
        else:
            # Previsualización en navegador
            response['Content-Disposition'] = f'inline; filename="Documento_{document.document_number}.pdf"'
            # Cache control para previsualización
            response['Cache-Control'] = 'public, max-age=3600'
        
        return response
        
    except Exception as e:
        logger.error(f"Error al generar PDF con WeasyPrint: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        messages.error(request, f"Error al generar el PDF: {str(e)}")
        return redirect('view-document', document_id=document_id)
'''

# Encontrar inicio y fin de la función actual
inicio = content.find('@login_required\ndef download_document_pdf(request, document_id):')
if inicio == -1:
    print("No se encontró la función download_document_pdf")
    exit(1)

# Buscar la siguiente función
fin = content.find('\ndef verify_document(request, hash):', inicio)
if fin == -1:
    print("No se encontró el final de la función")
    exit(1)

# Reemplazar
nuevo_content = content[:inicio] + nueva_funcion + '\n\n' + content[fin:]

# Guardar
with open('censoapp/document_views.py', 'w', encoding='utf-8') as f:
    f.write(nuevo_content)

print("✅ Función reemplazada exitosamente")
print(f"   - Inicio en posición: {inicio}")
print(f"   - Fin en posición: {fin}")
print(f"   - Líneas eliminadas: ~{(fin - inicio) // 50}")
print(f"   - Nueva función: ~100 líneas")

