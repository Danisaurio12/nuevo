from flask import Flask, render_template, request, redirect, url_for, flash
from psycopg2 import errors

from config import Config
from db import get_connection

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY


@app.route("/")
def listado():
    """Muestra el listado de productos, con búsqueda opcional por
    código, nombre o categoría a través del parámetro ?q="""
    q = request.args.get("q", "").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        if q:
            patron = f"%{q}%"
            cur.execute(
                """
                SELECT * FROM productos
                WHERE codigo ILIKE %s
                   OR nombre ILIKE %s
                   OR categoria ILIKE %s
                ORDER BY id
                """,
                (patron, patron, patron),
            )
        else:
            cur.execute("SELECT * FROM productos ORDER BY id")
        productos = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return render_template("listado.html", productos=productos, q=q)


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    """Formulario y procesamiento del alta de un nuevo producto."""
    if request.method == "POST":
        datos = _leer_datos_formulario(request.form)

        error_validacion = _validar_datos(datos)
        if error_validacion:
            flash(error_validacion, "danger")
            return render_template("formulario.html", producto=request.form, accion="Registrar")

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO productos (codigo, nombre, categoria, precio, existencia, activo)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    datos["codigo"],
                    datos["nombre"],
                    datos["categoria"],
                    datos["precio"],
                    datos["existencia"],
                    datos["activo"],
                ),
            )
            conn.commit()
            flash(f'Producto "{datos["nombre"]}" registrado correctamente.', "success")
            return redirect(url_for("listado"))
        except errors.UniqueViolation:
            conn.rollback()
            flash(f'Ya existe un producto con el código "{datos["codigo"]}".', "danger")
            return render_template("formulario.html", producto=request.form, accion="Registrar")
        except Exception as error:
            conn.rollback()
            flash(f"Ocurrió un error al registrar el producto: {error}", "danger")
            return render_template("formulario.html", producto=request.form, accion="Registrar")
        finally:
            cur.close()
            conn.close()

    return render_template("formulario.html", producto=None, accion="Registrar")


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    """Formulario y procesamiento de la edición de un producto existente."""
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        datos = _leer_datos_formulario(request.form)

        error_validacion = _validar_datos(datos)
        if error_validacion:
            cur.close()
            conn.close()
            flash(error_validacion, "danger")
            return render_template("formulario.html", producto=request.form, accion="Editar")

        try:
            cur.execute(
                """
                UPDATE productos
                SET codigo = %s, nombre = %s, categoria = %s,
                    precio = %s, existencia = %s, activo = %s
                WHERE id = %s
                """,
                (
                    datos["codigo"],
                    datos["nombre"],
                    datos["categoria"],
                    datos["precio"],
                    datos["existencia"],
                    datos["activo"],
                    id,
                ),
            )
            conn.commit()
            flash(f'Producto "{datos["nombre"]}" actualizado correctamente.', "success")
            return redirect(url_for("listado"))
        except errors.UniqueViolation:
            conn.rollback()
            flash(f'Ya existe otro producto con el código "{datos["codigo"]}".', "danger")
            return render_template("formulario.html", producto=request.form, accion="Editar")
        except Exception as error:
            conn.rollback()
            flash(f"Ocurrió un error al actualizar el producto: {error}", "danger")
            return render_template("formulario.html", producto=request.form, accion="Editar")
        finally:
            cur.close()
            conn.close()

    # GET: cargar el producto a editar
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cur.fetchone()
    cur.close()
    conn.close()

    if producto is None:
        flash("El producto solicitado no existe.", "warning")
        return redirect(url_for("listado"))

    return render_template("formulario.html", producto=producto, accion="Editar")


@app.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    """Elimina un producto. La confirmación se solicita en el navegador
    (ver el 'onsubmit=confirm(...)' del formulario en listado.html)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nombre FROM productos WHERE id = %s", (id,))
        producto = cur.fetchone()

        if producto is None:
            flash("El producto solicitado no existe.", "warning")
        else:
            cur.execute("DELETE FROM productos WHERE id = %s", (id,))
            conn.commit()
            flash(f'Producto "{producto["nombre"]}" eliminado correctamente.', "success")
    except Exception as error:
        conn.rollback()
        flash(f"Ocurrió un error al eliminar el producto: {error}", "danger")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("listado"))


def _leer_datos_formulario(form):
    """Extrae y normaliza los campos del formulario de producto."""
    return {
        "codigo": form.get("codigo", "").strip(),
        "nombre": form.get("nombre", "").strip(),
        "categoria": form.get("categoria", "").strip(),
        "precio": form.get("precio", "").strip(),
        "existencia": form.get("existencia", "").strip(),
        "activo": "activo" in form,
    }


def _validar_datos(datos):
    """Valida los datos del formulario de producto.

    Devuelve None si todo es válido, o un mensaje de error específico
    (string) indicando cuál fue el problema, para mostrarlo al usuario.
    """
    if not all([datos["codigo"], datos["nombre"], datos["categoria"], datos["precio"], datos["existencia"]]):
        return "Todos los campos son obligatorios."

    try:
        precio = float(datos["precio"])
    except ValueError:
        return "El precio debe ser un número válido."

    try:
        existencia = int(datos["existencia"])
    except ValueError:
        return "La existencia debe ser un número entero."

    if precio <= 0:
        return "El precio debe ser mayor que cero."

    if existencia < 0:
        return "La existencia no puede ser negativa."

    return None


if __name__ == "__main__":
    app.run(debug=True)
