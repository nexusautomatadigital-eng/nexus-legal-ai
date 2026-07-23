# Architectural Decisions

---

## DEC-001

El Dashboard nunca ejecutará SQL directamente.

Toda consulta deberá pasar por Repository.

Estado:

Aceptada

---

## DEC-002

Toda la lógica de negocio deberá implementarse mediante Domain Services.

La UI únicamente consume servicios.

Estado:

Aceptada

---

## DEC-003

PriorityEngine dependerá únicamente del modelo Proceso.

La consulta de datos permanecerá fuera del Engine.

Estado:

Aceptada

---

## DEC-004

SessionService será la única fuente oficial del contexto del usuario autenticado.

Queda prohibido acceder directamente a st.session_state desde los componentes del dominio.

Estado:

Aceptada

Aquí registraremos decisiones como:

Congelar la V1.
Construir la V2 en paralelo.
La Home no tendrá scroll.
El Dashboard se convierte en Command Center.

Esto evitará volver a debatir decisiones ya tomadas.