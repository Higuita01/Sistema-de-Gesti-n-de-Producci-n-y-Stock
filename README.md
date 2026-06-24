# Sistema de Gestión de Producción y Stock

Aplicación web desarrollada con **Django** para gestionar la producción, stock, envasado y despacho de una fábrica de velas.

El sistema permite registrar la producción diaria, controlar el stock disponible, gestionar pallets por lote y llevar un historial de movimientos de manera centralizada.

---

## Características principales

### Producción

* Registro de fecha de elaboración.
* Registro del operario responsable.
* Selección del tipo de vela:

  * X68
  * X60
  * Largas
  * CRISTIX60
* Registro de cantidades:

  * Buenas
  * Feas
  * Especiales (pruebas o nuevas fórmulas)
* Historial completo de producción ordenado por fecha.

---

### Stock

El sistema actualiza el stock automáticamente a partir de la producción registrada.

Características:

* Consolidación automática por operario y tipo de vela.
* Suma automática cuando coinciden:

  * Operario
  * Tipo de vela
  * Categoría
* Descuento automático cuando se registran movimientos de envasado.
* Tabla resumen con el total disponible de cada tipo y categoría.

---

### Envasado

Permite registrar el consumo de stock para el proceso de envasado.

Validaciones:

* Verifica que exista stock suficiente.
* Comprueba coincidencia entre:

  * Operario
  * Tipo de vela
  * Categoría
* Si los datos no coinciden, la operación se cancela y se muestra una advertencia.

Además, mantiene un historial de movimientos indicando:

* Fecha
* Operario
* Tipo de vela
* Categoría
* Cantidad utilizada

---

### Gestión de Pallets

Permite administrar el stock de pallets en depósito.

Características:

* Registro por:

  * Tipo de vela
  * Número de lote
* Agrupación automática por lote.
* Conteo independiente para pallets del mismo tipo pero distinto lote.

Ejemplo:

LO50 = 2

LO51 = 1

LO52 = 2

LO53 = 7

---

### Despacho

Permite registrar la salida de pallets del depósito.

El sistema:

* Verifica que el lote exista.
* Comprueba la cantidad disponible.
* Descuenta automáticamente del stock de pallets.
* Impide operaciones inválidas.

---

## Tecnologías utilizadas

* Python
* Django
* HTML
* CSS
* JavaScript
* SQLite

---

## Objetivo del proyecto

Este proyecto fue desarrollado para practicar el diseño de aplicaciones orientadas a procesos productivos reales, implementando reglas de negocio, control de inventario y trazabilidad de operaciones mediante una aplicación web construida con Django.
