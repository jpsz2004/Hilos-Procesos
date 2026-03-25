# SECCIÓN 2: Análisis de Código

---

## 1. El Cajero Automático

### Problemas identificados:
- Acceso concurrente a la variable compartida `saldo_cuenta` sin ningún mecanismo de sincronización.
- Presencia de una condición de carrera (race condition) en la verificación y actualización del saldo.
- La operación de retiro (verificar saldo + descontar dinero) no es atómica.
- Uso de `time.sleep()` que incrementa la probabilidad de interleaving entre hilos.
- Múltiples hilos pueden leer el mismo saldo antes de que este sea actualizado.

### Riesgos:
- Inconsistencia en los datos (saldo incorrecto o negativo).
- Posibilidad de que múltiples clientes retiren dinero simultáneamente aunque el saldo no sea suficiente.
- Resultados no deterministas (el resultado puede variar en cada ejecución).
- Violación de la integridad del sistema (dinero "creado" o "perdido").
- Problemas críticos en sistemas reales como banca o transacciones financieras.

### Propuesta de corrección:
Se debe proteger la sección crítica utilizando un mecanismo de exclusión mutua (`threading.Lock`) para asegurar que solo un hilo pueda acceder y modificar el saldo a la vez.

Código corregido:

```
import threading
import time

saldo_cuenta = 1000
lock_cuenta = threading.Lock()

def retirar_dinero(cliente_id, monto):
    global saldo_cuenta
    print(f"Cliente {cliente_id} intenta retirar ${monto}...")
    
    with lock_cuenta:
        if saldo_cuenta >= monto:
            time.sleep(0.1)
            saldo_cuenta -= monto
            print(f"Cliente {cliente_id} retiró ${monto}. Nuevo saldo: ${saldo_cuenta}")
        else:
            print(f"Cliente {cliente_id}: Fondos insuficientes. Saldo actual: ${saldo_cuenta}")

clientes = []
for i in range(5):
    t = threading.Thread(target=retirar_dinero, args=(i, 600))
    clientes.append(t)
    t.start()

for t in clientes:
    t.join()

print(f"Saldo final: ${saldo_cuenta}")

```

---

## 2. El Contador Compartido (con doble verificación)

### Problemas identificados:
- Uso incorrecto del método `lock.locked()` para decidir si se adquiere el lock.
- Presencia de una condición de carrera tipo check-then-act (verificar antes de actuar sin atomicidad).
- La verificación del estado del lock y la adquisición del mismo no son operaciones atómicas.
- Pérdida de operaciones de incremento cuando el lock está ocupado (los hilos no hacen nada en el `else`).
- Implementación incorrecta de una supuesta optimización de concurrencia.
- No se garantiza que todos los accesos a la variable compartida estén protegidos correctamente.

### Riesgos:
- Pérdida de incrementos en el contador.
- Valor final incorrecto (menor al esperado).
- Comportamiento no determinista dependiendo del interleaving de los hilos.
- Condiciones de carrera difíciles de detectar (errores intermitentes).
- Inconsistencia en el estado del sistema.

### Propuesta de corrección:
Se debe eliminar la doble verificación y proteger completamente la sección crítica utilizando un `Lock`, asegurando que cada incremento sea ejecutado de forma segura.

Código corregido:

```
import threading

class ContadorSeguro:
    def __init__(self):
        self.valor = 0
        self.lock = threading.Lock()

    def incrementar_batch(self, cantidad): # En lugar de incrementar de uno en uno, se incrementa en batch para reducir la cantidad de veces que se adquiere el lock
        with self.lock: #
            self.valor += cantidad # Se incrementa el contador en una sola operación crítica, lo que mejora la eficiencia y evita la condición de carrera.

contador_obj = ContadorSeguro()

def tarea():
    local = 0
    for _ in range(100000):
        local += 1 
    
    # Se hace una sola operación crítica para incrementar el contador con el valor acumulado local, lo que reduce la contención del lock y mejora el rendimiento.
    contador_obj.incrementar_batch(local) 

hilos = [threading.Thread(target=tarea) for _ in range(10)]

for h in hilos:
    h.start()

for h in hilos:
    h.join()

print(f"Valor final del contador: {contador_obj.valor}")

```