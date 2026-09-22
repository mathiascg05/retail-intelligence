# Modelo relacional (esquema estrella)

`transacciones` es la tabla de hechos principal: una fila es un producto comprado por un cliente en una fecha. Alrededor están las dimensiones `clientes`, `productos` y fecha.

`devoluciones` cuelga de una transacción concreta (cada transacción tiene como mucho una devolución). `campanas_marketing` e `interacciones_crm` son eventos del cliente: solo tienen llave hacia `clientes`, no hacia una compra. Por eso la relación "esta campaña generó esta compra" no está en los datos y hay que inferirla por fechas (ver DECISIONES.md, #2).

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

Notas:

- `devoluciones.cliente_id` es redundante (siempre coincide con el cliente de la transacción; lo comprobamos en el notebook 01), pero lo dejamos porque viene en el archivo.
- La dimensión fecha no existe como archivo: se genera a partir de las fechas de las demás tablas.
- Cardinalidades comprobadas en `notebooks/01_calidad.ipynb`, sección 6.
