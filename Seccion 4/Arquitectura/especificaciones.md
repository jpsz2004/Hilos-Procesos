## Arquitectura del Sistema (Definición Profesional)

### Descripción General

El sistema propuesto implementa un modelo concurrente basado en el patrón **Productor-Consumidor**, donde múltiples clientes generan trabajos de procesamiento de video que son gestionados por una cola compartida con prioridad y consumidos por un conjunto de workers.

La arquitectura está diseñada para:

- Garantizar acceso seguro a recursos compartidos  
- Priorizar trabajos de clientes Premium  
- Evitar la inanición (starvation) de clientes Gratuitos  
- Permitir ejecución concurrente eficiente mediante hilos  

---

## Componentes Principales

### 1. Clientes (Productores)

- Representados como hilos independientes  

**Tipos:**
- 3 clientes Premium  
- 5 clientes Gratuitos  

**Responsabilidad:**
- Generar entre 5 y 10 trabajos  
- Enviar trabajos a la cola compartida  

---

### 2. Cola Prioritaria (Componente Central)

Encargada de:

- Gestionar dos colas internas:
  - `premium_queue`
  - `free_queue`
- Controlar acceso concurrente mediante `threading.Condition`
- Implementar política de prioridad:
  - Premium > Gratis
- Prevenir starvation mediante un mecanismo de fairness:
  - Máximo 3 trabajos Premium consecutivos antes de forzar uno Gratuito  

---

### 3. Workers (Consumidores)

- Pool de 3 hilos  

**Responsabilidad:**
- Obtener trabajos de la cola  
- Procesarlos (simulación con `sleep`)  
- Delegar la lógica de prioridad a la cola  

---

### 4. Modelo de Trabajo

Cada trabajo contiene:

- Identificador (ej: `VIDEO-A`, `VIDEO-B`)  
- Tipo de cliente (Premium / Gratis)  
- Cliente origen  

---

## Mecanismo de Sincronización

Se utiliza `threading.Condition` para:

- Coordinar acceso a la cola compartida  
- Permitir que los workers esperen cuando no hay trabajos  
- Notificar a los workers cuando nuevos trabajos son añadidos  

Esto evita:

- Condiciones de carrera  
- Accesos concurrentes no controlados  

---

## Política de Prioridad y Fairness

Se implementa una estrategia híbrida:

- Los trabajos Premium tienen prioridad  
- Se mantiene un contador de ejecuciones consecutivas Premium  

Después de 3 ejecuciones Premium:
- Se fuerza la ejecución de un trabajo Gratuito (si existe)  

Esto garantiza:

- Alta prioridad para Premium  
- Ausencia de starvation para Gratis  

---

## Finalización del Sistema

El sistema finaliza cuando:

- Todos los clientes han generado sus trabajos  
- Todos los trabajos han sido procesados  

Se utiliza un contador global de trabajos pendientes para determinar cuándo los workers deben terminar su ejecución.

---

## Patrones de Diseño Aplicados

- **Productor-Consumidor** → Clientes producen, workers consumen  
- **Thread Pool** → Workers reutilizados  
- **Monitor (Condition)** → Control de concurrencia  
- **Estrategia de priorización (implícita)** → Lógica de selección de trabajos  