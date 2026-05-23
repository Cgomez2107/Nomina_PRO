"""
engine.py
=========
Motor de cálculo de nómina para la Universidad de Caldas (UdeC).

Este módulo expone la función principal `liquidar_nomina`, que aplica las
reglas de negocio colombianas vigentes para el cálculo del salario neto
de un empleado, incluyendo horas extras, descuentos de seguridad social y
auxilio de transporte.

Cumple con:
  - PEP-8
  - Python 3.11+
  - Tipado estricto mediante anotaciones nativas
  - Docstrings formato Google
  - Preparado para auditoría por agentes LLM (CrewAI / LangChain)

Author: Lead Developer – UdeC
Version: 1.0.0
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Constantes de negocio
# ---------------------------------------------------------------------------

# Salario Mínimo Mensual Legal Vigente (SMMLV 2024)
SMMLV: float = 1_300_000.0

# Tope salarial para aplicar auxilio de transporte (2 × SMMLV)
TOPE_AUXILIO_TRANSPORTE: float = 2 * SMMLV  # $2.600.000

# Valor del auxilio de transporte mensual (decreto 2024)
VALOR_AUXILIO_TRANSPORTE: float = 162_000.0

# Porcentaje de descuento por salud (empleado)
PORCENTAJE_SALUD: float = 0.04  # 4 %

# Porcentaje de descuento por pensión (empleado)
PORCENTAJE_PENSION: float = 0.04  # 4 %

# Recargo aplicado a horas extras diurnas (R1)
RECARGO_EXTRA_DIURNA: float = 1.25  # 25 % adicional

# Recargo aplicado a horas extras nocturnas (R2)
RECARGO_EXTRA_NOCTURNA: float = 1.75  # 75 % adicional


# ---------------------------------------------------------------------------
# Excepciones personalizadas
# ---------------------------------------------------------------------------


class SalarioInvalidoError(ValueError):
    """Se lanza cuando el salario base es inferior al SMMLV vigente.

    Hereda de ``ValueError`` para mantener compatibilidad semántica con la
    jerarquía estándar de excepciones de Python y facilitar el manejo en
    bloques ``except ValueError``.
    """


class HorasExtrasInvalidasError(ValueError):
    """Se lanza cuando alguna cantidad de horas extras es un valor negativo.

    Hereda de ``ValueError`` por la misma razón que ``SalarioInvalidoError``.
    """


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------


def liquidar_nomina(
    salario_base: float,
    horas_extras_diurnas: int,
    horas_extras_nocturnas: int,
    vlr_hora: float,
) -> dict:
    """Calcula la nómina neta de un empleado aplicando las reglas colombianas.

    Aplica, en orden, las siguientes reglas de negocio:
      - **R1** – Horas extras diurnas con recargo del 25 %.
      - **R2** – Horas extras nocturnas con recargo del 75 %.
      - **R3** – Descuentos de salud (4 %) y pensión (4 %) sobre el devengado.
      - **R4** – Auxilio de transporte si ``salario_base`` ≤ 2 SMMLV.
      - **R5** – Validaciones de entrada (salario mínimo y horas no negativas).

    Args:
        salario_base (float):
            Salario mensual acordado con el empleado, expresado en pesos
            colombianos (COP). Debe ser ≥ $1.300.000 (1 SMMLV).
        horas_extras_diurnas (int):
            Cantidad de horas extras trabajadas en jornada diurna (06:00–21:00).
            Debe ser un entero no negativo.
        horas_extras_nocturnas (int):
            Cantidad de horas extras trabajadas en jornada nocturna (21:00–06:00).
            Debe ser un entero no negativo.
        vlr_hora (float):
            Valor monetario de una hora ordinaria de trabajo, en COP.

    Returns:
        dict: Desglose completo de la liquidación con las siguientes llaves:

            - ``salario_base`` (float): Salario base del empleado.
            - ``extras_diurnas`` (float): Valor liquidado por horas extras diurnas.
            - ``extras_nocturnas`` (float): Valor liquidado por horas extras nocturnas.
            - ``total_extras`` (float): Suma de extras diurnas + nocturnas.
            - ``total_devengado`` (float): salario_base + total_extras (base de descuentos).
            - ``descuento_salud`` (float): Descuento del 4 % por salud.
            - ``descuento_pension`` (float): Descuento del 4 % por pensión.
            - ``total_descuentos`` (float): Suma de salud + pensión.
            - ``auxilio_transporte`` (float): $162.000 si aplica, de lo contrario $0.
            - ``neto_a_pagar`` (float): Valor final a transferir al empleado.

    Raises:
        SalarioInvalidoError:
            Si ``salario_base`` es estrictamente menor a $1.300.000 (1 SMMLV).
        HorasExtrasInvalidasError:
            Si ``horas_extras_diurnas`` o ``horas_extras_nocturnas`` son negativos.

    Example:
        >>> resultado = liquidar_nomina(
        ...     salario_base=2_000_000,
        ...     horas_extras_diurnas=10,
        ...     horas_extras_nocturnas=5,
        ...     vlr_hora=12_500,
        ... )
        >>> resultado["neto_a_pagar"]
        2_112_625.0
    """

    # ------------------------------------------------------------------
    # R5 – Validaciones de entrada
    # Se ejecutan ANTES de cualquier cálculo para garantizar que los datos
    # de entrada sean coherentes con las reglas de negocio colombianas.
    # ------------------------------------------------------------------

    # R5.1 – Salario base no puede ser inferior al SMMLV
    if salario_base < SMMLV:
        raise SalarioInvalidoError(
            f"El salario base (${salario_base:,.0f}) es inferior al SMMLV "
            f"vigente (${SMMLV:,.0f}). No es posible liquidar una nómina "
            "por debajo del salario mínimo legal."
        )

    # R5.2 – Las horas extras no pueden ser valores negativos
    if horas_extras_diurnas < 0 or horas_extras_nocturnas < 0:
        raise HorasExtrasInvalidasError(
            "Las horas extras no pueden ser negativas. "
            f"Recibido: diurnas={horas_extras_diurnas}, "
            f"nocturnas={horas_extras_nocturnas}."
        )

    # ------------------------------------------------------------------
    # R1 – Cálculo de horas extras diurnas
    # Artículo 168 del CST: el recargo es del 25 % sobre la hora ordinaria.
    # Fórmula: cantidad × (vlr_hora × 1.25)
    # ------------------------------------------------------------------
    extras_diurnas: float = horas_extras_diurnas * (vlr_hora * RECARGO_EXTRA_DIURNA)

    # ------------------------------------------------------------------
    # R2 – Cálculo de horas extras nocturnas
    # Artículo 168 del CST: el recargo es del 75 % sobre la hora ordinaria.
    # Fórmula: cantidad × (vlr_hora × 1.75)
    # ------------------------------------------------------------------
    extras_nocturnas: float = horas_extras_nocturnas * (vlr_hora * RECARGO_EXTRA_NOCTURNA)

    # Total de dinero generado por horas extras (diurnas + nocturnas)
    total_extras: float = extras_diurnas + extras_nocturnas

    # ------------------------------------------------------------------
    # R3 – Descuentos de Seguridad Social
    # La base de cotización es el total devengado (salario + extras).
    # El empleado aporta 4 % a salud y 4 % a pensión (Ley 100 de 1993).
    # ------------------------------------------------------------------

    # Base sobre la cual se aplican los descuentos de seguridad social
    total_devengado: float = salario_base + total_extras

    # Descuento por salud: 4 % del total devengado
    descuento_salud: float = total_devengado * PORCENTAJE_SALUD

    # Descuento por pensión: 4 % del total devengado
    descuento_pension: float = total_devengado * PORCENTAJE_PENSION

    # Suma total de deducciones obligatorias (salud + pensión)
    total_descuentos: float = descuento_salud + descuento_pension

    # ------------------------------------------------------------------
    # R4 – Auxilio de transporte
    # Decreto 2613 de 2023: aplica si el salario base NO supera 2 SMMLV
    # ($2.600.000). Este rubro no hace parte de la base de cotización.
    # ------------------------------------------------------------------
    auxilio_transporte: float = (
        VALOR_AUXILIO_TRANSPORTE if salario_base <= TOPE_AUXILIO_TRANSPORTE else 0.0
    )

    # ------------------------------------------------------------------
    # Cálculo del neto a pagar
    # Fórmula: total_devengado - total_descuentos + auxilio_transporte
    # ------------------------------------------------------------------
    neto_a_pagar: float = total_devengado - total_descuentos + auxilio_transporte

    # Diccionario de retorno con desglose completo para trazabilidad y auditoría
    return {
        "salario_base": salario_base,
        "extras_diurnas": extras_diurnas,
        "extras_nocturnas": extras_nocturnas,
        "total_extras": total_extras,
        "total_devengado": total_devengado,
        "descuento_salud": descuento_salud,
        "descuento_pension": descuento_pension,
        "total_descuentos": total_descuentos,
        "auxilio_transporte": auxilio_transporte,
        "neto_a_pagar": neto_a_pagar,
    }
