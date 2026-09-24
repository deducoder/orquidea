---
name: parametros-de-regla-con-valor-al-abrir
description: cuando el entregable es una regla, el ADR fija los valores de los parámetros al abrirse, no solo sus nombres
metadata:
  type: feedback
---

El ciclo dice que el commit de `record-open` fija "the parameters of every rule". En s2, ADR-017 nombró los parámetros de la regla A ("qué tareas llevan pantallas de paso") pero no les dio valor. El valor ("formulario propio o confirmación") se fijó al elegir, después de ver lo que producía cada regla, y la regla A reprodujo exactamente las 9 pantallas de hoy.

**Why:** un valor fijado después de ver la salida es un parámetro ajustado al resultado. En la rejilla no se ve: sale igual que uno comprometido antes.
**How to apply:** al abrir el ADR de una regla, escribir cada valor candidato de cada parámetro como una opción de la rejilla (A con pasos / A sin pasos), no solo el nombre del parámetro. Ver [[screens-adr-antes-del-diseno]].
