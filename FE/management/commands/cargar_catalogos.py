"""
Management command para cargar todos los catálogos oficiales del
Ministerio de Hacienda de El Salvador.

Uso:  python manage.py cargar_catalogos
Es idempotente — no duplica registros si ya existen.
"""
from django.core.management.base import BaseCommand


def _bulk(Model, rows, code_field="codigo"):
    """Inserta registros que no existan (por código)."""
    existing = set(Model.objects.values_list(code_field, flat=True))
    to_create = [Model(**r) for r in rows if r[code_field] not in existing]
    if to_create:
        Model.objects.bulk_create(to_create, ignore_conflicts=True)
    return len(to_create)


class Command(BaseCommand):
    help = "Carga los catálogos oficiales del Ministerio de Hacienda de El Salvador"

    def handle(self, *args, **options):
        from FE.models import (
            Pais, Departamento, Municipio, ActividadEconomica,
            Ambiente, Modelofacturacion, TipoTransmision, TipoContingencia,
            TiposEstablecimientos, Tipo_dte, TiposDocIDReceptor,
            CondicionOperacion, FormasPago, Plazo, TipoDocContingencia,
            TipoInvalidacion, TipoDonacion, TipoPersona, TipoTransporte,
            INCOTERMS, TipoDomicilioFiscal, TipoMoneda, RecintoFiscal,
            RegimenExportacion, TipoGeneracionDocumento, TipoRetencionIVAMH,
            OtrosDicumentosAsociado, TiposServicio_Medico,
        )
        from INVENTARIO.models import (
            TipoItem, TipoTributo, Tributo, TipoValor,
            TipoUnidadMedida, UnidadMedida,
        )

        total = 0

        # ── Ambientes ──
        total += _bulk(Ambiente, [
            {"codigo": "00", "descripcion": "Pruebas"},
            {"codigo": "01", "descripcion": "Producción"},
        ])

        # ── Modelo de Facturación ──
        total += _bulk(Modelofacturacion, [
            {"codigo": "1", "descripcion": "Modelo Facturación previo"},
            {"codigo": "2", "descripcion": "Modelo Facturación diferido"},
        ])

        # ── Tipo Transmisión ──
        total += _bulk(TipoTransmision, [
            {"codigo": "1", "descripcion": "Normal"},
            {"codigo": "2", "descripcion": "Contingencia"},
        ])

        # ── Tipo Generación Documento ──
        total += _bulk(TipoGeneracionDocumento, [
            {"codigo": "1", "descripcion": "Normal"},
            {"codigo": "2", "descripcion": "Por contingencia"},
        ])

        # ── Tipo Contingencia ──
        total += _bulk(TipoContingencia, [
            {"codigo": "1", "descripcion": "No disponibilidad de sistema del MH"},
            {"codigo": "2", "descripcion": "No disponibilidad de sistema del emisor"},
            {"codigo": "3", "descripcion": "No disponibilidad de internet del emisor"},
            {"codigo": "4", "descripcion": "No disponibilidad de internet por caso fortuito"},
            {"codigo": "5", "descripcion": "Otro (detallar motivo)"},
        ])

        # ── Tipos de DTE ──
        total += _bulk(Tipo_dte, [
            {"codigo": "01", "descripcion": "Factura", "version": 1},
            {"codigo": "03", "descripcion": "Comprobante de Crédito Fiscal", "version": 3},
            {"codigo": "04", "descripcion": "Nota de Remisión", "version": 1},
            {"codigo": "05", "descripcion": "Nota de Crédito", "version": 3},
            {"codigo": "06", "descripcion": "Nota de Débito", "version": 3},
            {"codigo": "07", "descripcion": "Comprobante de Retención", "version": 1},
            {"codigo": "08", "descripcion": "Comprobante de Liquidación", "version": 1},
            {"codigo": "09", "descripcion": "Documento Contable de Liquidación", "version": 1},
            {"codigo": "11", "descripcion": "Factura de Exportación", "version": 1},
            {"codigo": "14", "descripcion": "Factura de Sujeto Excluido", "version": 1},
            {"codigo": "15", "descripcion": "Comprobante de Donación", "version": 1},
        ])

        # ── Tipo Documento ID Receptor ──
        total += _bulk(TiposDocIDReceptor, [
            {"codigo": "13", "descripcion": "DUI"},
            {"codigo": "36", "descripcion": "NIT"},
            {"codigo": "37", "descripcion": "Otro"},
            {"codigo": "02", "descripcion": "Carnet de Residente"},
            {"codigo": "03", "descripcion": "Pasaporte"},
        ])

        # ── Tipo Establecimiento ──
        total += _bulk(TiposEstablecimientos, [
            {"codigo": "01", "descripcion": "Sucursal / Agencia"},
            {"codigo": "02", "descripcion": "Casa Matriz"},
            {"codigo": "04", "descripcion": "Bodega"},
            {"codigo": "07", "descripcion": "Punto de Venta"},
            {"codigo": "20", "descripcion": "Otro"},
        ])

        # ── Condición de Operación ──
        total += _bulk(CondicionOperacion, [
            {"codigo": "1", "descripcion": "Contado"},
            {"codigo": "2", "descripcion": "A crédito"},
            {"codigo": "3", "descripcion": "Otro"},
        ])

        # ── Formas de Pago ──
        total += _bulk(FormasPago, [
            {"codigo": "01", "descripcion": "Billetes y monedas"},
            {"codigo": "02", "descripcion": "Tarjeta Débito"},
            {"codigo": "03", "descripcion": "Tarjeta Crédito"},
            {"codigo": "04", "descripcion": "Cheque"},
            {"codigo": "05", "descripcion": "Transferencia – Depósito Bancario"},
            {"codigo": "06", "descripcion": "Vales"},
            {"codigo": "07", "descripcion": "Letras de cambio"},
            {"codigo": "08", "descripcion": "Tarjeta Prepago / regalo"},
            {"codigo": "09", "descripcion": "Dinero electrónico"},
            {"codigo": "10", "descripcion": "Bitcoin"},
            {"codigo": "11", "descripcion": "Monedero electrónico"},
            {"codigo": "12", "descripcion": "Vale digital"},
            {"codigo": "13", "descripcion": "Pago con servicio de intermediación (PPI)"},
            {"codigo": "14", "descripcion": "Otros"},
            {"codigo": "99", "descripcion": "Otros"},
        ])

        # ── Plazos ──
        total += _bulk(Plazo, [
            {"codigo": "01", "descripcion": "Día/s"},
            {"codigo": "02", "descripcion": "Mes/es"},
            {"codigo": "03", "descripcion": "Año/s"},
        ])

        # ── Tipo Documento Contingencia ──
        total += _bulk(TipoDocContingencia, [
            {"codigo": "1", "descripcion": "Factura"},
            {"codigo": "2", "descripcion": "Comprobante de Crédito Fiscal"},
            {"codigo": "3", "descripcion": "Nota de Remisión"},
            {"codigo": "4", "descripcion": "Nota de Crédito"},
            {"codigo": "5", "descripcion": "Nota de Débito"},
            {"codigo": "6", "descripcion": "Comprobante de Retención"},
            {"codigo": "7", "descripcion": "Comprobante de Liquidación"},
            {"codigo": "8", "descripcion": "Documento Contable de Liquidación"},
            {"codigo": "9", "descripcion": "Factura de Exportación"},
            {"codigo": "10", "descripcion": "Factura de Sujeto Excluido"},
            {"codigo": "11", "descripcion": "Comprobante de Donación"},
        ])

        # ── Tipo Invalidación ──
        total += _bulk(TipoInvalidacion, [
            {"codigo": "1", "descripcion": "Error en la información del documento"},
            {"codigo": "2", "descripcion": "Rescindir de la operación realizada"},
            {"codigo": "3", "descripcion": "Otro motivo"},
        ])

        # ── Tipo Donación ──
        total += _bulk(TipoDonacion, [
            {"codigo": "1", "descripcion": "Bien"},
            {"codigo": "2", "descripcion": "Servicio"},
            {"codigo": "3", "descripcion": "Ambos"},
        ])

        # ── Tipo Persona ──
        total += _bulk(TipoPersona, [
            {"codigo": "1", "descripcion": "Persona Natural"},
            {"codigo": "2", "descripcion": "Persona Jurídica"},
        ])

        # ── Tipo Retención IVA MH ──
        total += _bulk(TipoRetencionIVAMH, [
            {"codigo": "22", "descripcion": "Retención 1%"},
            {"codigo": "C4", "descripcion": "Retención 13%"},
            {"codigo": "C9", "descripcion": "Retención total"},
        ])

        # ── Otros Documentos Asociados ──
        total += _bulk(OtrosDicumentosAsociado, [
            {"codigo": "1", "descripcion": "Documento emitido por el mismo contribuyente"},
            {"codigo": "2", "descripcion": "Documento emitido por otro contribuyente"},
            {"codigo": "3", "descripcion": "Resolución del MH"},
        ])

        # ── Tipo Transporte ──
        total += _bulk(TipoTransporte, [
            {"codigo": "01", "descripcion": "Terrestre"},
            {"codigo": "02", "descripcion": "Marítimo"},
            {"codigo": "03", "descripcion": "Aéreo"},
        ])

        # ── INCOTERMS ──
        total += _bulk(INCOTERMS, [
            {"codigo": "01", "descripcion": "Costo, seguro y flete - CIF"},
            {"codigo": "02", "descripcion": "Costo y flete - CFR"},
            {"codigo": "03", "descripcion": "Entrega en puerto de destino con derechos pagados - DDP"},
            {"codigo": "04", "descripcion": "Entrega en lugar convenido - DAP"},
            {"codigo": "05", "descripcion": "Entrega en puerto de destino sin derechos pagados - DAT"},
            {"codigo": "06", "descripcion": "En fábrica - EXW"},
            {"codigo": "07", "descripcion": "Franco al costado del buque - FAS"},
            {"codigo": "08", "descripcion": "Franco a bordo - FOB"},
            {"codigo": "09", "descripcion": "Franco transportista - FCA"},
            {"codigo": "10", "descripcion": "Transporte y seguro pagados hasta - CIP"},
            {"codigo": "11", "descripcion": "Transporte pagado hasta - CPT"},
            {"codigo": "12", "descripcion": "Entrega en lugar descargado - DPU"},
        ])

        # ── Tipo Domicilio Fiscal ──
        total += _bulk(TipoDomicilioFiscal, [
            {"codigo": "01", "descripcion": "Local propio"},
            {"codigo": "02", "descripcion": "Local arrendado"},
        ])

        # ── Tipo Moneda ──
        total += _bulk(TipoMoneda, [
            {"codigo": "USD", "descripcion": "Dólar estadounidense"},
            {"codigo": "CAD", "descripcion": "Dólar canadiense"},
            {"codigo": "EUR", "descripcion": "Euro"},
            {"codigo": "GBP", "descripcion": "Libra esterlina"},
            {"codigo": "GTQ", "descripcion": "Quetzal guatemalteco"},
            {"codigo": "HNL", "descripcion": "Lempira hondureño"},
            {"codigo": "NIO", "descripcion": "Córdoba nicaragüense"},
            {"codigo": "CRC", "descripcion": "Colón costarricense"},
            {"codigo": "MXN", "descripcion": "Peso mexicano"},
        ])

        # ── Recinto Fiscal ──
        total += _bulk(RecintoFiscal, [
            {"codigo": "01", "descripcion": "Aeropuerto Internacional El Salvador"},
            {"codigo": "02", "descripcion": "Puerto de Acajutla"},
            {"codigo": "03", "descripcion": "Puerto de La Unión"},
            {"codigo": "04", "descripcion": "Aduana terrestre San Bartolo"},
            {"codigo": "05", "descripcion": "Aduana terrestre Santa Ana"},
            {"codigo": "06", "descripcion": "Aduana terrestre El Poy"},
            {"codigo": "07", "descripcion": "Aduana terrestre El Amatillo"},
            {"codigo": "08", "descripcion": "Aduana terrestre Anguiatú"},
            {"codigo": "09", "descripcion": "Aduana terrestre Las Chinamas"},
            {"codigo": "10", "descripcion": "Aduana terrestre La Hachadura"},
            {"codigo": "11", "descripcion": "Aduana terrestre San Cristóbal"},
        ])

        # ── Régimen Exportación ──
        total += _bulk(RegimenExportacion, [
            {"codigo": "01", "descripcion": "Exportación Definitiva"},
            {"codigo": "02", "descripcion": "Exportación Temporal"},
            {"codigo": "03", "descripcion": "Reexportación"},
        ])

        # ── Tipos Servicio Médico ──
        total += _bulk(TiposServicio_Medico, [
            {"codigo": "1", "descripcion": "Consulta médica"},
            {"codigo": "2", "descripcion": "Consulta dental"},
            {"codigo": "3", "descripcion": "Hospitalización"},
            {"codigo": "4", "descripcion": "Cirugía"},
            {"codigo": "5", "descripcion": "Laboratorio clínico"},
            {"codigo": "6", "descripcion": "Imágenes diagnósticas"},
            {"codigo": "7", "descripcion": "Otros"},
        ])

        # ══════════════════════════════════════════════════════════
        # PAÍSES (El Salvador + Centroamérica + principales)
        # ══════════════════════════════════════════════════════════
        total += _bulk(Pais, [
            {"codigo": "9300", "descripcion": "El Salvador"},
            {"codigo": "9100", "descripcion": "Guatemala"},
            {"codigo": "9200", "descripcion": "Honduras"},
            {"codigo": "9400", "descripcion": "Nicaragua"},
            {"codigo": "9500", "descripcion": "Costa Rica"},
            {"codigo": "9600", "descripcion": "Panamá"},
            {"codigo": "9700", "descripcion": "Belice"},
            {"codigo": "4100", "descripcion": "Estados Unidos de América"},
            {"codigo": "4200", "descripcion": "México"},
            {"codigo": "1100", "descripcion": "España"},
        ])

        # ── Departamentos de El Salvador ──
        sv = Pais.objects.filter(codigo="9300").first()
        if sv:
            deptos_data = [
                ("01", "Ahuachapán"), ("02", "Santa Ana"), ("03", "Sonsonate"),
                ("04", "Chalatenango"), ("05", "La Libertad"), ("06", "San Salvador"),
                ("07", "Cuscatlán"), ("08", "La Paz"), ("09", "Cabañas"),
                ("10", "San Vicente"), ("11", "Usulután"), ("12", "San Miguel"),
                ("13", "Morazán"), ("14", "La Unión"),
            ]
            existing_deptos = set(Departamento.objects.values_list("codigo", flat=True))
            deptos_to_create = [
                Departamento(codigo=c, descripcion=d, pais=sv)
                for c, d in deptos_data if c not in existing_deptos
            ]
            if deptos_to_create:
                Departamento.objects.bulk_create(deptos_to_create, ignore_conflicts=True)
                total += len(deptos_to_create)

        # ── Municipios de El Salvador (44 nuevos — Decreto 762, mayo 2024) ──
        municipios_sv = {
            "01": [  # Ahuachapán
                ("01", "Ahuachapán Norte"), ("02", "Ahuachapán Centro"), ("03", "Ahuachapán Sur"),
            ],
            "02": [  # Santa Ana
                ("01", "Santa Ana Norte"), ("02", "Santa Ana Centro"),
                ("03", "Santa Ana Este"), ("04", "Santa Ana Oeste"),
            ],
            "03": [  # Sonsonate
                ("01", "Sonsonate Norte"), ("02", "Sonsonate Centro"),
                ("03", "Sonsonate Este"), ("04", "Sonsonate Oeste"),
            ],
            "04": [  # Chalatenango
                ("01", "Chalatenango Norte"), ("02", "Chalatenango Centro"),
                ("03", "Chalatenango Sur"),
            ],
            "05": [  # La Libertad
                ("01", "La Libertad Norte"), ("02", "La Libertad Centro"),
                ("03", "La Libertad Oeste"), ("04", "La Libertad Este"),
                ("05", "La Libertad Costa"), ("06", "La Libertad Sur"),
            ],
            "06": [  # San Salvador
                ("01", "San Salvador Norte"), ("02", "San Salvador Oeste"),
                ("03", "San Salvador Centro"), ("04", "San Salvador Este"),
                ("05", "San Salvador Sur"),
            ],
            "07": [  # Cuscatlán
                ("01", "Cuscatlán Norte"), ("02", "Cuscatlán Sur"),
            ],
            "08": [  # La Paz
                ("01", "La Paz Oeste"), ("02", "La Paz Centro"), ("03", "La Paz Este"),
            ],
            "09": [  # Cabañas
                ("01", "Cabañas Este"), ("02", "Cabañas Oeste"),
            ],
            "10": [  # San Vicente
                ("01", "San Vicente Norte"), ("02", "San Vicente Sur"),
            ],
            "11": [  # Usulután
                ("01", "Usulután Norte"), ("02", "Usulután Este"), ("03", "Usulután Oeste"),
            ],
            "12": [  # San Miguel
                ("01", "San Miguel Norte"), ("02", "San Miguel Centro"),
                ("03", "San Miguel Oeste"),
            ],
            "13": [  # Morazán
                ("01", "Morazán Norte"), ("02", "Morazán Sur"),
            ],
            "14": [  # La Unión
                ("01", "La Unión Norte"), ("02", "La Unión Sur"),
            ],
        }

        for depto_cod, munis in municipios_sv.items():
            depto = Departamento.objects.filter(codigo=depto_cod).first()
            if not depto:
                continue
            existing_munis = set(
                Municipio.objects.filter(departamento=depto).values_list("codigo", flat=True)
            )
            to_create = [
                Municipio(codigo=c, descripcion=d, departamento=depto)
                for c, d in munis if c not in existing_munis
            ]
            if to_create:
                Municipio.objects.bulk_create(to_create, ignore_conflicts=True)
                total += len(to_create)

        # ══════════════════════════════════════════════════════════
        # ACTIVIDADES ECONÓMICAS (principales)
        # ══════════════════════════════════════════════════════════
        actividades = [
            ("01111", "Cultivo de cereales"), ("01112", "Cultivo de legumbres"),
            ("10100", "Elaboración y conservación de carne"),
            ("10710", "Elaboración de productos de panadería"),
            ("41001", "Construcción de edificios"), ("41002", "Construcción de obras de ingeniería civil"),
            ("45100", "Venta de vehículos automotores"),
            ("46100", "Venta al por mayor a cambio de una retribución"),
            ("46310", "Venta al por mayor de alimentos"),
            ("46900", "Venta al por mayor no especializada"),
            ("47110", "Venta al por menor en almacenes no especializados"),
            ("47190", "Otras actividades de venta al por menor en almacenes no especializados"),
            ("47210", "Venta al por menor de alimentos en almacenes especializados"),
            ("47300", "Venta al por menor de combustibles para vehículos"),
            ("47410", "Venta al por menor de computadoras y equipo periférico"),
            ("47520", "Venta al por menor de materiales de construcción"),
            ("47610", "Venta al por menor de libros y periódicos"),
            ("47710", "Venta al por menor de prendas de vestir"),
            ("47810", "Venta al por menor de alimentos en puestos de venta"),
            ("49100", "Transporte interurbano de pasajeros por ferrocarril"),
            ("49320", "Transporte de pasajeros por taxi"),
            ("55101", "Hoteles y moteles"),
            ("56101", "Restaurantes"),
            ("56102", "Cafeterías"),
            ("56290", "Otras actividades de servicio de comidas"),
            ("58110", "Edición de libros"),
            ("61100", "Telecomunicaciones alámbricas"),
            ("62010", "Programación informática"),
            ("62020", "Consultoría de tecnología de información"),
            ("63110", "Procesamiento de datos"),
            ("64110", "Banca central"),
            ("64190", "Otros tipos de intermediación monetaria"),
            ("66110", "Administración de mercados financieros"),
            ("68100", "Actividades inmobiliarias realizadas con bienes propios"),
            ("69100", "Actividades jurídicas"),
            ("69200", "Actividades de contabilidad y auditoría"),
            ("70100", "Actividades de oficinas principales"),
            ("70200", "Actividades de consultoría de gestión"),
            ("71100", "Actividades de arquitectura e ingeniería"),
            ("73110", "Agencias de publicidad"),
            ("74100", "Actividades especializadas de diseño"),
            ("75000", "Actividades veterinarias"),
            ("80100", "Actividades de seguridad privada"),
            ("85100", "Enseñanza preescolar y primaria"),
            ("85200", "Enseñanza secundaria"),
            ("85300", "Enseñanza superior"),
            ("86100", "Actividades de hospitales"),
            ("86200", "Actividades de médicos y odontólogos"),
            ("86900", "Otras actividades de atención de la salud humana"),
            ("88100", "Actividades de asistencia social sin alojamiento"),
            ("90000", "Actividades creativas, artísticas y de entretenimiento"),
            ("93110", "Gestión de instalaciones deportivas"),
            ("95110", "Reparación de computadoras y equipo periférico"),
            ("96010", "Lavado y limpieza de prendas de tela y de piel"),
            ("96020", "Peluquería y otros tratamientos de belleza"),
            ("96090", "Otras actividades de servicios personales n.c.p."),
        ]
        total += _bulk(ActividadEconomica, [
            {"codigo": c, "descripcion": d} for c, d in actividades
        ])

        # ══════════════════════════════════════════════════════════
        # INVENTARIO — catálogos
        # ══════════════════════════════════════════════════════════
        total += _bulk(TipoItem, [
            {"codigo": "1", "descripcion": "Bienes"},
            {"codigo": "2", "descripcion": "Servicios"},
            {"codigo": "3", "descripcion": "Ambos (Bienes y Servicios)"},
            {"codigo": "4", "descripcion": "Otros tributos por ítem"},
        ])

        total += _bulk(TipoUnidadMedida, [
            {"codigo": "1", "descripcion": "Unidad"},
            {"codigo": "2", "descripcion": "Metro"},
            {"codigo": "3", "descripcion": "Kilogramo"},
            {"codigo": "4", "descripcion": "Litro"},
            {"codigo": "5", "descripcion": "Libra"},
            {"codigo": "6", "descripcion": "Yarda"},
            {"codigo": "8", "descripcion": "Onza"},
            {"codigo": "9", "descripcion": "Caja"},
            {"codigo": "10", "descripcion": "Millar"},
            {"codigo": "11", "descripcion": "Pares"},
            {"codigo": "12", "descripcion": "Docena"},
            {"codigo": "13", "descripcion": "Quintal"},
            {"codigo": "17", "descripcion": "Galón"},
            {"codigo": "18", "descripcion": "Botella"},
            {"codigo": "19", "descripcion": "Paquete"},
            {"codigo": "24", "descripcion": "Bolsa"},
            {"codigo": "36", "descripcion": "Mes"},
            {"codigo": "59", "descripcion": "Otro"},
            {"codigo": "99", "descripcion": "Otra"},
        ])

        existing_um = set(UnidadMedida.objects.values_list("nombre", flat=True))
        um_to_create = [
            UnidadMedida(nombre=n, abreviatura=a)
            for n, a in [
                ("Unidad", "Ud"), ("Metro", "m"), ("Kilogramo", "kg"),
                ("Litro", "L"), ("Libra", "lb"), ("Caja", "Cj"),
                ("Docena", "Doc"), ("Galón", "gal"), ("Paquete", "Paq"),
                ("Servicio", "Srv"), ("Hora", "hr"),
            ]
            if n not in existing_um
        ]
        if um_to_create:
            UnidadMedida.objects.bulk_create(um_to_create, ignore_conflicts=True)
            total += len(um_to_create)

        total += _bulk(TipoTributo, [
            {"codigo": "1", "descripcion": "Impuesto"},
            {"codigo": "2", "descripcion": "Tasa"},
            {"codigo": "3", "descripcion": "Contribución especial"},
        ])

        total += _bulk(TipoValor, [
            {"descripcion": "Porcentaje"},
            {"descripcion": "Valor fijo"},
        ], code_field="descripcion")

        # Tributo IVA (el principal)
        tipo_imp = TipoTributo.objects.filter(codigo="1").first()
        tipo_pct = TipoValor.objects.filter(descripcion="Porcentaje").first()
        if tipo_imp and tipo_pct:
            if not Tributo.objects.filter(codigo="20").exists():
                Tributo.objects.create(
                    tipo_tributo=tipo_imp, codigo="20",
                    descripcion="Impuesto al Valor Agregado 13%",
                    valor_tributo=13.00, tipo_valor=tipo_pct
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(
            f"Catálogos cargados: {total} registros nuevos insertados."
        ))
