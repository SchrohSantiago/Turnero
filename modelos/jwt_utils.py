import jwt
import secrets  # Esta libreria de python nos va a proporcionar una clave secreta y segura para la decodificacion de los tokens
from datetime import datetime, timedelta

clave_secreta = secrets.token_urlsafe(32)

# Generar un token JWT
def generar_token(payload, clave_secreta, tiempo_expiracion_minutos):
    tiempo_expiracion= datetime.utcnow() + timedelta(minutes=tiempo_expiracion_minutos)
    payload['exp'] = tiempo_expiracion
    return jwt.encode(payload, clave_secreta, algorithm='HS256')

# Validar un token JWT
def validar_token(token):
    try:
        payload = jwt.decode(token, clave_secreta, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'El token ha expirado.'
    except jwt.InvalidTokenError:
        return 'Token inválido.'

# Ejemplo de uso
payload = {'usuario_id': 1234, 'nombre': 'Usuario de Ejemplo'}
token = generar_token(payload, clave_secreta, 30)  # Generar un token con expiración de 30 minutos
print('Token generado:', token)

# Validar el token
resultado = validar_token(token)
exp_unix = 1710434918
exp_legible = datetime.fromtimestamp(exp_unix)

print("Fecha de expiración legible:", exp_legible)
print('Resultado de validación:', resultado)