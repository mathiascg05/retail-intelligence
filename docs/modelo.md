# Cómo se relacionan las tablas

Usamos un esquema estrella: una tabla central con los hechos (las ventas) y, alrededor, las tablas que los describen (quién compró, qué compró y cuándo).

- **Ventas (`transacciones`)** es la tabla central. Cada fila es un producto que un cliente compró en una fecha.
- **Clientes, productos y fechas** son las tablas que describen cada venta.
- **Devoluciones** se conecta con una venta concreta. Cada venta tiene como máximo una devolución.
- **Campañas y atención al cliente** solo se conectan con el cliente, no con una venta. Por eso los datos no dicen qué campaña generó qué compra, y hay que deducirlo por las fechas (ver `DECISIONES.md`, decisión A1.2).

```mermaid
erDiagram
    CLIENTES ||--o{ TRANSACCIONES : compra
    PRODUCTOS ||--o{ TRANSACCIONES : "se vende en"
    FECHA ||--o{ TRANSACCIONES : fecha
    TRANSACCIONES ||--o| DEVOLUCIONES : "puede tener"
    CLIENTES ||--o{ CAMPANAS_MARKETING : recibe
    CLIENTES ||--o{ INTERACCIONES_CRM : contacta
    FECHA ||--o{ DEVOLUCIONES : fecha_devolucion
    FECHA ||--o{ CAMPANAS_MARKETING : fecha_envio
    FECHA ||--o{ INTERACCIONES_CRM : fecha

    CLIENTES {
        string cliente_id PK
        int edad
        string genero
        string ciudad
        string segmento
        date fecha_registro
        string canal_adquisicion
    }
    PRODUCTOS {
        string producto_id PK
        string nombre
        string categoria
        string subcategoria
        float costo
        float precio_lista
        float margen_bruto_pct
    }
    FECHA {
        date fecha PK
        int anio
        int trimestre
        int mes
    }
    TRANSACCIONES {
        string transaccion_id PK
        string cliente_id FK
        string producto_id FK
        date fecha FK
        int cantidad
        float precio_unitario
        float descuento
        float monto_neto
        string canal
        string metodo_pago
    }
    DEVOLUCIONES {
        string devolucion_id PK
        string transaccion_id FK
        string cliente_id FK
        string motivo
        float monto_devuelto
        date fecha_devolucion FK
    }
    CAMPANAS_MARKETING {
        string campana_id PK
        string cliente_id FK
        string tipo_campana
        date fecha_envio FK
        string canal_campana
        int abierto
        int convertido
        float descuento_ofrecido
    }
    INTERACCIONES_CRM {
        string interaccion_id PK
        string cliente_id FK
        string tipo
        date fecha FK
        string canal
        string resolucion
        float tiempo_respuesta_hrs
    }
```

## Notas

- La tabla de fechas no viene en los archivos. Se arma con las fechas de las demás tablas.
- Devoluciones trae también el código del cliente. Es un dato repetido: siempre coincide con el cliente de la venta (lo comprobamos en el notebook 01).
- Las relaciones "uno a muchos" están comprobadas en el notebook 01, sección 6.
