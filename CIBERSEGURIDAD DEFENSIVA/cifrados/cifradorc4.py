class CifradoRC4:
    def __init__(self, clave):
        """
        Inicializa el cifrador RC4 con una clave.
        
        Args:
            clave: Contraseña (string o bytes)
        """
        # Convertir clave a bytes si es string
        if isinstance(clave, str):
            self.clave = clave.encode('utf-8')
        else:
            self.clave = clave
    
    def ksa(self):
        """
        Key Scheduling Algorithm
        Inicializa el array S (estado interno)
        """
        # Inicializar S con valores 0..255
        S = list(range(256))
        
        # Permutar S según la clave
        j = 0
        for i in range(256):
            j = (j + S[i] + self.clave[i % len(self.clave)]) % 256
            S[i], S[j] = S[j], S[i]  # Intercambiar
        
        return S
    
    def prga(self, S, longitud):
        """
        Pseudo-Random Generation Algorithm
        Genera keystream de la longitud solicitada
        
        Args:
            S: Array de estado (después de KSA)
            longitud: Número de bytes a generar
        
        Returns:
            Lista de bytes del keystream
        """
        keystream = []
        i = 0
        j = 0
        
        for _ in range(longitud):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]  # Intercambiar
            
            # Generar byte del keystream
            k = S[(S[i] + S[j]) % 256]
            keystream.append(k)
        
        return keystream
    
    def cifrar(self, texto):
        """
        Cifra o descifra un texto (el proceso es el mismo)
        
        Args:
            texto: Texto a cifrar (string o bytes)
        
        Returns:
            Bytes cifrados
        """
        # Convertir texto a bytes si es string
        if isinstance(texto, str):
            texto_bytes = texto.encode('utf-8')
        else:
            texto_bytes = texto
        
        # Inicializar RC4
        S = self.ksa()
        
        # Generar keystream de la misma longitud que el texto
        keystream = self.prga(S.copy(), len(texto_bytes))
        
        # Aplicar XOR byte a byte
        cifrado = bytes([texto_bytes[i] ^ keystream[i] for i in range(len(texto_bytes))])
        
        return cifrado
    
    def descifrar(self, cifrado):
        """
        Descifra (es idéntico al cifrado por la propiedad XOR)
        
        Args:
            cifrado: Bytes cifrados
        
        Returns:
            Bytes descifrados
        """
        # RC4 es simétrico: cifrar y descifrar son lo mismo
        return self.cifrar(cifrado)
    
    def cifrar_texto(self, texto):
        """Cifra texto y devuelve representación hexadecimal"""
        cifrado = self.cifrar(texto)
        return cifrado.hex()
    
    def descifrar_hex(self, hex_cifrado):
        """Descifra desde hexadecimal"""
        cifrado_bytes = bytes.fromhex(hex_cifrado)
        return self.descifrar(cifrado_bytes).decode('utf-8')
    
    # Crear cifrador con una clave
rc4 = CifradoRC4("miClaveSecreta")

# Texto a cifrar
texto = "Este es un mensaje secreto."

print(f"Original: {texto}")
print()

# Cifrar
cifrado_bytes = rc4.cifrar(texto)
cifrado_hex = rc4.cifrar_texto(texto)
print(f"Cifrado (hex): {cifrado_hex}")

# Descifrar
descifrado_bytes = rc4.descifrar(cifrado_bytes)
descifrado = descifrado_bytes.decode('utf-8')
print(f"Descifrado: {descifrado}")