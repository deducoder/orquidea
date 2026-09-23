---
name: verificar-el-efecto-en-el-render
description: Una prueba de CSS que revisa una propiedad no ve el efecto de otra; una decisión visual se confirma también en una captura
metadata:
  type: feedback
---

Una prueba que afirma la forma de una regla (sin `padding`) no prueba el efecto buscado (el texto alineado): otra propiedad puede producir el mismo defecto.

**Why:** en s1 (2026-09-23) la prueba de la sangría de `.accion` pasaba sin relleno, pero `justify-content: center` dentro del objetivo de 48 px seguía sangrando «Ficha» 6 px. Solo se vio en la captura a 360 px con datos reales, y costó un `fix` aparte (`4ff62f3`).
**How to apply:** tras aplicar un ajuste visual, capturar la página real (ver [[captura-360-en-chrome-de-windows]]) y mirarla antes del siguiente paso; al escribir la prueba, listar las propiedades que producen el mismo efecto. Ver [[afirmar-presencia-no-ve-el-lugar]].
