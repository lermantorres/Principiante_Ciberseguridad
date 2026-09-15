# 🔐 Detección de Ataques Brute Force con Splunk

## 📌 Descripción

Laboratorio de ciberseguridad orientado a la **detección e investigación de ataques de fuerza bruta (Brute Force)** utilizando **Splunk como plataforma SIEM** y eventos de seguridad de Windows.

El laboratorio simula un escenario en el que un usuario recibe múltiples intentos de autenticación fallidos. Los eventos generados son recopilados por Splunk para posteriormente realizar una búsqueda mediante **SPL (Search Processing Language)** y generar una alerta cuando se supera un umbral determinado de intentos fallidos.

El objetivo es demostrar el proceso básico de monitoreo, detección e investigación de un evento de seguridad desde la perspectiva de un **Analista SOC**.

---

## 🎯 Objetivos

* Configurar la recepción de eventos de seguridad en Splunk.
* Generar eventos de autenticación fallida en un entorno controlado.
* Identificar patrones asociados a ataques de fuerza bruta.
* Analizar eventos de Windows relacionados con autenticaciones.
* Crear consultas utilizando SPL.
* Establecer un umbral para la detección de múltiples intentos fallidos.
* Crear una alerta en Splunk.
* Documentar el proceso de investigación y detección.

---

## 🧪 Entorno del laboratorio

### Herramientas utilizadas

* **Splunk**
* **Windows Event Viewer**
* **Splunk Universal Forwarder / agente de Splunk**
* **PowerShell**
* **Script `localbrute.ps1`**
* **SPL (Search Processing Language)**

### Fuente de eventos

Los eventos utilizados en el laboratorio provienen del registro de seguridad de Windows:

```text
WinEventLog:Security
```

Se utilizan principalmente los siguientes códigos de evento:

| EventCode | Descripción              |
| --------- | ------------------------ |
| 4624      | Inicio de sesión exitoso |
| 4625      | Inicio de sesión fallido |

---

# 🏗️ Arquitectura del laboratorio

El flujo utilizado durante el laboratorio es el siguiente:

```text
┌──────────────────────┐
│       Windows        │
│                      │
│  Security Event Log  │
└──────────┬───────────┘
           │
           │ Eventos
           ▼
┌──────────────────────┐
│ Splunk Agent /       │
│ Universal Forwarder  │
└──────────┬───────────┘
           │
           │ Forwarding
           ▼
┌──────────────────────┐
│       Splunk         │
│                      │
│       Index          │
└──────────┬───────────┘
           │
           │ SPL
           ▼
┌──────────────────────┐
│ Brute Force Detection│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Alert          │
└──────────────────────┘
```

---

# 🔎 Procedimiento del laboratorio

## 1. Configuración de Splunk

El primer paso consiste en configurar Splunk para recibir los eventos generados por el agente instalado en el equipo Windows.

Se configura el puerto de recepción en Splunk para permitir que el agente envíe los eventos de seguridad.

Posteriormente se crea un índice destinado a almacenar los eventos provenientes de Windows.

### Objetivo

Centralizar los eventos de seguridad en Splunk para posteriormente realizar consultas y detecciones.

📷 **Evidencia:**

![Configuración de Splunk](/puerto_escucha.png) 

---

# 2. Descarga del script utilizado para generar los eventos

Para generar los intentos de autenticación fallidos se utilizó el script `localbrute.ps1`.

El script fue obtenido desde el siguiente repositorio:

**Minimalistic Offensive Security Tools – localbrute.ps1**

https://github.com/InfosecMatter/Minimalistic-offensive-security-tools/blob/master/localbrute.ps1

> ⚠️ El script se utilizó únicamente dentro de un entorno de laboratorio controlado con fines educativos y de detección.

El objetivo de esta herramienta dentro del laboratorio es generar múltiples intentos de autenticación para posteriormente analizar los eventos producidos en Windows.

---

# 3. Ejecución del laboratorio

Una vez descargado el script, se procede a ejecutarlo dentro del equipo Windows utilizado para el laboratorio.

## 3.1 Cargar el script en memoria

Para cargar el contenido del script en memoria se utilizó PowerShell:

```powershell
Get-Content C:\Users\*****\Downloads\localbrute.ps1 -Raw | Invoke-Expression
```

Este comando permite cargar y ejecutar el contenido del script directamente desde PowerShell.

📷 **Evidencia:**

![Ejecución del script](images/02-ejecucion-script.png)

---

## 3.2 Ejecución del ataque simulado

Posteriormente se ejecuta el script indicando el usuario objetivo y el archivo utilizado como diccionario.

En este laboratorio se creó un diccionario compuesto por **100 palabras**.

```powershell
localbrute "nombredelusuario" "C:\Users\****\Downloads\dc.txt" $true
```

Los parámetros utilizados corresponden a:

```text
nombredelusuario → Usuario objetivo
dc.txt            → Diccionario utilizado
$true             → Parámetro de ejecución del script
```

El objetivo es generar múltiples intentos de autenticación fallidos contra el usuario seleccionado.

📷 **Evidencia:**

![Ataque Brute Force simulado](images/03-bruteforce.png)

---

# 3.3 Validación de eventos en Windows

Después de ejecutar el script se valida que los intentos de autenticación hayan generado eventos dentro del **Visor de eventos de Windows**.

Ruta utilizada:

```text
Event Viewer
    └── Windows Logs
        └── Security
```

Se verifican principalmente los eventos:

```text
Event ID 4625 → An account failed to log on
```

Este evento representa un intento de inicio de sesión fallido.

También se puede validar la presencia de:

```text
Event ID 4624 → An account was successfully logged on
```

Este evento representa un inicio de sesión exitoso.

📷 **Evidencia:**

![Windows Event Viewer](images/04-event-viewer.png)

---

# 4. Detección utilizando SPL

Una vez generados y recopilados los eventos, se realiza la búsqueda desde Splunk.

La consulta utilizada es:

```spl
index=wineventlog source="WinEventLog:Security" (EventCode=4624 OR EventCode=4625)
| stats count(eval(EventCode=4624)) as successful_logons, count(eval(EventCode=4625)) as login_failures by Nombre_de_cuenta
| where successful_logons >= 0 AND login_failures > 10
```

## 🔍 Funcionamiento de la consulta

La búsqueda realiza las siguientes acciones:

### 1. Selección del índice

```spl
index=wineventlog
```

Limita la búsqueda al índice donde se almacenan los eventos de Windows.

### 2. Selección de la fuente

```spl
source="WinEventLog:Security"
```

Filtra los eventos provenientes del registro de seguridad de Windows.

### 3. Selección de eventos

```spl
(EventCode=4624 OR EventCode=4625)
```

Permite analizar tanto:

* **4624:** autenticaciones exitosas.
* **4625:** autenticaciones fallidas.

### 4. Conteo de eventos

```spl
stats count(eval(EventCode=4624)) as successful_logons,
      count(eval(EventCode=4625)) as login_failures
      by Nombre_de_cuenta
```

Agrupa los eventos por cuenta y calcula:

* Cantidad de autenticaciones exitosas.
* Cantidad de autenticaciones fallidas.

### 5. Aplicación del umbral

```spl
| where successful_logons >= 0 AND login_failures > 10
```

Finalmente se muestran las cuentas que presentan **más de 10 intentos de autenticación fallidos**.

Este umbral permite identificar un comportamiento potencialmente asociado a un ataque de fuerza bruta.

📷 **Evidencia:**

![Consulta SPL Brute Force](images/05-spl-query.png)

---

# 5. Análisis del resultado

El resultado obtenido en Splunk permite identificar las cuentas que superan el umbral establecido de intentos de autenticación fallidos.

En un escenario real, este comportamiento podría indicar:

* Ataque de fuerza bruta.
* Password spraying.
* Intentos automatizados de autenticación.
* Credenciales incorrectas debido a una configuración o aplicación.
* Actividad legítima que requiere investigación.

Por este motivo, la detección debe ser complementada con información adicional antes de determinar que se trata definitivamente de una actividad maliciosa.

Durante el laboratorio, el comportamiento fue generado de manera controlada para validar la capacidad de detección de Splunk.

---

# 🚨 6. Creación de la alerta

Después de validar que la consulta permite detectar el comportamiento esperado, se guarda la búsqueda como una **alerta en Splunk**.

La alerta se configura para detectar cuentas que superen el umbral definido:

```text
login_failures > 10
```

### Objetivo de la alerta

Generar una notificación cuando se detecte una cantidad elevada de intentos fallidos de autenticación, permitiendo que un analista de seguridad pueda iniciar una investigación.

📷 **Evidencia:**

![Alerta en Splunk](images/06-alert.png)

---

# 🧑‍💻 7. Perspectiva de un SOC Analyst

Desde la perspectiva de un analista SOC, el proceso realizado puede representarse de la siguiente manera:

```text
          Eventos de Windows
                  │
                  ▼
           Recopilación
                  │
                  ▼
               Splunk
                  │
                  ▼
             Consulta SPL
                  │
                  ▼
       Más de 10 intentos fallidos
                  │
                  ▼
              Alerta
                  │
                  ▼
          Investigación
                  │
                  ▼
        Clasificación del evento
```

Durante una investigación real, el analista debería complementar la información con:

* Dirección IP de origen.
* Usuario afectado.
* Host de origen.
* Timestamp de los eventos.
* Cantidad de intentos.
* Duración de la actividad.
* Existencia de autenticaciones exitosas.
* Actividad posterior al inicio de sesión.
* Geolocalización de la IP, cuando aplique.
* Información adicional disponible en el SIEM.

---

# 🛡️ 8. Recomendaciones

Ante una posible actividad de fuerza bruta, algunas acciones recomendadas serían:

1. Validar si la actividad corresponde a un usuario legítimo.
2. Identificar la dirección IP de origen.
3. Revisar si existen autenticaciones exitosas posteriores a los intentos fallidos.
4. Revisar la actividad del usuario afectado.
5. Aplicar bloqueo o medidas de contención cuando la actividad maliciosa sea confirmada.
6. Implementar MFA.
7. Aplicar políticas de bloqueo y limitación de intentos.
8. Ajustar los umbrales de detección para reducir falsos positivos.
9. Correlacionar los eventos con otras fuentes de seguridad.

---

# 📊 9. Resultados obtenidos

Con este laboratorio se logró:

* Configurar la recepción de eventos de Windows en Splunk.
* Centralizar eventos de autenticación.
* Generar eventos de autenticación fallida en un entorno controlado.
* Identificar eventos Windows 4625.
* Analizar eventos de autenticación 4624 y 4625.
* Crear una búsqueda utilizando SPL.
* Establecer un umbral de detección.
* Identificar posibles comportamientos de fuerza bruta.
* Crear una alerta en Splunk.
* Documentar un proceso básico de investigación SOC.

---

# 🧠 10. MITRE ATT&CK

Este laboratorio se relaciona con la técnica:

**T1110 – Brute Force**

La técnica describe ataques destinados a obtener acceso mediante intentos repetidos de autenticación utilizando diferentes credenciales o combinaciones.

Subtécnicas relacionadas pueden incluir:

* T1110.001 – Password Guessing
* T1110.002 – Password Cracking
* T1110.003 – Password Spraying
* T1110.004 – Credential Stuffing

En este laboratorio se utiliza principalmente el concepto de **Brute Force / Password Guessing**.

---

# 🛠️ 11. Tecnologías y conocimientos demostrados

```text
Splunk
SPL
SIEM
Windows Event Logs
PowerShell
Event ID 4624
Event ID 4625
Log Analysis
Security Monitoring
Brute Force Detection
Alerting
Incident Investigation
SOC Analysis
MITRE ATT&CK
```

---

# ⚠️ Disclaimer

Este proyecto fue realizado exclusivamente con fines educativos y dentro de un entorno de laboratorio controlado.

Las técnicas utilizadas para generar los eventos no deben ejecutarse contra sistemas, cuentas o infraestructura sin autorización.

No se incluyen credenciales reales ni información sensible en este repositorio.

---

# 📁 Estructura del proyecto

```text
splunk-bruteforce-detection/
│
├── README.md
│
├── images/
│   ├── 01-configuracion-splunk.png
│   ├── 02-ejecucion-script.png
│   ├── 03-bruteforce.png
│   ├── 04-event-viewer.png
│   ├── 05-spl-query.png
│   └── 06-alert.png
│
└── queries/
    └── brute_force_detection.spl
```

---

# 📚 Referencias

* Splunk
* Windows Security Event Logs
* MITRE ATT&CK
* InfosecMatter – Minimalistic Offensive Security Tools

Script utilizado en el laboratorio:

https://github.com/InfosecMatter/Minimalistic-offensive-security-tools/blob/master/localbrute.ps1

---

## 👨‍💻 Autor

**Lerman Torres**

Proyecto desarrollado como parte de un laboratorio práctico de ciberseguridad y monitoreo mediante SIEM.

