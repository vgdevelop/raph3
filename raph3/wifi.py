# ===================================================== #
# ================== WIFI CONTROLLER ================== #
# ===================================================== #
# Default AP Credentials ============================== #
# Connection Handdling ================================ #
# ===================================================== #

import network
import utime
import usocket

# MESSAGE HANDDLING
DMC = True

# AP SERVER HANDDLING
AP_SERVER_SSID = "Raph"
AP_SERVER_PASSWORD = "RaphRaph"

# GLOBAL VARIABLES
IP_ADDRESS = ""
CONNECTING_TIME = 10

NETWORKS = []

# Funcion de Stream en modo AP
def stream(ssid = AP_SERVER_SSID, password = AP_SERVER_PASSWORD):
    try:
        wf = network.WLAN(network.AP_IF)
        
        if not wf.active():
            wf.config(ssid=ssid, password=password)
            wf.active(True)
            if DMC: print("Punto de Acceso establecido en: "+str(wf.ifconfig()[0]))
        else:
            if DMC: print("Punto de Acceso ya establecido en: "+str(wf.ifconfig()[0]))
            wf.active(False)
            utime.sleep_ms(100)
            wf.config(ssid=ssid, password=password)
            wf.active(True)
            if DMC: print("Punto de Acceso establecido en: "+str(wf.ifconfig()[0]))

        global IP_ADDRESS
        IP_ADDRESS = str(wf.ifconfig()[0])

        return True
    except Exception as e:
        if DMC: print("Error: "+str(e))

def stop():
    wf = network.WLAN(network.AP_IF)
    if wf.active():
        wf.active(False)
        if DMC: print("Punto de Acceso detenido")
    else:
        if DMC: print("El Punto de Acceso no esta activo")

# Escanear redes WiFi y las almacena en la global NETWORKS
def scan():
    wf = network.WLAN(network.STA_IF)
    last_status = wf.active()
    if not wf.active():
        wf.active(True)

    global NETWORKS
    NETWORKS.clear()

    redes = wf.scan()

    for red in redes:
        NETWORKS.append(red[0].decode("utf-8"))

    wf.active(last_status)

    return NETWORKS

# Conectar a una red WiFi
def connect(ssid = AP_SERVER_SSID, password = AP_SERVER_PASSWORD):
    counter = CONNECTING_TIME
    time = utime.time()
    wf = network.WLAN(network.STA_IF)

    if not wf.active():
        wf.active(True)
    else:
        wf.active(False)
        utime.sleep_ms(100)
        wf.active(True)

    wf.connect(ssid, password)

    while not wf.isconnected() and utime.time() < time + counter:
        print('Conectando a la red WiFi...')
        utime.sleep(1)

    if wf.isconnected():
        if DMC: print("Conectado a "+ssid+" con el IP: "+str(wf.ifconfig()[0]))
        global IP_ADDRESS
        IP_ADDRESS = str(wf.ifconfig()[0])
        return True
    else:
        if DMC: print("No se pudo conectar a "+ssid)
        return False

def is_connected():
    wf = network.WLAN(network.STA_IF)
    return wf.isconnected()

def test():

    wf = network.WLAN(network.STA_IF)
    wf.active(True)
    wf.connect('Domotica_IA_Raph003', 'Tatenoyuya$Raph')
    while not wf.isconnected():
        print('Connecting to WiFi...')
        utime.sleep(1)
    print(wf.ifconfig()[0])

    s = usocket.socket()
    s.bind((str(wf.ifconfig()[0]), 2020))
    s.listen(5)
    print("Listening on", str(wf.ifconfig()[0]))
    step1 = True
    while step1:
        (conn, addr) = s.accept()
        print("Connection from", addr)
        print("Received:", conn.recv(1024).decode("utf-8"))
        step2 = True
        while step2:
            mensaje = conn.recv(1024).decode("utf-8")
            if not mensaje:
                step2 = False
            elif mensaje == "end":
                step1 = False
                step2 = False
                print("Received:", mensaje)
            else:
                print("Received:", mensaje)
        
        conn.close()
    s.close()
    print("Socket closed")


    # s = usocket.socket()
    # s.bind((str(wf.ifconfig()[0]), 2020))
    # s.listen(5)
    # print("Listening on", str(wf.ifconfig()[0]))
    # step1 = True
    # while step1:
    #     (conn, addr) = s.accept()
    #     print("Connection from", addr)
    #     print("Received:", conn.recv(1024).decode("utf-8"))
    #     step2 = True
    #     while step2:
    #         mensaje = conn.recv(1024).decode("utf-8")
    #         if not mensaje:
    #             step2 = False
    #         elif mensaje == "end":
    #             step1 = False
    #             step2 = False
    #             print("Received:", mensaje)
    #         else:
    #             print("Received:", mensaje)
        
    #     conn.close()
    # s.close()
    # print("Socket closed")

def getAddress():
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    global IP_ADDRESS
    
    if sta_if.active(): 
        return str(sta_if.ifconfig()[0])
    elif ap_if.active(): 
        return str(sta_if.ifconfig()[0])
    else:
        return IP_ADDRESS
