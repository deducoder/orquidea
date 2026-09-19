CREATE TABLE sesiones (
    id_hash TEXT PRIMARY KEY,
    csrf TEXT NOT NULL,
    creada INTEGER NOT NULL,
    ultima_actividad INTEGER NOT NULL
);
