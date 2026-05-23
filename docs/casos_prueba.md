# Matriz de Oráculo — Nómina Pro

**Autor:** Juan Sebastian Quijano Ramirez  
**Universidad:** Universidad Manuela Beltrán  
**Materia:** Patrones y Metodologías de Software  
**Fecha:** Mayo, 2026

## Reglas de Negocio (Contrato)

| Regla | Descripción |
|-------|-------------|
| **R1** | Recargo diurno: 25 % sobre el valor de la hora ordinaria. |
| **R2** | Recargo nocturno: 75 % sobre el valor de la hora ordinaria. |
| **R3** | Seguridad social: descontar 4 % salud + 4 % pensión sobre el total devengado (salario base + extras). |
| **R4** | Auxilio de transporte: sumar $162.000 solo si `salario_base ≤ $2.600.000`. |
| **R5** | Validaciones: lanzar `SalarioInvalidoError` si `salario_base < $1.300.000`; lanzar `HorasExtrasInvalidasError` si alguna cantidad de horas es negativa. |

## Escenarios de Prueba (Oráculo)

| ID | Regla(s) | Descripción | Entrada | Salida Esperada (claves del dict) |
|----|----------|-------------|---------|-----------------------------------|
| **CP-01** | R1, R3, R4 | Salario básico sin horas extras | `salario_base=2000000`, `horas_extras_diurnas=0`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `total_devengado=2000000`, `descuento_salud=80000`, `descuento_pension=80000`, `auxilio_transporte=162000`, `neto_a_pagar=2002000` |
| **CP-02** | R4 | Límite exacto de auxilio de transporte ($2.600.000) | `salario_base=2600000`, `horas_extras_diurnas=0`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `auxilio_transporte=162000` |
| **CP-03** | R4 | Salario supera el límite de auxilio | `salario_base=3000000`, `horas_extras_diurnas=0`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `auxilio_transporte=0` |
| **CP-04** | R1, R2 | Horas extras diurnas (5 horas) | `salario_base=1800000`, `horas_extras_diurnas=5`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `extras_diurnas=78125`, `total_devengado=1878125` |
| **CP-05** | R1, R2 | Horas extras nocturnas (5 horas) | `salario_base=1800000`, `horas_extras_diurnas=0`, `horas_extras_nocturnas=5`, `vlr_hora=12500` | `extras_nocturnas=109375`, `total_devengado=1909375` |
| **CP-06** | R1, R2 | Horas extras mixtas (3 diurnas + 2 nocturnas) | `salario_base=2200000`, `horas_extras_diurnas=3`, `horas_extras_nocturnas=2`, `vlr_hora=12500` | `extras_diurnas=46875`, `extras_nocturnas=43750`, `total_extras=90625` |
| **CP-07** | R3 | Descuento de salud al 4 % | `salario_base=2500000`, `horas_extras_diurnas=0`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `descuento_salud=100000` |
| **CP-08** | R3 | Descuento de pensión al 4 % | `salario_base=2500000`, `horas_extras_diurnas=0`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `descuento_pension=100000` |
| **CP-09** | R5 | Horas extras negativas | `salario_base=2000000`, `horas_extras_diurnas=-2`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `raise HorasExtrasInvalidasError` |
| **CP-10** | R5 | Salario inferior al SMMLV | `salario_base=1000000`, `horas_extras_diurnas=0`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `raise SalarioInvalidoError` |
| **CP-11** | R1, R3 | Salario mínimo legal ($1.300.000) sin extras | `salario_base=1300000`, `horas_extras_diurnas=0`, `horas_extras_nocturnas=0`, `vlr_hora=12500` | `total_devengado=1300000`, `descuento_salud=52000`, `descuento_pension=52000`, `auxilio_transporte=162000`, `neto_a_pagar=1358000` |
| **CP-12** | R1, R2 | Alto volumen de horas extras (40 diurnas + 30 nocturnas) | `salario_base=2500000`, `horas_extras_diurnas=40`, `horas_extras_nocturnas=30`, `vlr_hora=12500` | `extras_diurnas=625000`, `extras_nocturnas=656250`, `total_extras=1281250`, `total_devengado=3781250`, `neto_a_pagar=3640750` |

## Conclusión

La elaboración de los casos de prueba permitió validar de manera estructurada
las principales reglas de negocio del sistema de nómina. A través de los
diferentes escenarios planteados, fue posible comprobar el correcto
funcionamiento de cálculos relacionados con salario base, horas extras diurnas
y nocturnas, descuentos de salud y pensión, así como la aplicación del auxilio
de transporte según las condiciones establecidas.

Además, las pruebas incluyeron escenarios de validación y manejo de errores,
como el ingreso de valores negativos y salarios por debajo del mínimo legal,
garantizando que el sistema responda de forma segura y confiable ante entradas
inválidas o situaciones límite.

En conclusión, los casos de prueba diseñados contribuyen a asegurar la calidad,
estabilidad y confiabilidad del sistema, permitiendo detectar posibles fallos
antes de su implementación final y garantizando que el software cumpla
correctamente con los requisitos funcionales y las reglas de negocio definidas.
