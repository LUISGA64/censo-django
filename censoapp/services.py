# censo/services.py
from django.db import transaction, IntegrityError
from django.db.models import Max
from .models import FamilyCard, Person

class FamilyCardServiceError(Exception):
    """Error personalizado para el servicio de creación de ficha."""
    pass

def create_family_with_head(family_form, person_form):
    if not (family_form.is_valid() and person_form.is_valid()):
        raise FamilyCardServiceError("Formularios inválidos")

    identification = person_form.cleaned_data['identification_person']
    if Person.objects.filter(identification_person=identification).exists():
        raise FamilyCardServiceError("Ya existe una persona con esa identificación")

    try:
        with transaction.atomic():
            family_card = family_form.save(commit=False)
            last_number = FamilyCard.objects.aggregate(Max('family_card_number'))['family_card_number'] or 0
            family_card.family_card_number = last_number + 1
            family_card.save()

            person = person_form.save(commit=False)
            person.family_card = family_card
            person.family_head = True
            person.save()

            return family_card
    except IntegrityError as e:
        raise FamilyCardServiceError(f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise FamilyCardServiceError(f"Error inesperado: {str(e)}")
