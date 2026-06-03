import hmac
import hashlib

# Solo TÚ y tu MAMÁ conocen esta clave secreta (como una contraseña compartida)
CLAVE_SECRETA = "mi_clave_super_secreta_123"

def crear_mensaje_seguro(mensaje):
    """Crear mensaje + su HMAC (sello de autenticidad)"""
    
    # El mensaje original
    texto = f"Mensaje: {mensaje}"
    
    # Crear el HMAC (sello) usando la clave secreta
    sello = hmac.new(
        CLAVE_SECRETA.encode('utf-8'),
        texto.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return f"{texto}||SELLO:{sello}"

def verificar_mensaje(mensaje_con_sello):
    """Verificar si el mensaje es auténtico y no fue modificado"""
    
    # Separar el mensaje del sello
    partes = mensaje_con_sello.split("||SELLO:")
    texto_original = partes[0]
    sello_recibido = partes[1]
    
    # Recalcular el sello que DEBERÍA tener
    sello_calculado = hmac.new(
        CLAVE_SECRETA.encode('utf-8'),
        texto_original.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Comparar sellos
    if sello_calculado == sello_recibido:
        return f"✅ MENSAJE VÁLIDO: {texto_original}"
    else:
        return f"❌ MENSAJE FALSO o MODIFICADO"

# ---------- EJEMPLO PRÁCTICO ----------

# 1. Juan crea un mensaje para su mamá
mensaje_original = "Mamá, dale $100 a mi hermano Juan"
mensaje_seguro = crear_mensaje_seguro(mensaje_original)

print("📨 Juan envía:")
print(mensaje_seguro)
print("\n" + "="*60 + "\n")

# 2. Mamá recibe y verifica
print("👩 Mamá verifica:")
resultado = verificar_mensaje(mensaje_seguro)
print(resultado)

print("\n" + "="*60 + "\n")

# 3. Pero si alguien INTERCEPTA y MODIFICA el mensaje...
mensaje_modificado = mensaje_seguro.replace("$100", "$10,000")

print("😈 Hacker modifica el mensaje:")
print(mensaje_modificado)
print("\n👩 Mamá verifica mensaje modificado:")
resultado = verificar_mensaje(mensaje_modificado)
print(resultado)