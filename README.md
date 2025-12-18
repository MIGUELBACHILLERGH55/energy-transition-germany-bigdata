# Energy Transition Germany — Big Data Project

## Objetivo del proyecto

Este proyecto forma parte de la **Unidad 3 — Adquisición de Datos** de la asignatura **Big Data**.

El objetivo principal es **diseñar e implementar un proceso ETL con Apache Spark**, capaz de **extraer, transformar y almacenar datos energéticos reales de Alemania** para analizar distintos aspectos de la transición energética del país.

El proyecto sigue una **arquitectura lakehouse**, separando claramente las fases de:

* **Ingesta de datos (Landing)**
* **Materialización raw (Bronze)**
* **Transformación limpia y estructurada (Silver)**

Las fuentes de datos utilizadas son **oficiales y públicas**, garantizando la fiabilidad del análisis.

---

## Fuentes de datos

Las fuentes utilizadas en el proyecto son:

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

La arquitectura está organizada por capas siguiendo buenas prácticas en Big Data:

```text
data/
├── landing/          # Datos originales tal y como se descargan
│   ├── smard/
│   ├── ageb/
│   ├── opsd/
│   └── eea/
├── bronze/           # Datos raw materializados en Parquet (Spark)
│   └── opsd/
├── silver/           # Datos limpios, tipados y enriquecidos
│   └── opsd/
```

### Capas del lakehouse

* **Landing**
  Datos originales en formatos CSV, Excel o JSON.

* **Bronze**
  Datos leídos con Spark y almacenados en formato Parquet, sin aplicar lógica de negocio.

* **Silver**
  Datos transformados:

  * Tipos de datos correctos
  * Timestamps normalizados
  * Columnas limpias y estructuradas

---

## Requisitos del sistema

* Sistema operativo: Windows, macOS o Linux
* Acceso a internet
* **Java 11 o superior** (recomendado Java 17)
* **Conda / Miniforge**

### Verificación rápida de Java

```bash
java -version
```

---

## Instalación del entorno

### 1. Instalar Miniforge

Descargar e instalar Miniforge desde:

[https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge)

Durante la instalación, aceptar las opciones por defecto.

---

### 2. Clonar el repositorio y abrir una terminal

```bash
cd energy-transition-germany-bigdata
```

---

### 3. Crear el entorno Conda

Desde la raíz del proyecto:

```bash
conda env create -f environment.yml
```

Esto creará el entorno `energy-trans-env` con todas las dependencias necesarias.

---

### 4. Activar el entorno

```bash
conda activate energy-trans-env
```

---

## Ejecución del pipeline OPSD (Spark ETL)

### Preparar los datos de entrada

El pipeline asume que los ficheros de OPSD se encuentran en:

```text
data/landing/opsd/
```

Ejemplo:

```text
data/landing/opsd/time_series_60min_singleindex.csv
```

El pipeline admite **uno o varios ficheros** dentro de esta carpeta.

---

### Ejecutar el pipeline

El pipeline de transformación de OPSD se encuentra en:

```text
src/transform/sources/opsd/pipeline.py
```

Para ejecutarlo:

```bash
python -m src.transform.sources.opsd.pipeline
```

---

## Resultados generados

Tras la ejecución se generan datasets en formato **Parquet**, siguiendo el comportamiento estándar de Spark (directorios con ficheros `part-*`).

### Bronze

```text
data/bronze/opsd/timeseries_raw/
```

### Silver

```text
data/silver/opsd/timeseries_hourly/
```

Durante la ejecución se muestran por consola:

* Ejemplos de datos (`df.show()`)
* Esquema del DataFrame (`df.printSchema()`)
* Validaciones básicas del proceso ETL

---

## Visualización y exploración

La exploración de los datos se realiza utilizando **Spark** y, en algunos casos, conversión a **pandas** para visualización básica.

Se incluyen:

* Estadísticas descriptivas
* Ejemplos de análisis temporal

Todo ello para cumplir con los requisitos de exploración establecidos en el enunciado.

---

## Autores

* **Tomás Morales**
* **Miguel Bachiller Segovia**

**Asignatura:** Big Data — Unidad 3 — Adquisición de Datos
**Curso:** 2025 / 2026

