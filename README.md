readme_content = """# ⬢ TecnoParking Colmena ⬢

**TecnoParking Colmena** es un sistema de parqueo automatizado basado en una estructura modular hexagonal. Diseñado para optimizar el espacio urbano, este proyecto integra una solución de software con una visión de ingeniería estructural para resolver la crisis de movilidad y falta de estacionamiento en zonas de alta densidad.

---

## 🚀 El Proyecto y Modelo de Negocio

El problema actual de las ciudades radica en parquear en dos dimensiones en un mundo tridimensional. Tecnoparking propone una **estructura hexagonal (panal)** que elimina rampas y pasillos de maniobra, maximizando la capacidad del terreno.

### 💼 Viabilidad y Rentabilidad
- **Alta densidad por m²:** Triplica la capacidad de almacenamiento de vehículos en la misma huella de terreno en comparación con un parqueadero tradicional.
- **Reducción de costos operativos:** Automatización total del ingreso y salida, eliminando la necesidad de personal logístico o acomodadores en cada piso.
- **Flujo de caja automatizado:** Facturación exacta por tiempo mediante el cálculo de horas, con tarifas base de $4,000/h (Carros) y $2,000/h (Motos).

### 🌍 Impacto Integral
- **Ambiental:** Reducción drástica (hasta un 80%) de emisiones de CO2 al eliminar el tiempo de ralentí y búsqueda de parqueo de los vehículos.
- **Social:** Al compactar el área requerida para parqueo, se libera suelo urbano que puede ser devuelto a la comunidad en forma de parques, ciclorrutas y recuperación del espacio público.
- **Económico (Usuario):** Ahorro directo de tiempo (cero búsquedas de parqueo), ahorro de combustible y protección total del vehículo contra rayones y robos.

---

## 💻 Arquitectura del Software

El cerebro del sistema está desarrollado en **Python** con una interfaz gráfica en **Tkinter**.

### Características Técnicas del Código:
1. **Terminal Automática (Modo Usuario):** Interfaz rápida para el registro de vehículos con validación estricta de seguridad (cédulas únicamente numéricas y de máximo 10 dígitos).
2. **Panel de Control (Modo Admin):** Acceso restringido (protegido por clave) para auditar celdas activas y descargar reportes diarios completos de ingresos/salidas.
3. **Persistencia de Datos (Archivos Planos):** Uso eficiente de operaciones de lectura/escritura en archivos `.txt` (`tecnoparking_activos.txt` y `tecnoparking_historial.txt`) para mantener el estado del sistema en tiempo real y tener trazabilidad.
4. **Ciclo de Ejecución Manual:** Implementación de un ciclo `while True` personalizado con `root.update()` (requisito técnico), reemplazando el `mainloop()` tradicional de Tkinter para un control de refresco manual.

---

## 🛠️ Instalación y Uso

1. **Clonar el repositorio:**
