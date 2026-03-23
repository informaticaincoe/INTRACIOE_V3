from decimal import Decimal
from datetime import date
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from .models import Departamentos, Cargo, Empleados, Boleta_pago

User = get_user_model()


# ---------------------------------------------------------------------------
# Modelos: Departamentos y Cargo
# ---------------------------------------------------------------------------

class DepartamentosModelTest(TestCase):
    def test_crear_departamento(self):
        depto = Departamentos.objects.create(nombre_departamento='Tecnología')
        self.assertEqual(depto.nombre_departamento, 'Tecnología')

    def test_str_departamento(self):
        depto = Departamentos.objects.create(nombre_departamento='RRHH')
        self.assertEqual(str(depto), 'RRHH')


class CargoModelTest(TestCase):
    def setUp(self):
        self.depto = Departamentos.objects.create(nombre_departamento='Ventas')

    def test_crear_cargo(self):
        cargo = Cargo.objects.create(departamento=self.depto, nombre_cargo='Gerente de Ventas')
        self.assertEqual(cargo.nombre_cargo, 'Gerente de Ventas')
        self.assertEqual(cargo.departamento, self.depto)

    def test_str_cargo(self):
        cargo = Cargo.objects.create(departamento=self.depto, nombre_cargo='Vendedor')
        self.assertEqual(str(cargo), 'Vendedor')

    def test_cascade_al_eliminar_departamento(self):
        Cargo.objects.create(departamento=self.depto, nombre_cargo='Ejecutivo')
        depto_id = self.depto.pk
        self.depto.delete()
        self.assertEqual(Cargo.objects.filter(departamento_id=depto_id).count(), 0)


# ---------------------------------------------------------------------------
# Modelos: Empleados
# ---------------------------------------------------------------------------

class EmpleadosModelTest(TestCase):
    def setUp(self):
        self.empleado = Empleados.objects.create(
            nombre='Juan',
            apellido='Pérez',
            dui='01234567-8',
            codigo_empleado='EMP-001',
            edad=30,
            salario=800,
            cargo='Desarrollador',
            email='juan@empresa.com',
            num_telefono='7777-8888',
        )

    def test_str_empleado(self):
        self.assertEqual(str(self.empleado), 'Juan Pérez')

    def test_campos_empleado(self):
        self.assertEqual(self.empleado.dui, '01234567-8')
        self.assertEqual(self.empleado.salario, 800)
        self.assertEqual(self.empleado.email, 'juan@empresa.com')

    def test_crear_multiple_empleados(self):
        Empleados.objects.create(
            nombre='María', apellido='López', dui='09876543-2',
            codigo_empleado='EMP-002', edad=25, salario=700,
            cargo='Diseñadora', email='maria@empresa.com', num_telefono='6666-5555'
        )
        self.assertEqual(Empleados.objects.count(), 2)


# ---------------------------------------------------------------------------
# Modelos: Boleta de pago
# ---------------------------------------------------------------------------

class BoletaPagoModelTest(TestCase):
    def setUp(self):
        self.empleado = Empleados.objects.create(
            nombre='Carlos', apellido='García',
            dui='11111111-1', codigo_empleado='EMP-003',
            edad=35, salario=1000, cargo='Contador',
            email='carlos@empresa.com', num_telefono='5555-4444'
        )

    def _crear_boleta(self, **kwargs):
        defaults = dict(
            fecha_pago=date(2025, 1, 31),
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 1, 31),
            dias_laborados=Decimal('30.00'),
            empleado=self.empleado,
            descuento_afp=Decimal('30.00'),
            descuento_isss=Decimal('22.50'),
            descuento_renta=Decimal('0.00'),
            otro_descuento1=Decimal('0.00'),
            otro_descuento2=Decimal('0.00'),
            total_descuentos=Decimal('52.50'),
            comisiones=Decimal('0.00'),
            viaticos=Decimal('0.00'),
            hr_extra_fer=Decimal('0.00'),
            hr_extra_fer_noc=Decimal('0.00'),
            total_pago=Decimal('1000.00'),
            liquido_recibir=Decimal('947.50'),
        )
        defaults.update(kwargs)
        return Boleta_pago.objects.create(**defaults)

    def test_crear_boleta(self):
        boleta = self._crear_boleta()
        self.assertEqual(boleta.empleado, self.empleado)
        self.assertEqual(boleta.liquido_recibir, Decimal('947.50'))

    def test_str_boleta(self):
        boleta = self._crear_boleta()
        self.assertIn('2025', str(boleta))

    def test_total_descuentos(self):
        boleta = self._crear_boleta(
            descuento_afp=Decimal('30.00'),
            descuento_isss=Decimal('22.50'),
            total_descuentos=Decimal('52.50'),
        )
        # El total debe ser >= suma de descuentos principales
        self.assertGreaterEqual(
            boleta.total_descuentos,
            boleta.descuento_afp + boleta.descuento_isss
        )

    def test_cascade_al_eliminar_empleado(self):
        self._crear_boleta()
        emp_id = self.empleado.pk
        self.empleado.delete()
        self.assertEqual(Boleta_pago.objects.filter(empleado_id=emp_id).count(), 0)

    def test_multiple_boletas_mismo_empleado(self):
        self._crear_boleta(fecha_pago=date(2025, 1, 31))
        self._crear_boleta(
            fecha_pago=date(2025, 2, 28),
            fecha_inicio=date(2025, 2, 1),
            fecha_fin=date(2025, 2, 28),
        )
        self.assertEqual(Boleta_pago.objects.filter(empleado=self.empleado).count(), 2)
