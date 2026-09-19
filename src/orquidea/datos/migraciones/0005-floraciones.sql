CREATE TABLE floraciones (
    id INTEGER PRIMARY KEY,
    ejemplar_id INTEGER NOT NULL REFERENCES ejemplares (id) ON DELETE CASCADE,
    inicio TEXT NOT NULL CHECK (inicio GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    fin TEXT CHECK (fin GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    CHECK (fin IS NULL OR fin >= inicio)
);

CREATE INDEX floraciones_por_ejemplar ON floraciones (ejemplar_id, inicio);
