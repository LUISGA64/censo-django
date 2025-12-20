import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from django.contrib.auth.models import User
from censoapp.models import UserProfile

users = User.objects.all()
print('Total usuarios:', users.count())
print()

for u in users:
    tiene_perfil = hasattr(u, 'userprofile')
    print(f'Usuario: {u.username}')
    print(f'  Superuser: {u.is_superuser}')
    print(f'  Tiene perfil: {tiene_perfil}')
    if tiene_perfil:
        org = u.userprofile.organization
        print(f'  Organización: {org.organization_name if org else "SIN ORGANIZACIÓN"}')
    print()

