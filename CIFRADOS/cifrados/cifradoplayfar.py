class CifradoPlayfair:
    def __init__(self, clave):
        self.matriz = self.construir_matriz(clave)
    
    def construir_matriz(self, clave):
        # Limpiar clave: mayúsculas, eliminar J (cambiar por I)
        clave = clave.upper().replace('J', 'I')
        # Eliminar duplicados manteniendo orden
        letras_vistas = set()
        letras_clave = []
        for letra in clave:
            if letra not in letras_vistas and letra.isalpha():
                letras_vistas.add(letra)
                letras_clave.append(letra)
        
        # Agregar el resto del alfabeto (excepto J)
        alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # Sin J
        for letra in alfabeto:
            if letra not in letras_vistas:
                letras_clave.append(letra)
        
        # Crear matriz 5x5
        matriz = []
        for i in range(0, 25, 5):
            matriz.append(letras_clave[i:i+5])
        return matriz
    
    def mostrar_matriz(self):
        print("Matriz Playfair:")
        for fila in self.matriz:
            print(" ".join(fila))
    
    def encontrar_posicion(self, letra):
        """Devuelve (fila, columna) de una letra en la matriz"""
        for i, fila in enumerate(self.matriz):
            if letra in fila:
                return (i, fila.index(letra))
        return None
    
    def preparar_texto(self, texto):
        """Prepara el texto para cifrar: mayúsculas, J→I, inserta X entre letras iguales"""
        texto = texto.upper().replace('J', 'I')
        # Eliminar caracteres no alfabéticos
        texto = ''.join([c for c in texto if c.isalpha()])
        
        # Dividir en pares, insertar X entre letras iguales
        i = 0
        resultado = []
        while i < len(texto):
            a = texto[i]
            if i + 1 < len(texto):
                b = texto[i + 1]
                if a == b:
                    resultado.append(a + 'X')
                    i += 1
                else:
                    resultado.append(a + b)
                    i += 2
            else:
                resultado.append(a + 'X')  # Si queda impar, agregar X
                i += 1
        return resultado
    
    def cifrar_par(self, par):
        a, b = par[0], par[1]
        fila_a, col_a = self.encontrar_posicion(a)
        fila_b, col_b = self.encontrar_posicion(b)
        
        if fila_a == fila_b:  # Misma fila
            return self.matriz[fila_a][(col_a + 1) % 5] + self.matriz[fila_b][(col_b + 1) % 5]
        elif col_a == col_b:  # Misma columna
            return self.matriz[(fila_a + 1) % 5][col_a] + self.matriz[(fila_b + 1) % 5][col_b]
        else:  # Rectángulo
            return self.matriz[fila_a][col_b] + self.matriz[fila_b][col_a]
    
    def descifrar_par(self, par):
        a, b = par[0], par[1]
        fila_a, col_a = self.encontrar_posicion(a)
        fila_b, col_b = self.encontrar_posicion(b)
        
        if fila_a == fila_b:  # Misma fila
            return self.matriz[fila_a][(col_a - 1) % 5] + self.matriz[fila_b][(col_b - 1) % 5]
        elif col_a == col_b:  # Misma columna
            return self.matriz[(fila_a - 1) % 5][col_a] + self.matriz[(fila_b - 1) % 5][col_b]
        else:  # Rectángulo
            return self.matriz[fila_a][col_b] + self.matriz[fila_b][col_a]
    
    def cifrar(self, texto_plano):
        pares = self.preparar_texto(texto_plano)
        texto_cifrado = []
        for par in pares:
            texto_cifrado.append(self.cifrar_par(par))
        return ''.join(texto_cifrado)
    
    def descifrar(self, texto_cifrado):
        # Dividir en pares
        pares = [texto_cifrado[i:i+2] for i in range(0, len(texto_cifrado), 2)]
        texto_descifrado = []
        for par in pares:
            texto_descifrado.append(self.descifrar_par(par))
        
        # Eliminar las X que se agregaron (esto es imperfecto, puede eliminar X reales)
        resultado = ''.join(texto_descifrado)
        # Limpieza básica: eliminar X al final de un par si la siguiente letra es igual
        # (en una implementación real, esto es más complejo)
        return resultado
    


# Crear cifrador con una clave
playfair = CifradoPlayfair("PLAYFAR")

# Mostrar la matriz generada
playfair.mostrar_matriz()

# Texto a cifrar
texto = "PLAYFAIR CIPHER"
print(f"\nTexto original: {texto}")

# Cifrar
cifrado = playfair.cifrar(texto)
print(f"Texto cifrado: {cifrado}")

# Descifrar
descifrado = playfair.descifrar(cifrado)
print(f"Texto descifrado: {descifrado}")