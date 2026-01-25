# ==================================
# PRICING STRATEGY - CENSO WEB 2026
# ==================================
# Definicion de planes y pricing para monetizacion SaaS

from decimal import Decimal
from typing import Dict, List, Any

class PricingPlan:
    """Clase para definir un plan de pricing"""

    def __init__(
        self,
        code: str,
        name: str,
        price_monthly: Decimal,
        price_yearly: Decimal,
        max_members: int,
        max_family_cards: int,
        max_users: int,
        storage_mb: int,
        features: List[str],
        limitations: List[str] = None,
        ideal_for: str = ""
    ):
        self.code = code
        self.name = name
        self.price_monthly = price_monthly
        self.price_yearly = price_yearly
        self.max_members = max_members
        self.max_family_cards = max_family_cards
        self.max_users = max_users
        self.storage_mb = storage_mb
        self.features = features
        self.limitations = limitations or []
        self.ideal_for = ideal_for

    def get_yearly_discount(self) -> Decimal:
        """Calcular descuento anual"""
        monthly_total = self.price_monthly * 12
        if monthly_total == 0:
            return Decimal('0')
        return ((monthly_total - self.price_yearly) / monthly_total * 100).quantize(Decimal('0.01'))

    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            'code': self.code,
            'name': self.name,
            'price_monthly': float(self.price_monthly),
            'price_yearly': float(self.price_yearly),
            'yearly_discount': float(self.get_yearly_discount()),
            'limits': {
                'members': self.max_members,
                'family_cards': self.max_family_cards,
                'users': self.max_users,
                'storage_mb': self.storage_mb,
            },
            'features': self.features,
            'limitations': self.limitations,
            'ideal_for': self.ideal_for
        }


# ==================================
# DEFINICIÓN DE PLANES
# ==================================

PLAN_COMUNITARIO = PricingPlan(
    code='comunitario',
    name='Comunitario',
    price_monthly=Decimal('0.00'),
    price_yearly=Decimal('0.00'),
    max_members=150,
    max_family_cards=50,
    max_users=2,
    storage_mb=500,
    features=[
        'Censo poblacional básico',
        'Gestión de fichas familiares',
        'Registro de personas',
        'Exportación a PDF',
        'Logo personalizado',
        'Búsqueda básica',
        'Soporte por comunidad (foro)',
    ],
    limitations=[
        'Sin API REST',
        'Sin reportes avanzados',
        'Sin backup automático',
        'Sin geolocalización',
        'Marca "Powered by CensoWeb"',
        'Sin exportación Excel',
    ],
    ideal_for='Comunidades pequeñas (hasta 150 miembros) que están empezando'
)

PLAN_RESGUARDO = PricingPlan(
    code='resguardo',
    name='Resguardo',
    price_monthly=Decimal('49.00'),
    price_yearly=Decimal('490.00'),  # 16% descuento
    max_members=1000,
    max_family_cards=300,
    max_users=10,
    storage_mb=5120,  # 5 GB
    features=[
        '✅ Todo lo del plan Comunitario',
        '✅ Estadísticas demográficas',
        '✅ Dashboard con gráficos',
        '✅ Reportes personalizables',
        '✅ Exportación a Excel/CSV',
        '✅ Backup automático semanal',
        '✅ Certificados oficiales',
        '✅ Sin marca de agua',
        '✅ Búsqueda avanzada',
        '✅ Historial de cambios',
        '✅ Integración WhatsApp (notificaciones)',
        '✅ Soporte por email (48h)',
    ],
    limitations=[
        'Sin API REST',
        'Sin webhooks',
        'Sin geolocalización avanzada',
        'Sin módulo de salud',
    ],
    ideal_for='Resguardos pequeños y medianos (100-1,000 miembros)'
)

PLAN_TERRITORIO = PricingPlan(
    code='territorio',
    name='Territorio',
    price_monthly=Decimal('149.00'),
    price_yearly=Decimal('1490.00'),  # 16% descuento
    max_members=5000,
    max_family_cards=1500,
    max_users=50,
    storage_mb=51200,  # 50 GB
    features=[
        '✅ Todo lo del plan Resguardo',
        '✅ Dashboard analítico avanzado',
        '✅ API REST documentada',
        '✅ Webhooks para integraciones',
        '✅ Exportación masiva programada',
        '✅ Backup diario automático',
        '✅ Geolocalización con mapas interactivos',
        '✅ Árbol genealógico digital',
        '✅ Módulo de salud comunitaria',
        '✅ Gestión de proyectos',
        '✅ Preservación cultural (multimedia)',
        '✅ Calendario de eventos',
        '✅ Notificaciones push',
        '✅ Modo offline (PWA)',
        '✅ Capacitación virtual (2h/mes)',
        '✅ Soporte prioritario (24h)',
    ],
    limitations=[
        'Instancia compartida',
    ],
    ideal_for='Asociaciones de resguardos y territorios grandes (1,000-5,000 miembros)'
)

PLAN_ENTERPRISE = PricingPlan(
    code='enterprise',
    name='Enterprise',
    price_monthly=Decimal('500.00'),  # Base, personalizable
    price_yearly=Decimal('5000.00'),
    max_members=999999,  # Ilimitado
    max_family_cards=999999,
    max_users=999999,
    storage_mb=999999,  # Ilimitado
    features=[
        '✅ Todo lo del plan Territorio',
        '✅ Instancia dedicada',
        '✅ On-premise opcional',
        '✅ SSO (Single Sign-On)',
        '✅ LDAP/Active Directory',
        '✅ Personalización completa',
        '✅ Desarrollo a medida',
        '✅ SLA 99.9% uptime',
        '✅ Soporte telefónico 24/7',
        '✅ Consultoría estratégica',
        '✅ Capacitación presencial ilimitada',
        '✅ Integración con sistemas gubernamentales',
        '✅ Cumplimiento normativo (ISO, SOC2)',
        '✅ Backup en tiempo real',
        '✅ Disaster recovery',
    ],
    limitations=[],
    ideal_for='Ministerios, ONGs, organismos internacionales, gobiernos departamentales'
)


# ==================================
# SERVICIOS PROFESIONALES (One-time)
# ==================================

PROFESSIONAL_SERVICES = {
    'implementacion_basica': {
        'name': 'Implementación Básica',
        'price': Decimal('500.00'),
        'description': 'Setup inicial + configuración + capacitación básica (4 horas)',
        'includes': [
            'Instalación y configuración',
            'Migración de datos (hasta 500 registros)',
            'Capacitación 2 usuarios',
            'Soporte 30 días post-implementación',
        ]
    },
    'implementacion_completa': {
        'name': 'Implementación Completa',
        'price': Decimal('2000.00'),
        'description': 'Implementación enterprise con migración masiva',
        'includes': [
            'Todo lo de Implementación Básica',
            'Migración ilimitada de datos',
            'Personalización de reportes',
            'Capacitación hasta 20 usuarios',
            'Soporte 90 días post-implementación',
            'Documentación personalizada',
        ]
    },
    'capacitacion_presencial': {
        'name': 'Capacitación Presencial',
        'price': Decimal('300.00'),
        'unit': 'día',
        'description': 'Capacitación on-site para equipos',
        'includes': [
            'Hasta 25 participantes',
            'Material didáctico',
            'Certificado de participación',
            'Video grabado de la sesión',
        ]
    },
    'desarrollo_personalizado': {
        'name': 'Desarrollo Personalizado',
        'price': Decimal('80.00'),
        'unit': 'hora',
        'description': 'Desarrollo de features a medida',
        'includes': [
            'Análisis de requerimientos',
            'Desarrollo y testing',
            'Documentación técnica',
            'Garantía 90 días',
        ]
    },
    'consultoria_estrategica': {
        'name': 'Consultoría Estratégica',
        'price': Decimal('150.00'),
        'unit': 'hora',
        'description': 'Asesoría en gestión censal y análisis de datos',
        'includes': [
            'Análisis de datos demográficos',
            'Recomendaciones estratégicas',
            'Diseño de políticas públicas',
            'Presentación ejecutiva',
        ]
    },
    'soporte_premium': {
        'name': 'Soporte Premium Mensual',
        'price': Decimal('200.00'),
        'unit': 'mes',
        'description': 'SLA dedicado con respuesta inmediata',
        'includes': [
            'Respuesta < 1 hora',
            'Soporte telefónico 24/7',
            'Acceso a Slack privado',
            'Revisiones mensuales',
        ]
    },
}


# ==================================
# STRIPE PRODUCT IDS (configurar en Stripe Dashboard)
# ==================================

STRIPE_PRODUCTS = {
    'resguardo_monthly': 'price_XXXXXXXXX',  # Reemplazar con ID real de Stripe
    'resguardo_yearly': 'price_XXXXXXXXX',
    'territorio_monthly': 'price_XXXXXXXXX',
    'territorio_yearly': 'price_XXXXXXXXX',
    'enterprise_monthly': 'price_XXXXXXXXX',
    'enterprise_yearly': 'price_XXXXXXXXX',
}


# ==================================
# HELPER FUNCTIONS
# ==================================

def get_all_plans() -> List[PricingPlan]:
    """Obtener todos los planes disponibles"""
    return [
        PLAN_COMUNITARIO,
        PLAN_RESGUARDO,
        PLAN_TERRITORIO,
        PLAN_ENTERPRISE,
    ]


def get_plan_by_code(code: str) -> PricingPlan:
    """Obtener plan por código"""
    plans = {
        'comunitario': PLAN_COMUNITARIO,
        'resguardo': PLAN_RESGUARDO,
        'territorio': PLAN_TERRITORIO,
        'enterprise': PLAN_ENTERPRISE,
    }
    return plans.get(code)


def calculate_revenue_projection(clients_by_plan: Dict[str, int]) -> Dict[str, Decimal]:
    """
    Calcular proyección de ingresos

    Args:
        clients_by_plan: {'resguardo': 15, 'territorio': 5, 'enterprise': 2}

    Returns:
        {'mrr': Decimal, 'arr': Decimal}
    """
    mrr = Decimal('0.00')

    for plan_code, client_count in clients_by_plan.items():
        plan = get_plan_by_code(plan_code)
        if plan:
            mrr += plan.price_monthly * client_count

    arr = mrr * 12

    return {
        'mrr': mrr,
        'arr': arr,
        'clients_total': sum(clients_by_plan.values()),
        'breakdown': {
            code: {
                'clients': count,
                'monthly_revenue': get_plan_by_code(code).price_monthly * count
            }
            for code, count in clients_by_plan.items()
        }
    }


# ==================================
# EJEMPLO DE USO
# ==================================

if __name__ == '__main__':
    # Mostrar todos los planes
    print("=" * 60)
    print("PLANES DE PRICING - CENSO WEB")
    print("=" * 60)

    for plan in get_all_plans():
        print(f"\n{plan.name.upper()}")
        print(f"  Precio mensual: ${plan.price_monthly}")
        print(f"  Precio anual: ${plan.price_yearly} ({plan.get_yearly_discount()}% descuento)")
        print(f"  Límites:")
        print(f"    - Miembros: {plan.max_members}")
        print(f"    - Fichas: {plan.max_family_cards}")
        print(f"    - Usuarios: {plan.max_users}")
        print(f"  Features: {len(plan.features)}")

    # Proyección de ingresos
    print("\n" + "=" * 60)
    print("PROYECCIÓN DE INGRESOS - ESCENARIO CONSERVADOR")
    print("=" * 60)

    projection = calculate_revenue_projection({
        'resguardo': 15,
        'territorio': 5,
        'enterprise': 2,
    })

    print(f"\nClientes totales: {projection['clients_total']}")
    print(f"MRR: ${projection['mrr']:,.2f}")
    print(f"ARR: ${projection['arr']:,.2f}")
    print("\nDesglose por plan:")
    for code, data in projection['breakdown'].items():
        plan = get_plan_by_code(code)
        print(f"  {plan.name}: {data['clients']} clientes × ${plan.price_monthly} = ${data['monthly_revenue']}")
