# Energy Transition Germany — Big Data Project

## Descripción general

Este proyecto analiza la transición energética de Alemania a partir de fuentes oficiales y públicas, mediante el diseño e implementación de un pipeline ETL completo con Apache Spark.

El sistema cubre todo el flujo de datos, desde la extracción hasta la generación de datasets analíticos listos para herramientas de BI, siguiendo una arquitectura lakehouse clara, reproducible y mantenible.

Las fuentes utilizadas son organismos oficiales europeos y alemanes, lo que garantiza fiabilidad, trazabilidad y rigor en los datos.

---

## Fuentes de datos

SMARD.de
Datos horarios del sistema eléctrico alemán:

* generación eléctrica
* demanda (load)
* precios de electricidad

Fuente accesible vía API.

AGEB
Evaluation Tables of the Energy Balance for Germany (1990–2024).

* Datos estructurales del sistema energético alemán
* Consumo final, mix energético, intensidad energética

Nota: se utilizan exclusivamente las evaluation tables, no los balances energéticos históricos completos.
Fuente de tipo archivo (file).

Eurostat
Indicadores energéticos y económicos a nivel europeo:

* índices de precios al consumidor relacionados con la energía
* datos estandarizados y comparables a nivel UE

Fuente de tipo archivo (file).

OPSD (Open Power System Data)
Series temporales energéticas:

* generación y demanda eléctrica
* datos históricos consolidados (2015–2020)

Fuente de tipo archivo (file).

EEA (European Environment Agency)
Emisiones nacionales de gases de efecto invernadero:

* series anuales oficiales
* cobertura temporal 1985–2023

Fuente de tipo archivo (file).

---

## Resumen de fuentes

* Total de fuentes de datos: 5
* Fuentes tipo archivo (file): AGEB, Eurostat, OPSD, EEA
* Fuentes tipo API: SMARD

---

## Arquitectura del proyecto

El proyecto sigue una arquitectura lakehouse, separando claramente las responsabilidades por capas:

```
data/
├── landing/          # Datos originales descargados
│   ├── smard/
│   ├── ageb/
│   ├── eurostat/
│   ├── opsd/
│   └── eea/
├── bronze/           # Datos raw materializados en Parquet
├── silver/           # Datos transformados y normalizados
└── gold/             # Datasets analíticos listos para BI
```

---

## Capas del lakehouse

Landing
Datos originales tal y como se descargan de las fuentes oficiales, sin modificaciones.

Bronze
Persistencia de los datos en formato Parquet mediante Spark, sin aplicar lógica de negocio.
Objetivo: reproducibilidad, trazabilidad y separación clara respecto a las fuentes originales.

Silver
Transformación y limpieza de los datos:

* tipado correcto de columnas
* normalización temporal
* limpieza y estandarización
* estructura consistente por fuente

Esta capa sirve como base estable para análisis posteriores.

Gold
Capa analítica final, orientada a consumo directo en BI y análisis exploratorio.

Incluye datasets sobre mix energético, precios, renovables, consumo final, perfiles diarios y contexto del cierre nuclear alemán.

Todos los datasets Gold:

* están en formato long
* tienen tipado temporal consistente
* incluyen unidades explícitas
* son reproducibles mediante Makefile

---

## Datasets Gold (capa analítica)

La siguiente tabla resume los datasets finales generados en la capa Gold.

| Dataset                            | Fuente principal | Frecuencia         | Contenido       | Descripción                                                          |
| ---------------------------------- | ---------------- | ------------------ | --------------- | -------------------------------------------------------------------- |
| energy_mix_total                   | AGEB             | Anual              | Energía, share  | Mix energético total de Alemania y participación relativa por fuente |
| energy_intensity_indicators        | AGEB             | Anual              | Indicadores     | Indicadores de intensidad energética agregados                       |
| final_energy_consumption_by_sector | AGEB             | Anual              | Energía, share  | Consumo final de energía por sector económico                        |
| renewables_by_technology           | AGEB             | Anual              | Energía         | Producción renovable desagregada por tecnología                      |
| daily_electricity_profile          | OPSD             | Diario             | Energía, ratios | Perfil diario de carga, generación renovable y cuotas                |
| latest_energy_day                  | SMARD            | Horaria (snapshot) | Load, price     | Último día completo disponible del sistema eléctrico alemán          |
| electricity_price_trends_monthly   | SMARD / Eurostat | Mensual            | Precio          | Tendencias mensuales de precios eléctricos                           |
| nuclear_exit_context_monthly       | SMARD            | Mensual            | Energía         | Contexto temporal del cierre nuclear (pre / post phase-out)          |

---

## Requisitos del sistema

* Windows, macOS o Linux
* Acceso a internet
* Java 11 o superior (recomendado Java 17)

Apache Spark se ejecuta sobre la Java Virtual Machine (JVM), por lo que Java es obligatorio incluso si el entorno Python se gestiona con Micromamba o Conda.

```
java -version
```

---

## Entorno de ejecución (Micromamba recomendado)

```
micromamba create -f environment.yml
micromamba activate energy-trans-env
```

Micromamba gestiona las dependencias de Python, pero no instala Java.

---

## Ejecución del proyecto (Makefile)

La ejecución del proyecto se gestiona exclusivamente mediante make, garantizando reproducibilidad y simplicidad.

Extracción de datos (Landing)

```
make extract-ageb
make extract-eea
make extract-opsd
make extract-eurostat
```

O todas a la vez:

```
make bronze
```

Regeneración de Bronze

```
make refresh-bronze
```

Transformación a Silver

```
make silver
```

O por fuente:

```
make transform-ageb
make transform-eea
make transform-opsd
make transform-smard
make transform-eurostat
```

Generación de Gold

```
make gold
```

O datasets individuales:

```
make gold-energy-mix-total
make gold-electricity-price-trends-monthly
make gold-nuclear-exit-context-monthly
```

Rebuild completo desde cero

```
make refresh-all
```

---

## Estado del proyecto

Versión actual: v1.0.0

La versión 1.0.0 marca un primer release estable que incluye:

* pipeline ETL completo (extract → bronze → silver → gold)
* capa Gold estable y reproducible
* datasets analíticos listos para BI
* normalización temporal consistente
* orquestación completa mediante Makefile

A partir de esta versión, el proyecto evoluciona de forma incremental.

---

## Autores

Tomás Morales
Miguel Bachiller Segovia
