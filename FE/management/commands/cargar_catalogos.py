"""
Management command para cargar todos los catálogos oficiales del
Ministerio de Hacienda de El Salvador — Versión 1.1 (08/2024).

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
    help = "Carga catálogos oficiales MH El Salvador v1.1 (08/2024)"

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

        # ═══════════════════════════════════════════════════════════
        # CAT-001 Ambiente de destino
        # ═══════════════════════════════════════════════════════════
        total += _bulk(Ambiente, [
            {"codigo": "00", "descripcion": "Modo prueba"},
            {"codigo": "01", "descripcion": "Modo producción"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-002 Tipo de Documento
        # ═══════════════════════════════════════════════════════════
        total += _bulk(Tipo_dte, [
            {"codigo": "01", "descripcion": "Factura", "version": 1},
            {"codigo": "03", "descripcion": "Comprobante de crédito fiscal", "version": 3},
            {"codigo": "04", "descripcion": "Nota de remisión", "version": 1},
            {"codigo": "05", "descripcion": "Nota de crédito", "version": 3},
            {"codigo": "06", "descripcion": "Nota de débito", "version": 3},
            {"codigo": "07", "descripcion": "Comprobante de retención", "version": 1},
            {"codigo": "08", "descripcion": "Comprobante de liquidación", "version": 1},
            {"codigo": "09", "descripcion": "Documento contable de liquidación", "version": 1},
            {"codigo": "11", "descripcion": "Facturas de exportación", "version": 1},
            {"codigo": "14", "descripcion": "Factura de sujeto excluido", "version": 1},
            {"codigo": "15", "descripcion": "Comprobante de donación", "version": 1},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-003 Modelo de Facturación
        # ═══════════════════════════════════════════════════════════
        total += _bulk(Modelofacturacion, [
            {"codigo": "1", "descripcion": "Modelo Facturación previo"},
            {"codigo": "2", "descripcion": "Modelo Facturación diferido"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-004 Tipo de Transmisión
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoTransmision, [
            {"codigo": "1", "descripcion": "Transmisión normal"},
            {"codigo": "2", "descripcion": "Transmisión por contingencia"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-005 Tipo de Contingencia
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoContingencia, [
            {"codigo": "1", "descripcion": "No disponibilidad de sistema del MH"},
            {"codigo": "2", "descripcion": "No disponibilidad de sistema del emisor"},
            {"codigo": "3", "descripcion": "Falla en el suministro de servicio de Internet del Emisor"},
            {"codigo": "4", "descripcion": "Falla en el suministro de servicio de energía eléctrica del emisor que impida la transmisión de los DTE"},
            {"codigo": "5", "descripcion": "Otro (deberá digitar un máximo de 500 caracteres explicando el motivo)"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-006 Retención IVA MH
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoRetencionIVAMH, [
            {"codigo": "22", "descripcion": "Retención IVA 1%"},
            {"codigo": "C4", "descripcion": "Retención IVA 13%"},
            {"codigo": "C9", "descripcion": "Otras retenciones IVA casos especiales"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-007 Tipo de Generación del Documento
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoGeneracionDocumento, [
            {"codigo": "1", "descripcion": "Físico"},
            {"codigo": "2", "descripcion": "Electrónico"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-009 Tipo de establecimiento
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TiposEstablecimientos, [
            {"codigo": "01", "descripcion": "Sucursal"},
            {"codigo": "02", "descripcion": "Casa Matriz"},
            {"codigo": "04", "descripcion": "Bodega"},
            {"codigo": "07", "descripcion": "Patio"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-010 Código tipo de Servicio (Médico)
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TiposServicio_Medico, [
            {"codigo": "1", "descripcion": "Cirugía"},
            {"codigo": "2", "descripcion": "Operación"},
            {"codigo": "3", "descripcion": "Tratamiento médico"},
            {"codigo": "4", "descripcion": "Cirugía instituto salvadoreño de Bienestar Magisterial"},
            {"codigo": "5", "descripcion": "Operación Instituto Salvadoreño de Bienestar Magisterial"},
            {"codigo": "6", "descripcion": "Tratamiento médico Instituto Salvadoreño de Bienestar Magisterial"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-011 Tipo de Item
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoItem, [
            {"codigo": "1", "descripcion": "Bienes"},
            {"codigo": "2", "descripcion": "Servicios"},
            {"codigo": "3", "descripcion": "Ambos (Bienes y Servicios, incluye los dos inherente a los Productos o servicios)"},
            {"codigo": "4", "descripcion": "Otros tributos por ítem"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-012 Departamento
        # ═══════════════════════════════════════════════════════════
        # Primero crear El Salvador como país
        if not Pais.objects.filter(codigo="SV").exists():
            Pais.objects.create(codigo="SV", descripcion="El Salvador")
            total += 1
        sv = Pais.objects.filter(codigo="SV").first()
        # Fallback al código viejo si existe
        if not sv:
            sv = Pais.objects.filter(descripcion__icontains="salvador").first()

        deptos_data = [
            ("00", "Otro (Para extranjeros)"),
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

        # ═══════════════════════════════════════════════════════════
        # CAT-013 Municipio (44 nuevos — Decreto 762, v1.1)
        # ═══════════════════════════════════════════════════════════
        municipios_sv = {
            "00": [("00", "Otro (Para extranjeros)")],
            "01": [  # Ahuachapán
                ("13", "AHUACHAPAN NORTE"), ("14", "AHUACHAPAN CENTRO"), ("15", "AHUACHAPAN SUR"),
            ],
            "02": [  # Santa Ana
                ("14", "SANTA ANA NORTE"), ("15", "SANTA ANA CENTRO"),
                ("16", "SANTA ANA ESTE"), ("17", "SANTA ANA OESTE"),
            ],
            "03": [  # Sonsonate
                ("17", "SONSONATE NORTE"), ("18", "SONSONATE CENTRO"),
                ("19", "SONSONATE ESTE"), ("20", "SONSONATE OESTE"),
            ],
            "04": [  # Chalatenango
                ("34", "CHALATENANGO NORTE"), ("35", "CHALATENANGO CENTRO"),
                ("36", "CHALATENANGO SUR"),
            ],
            "05": [  # La Libertad
                ("23", "LA LIBERTAD NORTE"), ("24", "LA LIBERTAD CENTRO"),
                ("25", "LA LIBERTAD OESTE"), ("26", "LA LIBERTAD ESTE"),
                ("27", "LA LIBERTAD COSTA"), ("28", "LA LIBERTAD SUR"),
            ],
            "06": [  # San Salvador
                ("20", "SAN SALVADOR NORTE"), ("21", "SAN SALVADOR OESTE"),
                ("22", "SAN SALVADOR ESTE"), ("23", "SAN SALVADOR CENTRO"),
                ("24", "SAN SALVADOR SUR"),
            ],
            "07": [  # Cuscatlán
                ("17", "CUSCATLAN NORTE"), ("18", "CUSCATLAN SUR"),
            ],
            "08": [  # La Paz
                ("23", "LA PAZ OESTE"), ("24", "LA PAZ CENTRO"), ("25", "LA PAZ ESTE"),
            ],
            "09": [  # Cabañas
                ("10", "CABAÑAS OESTE"), ("11", "CABAÑAS ESTE"),
            ],
            "10": [  # San Vicente
                ("14", "SAN VICENTE NORTE"), ("15", "SAN VICENTE SUR"),
            ],
            "11": [  # Usulután
                ("24", "USULUTAN NORTE"), ("25", "USULUTAN ESTE"), ("26", "USULUTAN OESTE"),
            ],
            "12": [  # San Miguel
                ("21", "SAN MIGUEL NORTE"), ("22", "SAN MIGUEL CENTRO"),
                ("23", "SAN MIGUEL OESTE"),
            ],
            "13": [  # Morazán
                ("27", "MORAZAN NORTE"), ("28", "MORAZAN SUR"),
            ],
            "14": [  # La Unión
                ("19", "LA UNION NORTE"), ("20", "LA UNION SUR"),
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

        # ═══════════════════════════════════════════════════════════
        # CAT-014 Unidad de Medida (v1.1 — Sistema Métrico)
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoUnidadMedida, [
            {"codigo": "1",  "descripcion": "metro"},
            {"codigo": "2",  "descripcion": "Yarda"},
            {"codigo": "6",  "descripcion": "milímetro"},
            {"codigo": "9",  "descripcion": "kilómetro cuadrado"},
            {"codigo": "10", "descripcion": "Hectárea"},
            {"codigo": "13", "descripcion": "metro cuadrado"},
            {"codigo": "15", "descripcion": "Vara cuadrada"},
            {"codigo": "18", "descripcion": "metro cúbico"},
            {"codigo": "20", "descripcion": "Barril"},
            {"codigo": "22", "descripcion": "Galón"},
            {"codigo": "23", "descripcion": "Litro"},
            {"codigo": "24", "descripcion": "Botella"},
            {"codigo": "26", "descripcion": "Millar"},
            {"codigo": "30", "descripcion": "Tonelada"},
            {"codigo": "32", "descripcion": "Quintal"},
            {"codigo": "33", "descripcion": "Arroba"},
            {"codigo": "34", "descripcion": "Kilogramo"},
            {"codigo": "36", "descripcion": "Libra"},
            {"codigo": "37", "descripcion": "Onza troy"},
            {"codigo": "38", "descripcion": "Onza"},
            {"codigo": "39", "descripcion": "Gramo"},
            {"codigo": "40", "descripcion": "Miligramo"},
            {"codigo": "42", "descripcion": "Megawatt"},
            {"codigo": "43", "descripcion": "Kilowatt"},
            {"codigo": "44", "descripcion": "Watt"},
            {"codigo": "45", "descripcion": "Megavoltio-amperio"},
            {"codigo": "46", "descripcion": "Kilovoltio-amperio"},
            {"codigo": "47", "descripcion": "Voltio-amperio"},
            {"codigo": "49", "descripcion": "Gigawatt-hora"},
            {"codigo": "50", "descripcion": "Megawatt-hora"},
            {"codigo": "51", "descripcion": "Kilowatt-hora"},
            {"codigo": "52", "descripcion": "Watt-hora"},
            {"codigo": "53", "descripcion": "Kilovoltio"},
            {"codigo": "54", "descripcion": "Voltio"},
            {"codigo": "55", "descripcion": "Millar"},
            {"codigo": "56", "descripcion": "Medio millar"},
            {"codigo": "57", "descripcion": "Ciento"},
            {"codigo": "58", "descripcion": "Docena"},
            {"codigo": "59", "descripcion": "Unidad"},
            {"codigo": "99", "descripcion": "Otra"},
        ])

        existing_um = set(UnidadMedida.objects.values_list("nombre", flat=True))
        um_to_create = [
            UnidadMedida(nombre=n, abreviatura=a)
            for n, a in [
                ("Unidad", "Ud"), ("Metro", "m"), ("Kilogramo", "kg"),
                ("Litro", "L"), ("Libra", "lb"), ("Caja", "Cj"),
                ("Docena", "Doc"), ("Galón", "gal"), ("Paquete", "Paq"),
                ("Servicio", "Srv"), ("Hora", "hr"), ("Quintal", "qq"),
                ("Tonelada", "ton"), ("Gramo", "g"), ("Mililitro", "ml"),
                ("Onza", "oz"), ("Botella", "bot"),
            ]
            if n not in existing_um
        ]
        if um_to_create:
            UnidadMedida.objects.bulk_create(um_to_create, ignore_conflicts=True)
            total += len(um_to_create)

        # ═══════════════════════════════════════════════════════════
        # CAT-016 Condición de la Operación
        # ═══════════════════════════════════════════════════════════
        total += _bulk(CondicionOperacion, [
            {"codigo": "1", "descripcion": "Contado"},
            {"codigo": "2", "descripcion": "A crédito"},
            {"codigo": "3", "descripcion": "Otro"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-017 Forma de Pago (v1.1)
        # ═══════════════════════════════════════════════════════════
        total += _bulk(FormasPago, [
            {"codigo": "01", "descripcion": "Billetes y monedas"},
            {"codigo": "02", "descripcion": "Tarjeta Débito"},
            {"codigo": "03", "descripcion": "Tarjeta Crédito"},
            {"codigo": "04", "descripcion": "Cheque"},
            {"codigo": "05", "descripcion": "Transferencia-Depósito Bancario"},
            {"codigo": "06", "descripcion": "Dinero electrónico"},
            {"codigo": "08", "descripcion": "Dinero electrónico"},
            {"codigo": "09", "descripcion": "Monedero electrónico"},
            {"codigo": "11", "descripcion": "Bitcoin"},
            {"codigo": "12", "descripcion": "Otras Criptomonedas"},
            {"codigo": "13", "descripcion": "Cuentas por pagar del receptor"},
            {"codigo": "14", "descripcion": "Giro bancario"},
            {"codigo": "99", "descripcion": "Otros (se debe indicar el medio de pago)"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-018 Plazo
        # ═══════════════════════════════════════════════════════════
        total += _bulk(Plazo, [
            {"codigo": "01", "descripcion": "Días"},
            {"codigo": "02", "descripcion": "Meses"},
            {"codigo": "03", "descripcion": "Años"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-020 País (códigos ISO 2 letras — v1.1)
        # ═══════════════════════════════════════════════════════════
        paises = [
            ("AF","Afganistán"),("AX","Aland"),("AL","Albania"),("DE","Alemania"),
            ("AD","Andorra"),("AO","Angola"),("AI","Anguila"),("AQ","Antártica"),
            ("AG","Antigua y Barbuda"),("AW","Aruba"),("SA","Arabia Saudita"),
            ("DZ","Argelia"),("AR","Argentina"),("AM","Armenia"),("AU","Australia"),
            ("AT","Austria"),("AZ","Azerbaiyán"),("BS","Bahamas"),("BH","Bahrein"),
            ("BD","Bangladesh"),("BB","Barbados"),("BE","Bélgica"),("BZ","Belice"),
            ("BJ","Benín"),("BM","Bermudas"),("BY","Bielorrusia"),("BO","Bolivia"),
            ("BQ","Bonaire, Sint Eustatius and Saba"),("BA","Bosnia-Herzegovina"),
            ("BW","Botswana"),("BR","Brasil"),("BN","Brunei"),("BG","Bulgaria"),
            ("BF","Burkina Faso"),("BI","Burundi"),("BT","Bután"),("CV","Cabo Verde"),
            ("KY","Caimán, Islas"),("KH","Camboya"),("CM","Camerún"),("CA","Canadá"),
            ("CF","Centroafricana, República"),("TD","Chad"),("CL","Chile"),
            ("CN","China"),("CY","Chipre"),("VA","Ciudad del Vaticano"),
            ("CO","Colombia"),("KM","Comoras"),("CG","Congo"),("CI","Costa de Marfil"),
            ("CR","Costa Rica"),("HR","Croacia"),("CU","Cuba"),("CW","Curazao"),
            ("DK","Dinamarca"),("DM","Dominica"),("DJ","Djibouti"),("EC","Ecuador"),
            ("EG","Egipto"),("SV","El Salvador"),("AE","Emiratos Árabes Unidos"),
            ("ER","Eritrea"),("SK","Eslovaquia"),("SI","Eslovenia"),("ES","España"),
            ("US","Estados Unidos"),("EE","Estonia"),("ET","Etiopía"),("FJ","Fiji"),
            ("PH","Filipinas"),("FI","Finlandia"),("FR","Francia"),("GA","Gabón"),
            ("GM","Gambia"),("GE","Georgia"),("GH","Ghana"),("GI","Gibraltar"),
            ("GD","Granada"),("GR","Grecia"),("GL","Groenlandia"),("GP","Guadalupe"),
            ("GU","Guam"),("GT","Guatemala"),("GF","Guayana Francesa"),
            ("GG","Guernsey"),("GN","Guinea"),("GQ","Guinea Ecuatorial"),
            ("GW","Guinea-Bissau"),("GY","Guyana"),("HT","Haití"),("HN","Honduras"),
            ("HK","Hong Kong"),("HU","Hungría"),("IN","India"),("ID","Indonesia"),
            ("IQ","Irak"),("IE","Irlanda"),("BV","Isla Bouvet"),("IM","Isla de Man"),
            ("NF","Isla Norfolk"),("IS","Islandia"),("CX","Islas Navidad"),
            ("CC","Islas Cocos"),("CK","Islas Cook"),("FO","Islas Faroe"),
            ("GS","Islas Georgias d. S. -Sandwich d. S."),("HM","Islas Heard y McDonald"),
            ("FK","Islas Malvinas (Falkland)"),("MP","Islas Marianas del Norte"),
            ("MH","Islas Marshall"),("PN","Islas Pitcairn"),("TC","Islas Turcas y Caicos"),
            ("UM","Islas Ultramarinas de E.E.U.U"),("VI","Islas Vírgenes"),
            ("IL","Israel"),("IT","Italia"),("JM","Jamaica"),("JP","Japón"),
            ("JE","Jersey"),("JO","Jordania"),("KZ","Kazajistán"),("KE","Kenia"),
            ("KG","Kirguistán"),("KI","Kiribati"),("KW","Kuwait"),
            ("LA","Laos, República Democrática"),("LS","Lesotho"),("LV","Letonia"),
            ("LB","Líbano"),("LR","Liberia"),("LY","Libia"),("LI","Liechtenstein"),
            ("LT","Lituania"),("LU","Luxemburgo"),("MO","Macao"),("MK","Macedonia"),
            ("MG","Madagascar"),("MY","Malasia"),("MW","Malawi"),("MV","Maldivas"),
            ("ML","Malí"),("MT","Malta"),("MA","Marruecos"),("MQ","Martinica e.a."),
            ("MU","Mauricio"),("MR","Mauritania"),("YT","Mayotte"),("MX","México"),
            ("FM","Micronesia"),("MD","Moldavia, República de"),("MC","Mónaco"),
            ("MN","Mongolia"),("ME","Montenegro"),("MS","Montserrat"),
            ("MZ","Mozambique"),("MM","Myanmar"),("NA","Namibia"),("NR","Nauru"),
            ("NP","Nepal"),("NI","Nicaragua"),("NE","Niger"),("NG","Nigeria"),
            ("NU","Niue"),("NO","Noruega"),("NC","Nueva Caledonia"),
            ("NZ","Nueva Zelanda"),("OM","Omán"),("NL","Países Bajos"),
            ("PK","Pakistán"),("PW","Palaos"),("PS","Palestina"),("PA","Panamá"),
            ("PG","Papúa, Nueva Guinea"),("PY","Paraguay"),("PE","Perú"),
            ("PF","Polinesia Francesa"),("PL","Polonia"),("PT","Portugal"),
            ("PR","Puerto Rico"),("QA","Qatar"),("GB","Reino Unido"),
            ("KP","Rep. Democrática popular de Corea"),("CZ","República Checa"),
            ("KR","República de Corea"),("CD","República Democrática del Congo"),
            ("DO","República Dominicana"),("IR","República Islámica de Irán"),
            ("RE","Reunión"),("RW","Ruanda"),("RO","Rumanía"),("RU","Rusia"),
            ("EH","Sahara Occidental"),("BL","Saint Barthélemy"),
            ("MF","Saint Martin (French part)"),("SB","Salomón, Islas"),
            ("WS","Samoa"),("AS","Samoa Americana"),("KN","San Cristóbal y Nieves"),
            ("SM","San Marino"),("PM","San Pedro y Miquelón"),
            ("VC","San Vicente y las Granadinas"),("SH","Santa Elena"),
            ("LC","Santa Lucía"),("ST","Santo Tomé y Príncipe"),("SN","Senegal"),
            ("RS","Serbia"),("SC","Seychelles"),("SL","Sierra Leona"),
            ("SG","Singapur"),("SX","Sint Maarten (Dutch part)"),("SY","Siria"),
            ("SO","Somalia"),("SS","South Sudán"),("LK","Sri Lanka"),
            ("ZA","Sudáfrica"),("SD","Sudán"),("SE","Suecia"),("CH","Suiza"),
            ("SR","Surinam"),("SJ","Svalbard y Jan Mayen"),("SZ","Swazilandia"),
            ("TH","Tailandia"),("TW","Taiwan, Provincia de China"),
            ("TZ","Tanzania, República Unida de"),("TJ","Tayikistán"),
            ("IO","Territorio Británico Océano Índico"),
            ("TF","Territorios Australes Franceses"),("TL","Timor Oriental"),
            ("TG","Togo"),("TK","Tokelau"),("TO","Tonga"),
            ("TT","Trinidad y Tobago"),("TN","Túnez"),("TM","Turkmenistán"),
            ("TR","Turquía"),("TV","Tuvalu"),("UA","Ucrania"),("UG","Uganda"),
            ("UY","Uruguay"),("UZ","Uzbekistán"),("VU","Vanuatu"),
            ("VE","Venezuela"),("VN","Vietnam"),("VG","Islas Vírgenes Británicas"),
            ("WF","Wallis y Fortuna, Islas"),("YE","Yemen"),("ZM","Zambia"),
            ("ZW","Zimbabue"),
        ]
        total += _bulk(Pais, [{"codigo": c, "descripcion": d} for c, d in paises])

        # ═══════════════════════════════════════════════════════════
        # CAT-021 Otros Documentos Asociados
        # ═══════════════════════════════════════════════════════════
        total += _bulk(OtrosDicumentosAsociado, [
            {"codigo": "1", "descripcion": "Emisor"},
            {"codigo": "2", "descripcion": "Receptor"},
            {"codigo": "3", "descripcion": "Médico (solo aplica para contribuyentes obligados a la presentación de F-958)"},
            {"codigo": "4", "descripcion": "Transporte (solo aplica para Factura de exportación)"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-022 Tipo de documento de identificación del Receptor
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TiposDocIDReceptor, [
            {"codigo": "36", "descripcion": "NIT"},
            {"codigo": "13", "descripcion": "DUI"},
            {"codigo": "37", "descripcion": "Otro"},
            {"codigo": "03", "descripcion": "Pasaporte"},
            {"codigo": "02", "descripcion": "Carnet de Residente"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-023 Tipo de Documento en Contingencia
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoDocContingencia, [
            {"codigo": "01", "descripcion": "Factura Electrónico"},
            {"codigo": "03", "descripcion": "Comprobante de Crédito Fiscal Electrónico"},
            {"codigo": "04", "descripcion": "Nota de Remisión Electrónica"},
            {"codigo": "05", "descripcion": "Nota de Crédito Electrónica"},
            {"codigo": "06", "descripcion": "Nota de Débito Electrónica"},
            {"codigo": "11", "descripcion": "Factura de Exportación Electrónica"},
            {"codigo": "14", "descripcion": "Factura de Sujeto Excluido Electrónica"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-024 Tipo de Invalidación
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoInvalidacion, [
            {"codigo": "1", "descripcion": "Error en la Información del Documento Tributario Electrónico a invalidar"},
            {"codigo": "2", "descripcion": "Rescindir de la operación realizada"},
            {"codigo": "3", "descripcion": "Otro"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-026 Tipo de Donación
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoDonacion, [
            {"codigo": "1", "descripcion": "Efectivo"},
            {"codigo": "2", "descripcion": "Bien"},
            {"codigo": "3", "descripcion": "Servicio"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-027 Recinto fiscal (v1.1 — ampliado)
        # ═══════════════════════════════════════════════════════════
        total += _bulk(RecintoFiscal, [
            {"codigo": "01", "descripcion": "Terrestre San Bartolo"},
            {"codigo": "02", "descripcion": "Marítima de Acajutla"},
            {"codigo": "03", "descripcion": "Aérea De Comalapa"},
            {"codigo": "04", "descripcion": "Terrestre Las Chinamas"},
            {"codigo": "05", "descripcion": "Terrestre La Hachadura"},
            {"codigo": "06", "descripcion": "Terrestre Santa Ana"},
            {"codigo": "07", "descripcion": "Terrestre San Cristóbal"},
            {"codigo": "08", "descripcion": "Terrestre Anguiatú"},
            {"codigo": "09", "descripcion": "Terrestre El Amatillo"},
            {"codigo": "10", "descripcion": "Marítima La Unión"},
            {"codigo": "11", "descripcion": "Terrestre El Poy"},
            {"codigo": "12", "descripcion": "Terrestre Metallo"},
            {"codigo": "15", "descripcion": "Fardos Postales"},
            {"codigo": "16", "descripcion": "Z.F. San Marcos"},
            {"codigo": "17", "descripcion": "Z.F. El Pedregal"},
            {"codigo": "18", "descripcion": "Z.F. San Bartolo"},
            {"codigo": "20", "descripcion": "Z.F. Exportsalva"},
            {"codigo": "21", "descripcion": "Z.F. American Park"},
            {"codigo": "23", "descripcion": "Z.F. Internacional"},
            {"codigo": "24", "descripcion": "Z.F. Diez"},
            {"codigo": "26", "descripcion": "Z.F. Miramar"},
            {"codigo": "27", "descripcion": "Z.F. Santo Tomás"},
            {"codigo": "28", "descripcion": "Z.F. Santa Tecla"},
            {"codigo": "29", "descripcion": "Z.F. Santa Ana"},
            {"codigo": "30", "descripcion": "Z.F. La Concordia"},
            {"codigo": "31", "descripcion": "Aérea Ilopango"},
            {"codigo": "32", "descripcion": "Z.F. Pipil"},
            {"codigo": "33", "descripcion": "Puerto Barillas"},
            {"codigo": "34", "descripcion": "Z.F. Calvo Conservas"},
            {"codigo": "35", "descripcion": "Feria Internacional"},
            {"codigo": "36", "descripcion": "Aduana El Papalón"},
            {"codigo": "37", "descripcion": "Z.F. Sam-Li"},
            {"codigo": "38", "descripcion": "Z.F. San José"},
            {"codigo": "39", "descripcion": "Z.F. Las Mercedes"},
            {"codigo": "71", "descripcion": "Aldesa"},
            {"codigo": "72", "descripcion": "Agdosa Merliot"},
            {"codigo": "73", "descripcion": "Bodesa"},
            {"codigo": "76", "descripcion": "Delegación DHL"},
            {"codigo": "77", "descripcion": "Transauto"},
            {"codigo": "80", "descripcion": "Nejapa"},
            {"codigo": "81", "descripcion": "Almaconsa"},
            {"codigo": "83", "descripcion": "Agdosa Apopa"},
            {"codigo": "85", "descripcion": "Gutiérrez Courier Y Cargo"},
            {"codigo": "99", "descripcion": "San Bartolo Envío Hn/Gt"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-029 Tipo de persona
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoPersona, [
            {"codigo": "1", "descripcion": "Persona Natural"},
            {"codigo": "2", "descripcion": "Persona Jurídica"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-030 Transporte
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoTransporte, [
            {"codigo": "01", "descripcion": "Terrestre"},
            {"codigo": "02", "descripcion": "Marítimo"},
            {"codigo": "03", "descripcion": "Aéreo"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-032 Domicilio Fiscal
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoDomicilioFiscal, [
            {"codigo": "01", "descripcion": "Local propio"},
            {"codigo": "02", "descripcion": "Local arrendado"},
        ])

        # ═══════════════════════════════════════════════════════════
        # CAT-015 Tributos (principales)
        # ═══════════════════════════════════════════════════════════
        total += _bulk(TipoTributo, [
            {"codigo": "1", "descripcion": "Impuesto"},
            {"codigo": "2", "descripcion": "Tasa"},
            {"codigo": "3", "descripcion": "Contribución especial"},
        ])

        total += _bulk(TipoValor, [
            {"descripcion": "Porcentaje"},
            {"descripcion": "Valor fijo"},
        ], code_field="descripcion")

        # Tributo IVA 13%
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

        # ═══════════════════════════════════════════════════════════
        # CAT-019 Actividades Económicas (todas del PDF)
        # ═══════════════════════════════════════════════════════════
        actividades = [
            ("01111","Cultivo de cereales excepto arroz y para forrajes"),
            ("01112","Cultivo de legumbres"),
            ("01113","Cultivo de semillas oleaginosas"),
            ("01114","Cultivo de plantas para la preparación de semillas"),
            ("01119","Cultivo de otros cereales excepto arroz y forrajeros n.c.p."),
            ("01120","Cultivo de arroz"),
            ("01131","Cultivo de raíces y tubérculos"),
            ("01132","Cultivo de brotes, bulbos, vegetales tubérculos y cultivos similares"),
            ("01133","Cultivo hortícola de fruto"),
            ("01134","Cultivo de hortalizas de hoja y otras hortalizas ncp"),
            ("01140","Cultivo de caña de azúcar"),
            ("01150","Cultivo de tabaco"),
            ("01161","Cultivo de algodón"),
            ("01162","Cultivo de fibras vegetales excepto algodón"),
            ("01191","Cultivo de plantas no perennes para la producción de semillas y flores"),
            ("01192","Cultivo de cereales y pastos para la alimentación animal"),
            ("01199","Producción de cultivos no estacionales ncp"),
            ("01220","Cultivo de frutas tropicales"),
            ("01230","Cultivo de cítricos"),
            ("01240","Cultivo de frutas de pepita y hueso"),
            ("01251","Cultivo de frutas ncp"),
            ("01252","Cultivo de otros frutos y nueces de árboles y arbustos"),
            ("01260","Cultivo de frutos oleaginosos"),
            ("01271","Cultivo de café"),
            ("01272","Cultivo de plantas para la elaboración de bebidas excepto café"),
            ("01281","Cultivo de especias y aromáticas"),
            ("01282","Cultivo de plantas para la obtención de productos medicinales y farmacéuticos"),
            ("01291","Cultivo de árboles de hule (caucho) para la obtención de látex"),
            ("01292","Cultivo de plantas para la obtención de productos químicos y colorantes"),
            ("01299","Producción de cultivos perennes ncp"),
            ("01300","Propagación de plantas"),
            ("01301","Cultivo de plantas y flores ornamentales"),
            ("01410","Cría y engorde de ganado bovino"),
            ("01420","Cría de caballos y otros equinos"),
            ("01440","Cría de ovejas y cabras"),
            ("01450","Cría de cerdos"),
            ("01460","Cría de aves de corral y producción de huevos"),
            ("01491","Cría de abejas apicultura para la obtención de miel y otros productos apícolas"),
            ("01492","Cría de conejos"),
            ("01493","Cría de iguanas y garrobos"),
            ("01494","Cría de mariposas y otros insectos"),
            ("01499","Cría y obtención de productos animales n.c.p."),
            ("01500","Cultivo de productos agrícolas en combinación con la cría de animales"),
            ("01611","Servicios de maquinaria agrícola"),
            ("01612","Control de plagas"),
            ("01613","Servicios de riego"),
            ("01614","Servicios de contratación de mano de obra para la agricultura"),
            ("01619","Servicios agrícolas ncp"),
            ("01621","Actividades para mejorar la reproducción, el crecimiento y rendimiento de los animales y sus productos"),
            ("01622","Servicios de mano de obra pecuaria"),
            ("01629","Servicios pecuarios ncp"),
            ("01631","Labores post cosecha de preparación de los productos agrícolas para su comercialización o para la industria"),
            ("01632","Servicio de beneficio de café"),
            ("01633","Servicio de beneficiado de plantas textiles"),
            ("01640","Tratamiento de semillas para la propagación"),
            ("01700","Caza ordinaria y mediante trampas, repoblación de animales de caza y servicios conexos"),
            ("02100","Silvicultura y otras actividades forestales"),
            ("02200","Extracción de madera"),
            ("02300","Recolección de productos diferentes a la madera"),
            ("02400","Servicios de apoyo a la silvicultura"),
            ("03110","Pesca marítima de altura y costera"),
            ("03120","Pesca de agua dulce"),
            ("03210","Acuicultura marítima"),
            ("03220","Acuicultura de agua dulce"),
            ("03300","Servicios de apoyo a la pesca y acuicultura"),
            ("05100","Extracción de hulla"),
            ("05200","Extracción y aglomeración de lignito"),
            ("06100","Extracción de petróleo crudo"),
            ("06200","Extracción de gas natural"),
            ("10101","Servicio de rastros y mataderos de bovinos y porcinos"),
            ("10102","Matanza y procesamiento de bovinos y porcinos"),
            ("10103","Matanza y procesamientos de aves de corral"),
            ("10104","Elaboración y conservación de embutidos y tripas naturales"),
            ("10105","Servicios de conservación y empaque de carne"),
            ("10106","Elaboración y conservación de grasas y aceites animales"),
            ("10107","Servicios de molienda de carne"),
            ("10108","Elaboración de productos de carne ncp"),
            ("10201","Procesamiento y conservación de pescado, crustáceos y moluscos"),
            ("10209","Fabricación de productos de pescado ncp"),
            ("10301","Elaboración de jugos de frutas y hortalizas"),
            ("10302","Elaboración y envase de jaleas, mermeladas y frutas deshidratadas"),
            ("10309","Elaboración de productos de frutas y hortalizas n.c.p."),
            ("10401","Fabricación de aceites y grasas vegetales y animales comestibles"),
            ("10402","Fabricación de aceites y grasas vegetales y animales no comestibles"),
            ("10409","Servicio de maquilado de aceites"),
            ("10501","Fabricación de productos lácteos excepto sorbetes y quesos sustitutos"),
            ("10502","Fabricación de sorbetes y helados"),
            ("10503","Fabricación de quesos"),
            ("10611","Molienda de cereales"),
            ("10612","Elaboración de cereales para el desayuno y similares"),
            ("10613","Servicios de beneficiado de productos agrícolas ncp"),
            ("10621","Fabricación de almidón"),
            ("10628","Servicio de molienda de maíz húmedo molino para nixtamal"),
            ("10711","Elaboración de tortillas"),
            ("10712","Fabricación de pan, galletas y barquillos"),
            ("10713","Fabricación de repostería"),
            ("10721","Ingenios azucareros"),
            ("10722","Molienda de caña de azúcar para la elaboración de dulces"),
            ("10723","Elaboración de jarabes de azúcar y otros similares"),
            ("10724","Maquilado de azúcar de caña"),
            ("10730","Fabricación de cacao, chocolates y productos de confitería"),
            ("10740","Elaboración de macarrones, fideos, y productos farináceos similares"),
            ("10750","Elaboración de comidas y platos preparados para la reventa en establecimientos"),
            ("10791","Elaboración de productos de café"),
            ("10792","Elaboración de especias, sazonadores y condimentos"),
            ("10793","Elaboración de sopas, cremas y consomé"),
            ("10794","Fabricación de bocadillos tostados y/o fritos"),
            ("10799","Elaboración de productos alimenticios ncp"),
            ("10800","Elaboración de alimentos preparados para animales"),
            ("11012","Fabricación de aguardiente y licores"),
            ("11020","Elaboración de vinos"),
            ("11030","Fabricación de cerveza"),
            ("11041","Fabricación de aguas gaseosas"),
            ("11042","Fabricación y envasado de agua"),
            ("11043","Fabricación de refrescos"),
            ("11048","Maquilado de aguas gaseosas"),
            ("11049","Elaboración de bebidas no alcohólicas"),
            ("12000","Elaboración de productos de tabaco"),
            ("47110","Venta al por menor en almacenes no especializados"),
            ("47710","Venta al por menor de prendas de vestir"),
            ("56101","Restaurantes"),
            ("56102","Cafeterías"),
            ("62010","Programación informática"),
            ("62020","Consultoría de tecnología de información"),
            ("69200","Actividades de contabilidad y auditoría"),
            ("86100","Actividades de hospitales"),
            ("86200","Actividades de médicos y odontólogos"),
            ("96010","Lavado y limpieza de prendas de tela y de piel"),
            ("96020","Peluquería y otros tratamientos de belleza"),
        ]
        total += _bulk(ActividadEconomica, [
            {"codigo": c, "descripcion": d} for c, d in actividades
        ])

        self.stdout.write(self.style.SUCCESS(
            f"✅ Catálogos MH v1.1 cargados: {total} registros nuevos insertados."
        ))
