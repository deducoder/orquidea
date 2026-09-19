# PRD: Orquídea

What the product must do. One requirement per `RF-XX`, observable and testable.

### RF-01: Catálogo cargado desde JSON con esquema

El catálogo de especies nativas de Chiapas vive en archivos JSON versionados en
el repositorio y lo mantiene el equipo desde código. Existe un esquema que
define la forma de una especie (incluida al menos una fuente, ver
`must-data-001`). Al cargar, un archivo que no cumple el esquema se rechaza con
un error que señala el archivo y el campo; nunca se carga a medias ni falla en
silencio.

### RF-02: Explorar y buscar en el catálogo

El usuario recorre el catálogo y busca especies por nombre científico o nombre
común; la búsqueda devuelve las especies cuyo nombre coincide, sin distinguir
mayúsculas ni acentos.

### RF-03: Ficha de especie

Cada especie tiene una ficha con su información general y sus cuidados
técnicos: luz, riego, temperatura y sustrato, junto con la fuente de cada dato.

### RF-04: Ejemplares en mi colección

El usuario agrega a su colección un ejemplar, ligado a una especie del catálogo
o sin especie de catálogo (con nombre y notas); lo edita y lo quita. Puede
haber varios ejemplares de la misma especie, y cada uno es independiente.

### RF-05: Foto del ejemplar

El usuario sube una foto de cada ejemplar de su colección y la ve en su ficha y,
en miniatura, en las listas.

### RF-06: Registro de riegos

El usuario registra riegos por ejemplar (fecha) y ve su historial y la fecha
del último riego.

### RF-07: Registro de floraciones

El usuario registra floraciones por ejemplar (fecha de inicio y, opcionalmente,
de fin) y ve su historial.

### RF-08: Un solo usuario con contraseña

La aplicación tiene un único usuario. El acceso está protegido con contraseña;
no hay registro ni varias cuentas. La colección se guarda en el servidor de la
aplicación.
