-- =====================================================================
-- Inventario Tienda de Tecnología - Script de base de datos
-- =====================================================================
-- Ejecutar este script conectado al servidor de PostgreSQL.
-- La creación de la base de datos debe hacerse estando conectado a
-- otra base (por ejemplo "postgres"); el resto del script debe
-- ejecutarse ya conectado a "inventario_db".
-- =====================================================================

-- 1) Crear la base de datos
CREATE DATABASE inventario_db;

-- -----------------------------------------------------------------------
-- A partir de aquí, conectarse a inventario_db:
--   psql -U postgres -d inventario_db -f database/schema.sql
-- (o ejecutar el bloque de abajo manualmente ya conectado a inventario_db)
-- -----------------------------------------------------------------------

-- 2) Crear la tabla productos
CREATE TABLE IF NOT EXISTS productos (
    id          SERIAL PRIMARY KEY,
    codigo      VARCHAR(20)    NOT NULL UNIQUE,
    nombre      VARCHAR(100)   NOT NULL,
    categoria   VARCHAR(50)    NOT NULL,
    precio      NUMERIC(10, 2) NOT NULL CHECK (precio >= 0),
    existencia  INTEGER        NOT NULL CHECK (existencia >= 0),
    activo      BOOLEAN        NOT NULL DEFAULT TRUE
);

-- Índices de apoyo para la búsqueda por código, nombre y categoría
CREATE INDEX IF NOT EXISTS idx_productos_codigo    ON productos (codigo);
CREATE INDEX IF NOT EXISTS idx_productos_nombre    ON productos (nombre);
CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos (categoria);

-- 3) Datos de prueba (al menos 5 productos, en 2 o más categorías)
INSERT INTO productos (codigo, nombre, categoria, precio, existencia, activo) VALUES
    ('TEC-001', 'Mouse inalámbrico Logitech M185',      'Periféricos',    89.99,  45, TRUE),
    ('TEC-002', 'Teclado mecánico Redragon K552',        'Periféricos',   249.50,  20, TRUE),
    ('TEC-003', 'Memoria RAM Kingston Fury 8GB DDR4',     'Componentes',   210.00,  15, TRUE),
    ('TEC-004', 'Disco SSD Kingston A400 480GB',          'Almacenamiento',320.75,  12, TRUE),
    ('TEC-005', 'Monitor LG 21.5" Full HD',                'Monitores',    899.00,   8, TRUE),
    ('TEC-006', 'Audífonos HyperX Cloud Stinger',          'Periféricos',   275.00,   0, FALSE),
    ('TEC-007', 'Procesador AMD Ryzen 5 5600G',            'Componentes',   950.00,   6, TRUE)
ON CONFLICT (codigo) DO NOTHING;
