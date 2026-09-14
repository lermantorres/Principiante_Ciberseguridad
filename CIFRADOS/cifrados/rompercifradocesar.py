def romper_cesar(texto_cifrado):
    print("=== ATAQUE DE FUERZA BRUTA ===")
    print("Probando los 25 desplazamientos posibles:\n")
    
    for desplazamiento in range(1, 26):
        intento = ""
        for letra in texto_cifrado:
            if letra.isupper():
                intento += chr((ord(letra) - 65 - desplazamiento) % 26 + 65)
            elif letra.islower():
                intento += chr((ord(letra) - 97 - desplazamiento) % 26 + 97)
            else:
                intento += letra
        print(f"Clave {desplazamiento:2}: {intento}")

# Ejemplo
texto_cifrado = "ohupdqsur hv xq judq surjudpdgru"
romper_cesar(texto_cifrado)