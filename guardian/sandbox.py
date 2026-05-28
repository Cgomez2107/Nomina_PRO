# guardian/sandbox.py
import subprocess
import json
from pathlib import Path
import os

def auditar_sandbox() -> dict:
    print("[Sandbox] Lanzando contenedor Docker 'guardian-sandbox'...")
    ruta_proyecto = os.path.abspath(os.getcwd())

    comando_docker = [
        "docker", "run", "--rm",
        "-v", f"{ruta_proyecto}:/app",
        "-w", "/app",
        "-e", "PYTHONPATH=src",
        "guardian-sandbox", "pytest", "--json-report", "--json-report-file=.report.json", "test_generated.py"
    ]
    
    subprocess.run(comando_docker, capture_output=True, text=True)

    ruta_reporte = Path(".report.json")
    
    if not ruta_reporte.exists():
        return {
            "passed": 0, "failed": 0, "bugs_detectados": 1,
            "veredicto": "RECHAZADO"
        }

    datos = json.loads(ruta_reporte.read_text(encoding="utf-8"))
    summary = datos.get("summary", {})
    
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    
    # Criterios 5 y 6: Lógica del veredicto
    if failed == 0 and passed > 0:
        veredicto = "APROBADO"
        bugs_detectados = 0
    else:
        veredicto = "RECHAZADO"
        bugs_detectados = failed

    # Criterio 4: Retorna diccionario exacto
    return {
        "passed": passed,
        "failed": failed,
        "bugs_detectados": bugs_detectados,
        "veredicto": veredicto
    }

if __name__ == "__main__":
    resultado = auditar_sandbox()
    print("\n================ VEREDICTO AUDITABLE ================")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
    print("=====================================================")