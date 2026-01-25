# Dashboard Analytics Module
# Servicios para generar datos analíticos del censo

from django.db.models import Count, Q, Avg, Max, Min, Sum
from django.db.models.functions import ExtractYear
from datetime import datetime, date, timedelta
from censoapp.models import (
    Person, FamilyCard, Organizations, Gender,
    EducationLevel, CivilState, Occupancy, Sidewalks
)


class DashboardAnalytics:
    """Clase para generar analytics del dashboard"""

    def __init__(self, organization=None):
        self.organization = organization

    def get_total_population(self):
        """Total de población activa"""
        qs = Person.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)
        return qs.count()

    def get_total_families(self):
        """Total de fichas familiares activas"""
        qs = FamilyCard.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(organization=self.organization)
        return qs.count()

    def get_gender_distribution(self):
        """Distribución por género"""
        qs = Person.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)

        data = qs.values('gender__gender').annotate(
            count=Count('id')
        ).order_by('-count')

        return {
            'labels': [item['gender__gender'] for item in data],
            'data': [item['count'] for item in data],
            'colors': ['#4F46E5', '#EC4899', '#8B5CF6', '#10B981']
        }

    def get_age_pyramid(self):
        """Pirámide poblacional por rangos de edad"""
        qs = Person.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)

        # Calcular edades
        today = date.today()
        age_ranges = {
            '0-5': (0, 5),
            '6-12': (6, 12),
            '13-18': (13, 18),
            '19-30': (19, 30),
            '31-50': (31, 50),
            '51-70': (51, 70),
            '70+': (71, 150)
        }

        male_data = []
        female_data = []
        labels = []

        for label, (min_age, max_age) in age_ranges.items():
            min_date = today - timedelta(days=max_age*365.25)
            max_date = today - timedelta(days=min_age*365.25)

            # Hombres
            male_count = qs.filter(
                gender__gender='Masculino',
                date_birth__gte=min_date,
                date_birth__lte=max_date
            ).count()

            # Mujeres
            female_count = qs.filter(
                gender__gender='Femenino',
                date_birth__gte=min_date,
                date_birth__lte=max_date
            ).count()

            labels.append(label)
            male_data.append(-male_count)  # Negativo para el lado izquierdo
            female_data.append(female_count)

        return {
            'labels': labels,
            'male_data': male_data,
            'female_data': female_data
        }

    def get_education_distribution(self):
        """Distribución por nivel educativo"""
        qs = Person.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)

        data = qs.values('education_level__education_level').annotate(
            count=Count('id')
        ).order_by('-count')

        return {
            'labels': [item['education_level__education_level'] for item in data],
            'data': [item['count'] for item in data],
            'colors': [
                '#3B82F6', '#10B981', '#F59E0B', '#EF4444',
                '#8B5CF6', '#EC4899', '#14B8A6', '#F97316'
            ]
        }

    def get_civil_state_distribution(self):
        """Distribución por estado civil"""
        qs = Person.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)

        data = qs.values('civil_state__state_civil').annotate(
            count=Count('id')
        ).order_by('-count')

        return {
            'labels': [item['civil_state__state_civil'] for item in data],
            'data': [item['count'] for item in data],
            'colors': ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        }

    def get_occupation_distribution(self):
        """Top 10 ocupaciones"""
        qs = Person.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)

        data = qs.values('occupation__description_occupancy').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        return {
            'labels': [item['occupation__description_occupancy'] for item in data],
            'data': [item['count'] for item in data],
            'colors': ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        }

    def get_sidewalks_distribution(self):
        """Distribución por veredas"""
        qs = FamilyCard.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(organization=self.organization)

        data = qs.values('sidewalk_home__sidewalk_name').annotate(
            families=Count('id'),
            people=Count('person')
        ).order_by('-people')

        return {
            'labels': [item['sidewalk_home__sidewalk_name'] for item in data],
            'families': [item['families'] for item in data],
            'people': [item['people'] for item in data],
            'colors': ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        }

    def get_population_growth(self, years=5):
        """Crecimiento poblacional por año"""
        qs = Person.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)

        current_year = datetime.now().year
        labels = []
        data = []

        for i in range(years, -1, -1):
            year = current_year - i
            count = qs.filter(date_birth__year__lte=year).count()
            labels.append(str(year))
            data.append(count)

        return {
            'labels': labels,
            'data': data
        }

    def get_age_statistics(self):
        """Estadísticas de edad"""
        qs = Person.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)

        today = date.today()
        ages = []

        for person in qs:
            age = today.year - person.date_birth.year
            if (today.month, today.day) < (person.date_birth.month, person.date_birth.day):
                age -= 1
            ages.append(age)

        if ages:
            return {
                'average': sum(ages) / len(ages),
                'min': min(ages),
                'max': max(ages),
                'total': len(ages)
            }
        return {'average': 0, 'min': 0, 'max': 0, 'total': 0}

    def get_family_size_distribution(self):
        """Distribución por tamaño de familia"""
        qs = FamilyCard.objects.filter(state=True)
        if self.organization:
            qs = qs.filter(organization=self.organization)

        family_sizes = {}
        for family in qs:
            size = Person.objects.filter(family_card=family, state=True).count()
            size_range = self._get_size_range(size)
            family_sizes[size_range] = family_sizes.get(size_range, 0) + 1

        labels = sorted(family_sizes.keys())
        data = [family_sizes[label] for label in labels]

        return {
            'labels': labels,
            'data': data,
            'colors': ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        }

    def _get_size_range(self, size):
        """Clasificar tamaño de familia"""
        if size == 1:
            return '1 persona'
        elif size <= 3:
            return '2-3 personas'
        elif size <= 5:
            return '4-5 personas'
        elif size <= 7:
            return '6-7 personas'
        else:
            return '8+ personas'

    def get_summary_statistics(self):
        """Estadísticas resumidas para cards"""
        total_population = self.get_total_population()
        total_families = self.get_total_families()
        age_stats = self.get_age_statistics()

        # Tasa de natalidad (últimos 12 meses)
        one_year_ago = date.today() - timedelta(days=365)
        qs = Person.objects.filter(state=True, date_birth__gte=one_year_ago)
        if self.organization:
            qs = qs.filter(family_card__organization=self.organization)
        births_last_year = qs.count()

        # Promedio personas por familia
        avg_family_size = total_population / total_families if total_families > 0 else 0

        # Género mayoritario
        gender_dist = self.get_gender_distribution()
        majority_gender = gender_dist['labels'][0] if gender_dist['labels'] else 'N/A'

        return {
            'total_population': total_population,
            'total_families': total_families,
            'average_age': round(age_stats['average'], 1),
            'births_last_year': births_last_year,
            'avg_family_size': round(avg_family_size, 1),
            'majority_gender': majority_gender,
            'min_age': age_stats['min'],
            'max_age': age_stats['max']
        }
