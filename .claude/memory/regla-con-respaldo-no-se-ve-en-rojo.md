---
name: regla-con-respaldo-no-se-ve-en-rojo
description: Una regla de la técnica ui con "si no cumple, toma el escalón que cumpla" nunca se ve en rojo; fijar respaldo ninguno al abrir el ADR
metadata:
  type: feedback
---

En s5.5 (2026-09-22) el diseño proponía que `campo-borde` cayera "al escalón más cercano que llegue a 3:1" si su escalón no llegaba. Con ese respaldo, la regla (B) uniforme en OKLCH habría salido verde, y el rojo real (`campo-borde` sobre `fondo` 2.76:1, `texto-secundario` 6.86:1) no se habría visto. ADR-013 fijó "Respaldo: ninguno" antes de correr las reglas.

**Why:** el paso `counterexample` del ciclo exige ver fallar cada criterio medible. Un respaldo automático convierte cualquier regla en verde y esconde el defecto que la regla causa.

**How to apply:** en s5.6 (escala, espaciado, componentes), al abrir el ADR declarar como parámetro qué pasa cuando un valor no llega a su umbral. Por omisión, la regla queda en rojo, y el ajuste va a otra candidata o a un rol fijado, nunca a un desplazamiento automático. Ver [[poblacion-no-cuenta-lo-que-no-es-sujeto]].
