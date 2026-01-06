# 📋 Plan de Desarrollo: Sistema de Gestión de Biblioteca

## 🔴 Fase 1: Prioridad Alta (Cierre del MVP - Libros)

*Tareas indispensables para que el módulo de libros sea funcional y seguro antes de pasar a otras entidades.*

* [X] **Pruebas de Unidad (Modelo):** Finalizar los 3 tests básicos (Verificación de códigos, Integridad por préstamos y Continuidad de secuencia).

* [X] **Pruebas de Integración (Controlador):** Implementar los tests de búsqueda (formato de detalles) e inyección automática de `CURRENT_USER_ID`.

* [ ] **Vista de Actualización:** * [ ] Crear el formulario que se autopueble al buscar un libro.
* [ ] Integrar el `ttk.Treeview` para visualizar la lista de copias únicas y sus estados.

* [ ] **Borrado Lógico (Eliminar):** Implementar la función `delete_book` en las tres capas.
* *Nota:* No usar `DELETE`, sino cambiar `status` a "Inactivo" para preservar la integridad referencial.

* [ ] **Gran Refactor de Libros:** Limpieza de código, eliminación de comentarios obsoletos y estandarización de nombres de variables en el CRUD de libros.

## 🟡 Fase 2: Expansión de Entidades (Flujo Principal)

*Una vez que Libros es sólido, replicar el esquema en los otros pilares del sistema.*

* [ ] **Módulo de Socios (Members):**
* [ ] Desarrollar CRUD completo (Modelo, Controlador, Vista).
* [ ] Implementar validación de DNI/ID único.


* [ ] **Módulo de Préstamos (Loans):**
* [ ] Lógica para asociar un `copy_id` con un `member_id`.
* [ ] Cambio automático de `status_loan` de "Disponible" a "Prestado".


* [ ] **Gestión de Sesión Real:**
* [ ] Limpiar campos de login tras ingreso exitoso.
* [ ] Reemplazar la constante `CURRENT_USER_ID = 1` por el ID capturado dinámicamente desde la vista Home hacia las demás capas.

* [ ] **Búsqueda Global:**
* [ ] Implementar vista de búsqueda tipo "Inventario Total" (Lectura de todos los libros).



## 🟢 Fase 3: Feedback Visual y UX (Pulido del MVP)

*Mejoras en la experiencia de usuario sin añadir complejidad en la base de datos.*

* [ ] **Alertas Visuales en el Treeview:**
* [ ] Configurar Tags de colores en `books_view.py`.
* [ ] Lógica: Fila **Rojo suave** para Stock = 0.
* [ ] Lógica: Fila **Gris** para libros "Inactivos".


* [ ] **Manejo de Errores en UI:** Asegurar que todos los mensajes de error del controlador se muestren en `messagebox` de Tkinter.

## 🔵 Fase 4: Versión Mejorada (Post-MVP / Futuro)

*Ideas para cuando el sistema base esté funcionando al 100%.*

* [ ] **Optimización de Consultas (SQL JOINs):** Unificar las llamadas en `get_book_by_id` para traer autores y géneros en una sola sentencia.
* [ ] **Múltiples Autores:** Rediseñar el modelo y la vista para permitir N autores por libro.
* [ ] **Motivos de Inactividad Detallados:** Ampliar el campo `unavailable_reason` con un catálogo (ej. "En reparación", "Extraviado", "Donación").
* [ ] **Buscador Avanzado:** Implementar un buscador dinámico con filtros avanzados (por autor, por género, título o ISBN, con búsqueda predictiva). Implementar el "Doble clic para editar" (paso de parámetros entre ventanas).
* [ ] **Validación de ISBN:** Implementar Regex para asegurar el formato estándar de 13 dígitos.
* [ ] **Carga de Imágenes:** Permitir vincular una ruta de imagen para la portada del libro.

