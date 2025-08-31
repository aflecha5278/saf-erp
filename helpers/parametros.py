from articulos.models import ParametroSistema

def get_parametro(nombre, default=None):
    """
    Devuelve el valor del parámetro institucional según su clave.
    Si no existe, devuelve el valor por defecto.
    """
    try:
        return ParametroSistema.objects.get(clave=nombre.strip().upper()).valor
    except ParametroSistema.DoesNotExist:
        return default


def parametro_activo(nombre):
    """
    Devuelve True si el parámetro está activo ('S').
    """
    valor = get_parametro(nombre, "N")
    return valor.strip().upper() == "S"
