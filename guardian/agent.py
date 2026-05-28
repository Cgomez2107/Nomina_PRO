# guardian/agent.py
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def ejecutar_agente():
    print("[Agent] Inicializando conexión local con Llama 3 (Ollama)...")
    llm = OllamaLLM(model="llama3", temperature=0.1)

    print("[Agent] Buscando y leyendo archivos (src/engine.py y docs/casos_prueba.md)...")
    try:
        engine_code = Path("src/engine.py").read_text(encoding="utf-8")
        casos_prueba = Path("docs/casos_prueba.md").read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"❌ Error: No se encontró el archivo - {e}")
        return

    prompt = ChatPromptTemplate.from_template(
        "Actúas como un QA Engineer experto.\n\n"
        "### Código fuente (src/engine.py)\n{engine}\n\n"
        "### Matriz del Oráculo (docs/casos_prueba.md)\n{casos}\n\n"
        "Genera un archivo único de Pytest llamado `test_generated.py` que valide todas las reglas R1 a R5.\n"
        "REGLAS OBLIGATORIAS:\n"
        "1. Importa la función exactamente así: `from engine import liquidar_nomina, SalarioInvalidoError, HorasExtrasInvalidasError`.\n"
        "2. Devuelve ÚNICAMENTE el bloque de código Python ejecutable dentro de comillas triples de markdown (```python ... ```).\n"
        "3. No incluyas explicaciones ni texto adicional."
    )

    cadena = prompt | llm
    
    print("[Agent] Enviando contexto a Llama 3. Generando código en tiempo real... ⏳\n")
    print("-" * 50) # Una línea separadora visual
    
    # En lugar de esperar todo el bloque, recibimos e imprimimos token por token
    output = ""
    for chunk in cadena.stream({"engine": engine_code, "casos": casos_prueba}):
        print(chunk, end="", flush=True)
        output += chunk
        
    print("\n" + "-" * 50)
    print("\n[Agent] ¡Generación terminada! Limpiando el código...")

    # Limpieza estricta de la salida
    codigo_limpio = output
    if "```python" in output:
        codigo_limpio = output.split("```python")[1].split("```")[0].strip()
    elif "```" in output:
        codigo_limpio = output.split("```")[1].split("```")[0].strip()

    print("[Agent] Guardando el archivo test_generated.py en la raíz...")
    Path("test_generated.py").write_text(codigo_limpio, encoding="utf-8")
    print("✅ [Agent] Archivo generado exitosamente. ¡Proceso completado!")

if __name__ == "__main__":
    ejecutar_agente()