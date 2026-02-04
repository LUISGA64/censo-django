# Dashboard Views for Analytics

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .analytics import DashboardAnalytics


@login_required
def dashboard_analytics(request):
    """Vista principal del dashboard"""
    from datetime import date, timedelta
    from .models import GeneratedDocument

    org = None
    if hasattr(request.user, 'userprofile') and not request.user.userprofile.can_view_all_organizations:
        org = request.user.userprofile.organization

    analytics = DashboardAnalytics(organization=org)

    # KPIs principales
    context = {
        'total_personas': analytics.get_total_population(),
        'total_familias': analytics.get_total_families(),
        'organization': org,
    }

    # Documentos próximos a vencer (30 días)
    try:
        docs_qs = GeneratedDocument.objects.filter(
            expiration_date__lte=date.today() + timedelta(days=30),
            expiration_date__gte=date.today(),
            status='ISSUED'
        )
        if org:
            docs_qs = docs_qs.filter(organization=org)
        context['docs_expiring'] = docs_qs.count()
    except:
        context['docs_expiring'] = 0

    return render(request, 'dashboard/analytics.html', context)


@login_required
def api_gender_distribution(request):
    """API: Distribución por género"""
    org = None
    if hasattr(request.user, 'profile') and not request.user.profile.can_view_all_organizations:
        org = request.user.profile.organization
    return JsonResponse(DashboardAnalytics(organization=org).get_gender_distribution())


@login_required
def api_age_pyramid(request):
    """API: Pirámide poblacional"""
    org = None
    if hasattr(request.user, 'profile') and not request.user.profile.can_view_all_organizations:
        org = request.user.profile.organization
    return JsonResponse(DashboardAnalytics(organization=org).get_age_pyramid())


@login_required
def api_education_distribution(request):
    """API: Distribución educativa"""
    org = None
    if hasattr(request.user, 'profile') and not request.user.profile.can_view_all_organizations:
        org = request.user.profile.organization
    return JsonResponse(DashboardAnalytics(organization=org).get_education_distribution())


@login_required
def api_civil_state(request):
    """API: Estado civil"""
    org = None
    if hasattr(request.user, 'profile') and not request.user.profile.can_view_all_organizations:
        org = request.user.profile.organization
    return JsonResponse(DashboardAnalytics(organization=org).get_civil_state_distribution())


@login_required
def api_sidewalks(request):
    """API: Veredas"""
    org = None
    if hasattr(request.user, 'profile') and not request.user.profile.can_view_all_organizations:
        org = request.user.profile.organization
    return JsonResponse(DashboardAnalytics(organization=org).get_sidewalks_distribution())


@login_required
def api_population_growth(request):
    """API: Crecimiento poblacional"""
    org = None
    if hasattr(request.user, 'profile') and not request.user.profile.can_view_all_organizations:
        org = request.user.profile.organization
    years = int(request.GET.get('years', 5))
    return JsonResponse(DashboardAnalytics(organization=org).get_population_growth(years=years))
