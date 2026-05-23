# Quality Guardian — Nómina Pro

Sistema de IA Agéntica local para validación automatizada de nómina.
Basado en COIL (UdeC × UMB), 100% open source.

## Flujo Agéntico

1. **Construir sandbox** → `docker build -t guardian-sandbox .`
2. **Generar tests con IA** → `python guardian/agent.py`
3. **Ejecutar oráculo** → `python guardian/sandbox.py`

## Stack

- Python 3.11+
- Ollama + Llama 3 (8B)
- LangChain
- Pytest
- Docker

## Comandos

```bash
# 1. Construir la imagen de Docker
docker build -t guardian-sandbox .

# 2. Ejecutar el agente de IA
python guardian/agent.py

# 3. Ejecutar el sandbox
python guardian/sandbox.py
```
