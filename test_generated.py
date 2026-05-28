# test_generated.py
import pytest
from engine import liquidar_nomina, SalarioInvalidoError, HorasExtrasInvalidasError

def test_cp01():
    result = liquidar_nomina(salario_base=2000000, horas_extras_diurnas=0, horas_extras_nocturnas=0, vlr_hora=12500)
    assert result["total_devengado"] == 2000000
    assert result["descuento_salud"] == 80000
    assert result["descuento_pension"] == 80000
    assert result["auxilio_transporte"] == 162000
    assert result["neto_a_pagar"] == 2002000

def test_cp02():
    result = liquidar_nomina(salario_base=2600000, horas_extras_diurnas=0, horas_extras_nocturnas=0, vlr_hora=12500)
    assert result["auxilio_transporte"] == 162000

def test_cp03():
    result = liquidar_nomina(salario_base=3000000, horas_extras_diurnas=0, horas_extras_nocturnas=0, vlr_hora=12500)
    assert result["auxilio_transporte"] == 0

def test_cp04():
    result = liquidar_nomina(salario_base=1800000, horas_extras_diurnas=5, horas_extras_nocturnas=0, vlr_hora=12500)
    assert result["extras_diurnas"] == 78125
    assert result["total_devengado"] == 1878125

def test_cp05():
    result = liquidar_nomina(salario_base=1800000, horas_extras_diurnas=0, horas_extras_nocturnas=5, vlr_hora=12500)
    assert result["extras_nocturnas"] == 109375
    assert result["total_devengado"] == 1909375

def test_cp06():
    result = liquidar_nomina(salario_base=2200000, horas_extras_diurnas=3, horas_extras_nocturnas=2, vlr_hora=12500)
    assert result["extras_diurnas"] == 46875
    assert result["extras_nocturnas"] == 43750
    assert result["total_extras"] == 90625

def test_cp07():
    result = liquidar_nomina(salario_base=2500000, horas_extras_diurnas=0, horas_extras_nocturnas=0, vlr_hora=12500)
    assert result["descuento_salud"] == 100000

def test_cp08():
    result = liquidar_nomina(salario_base=2500000, horas_extras_diurnas=0, horas_extras_nocturnas=0, vlr_hora=12500)
    assert result["descuento_pension"] == 100000

def test_cp09():
    with pytest.raises(HorasExtrasInvalidasError):
        liquidar_nomina(salario_base=2000000, horas_extras_diurnas=-2, horas_extras_nocturnas=0, vlr_hora=12500)

def test_cp10():
    with pytest.raises(SalarioInvalidoError):
        liquidar_nomina(salario_base=1000000, horas_extras_diurnas=0, horas_extras_nocturnas=0, vlr_hora=12500)

def test_cp11():
    result = liquidar_nomina(salario_base=1300000, horas_extras_diurnas=0, horas_extras_nocturnas=0, vlr_hora=12500)
    assert result["total_devengado"] == 1300000
    assert result["descuento_salud"] == 52000
    assert result["descuento_pension"] == 52000
    assert result["auxilio_transporte"] == 162000
    assert result["neto_a_pagar"] == 1358000

def test_cp12():
    result = liquidar_nomina(salario_base=2500000, horas_extras_diurnas=40, horas_extras_nocturnas=30, vlr_hora=12500)
    assert result["extras_diurnas"] == 625000
    assert result["extras_nocturnas"] == 656250
    assert result["total_extras"] == 1281250
    assert result["total_devengado"] == 3781250
    assert result["neto_a_pagar"] == 3640750