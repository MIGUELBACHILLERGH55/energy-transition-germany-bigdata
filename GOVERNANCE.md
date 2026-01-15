# GOVERNANCE.md  
## Políticas de gobernanza y control de versiones del proyecto

---

## 1. Repositorio y miembros del equipo

El proyecto se desarrolla en un repositorio único que centraliza el código fuente, la documentación y los artefactos generados durante el desarrollo.

**Miembros del equipo:**
- Tomás Morales
- Miguel Bachiller Segovia

El trabajo colaborativo se realiza mediante ramas individuales y Pull Requests hacia la rama principal.

---

## 2. Estructura y gestión de ramas

Se adopta la siguiente convención de ramas:

### Rama principal
- **main**  
  Rama estable del proyecto.  
  Contiene únicamente versiones revisadas y validadas.  
  No se permiten pushes directos.

### Ramas de trabajo
- **tomas-branch**
- **miguel-branch**

Cada miembro desarrolla su trabajo en su rama correspondiente y solicita la integración mediante Pull Requests.

Para desarrollos futuros se recomienda el uso de ramas con la siguiente nomenclatura:
- `feature/<descripcion>`
- `fix/<descripcion>`
- `docs/<descripcion>`

---

## 3. Convención de commits

A partir de la definición de este documento, los commits deberán ser descriptivos y seguir una convención basada en el tipo de cambio realizado:

- `feat:` nueva funcionalidad
- `fix:` corrección de errores
- `docs:` cambios de documentación
- `chore:` tareas de mantenimiento o refactor menor

Ejemplos:
- `feat: add OPSD silver transformation pipeline`
- `fix: handle null values in solar generation`
- `docs: add governance and contribution rules`

El historial previo a esta política no se modifica para preservar la trazabilidad del proyecto.

---

## 4. Pull Requests y revisión de código

Todos los cambios que afecten a la rama `main` deben integrarse mediante Pull Requests.

Reglas establecidas:
- No se permiten commits directos sobre `main`.
- Cada Pull Request debe ser revisado y aprobado por al menos un miembro del equipo distinto al autor.
- La revisión garantiza el cumplimiento de las normas del proyecto y la coherencia del código.

---

## 5. Versionado y etiquetado

El proyecto utiliza **versionado semántico (Semantic Versioning)**:

`vMAJOR.MINOR.PATCH`

Ejemplos:
- `v1.0.0`: primera versión estable
- `v1.0.1`: correcciones compatibles
- `v1.1.0`: nuevas funcionalidades compatibles

Las versiones estables se etiquetan en la rama `main` mediante tags en la plataforma de hosting.

---

## 6. Roles y responsabilidades

Los roles dentro del proyecto se definen de la siguiente manera:

- **Maintainer / Lead Developer – Tomás Morales**  
  Responsable del diseño de la arquitectura, desarrollo del proceso ETL y coordinación técnica del proyecto.

- **Developer / Analyst – Miguel Bachiller Segovia**  
  Responsable del análisis de datos, visualización y validación de resultados.

La gestión técnica de permisos en la plataforma de hosting se realiza por el propietario del repositorio, mientras que los roles anteriores definen las responsabilidades funcionales dentro del proyecto.

---

## 7. Ejecución del proyecto

Las instrucciones para la instalación del entorno, ejecución del pipeline ETL y estructura de los datos generados se encuentran documentadas en el archivo `README.md`.

