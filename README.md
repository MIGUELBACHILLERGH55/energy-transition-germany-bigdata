# README — Energy Transition Germany (Big Data Project)

## Objetivo del proyecto

Este proyecto forma parte de la Unidad 3 — Adquisición de datos en Big Data.
El objetivo es extraer y organizar datos energéticos reales de Alemania para analizar la transición energética del país.

Se han utilizado dispositivos virtuales de adquisición de datos (fuentes oficiales y públicas):

- **SMARD.de** → datos horarios de generación, demanda y precios del sistema eléctrico en Alemania
- **AGEB** → balances energéticos históricos (1990–2024)
- **OPSD** → series temporales energéticas 2015–2020
- **EEA** → emisiones nacionales de gases de efecto invernadero (1985–2023)

---

## Arquitectura del proyecto

```bash
├── data
│   ├── landing
│   │   ├── smard
│   │   │   ├── indices_metadata_summaries
│   │   │   └── time_series_metadata_summaries
│   │   ├── ageb
│   │   ├── opsd
│   │   └── eea
└── src
    ├── extract
    ├── exploration
    ├── smard
    └── prototypes
        └── smard_prototype_extractor.py
```

La zona _landing_ almacena los datos originales tal cual se obtienen de la fuente.

---

## Ejecución del extractor

### 1. Crear un entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 2. Instalar dependencias del proyecto

```bash
pip install -r requirements.txt
```

(Alternativamente, instalar manualmente: `requests`

### 3. Configurar PYTHONPATH

Ejecutar desde la raíz del proyecto:

```bash
export PYTHONPATH=$(pwd)/src
```

### 4. Ejecutar el extractor SMARD

```bash
python3 -m extract.exploration.smard.prototypes.smard_prototype_extractor
```

---

## Salida generada

Los archivos JSON se guardarán en las siguientes rutas:

```
data/landing/smard/indices_metadata_summaries/
data/landing/smard/time_series_metadata_summaries/
```

---

## Código de extracción

Archivo principal:

```
src/extract/exploration/smard/prototypes/smard_prototype_extractor.py
```

El script explora índices y extrae una muestra inicial de datos utilizando funciones internas del proyecto.

---

## Seguridad y cumplimiento legal

| Fuente | Licencia                | Datos personales |
| ------ | ----------------------- | ---------------- |
| SMARD  | Datos públicos abiertos | No               |
| AGEB   | Datos abiertos          | No               |
| OPSD   | CC-BY                   | No               |
| EEA    | CC-BY 4.0               | No               |

- No se procesan datos personales
- Se respeta la integridad de los datos originales
- Los datos se almacenan en local

---

## Autores

- Tomás Morales
- Miguel Bachiller Segovia

Asignatura: Big Data – UA3 – Adquisición de Datos
Curso: 2025 / 2026

---
