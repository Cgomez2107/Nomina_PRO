from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

llm = OllamaLLM(model="llama3:8b")

engine_code = Path("src/engine.py").read_text(encoding="utf-8")
casos_prueba = Path("docs/casos_prueba.md").read_text(encoding="utf-8")

prompt = ChatPromptTemplate.from_template(
    "Actúa como un QA Engineer experto.\n\n"
    "### Código fuente (engine.py)\n{engine}\n\n"
    "### Matriz de casos de prueba\n{casos}\n\n"
    "Genera un archivo único de Pytest llamado test_generated.py "
    "que valide el engine contra todos los casos de la matriz. "
    "Usa exclusivamente assert y la librería pytest. "
    "No incluyas explicaciones, solo el código."
)

cadena = prompt | llm
output = cadena.invoke({"engine": engine_code, "casos": casos_prueba})

Path("test_generated.py").write_text(output, encoding="utf-8")
print("[Agent] test_generated.py generado correctamente.")
