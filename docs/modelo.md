# Cómo se relacionan las tablas

Usamos una **constelación de hechos** (también se llama esquema de galaxia). Es como un esquema estrella, pero con varias tablas de hechos que comparten las mismas tablas de descripción (dimensiones): quién, qué y cuándo.

Hay cuatro tablas de hechos. Cada una registra un tipo de evento y tiene su propio nivel de detalle:

| Hecho | Una fila es… | Se conecta con |
|---|---|---|
| Ventas (`transacciones`) | un producto que un cliente compró en una fecha | cliente, producto, fecha |
| Devoluciones | la devolución de una venta (como mucho una por venta) | la venta que se devuelve, cliente, fecha de devolución |
| Campañas (`campanas_marketing`) | un envío de campaña a un cliente | cliente, fecha de envío |
| Atención al cliente (`interacciones_crm`) | un contacto de un cliente con la empresa | cliente, fecha |

Las dimensiones son **clientes**, **productos** y **fecha**.

- Devoluciones llega al producto a través de la venta.
- Campañas y atención al cliente solo se conectan con el cliente, no con una venta. Por eso los datos no dicen qué campaña generó qué compra, y hay que deducirlo por las fechas (ver `DECISIONES.md`, decisión A1.2).

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
- Devoluciones trae también el código del cliente. Es un dato repetido: siempre coincide con el cliente de la venta (lo comprobamos en el notebook 01). En Power BI, la relación con clientes se hace a través de la venta, para no tener dos caminos.
- Las relaciones "uno a muchos" están comprobadas en el notebook 01, sección 6.
