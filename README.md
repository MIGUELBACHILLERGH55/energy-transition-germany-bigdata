# Energy Transition Germany — Big Data Project

## Objetivo del proyecto

Este proyecto forma parte de la **Unidad 3 — Adquisición de Datos** de la asignatura **Big Data**.

El objetivo es **diseñar e implementar un proceso ETL con Apache Spark** que permita **extraer, transformar y almacenar datos energéticos reales de Alemania**, con el fin de analizar distintos aspectos de la transición energética del país.

El proyecto sigue una **arquitectura lakehouse**, diferenciando claramente las fases de:

* Ingesta de datos (**Landing**)
* Materialización raw (**Bronze**)
* Transformación limpia y estructurada (**Silver**)

Las fuentes de datos utilizadas son **oficiales y públicas**, garantizando la fiabilidad del análisis.

---

## Repositorio del proyecto

Repositorio GitHub:

[https://github.com/MIGUELBACHILLERGH55/energy-transition-germany-bigdata.git](https://github.com/MIGUELBACHILLERGH55/energy-transition-germany-bigdata.git)

```bash
git clone https://github.com/MIGUELBACHILLERGH55/energy-transition-germany-bigdata.git
cd energy-transition-germany-bigdata
```

---

## Fuentes de datos

* **SMARD.de**
  Datos horarios de generación, demanda y precios del sistema eléctrico alemán.

* **AGEB**
  Balances energéticos históricos de Alemania (1990–2024).

* **OPSD (Open Power System Data)**
  Series temporales energéticas (2015–2020).

* **EEA (European Environment Agency)**
  Emisiones nacionales de gases de efecto invernadero (1985–2023).

---

## Arquitectura del proyecto

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
```

---

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
```

---

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

---

## Autores

* **Tomás Morales**
* **Miguel Bachiller Segovia**

**Asignatura:** Big Data — Unidad 3 — Adquisición de Datos
**Curso:** 2025 / 2026

---

Si quieres, el siguiente paso natural sería:

* Una **nota al evaluador** explicando por qué esto es adquisición de datos
* Un **diagrama simple de la arquitectura ETL**
* O una revisión final con mentalidad de tribunal (qué mirarían para bajar nota)
