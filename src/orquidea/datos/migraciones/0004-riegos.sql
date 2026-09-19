CREATE TABLE riegos (
    id INTEGER PRIMARY KEY,
    ejemplar_id INTEGER NOT NULL REFERENCES ejemplares (id) ON DELETE CASCADE,
    fecha TEXT NOT NULL CHECK (fecha GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
);

CREATE INDEX riegos_por_ejemplar ON riegos (ejemplar_id, fecha);
