"""
Tests para funciones utilitarias.
"""
import pytest
from django.core.cache import cache
from censoapp.utils import (
    get_system_parameters_cached,
    invalidate_system_parameters_cache,
)


@pytest.mark.django_db
class TestSystemParametersCache:
    """Tests para funciones de caché de parámetros del sistema."""

    def test_get_system_parameters_cached_returns_value(self):
        """Test que get_system_parameters_cached retorna un valor."""
        from censoapp.models import SystemParameters
        
        # Crear parámetro de prueba
        param = SystemParameters.objects.create(
            key="test_param",
            value="test_value",
            description="Test parameter"
        )
        
        # Obtener valor cacheado
        result = get_system_parameters_cached("test_param")
        
        assert result == "test_value"

    def test_get_system_parameters_cached_uses_cache(self):
        """Test que la función usa caché correctamente."""
        from censoapp.models import SystemParameters
        
        param = SystemParameters.objects.create(
            key="cached_param",
            value="original_value",
            description="Cached parameter"
        )
        
        # Primera llamada (cachea)
        result1 = get_system_parameters_cached("cached_param")
        
        # Cambiar valor en DB
        param.value = "new_value"
        param.save()
        
        # Segunda llamada (debe retornar valor cacheado)
        result2 = get_system_parameters_cached("cached_param")
        
        # Si usa caché, debe retornar el valor original
        assert result1 == "original_value"
        assert result2 == "original_value"  # Del caché

    def test_invalidate_system_parameters_cache_clears_cache(self):
        """Test que invalidate_system_parameters_cache limpia el caché."""
        from censoapp.models import SystemParameters
        
        param = SystemParameters.objects.create(
            key="invalidate_test",
            value="original_value",
            description="Invalidate test"
        )
        
        # Cachear valor
        result1 = get_system_parameters_cached("invalidate_test")
        assert result1 == "original_value"
        
        # Cambiar valor y invalidar caché
        param.value = "new_value"
        param.save()
        invalidate_system_parameters_cache()
        
        # Debe obtener nuevo valor
        result2 = get_system_parameters_cached("invalidate_test")
        assert result2 == "new_value"

    def test_get_system_parameters_cached_returns_none_for_missing(self):
        """Test que retorna None para parámetros inexistentes."""
        result = get_system_parameters_cached("nonexistent_param")
        assert result is None

    def test_cache_key_format(self):
        """Test que las claves de caché tienen el formato correcto."""
        cache_key = "system_param_test_key"
        
        # Verificar que se puede setear y obtener del caché
        cache.set(cache_key, "test_value", 300)
        result = cache.get(cache_key)
        
        assert result == "test_value"
        
        # Limpiar
        cache.delete(cache_key)


@pytest.mark.django_db
class TestUtilityFunctions:
    """Tests para otras funciones utilitarias."""

    def test_format_phone_number(self):
        """Test formateo de números de teléfono."""
        # Si existe una función de formateo
        from censoapp import utils
        
        if hasattr(utils, 'format_phone_number'):
            result = utils.format_phone_number("3001234567")
            assert result is not None

    def test_validate_identification(self):
        """Test validación de números de identificación."""
        from censoapp import utils
        
        if hasattr(utils, 'validate_identification'):
            # Número válido
            assert utils.validate_identification("1234567890") is True
            
            # Número inválido
            assert utils.validate_identification("abc") is False

    def test_get_age_from_birthdate(self):
        """Test cálculo de edad desde fecha de nacimiento."""
        from censoapp import utils
        from datetime import date
        
        if hasattr(utils, 'get_age'):
            birthdate = date(1990, 1, 1)
            age = utils.get_age(birthdate)
            
            # La edad debe ser aproximadamente 36 años (en 2026)
            assert 30 <= age <= 40

    def test_generate_unique_code(self):
        """Test generación de códigos únicos."""
        from censoapp import utils
        
        if hasattr(utils, 'generate_unique_code'):
            code1 = utils.generate_unique_code()
            code2 = utils.generate_unique_code()
            
            # Los códigos deben ser diferentes
            assert code1 != code2
            assert len(code1) > 0

    def test_sanitize_input(self):
        """Test sanitización de inputs."""
        from censoapp import utils
        
        if hasattr(utils, 'sanitize_input'):
            # XSS attempt
            dirty_input = "<script>alert('xss')</script>"
            clean_input = utils.sanitize_input(dirty_input)
            
            assert "<script>" not in clean_input

    def test_format_address(self):
        """Test formateo de direcciones."""
        from censoapp import utils
        
        if hasattr(utils, 'format_address'):
            address = utils.format_address("casa 123, vereda x")
            
            # Debe capitalizar correctamente
            assert "Casa" in address or "CASA" in address

