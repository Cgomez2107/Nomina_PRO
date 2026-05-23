import subprocess
import json
from pathlib import Path


def ejecutar_en_sandbox():
    result = subprocess.run(
        ["docker", "run", "--rm", "-v", "./:/app", "-w", "/app",
         "guardian-sandbox", "pytest", "--json-report"],
        capture_output=True, text=True
    )
    report_path = Path(".report.json")
    if not report_path.exists():
        return {"passed": 0, "failed": 0, "bugs_detectados": 0,
                "veredicto": "ERROR: No se generó .report.json"}

    data = json.loads(report_path.read_text(encoding="utf-8"))
    passed = data.get("passed", 0)
    failed = data.get("failed", 0)
    return {
        "passed": passed,
        "failed": failed,
        "bugs_detectados": failed,
        "veredicto": "APROBADO" if failed == 0 else "RECHAZADO",
    }


if __name__ == "__main__":
    resultado = ejecutar_en_sandbox()
    print(json.dumps(resultado, indent=2))
