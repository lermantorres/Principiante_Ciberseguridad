def cifrar_cesar(texto, desplazamiento):
    resultado = ""
    for letra in texto:
        if letra.isupper():  # Mayúsculas
            resultado += chr((ord(letra) - 65 + desplazamiento) % 26 + 65)
        elif letra.islower():  # Minúsculas
            resultado += chr((ord(letra) - 97 + desplazamiento) % 26 + 97)
        else:
            resultado += letra  # Espacios, números, símbolos
    return resultado

def descifrar_cesar(texto, desplazamiento):
    # Descifrar es cifrar con desplazamiento negativo
    return cifrar_cesar(texto, -desplazamiento)

# Ejemplo de uso
texto_original = "lEDpo"
desplazamiento = 3

cifrado = cifrar_cesar(texto_original, desplazamiento)
print(f"Original: {texto_original}")
print(f"Cifrado:  {cifrado}")

descifrado = descifrar_cesar(cifrado, desplazamiento)
print(f"Descifrado: {descifrado}")