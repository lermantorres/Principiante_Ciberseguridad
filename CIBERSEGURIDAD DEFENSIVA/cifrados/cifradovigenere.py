def cifrar_vigenere(texto, clave):
    """
    Cifra un texto usando el cifrado Vigenère.
    
    Args:
        texto: Mensaje a cifrar (solo letras)
        clave: Palabra clave para el cifrado
    
    Returns:
        Texto cifrado
    """
    resultado = []
    clave = clave.upper()
    clave_idx = 0
    
    for letra in texto:
        if letra.isalpha():  # Solo cifrar letras
            # Determinar si es mayúscula o minúscula
            base = ord('A') if letra.isupper() else ord('a')
            
            # Obtener desplazamiento de la clave (A=0, B=1, ..., Z=25)
            desplazamiento = ord(clave[clave_idx % len(clave)]) - ord('A')
            
            # Aplicar cifrado: (letra + desplazamiento) mod 26
            letra_cifrada = chr((ord(letra) - base + desplazamiento) % 26 + base)
            resultado.append(letra_cifrada)
            
            # Avanzar en la clave solo si ciframos una letra
            clave_idx += 1
        else:
            # Mantener caracteres no alfabéticos sin cambios
            resultado.append(letra)
    
    return ''.join(resultado)


def descifrar_vigenere(texto_cifrado, clave):
    """
    Descifra un texto cifrado con Vigenère.
    
    Args:
        texto_cifrado: Mensaje cifrado
        clave: Misma palabra clave usada para cifrar
    
    Returns:
        Texto original
    """
    resultado = []
    clave = clave.upper()
    clave_idx = 0
    
    for letra in texto_cifrado:
        if letra.isalpha():
            base = ord('A') if letra.isupper() else ord('a')
            
            # Obtener desplazamiento (mismo que en cifrado)
            desplazamiento = ord(clave[clave_idx % len(clave)]) - ord('A')
            
            # Descifrar: (letra - desplazamiento) mod 26
            letra_descifrada = chr((ord(letra) - base - desplazamiento) % 26 + base)
            resultado.append(letra_descifrada)
            
            clave_idx += 1
        else:
            resultado.append(letra)
    
    return ''.join(resultado)

def menu_vigenere():
    print("\n=== CIFRADO VIGENÈRE ===")
    print("1. Cifrar mensaje")
    print("2. Descifrar mensaje")
    print("3. Salir")
    
    opcion = input("Elige una opción: ")
    
    if opcion == "1":
        texto = input("Texto a cifrar: ")
        clave = input("Palabra clave: ")
        resultado = cifrar_vigenere(texto, clave)
        print(f"\nTexto cifrado: {resultado}")
    elif opcion == "2":
        texto = input("Texto a descifrar: ")
        clave = input("Palabra clave: ")
        resultado = descifrar_vigenere(texto, clave)
        print(f"\nTexto descifrado: {resultado}")
    elif opcion == "3":
        return False
    return True

# Ejecutar menú
while menu_vigenere():
    pass