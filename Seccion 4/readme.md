# Taller de Concurrencia: Sistema de Procesamiento de Videos

## Descripción General

Este proyecto implementa un sistema concurrente para el procesamiento de trabajos de video utilizando múltiples hilos. El sistema sigue el patrón **Productor-Consumidor**, donde varios clientes generan trabajos que son procesados por un conjunto de workers a través de una cola compartida con prioridad.

El objetivo es aplicar conceptos de:
- Concurrencia
- Sincronización de hilos
- Prevención de condiciones de carrera
- Diseño de sistemas concurrentes
- Patrones de diseño

---

## Arquitectura del Sistema

El sistema está compuesto por los siguientes componentes:

- **Clientes (Productores)**  
  Generan trabajos de video de manera concurrente.

- **Cola Prioritaria Compartida**  
  Gestiona los trabajos con prioridad y controla el acceso concurrente mediante sincronización.

- **Workers (Consumidores)**  
  Procesan los trabajos utilizando un pool de hilos.

---

## Política de Prioridad

El sistema implementa una política de prioridad:

- Los trabajos **Premium** tienen prioridad sobre los **Gratis**
- Para evitar starvation:
  - Se procesan máximo **3 trabajos Premium consecutivos**
  - Luego se fuerza la ejecución de un trabajo Gratis (si existe)

---

## Sincronización

Se utiliza `threading.Condition` para:

- Coordinar el acceso a la cola compartida
- Suspender workers cuando no hay trabajos
- Notificar cuando nuevos trabajos son agregados

Esto garantiza:

- Exclusión mutua
- Ausencia de condiciones de carrera
- Correcta coordinación entre hilos

---

## Configuración del Sistema

- **Clientes Premium:** 3  
- **Clientes Gratis:** 5  
- **Workers:** 3  
- Cada cliente genera entre **5 y 10 trabajos**

---

## 📦 Estructura del Proyecto

```
Seccion 4/
│
├── src/
│   ├── main.py
│   │
│   ├── modelo/
│   │   └── trabajo.py
│   │
│   ├── cola/
│   │   └── cola_prioridad.py
│   │
│   ├── clientes/
│   │   └── cliente.py
│   │
│   ├── workers/
│   │   └── worker.py
│   │
│   └── utils/
│       └── constantes.py
│
├── Arquitectura/
│   └── arquitectura.puml
|   |
|   └── diseño.png
|   |
|   └── especificaciones.md
│
└── README.md
```

---

## Ejecución

Desde la carpeta ```Sección 4```:

```bash
python .\main.py
```

---

## Patrones de Diseño Aplicados

### Productor-Consumidor
Los clientes generan trabajos (productores) y los workers los consumen desde una cola compartida.

---

### Monitor (Condition)
La cola compartida actúa como un monitor que encapsula tanto la sincronización como la lógica de acceso a los recursos.

---

### Thread Pool
Se utiliza un conjunto fijo de workers (3 hilos) para procesar los trabajos, evitando la creación excesiva de hilos.

---

### Strategy (Implícito)
La lógica de selección de trabajos (Premium vs Gratis) se implementa como una estrategia dinámica dentro de la cola.

---

## 🛑 Finalización del Sistema

El sistema finaliza cuando:

- Todos los clientes han generado sus trabajos
- Todos los trabajos han sido procesados

Esto se logra mediante:
- Un contador de trabajos pendientes
- Una señal de finalización que permite a los workers terminar correctamente

---

## Ejemplo de Salida

```
Cliente-Premium-1: Envió trabajo VIDEO-Cliente-Premium-1-0
Worker-1: Procesando VIDEO-Cliente-Premium-1-0 de Cliente-Premium-1
Worker-2: Procesando VIDEO-Cliente-Gratis-2-1 de Cliente-Gratis-2
...
--- Sistema finalizado ---
```

---

## Objetivos Cumplidos

- ✔ Implementación de concurrencia con hilos  
- ✔ Sincronización correcta sin race conditions  
- ✔ Manejo de prioridad entre tareas  
- ✔ Prevención de starvation  
- ✔ Uso de patrones de diseño  
- ✔ Arquitectura modular y mantenible  

---

## Autores

- Juan Pablo Sánchez Zapata 
- Tomás Marulanda Aristizabal

---

## Conclusión

Este proyecto demuestra cómo diseñar e implementar un sistema concurrente robusto, aplicando principios de sincronización y patrones de diseño para garantizar eficiencia, seguridad y equidad en el procesamiento de tareas.
