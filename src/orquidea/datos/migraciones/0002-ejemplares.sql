CREATE TABLE ejemplares (
    id INTEGER PRIMARY KEY,
    especie_id TEXT,
    nombre TEXT NOT NULL DEFAULT '',
    notas TEXT NOT NULL DEFAULT '',
    creado INTEGER NOT NULL,
    CHECK (especie_id IS NOT NULL OR length(trim(nombre)) > 0)
);
