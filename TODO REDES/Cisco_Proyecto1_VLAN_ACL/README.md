# 🧩 Proyecto 1: Laboratorio de Aislamiento – Seguridad Básica con VLANs y ACLs

**Autor:** Lerman_Torres 
**Software usado:** Cisco Packet Tracer  
**Dispositivo principal:** Router Cisco 2811  
**Nivel:** Principiante / Intermedio  

---

## 🎯 Objetivo del Laboratorio

Aprender a **segmentar una red con VLANs** y **aplicar controles de acceso (ACLs)** para mejorar la seguridad y reducir el riesgo de movimientos laterales en caso de brechas.

Este laboratorio implementa:
- Principio de **mínimo privilegio**
- **Aislamiento de tráfico** entre redes
- Acceso seguro por **SSH** solo a administradores

---

## 🖥️ Topología de Red

| VLAN | Nombre             | Rango IP            | Descripción                          |
|------|--------------------|---------------------|--------------------------------------|
| 10   | RED INTERNA        | 192.168.10.0/24     | Usuarios corporativos                |
| 20   | RED INVITADOS      | 192.168.20.0/24     | Dispositivos de visitantes           |
| 99   | RED ADMINISTRACIÓN | 192.168.99.0/24     | Gestión de red (switches/routers)    |

---

## 🔒 Matriz de Seguridad (Control de Accesos entre VLANs)

| **Origen → Destino** | **VLAN 10 (Interna)** | **VLAN 20 (Invitados)** | **VLAN 99 (Admin)** | **Internet** |
|----------------------|----------------------|--------------------------|---------------------|---------------|
| **VLAN 10 (Interna)** | ✅ Permitido | ❌ Bloqueado | ⚙️ Solo 192.168.10.50 por SSH | ✅ Permitido |
| **VLAN 20 (Invitados)** | ❌ Bloqueado | ✅ Entre sí | ❌ Bloqueado | ✅ Permitido |
| **VLAN 99 (Admin)** | ✅ Permitido (SSH desde .50) | ❌ Bloqueado | ✅ Permitido | ✅ Permitido |

---

## ⚙️ Configuración del Router (R1)

Archivo: [`Proyecto1`]

```bash
hostname R1
ip domain-name laboratorio.local

interface fastEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 ip access-group SSH-ADMIN in
 no shutdown

interface fastEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 ip access-group GUEST-FILTER in
 no shutdown

interface fastEthernet0/0.99
 encapsulation dot1Q 99
 ip address 192.168.99.1 255.255.255.0
 no shutdown

ip access-list extended GUEST-FILTER
 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.20.0 0.0.0.255 192.168.99.0 0.0.0.255
 permit ip any any

ip access-list extended SSH-ADMIN
 permit tcp host 192.168.10.50 192.168.99.0 0.0.0.255 eq 22
 deny   tcp 192.168.10.0 0.0.0.255 192.168.99.0 0.0.0.255 eq 22
 permit ip any any

crypto key generate rsa modulus 1024
ip ssh version 2

username admin secret cisco123

line vty 0 4
 login local
 transport input ssh


## ⚙️ Pruebas

Ping desde VLAN 20 hacia VLAN 10 → ❌ Bloqueado

Ping desde VLAN 20 hacia VLAN 99 → ❌ Bloqueado

SSH desde 192.168.10.50 → 192.168.99.1 → ✅ Permitido 
(ssh -l admin 192.168.99.1)

SSH desde otro PC en VLAN 10 → 192.168.99.1 → ❌ Bloqueado


