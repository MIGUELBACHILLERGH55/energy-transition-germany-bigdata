# Energy Transition Germany — Big Data Project

## Descripción general

Este proyecto tiene como objetivo analizar la transición energética de Alemania a partir de fuentes de datos energéticos oficiales y públicas, mediante el diseño e implementación de un pipeline ETL con **Apache Spark**.

El sistema permite extraer, transformar y estructurar datos energéticos reales para su posterior análisis, siguiendo una arquitectura **lakehouse** clara y mantenible.

Las fuentes utilizadas son organismos oficiales europeos y alemanes, garantizando la fiabilidad y trazabilidad de los datos.

---

## Fuentes de datos

### SMARD.de
Datos horarios del sistema eléctrico alemán (generación, demanda y precios).

### AGEB
Evaluation Tables of the Energy Balance for Germany (1990–2024).

> **Nota:** se utilizan únicamente las *evaluation tables*, no los balances energéticos históricos completos.

### OPSD (Open Power System Data)
Series temporales energéticas (2015–2020).

### EEA (European Environment Agency)
Emisiones nacionales de gases de efecto invernadero (1985–2023).

---

## Arquitectura del proyecto

El proyecto sigue una arquitectura **lakehouse**, separando claramente las responsabilidades por capas:

```
data/
├── landing/          # Datos originales descargados
│   ├── smard/
│   ├── ageb/
│   ├── opsd/
│   └── eea/
├── bronze/           # Datos raw materializados en Parquet
│   └── opsd/
└── silver/           # Datos transformados y limpios
    └── opsd/
```

---

## Capas del lakehouse

### Landing
Datos originales tal y como se descargan de las fuentes oficiales, sin modificaciones.

### Bronze
Persistencia de los datos en formato **Parquet** mediante Spark, sin aplicar lógica de negocio.

### Silver
Transformación y limpieza de los datos:
- Tipado correcto de columnas
- Normalización temporal
- Limpieza y estandarización
- Estructura preparada para análisis

---

## Requisitos del sistema

- Windows, macOS o Linux
- Acceso a internet
- **Java 11 o superior** (recomendado Java 17)

### Requisito obligatorio: Java

Apache Spark se ejecuta sobre la **Java Virtual Machine (JVM)**, por lo que Java es obligatorio aunque el entorno Python se gestione con Micromamba o Conda.

```bash
java -version
```

---

## Entorno de ejecución (Micromamba — recomendado)

```bash
micromamba create -f environment.yml
micromamba activate energy-trans-env
```

> Micromamba gestiona las dependencias de Python, pero **no instala Java**.

---

## Ejecución del proyecto (Makefile)

La ejecución del proyecto se gestiona exclusivamente mediante **make**, lo que garantiza reproducibilidad y simplicidad.

### Extracción de datos (Landing)

```bash
make extract-ageb
make extract-eea
make extract-opsd
```

O todas a la vez:

```bash
make bronze
```

### Limpieza y regeneración de Bronze

```bash
make refresh-bronze
```

### Transformación a Silver

```bash
make silver
```

O por fuente:

```bash
make transform-ageb
make transform-eea
make transform-opsd
```

### Limpieza de Silver

```bash
make clean-silver
```

---

## Estado actual del proyecto

**Versión:** v0.1.0

Incluye actualmente:
- Capa de extracción modular por fuente
- Capa Bronze funcional con Spark
- Pipelines de transformación a Silver
- Arquitectura desacoplada (extract / transform / IO)
- Orquestación completa mediante Makefile

---

## Autores

- **Tomás Morales**
- **Miguel Bachiller Segovia**
