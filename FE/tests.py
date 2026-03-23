from decimal import Decimal
from datetime import date
from django.test import TestCase

from .models import (
    ActividadEconomica, Ambiente, Pais, Departamento, Municipio,
    TiposDocIDReceptor, TiposEstablecimientos, Receptor_fe,
    TipoContingencia, Descuento, Tipo_dte,
)
from .serializers import (
    ActividadEconomicaSerializer, AmbienteSerializer,
    ReceptorSerializer, TipoDteSerializer,
)


# ---------------------------------------------------------------------------
# Modelos: Catálogos básicos
# ---------------------------------------------------------------------------

class ActividadEconomicaModelTest(TestCase):
    def test_crear(self):
        act = ActividadEconomica.objects.create(codigo='4711', descripcion='Venta al por menor')
        self.assertEqual(act.codigo, '4711')

    def test_str(self):
        act = ActividadEconomica.objects.create(codigo='4711', descripcion='Comercio')
        self.assertIn('4711', str(act))
        self.assertIn('Comercio', str(act))


class AmbienteModelTest(TestCase):
    def test_crear(self):
        amb = Ambiente.objects.create(codigo='01', descripcion='Producción')
        self.assertEqual(amb.descripcion, 'Producción')

    def test_str(self):
        amb = Ambiente.objects.create(codigo='00', descripcion='Pruebas')
        self.assertEqual(str(amb), 'Pruebas')


class TipoDteModelTest(TestCase):
    def test_crear(self):
        tipo = Tipo_dte.objects.create(codigo='01', descripcion='Factura', version=1)
        self.assertEqual(tipo.codigo, '01')

    def test_str(self):
        tipo = Tipo_dte.objects.create(codigo='03', descripcion='CCF', version=3)
        self.assertIn('03', str(tipo))
        self.assertIn('CCF', str(tipo))


class PaisDepartamentoMunicipioTest(TestCase):
    def setUp(self):
        self.pais = Pais.objects.create(codigo='SV', descripcion='El Salvador')
        self.depto = Departamento.objects.create(
            codigo='06', descripcion='San Salvador', pais=self.pais
        )
        self.municipio = Municipio.objects.create(
            codigo='14', descripcion='San Salvador', departamento=self.depto
        )

    def test_relacion_pais_departamento(self):
        self.assertEqual(self.depto.pais, self.pais)

    def test_relacion_departamento_municipio(self):
        self.assertEqual(self.municipio.departamento, self.depto)

    def test_cascade_departamento(self):
        depto_id = self.depto.pk
        self.depto.delete()
        self.assertEqual(Municipio.objects.filter(departamento_id=depto_id).count(), 0)

    def test_str_pais(self):
        self.assertIn('SV', str(self.pais))


# ---------------------------------------------------------------------------
# Modelos: TipoContingencia
# ---------------------------------------------------------------------------

class TipoContingenciaModelTest(TestCase):
    def test_crear(self):
        cont = TipoContingencia.objects.create(
            codigo='1', descripcion='No hubiera energía eléctrica'
        )
        self.assertEqual(cont.codigo, '1')

    def test_motivo_opcional(self):
        cont = TipoContingencia.objects.create(codigo='2', descripcion='Falla del sistema')
        self.assertIsNone(cont.motivo_contingencia)

    def test_tipo_5_con_motivo(self):
        cont = TipoContingencia.objects.create(
            codigo='5', descripcion='Otro',
            motivo_contingencia='Falla inesperada del servidor'
        )
        self.assertIsNotNone(cont.motivo_contingencia)


# ---------------------------------------------------------------------------
# Modelos: Descuento
# ---------------------------------------------------------------------------

class DescuentoModelTest(TestCase):
    def test_crear_descuento(self):
        d = Descuento.objects.create(
            porcentaje=Decimal('10.00'),
            descripcion='Descuento de temporada',
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 12, 31),
        )
        self.assertEqual(d.porcentaje, Decimal('10.00'))
        self.assertTrue(d.estdo)  # activo por defecto

    def test_str_descuento(self):
        d = Descuento.objects.create(
            porcentaje=Decimal('5.00'),
            descripcion='Pronto pago',
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 3, 31),
        )
        self.assertIn('5.00', str(d))
        self.assertIn('Pronto pago', str(d))


# ---------------------------------------------------------------------------
# Modelos: Receptor_fe
# ---------------------------------------------------------------------------

class ReceptorFeModelTest(TestCase):
    def setUp(self):
        self.pais = Pais.objects.create(codigo='SV', descripcion='El Salvador')
        self.depto = Departamento.objects.create(
            codigo='06', descripcion='San Salvador', pais=self.pais
        )
        self.municipio = Municipio.objects.create(
            codigo='14', descripcion='San Salvador', departamento=self.depto
        )
        self.tipo_doc = TiposDocIDReceptor.objects.create(codigo='13', descripcion='DUI')

    def test_crear_receptor_minimo(self):
        receptor = Receptor_fe.objects.create(nombre='Cliente Prueba')
        self.assertEqual(receptor.nombre, 'Cliente Prueba')

    def test_crear_receptor_completo(self):
        receptor = Receptor_fe.objects.create(
            nombre='Empresa Prueba S.A.',
            tipo_documento=self.tipo_doc,
            num_documento='0614-123456-101-1',
            municipio=self.municipio,
            pais=self.pais,
            correo='empresa@test.com',
            telefono='2222-3333',
        )
        self.assertEqual(receptor.correo, 'empresa@test.com')
        self.assertEqual(receptor.tipo_documento, self.tipo_doc)

    def test_str_receptor(self):
        receptor = Receptor_fe.objects.create(nombre='Juan Pérez')
        self.assertEqual(str(receptor), 'Juan Pérez')

    def test_coordenadas_opcionales(self):
        receptor = Receptor_fe.objects.create(
            nombre='Con Geo',
            lat=Decimal('13.692940'),
            lng=Decimal('-89.218191'),
        )
        self.assertIsNotNone(receptor.lat)
        self.assertIsNotNone(receptor.lng)


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------

class ActividadEconomicaSerializerTest(TestCase):
    def test_serializar(self):
        act = ActividadEconomica.objects.create(codigo='4711', descripcion='Comercio')
        s = ActividadEconomicaSerializer(act)
        self.assertEqual(s.data['codigo'], '4711')
        self.assertEqual(s.data['descripcion'], 'Comercio')

    def test_deserializar_valido(self):
        s = ActividadEconomicaSerializer(data={'codigo': '1234', 'descripcion': 'Actividad'})
        self.assertTrue(s.is_valid(), s.errors)

    def test_deserializar_sin_codigo_invalido(self):
        s = ActividadEconomicaSerializer(data={'descripcion': 'Sin código'})
        self.assertFalse(s.is_valid())
        self.assertIn('codigo', s.errors)


class AmbienteSerializerTest(TestCase):
    def test_serializar(self):
        amb = Ambiente.objects.create(codigo='01', descripcion='Producción')
        s = AmbienteSerializer(amb)
        self.assertEqual(s.data['codigo'], '01')

    def test_deserializar_valido(self):
        s = AmbienteSerializer(data={'codigo': '00', 'descripcion': 'Pruebas'})
        self.assertTrue(s.is_valid(), s.errors)
