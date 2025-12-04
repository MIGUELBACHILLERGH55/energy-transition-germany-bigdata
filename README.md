<<<<<<< HEAD
```text
data/
├── landing/          # Datos originales descargados
│   ├── smard/
│   ├── ageb/
│   ├── opsd/
│   └── eea/
├── bronze/           # Datos raw materializados en Parquet
│   └── opsd/
├── silver/           # Datos transformados y limpios
│   └── opsd/
```

### Capas del lakehouse

* **Landing**
  Datos originales tal y como se descargan de las fuentes oficiales.
  **Los archivos ya están incluidos en el repositorio. No es necesario añadir ni modificar datos.**

* **Bronze**
  Lectura de los datos con Spark y persistencia en formato Parquet, sin aplicar lógica de negocio.

* **Silver**
  Transformación de los datos:

  * Tipado correcto de columnas
  * Normalización de timestamps
  * Limpieza y estandarización de nombres
  * Estructura lista para análisis

---

## Requisitos del sistema

* Windows, macOS o Linux
* Acceso a internet
* **Java 11 o superior** (recomendado Java 17)

---

## Requisito obligatorio: Java (Apache Spark)

Este proyecto utiliza **Apache Spark**, el cual se ejecuta sobre la **Java Virtual Machine (JVM)**.
Por este motivo, **Java es un requisito obligatorio**, independientemente de que el entorno Python se gestione con Micromamba o Conda.

> Micromamba gestiona las dependencias de Python, pero **no instala ni configura Java del sistema**.

### Comprobar si Java está instalado

```bash
java -version
```

Si la versión es **11 o superior**, no es necesario instalar nada más.

---

### Instalación de Java (macOS — opción recomendada)

Si Java no está instalado o la versión es inferior a 11:

```bash
brew install openjdk@17
```

Añadir Java al `PATH` (solo una vez):

```bash
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Verificación:

```bash
java -version
=======
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
>>>>>>> a65b2ed (Add final README.md with project documentation)
```

---

<<<<<<< HEAD
## Instalación del entorno Python (Micromamba — recomendado)

Para simplificar la instalación y reducir dependencias, se recomienda **Micromamba**, una alternativa ligera a Conda.

### 1. Instalar Micromamba (macOS)

```bash
brew install micromamba
```

Inicializar Micromamba (solo la primera vez):

```bash
micromamba shell init -s zsh -p ~/micromamba
```

Cerrar y volver a abrir la terminal.

---

### 2. Crear el entorno del proyecto

Desde la raíz del repositorio:

```bash
micromamba create -f environment.yml
```

Se creará el entorno:

```text
energy-trans-env
=======
## Salida generada

Los archivos JSON se guardarán en las siguientes rutas:

```
data/landing/smard/indices_metadata_summaries/
data/landing/smard/time_series_metadata_summaries/
>>>>>>> a65b2ed (Add final README.md with project documentation)
```

---

<<<<<<< HEAD
### 3. Activar el entorno

```bash
micromamba activate energy-trans-env
```

---

## Instalación alternativa (Conda / Miniforge)

```bash
conda env create -f environment.yml
conda activate energy-trans-env
```

---

## Ejecución del pipeline ETL (OPSD)

Los datos de entrada **ya están incluidos** en:

```text
data/landing/opsd/
```

No es necesario descargar ni preparar archivos adicionales.

### Ejecutar el pipeline

```bash
python -m src.transform.sources.opsd.pipeline
```

---

## Resultados generados

El pipeline genera datasets en formato **Parquet**, siguiendo el comportamiento estándar de Spark.

### Capa Bronze

```text
data/bronze/opsd/timeseries_raw/
```

### Capa Silver

```text
data/silver/opsd/timeseries_hourly/
```

Durante la ejecución se muestran por consola:

* Ejemplos de registros (`df.show()`)
* Esquema del DataFrame (`df.printSchema()`)
* Validaciones básicas del proceso ETL

Esto permite observar claramente la evolución de los datos desde **Landing → Bronze → Silver**.

---

## Exploración de datos

La exploración se realiza mediante:

* Spark DataFrames
* Conversión puntual a pandas cuando es necesario

Incluye estadísticas descriptivas y ejemplos de análisis temporal, cumpliendo los requisitos de la asignatura.
=======
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
>>>>>>> a65b2ed (Add final README.md with project documentation)

---

## Autores

<<<<<<< HEAD
* **Tomás Morales**
* **Miguel Bachiller Segovia**

**Asignatura:** Big Data — Unidad 3 — Adquisición de Datos
**Curso:** 2025 / 2026

---

Si quieres, el siguiente paso natural sería:

* Una **nota al evaluador** explicando por qué esto es adquisición de datos
* Un **diagrama simple de la arquitectura ETL**
* O una revisión final con mentalidad de tribunal (qué mirarían para bajar nota)
=======
- Tomás Morales
- Miguel Bachiller Segovia

Asignatura: Big Data – UA3 – Adquisición de Datos
Curso: 2025 / 2026

---
>>>>>>> a65b2ed (Add final README.md with project documentation)
