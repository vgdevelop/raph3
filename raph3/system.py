# ===================================================== #
# =================== RAPH Physical =================== #
# ===================================================== #
# Data Adquiring ====================================== #
# Data Store ========================================== #
# Execution Handling ================================== #
# Status Upgrading ==================================== #
# ===================================================== #

from machine import Pin, ADC, RTC
import utime
import asyncio
import json

# CONFIGURATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
RESET_PIN = 6
MODE = False
NAME = "Dispositivo"
INPUTS = []
OUTPUTS = []
SERVER = {"port": "80", "domain": "192.168.4.1", "name": "raph", "protocol": "http"}
CONNECTION = "none"
TOKEN = "YourTokenHere"
EXCEPTION_TIME = 10
CLIENT = {"time_sync": 10, "scope": "http://192.168.0.100"}
RESET_TIME = 10
ALARMS = []
NETWORK = "wan"
CORS = []
DEVICES = []

# FILE SYSTEM <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
FILE_RAPH3_PATH = "/raph3/" # RAPH3 PATH
FILE_SYSTEM_PATH = "/raph3/files/" # FILE SYSTEM PATH
FILE_DEFAULT_PATH = "/raph3/default/" # FILE DEFAULT PATH
FILE_TEMPLATE_PATH = "/raph3/templates/" # FILE TEMPLATE PATH

CONFIG_FILE = "/raph3/files/config.json"
STATUS_FILE = "/raph3/files/status.json"
WIFI_FILE = "/raph3/files/wifi.json"
SENSORS_FILE = "/raph3/files/sensors.json"
OUTPUTS_FILE = "/raph3/files/outputs.json"
ACTIONS_FILE = "/raph3/files/actions.json"
TIMESTAMP_FILE = "/raph3/files/timestamp.json"
CORS_FILE = "/raph3/files/cors.json"
ALARMS_FILE = "/raph3/files/alarms.json"
DEVICES_FILE = "/raph3/files/devices.json"

# GLOBALS HANDLER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

SENSORS = [] # Lista de los tipos de sensores
ACTIONS = [] # Lista de las acciones
STATUS = {} # Estado del sistema
WIFI_CREDENTIALS = {} # Configuracion de la red wifi
IP_ADDRESS = ""

TIMESTAMP = {} 

# STAUTS HANDLER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

INPUT_VALUES = [] # Lista de los valores de las entradas
OUTPUT_VALUES = [] # Lista de los valores de las salidas

# ACCESS POINT VARIABLES
AP_NAME = "Raph3"
AP_DOMAIN = "192.168.3.1"
AP_TEMPLATE_PATH = "ap_templates"
APP_TEMPLATE_PATH = "app_templates"



# DEVELOPMENT MESSAGES
DME = True
DMM = True
DMS = True
DMA = True


DMD = True

from machine import Pin
PIN_RESET_OUT = 0 # GPIO - OUT - RESET
PIN_RESET_IN = 1 # GPIO - IN - RESET
PIN_LED_STATUS = 2 # GPIO - OUT - LED STATUS

LED_STATUS = Pin(PIN_LED_STATUS, Pin.OUT) # LINK - LED STATUS
RESET_LINK = Pin(PIN_RESET_OUT,Pin.OUT) # LINK - RESET OUT
RESET_BUTTON = Pin(PIN_RESET_IN,Pin.IN) # LINK - RESET IN

# def loadJson(file):
    #     try:
    #         with open(file, "r") as f:
    #             data = json.load(f)
    #             f.close()
    #         if checkJson(data):
    #             return data
    #         else:
    #             if DME: print("Error: el archivo "+file+" no es un archivo JSON valido.")
    #             return False
    #     except Exception as e:
    #         if DME: print("Error: El archivo "+file+" no existe.")
    #         return False

def saveJson(file, data):
    try:
        valid = checkJson(data)
        if valid:
            with open(FSP+file+".json", "w") as f:
                json.dump(data, f)
                f.close()
                return True
        else:
            if DME: print("Error: el argumento no es un archivo JSON valido.")
            return False

    except Exception as e:
        if DME: print("Error al guardar archivo "+file)
        return False

def checkJson(data):
    try:
        json.loads(data)
        return True
    
    except Exception as e:
        if DME: print("Error: El archivo no es un archivo JSON valido.")
        return False

# Obtiene los tipos de sensores disponibles en sensors.json
def getSensorTypes():
    if DMM: print("Obteniendo tipos de sensores...")
    try:
        with open(SENSORS_FILE, "r") as f:
            data = json.load(f)
            f.close()
        return data
    except Exception as e:
        if DME: print("Error: No se encuentra el archivo de Sensores.")
        return False

def getValues():
    if DMM: print("Checkeando valores de entradas...")

    try:
        global INPUT_VALUES
        INPUT_VALUES.clear()

        for index, INPUT in enumerate(INPUTS):
            if SENSORS[INPUT["type"]]["type"] == "adc":
                value = ADC(INPUT["port"]).read_u16()
            else:
                io = Pin(INPUT["port"], Pin.IN).value()
                if io:
                    value = 1
                else:
                    value = 0 
                
            math = SENSORS[INPUT["type"]]["math"]
            replaced_value = math.replace("value", str(value))
            evaluation = eval(replaced_value)

            INPUT_VALUES.append(evaluation)

        if DMM: print("Valores de entradas adquiridos correctamente")

        return INPUT_VALUES

    except Exception as e:
        if DME: print("Error al configurar los valores de las entradas.")
        if DMS: print(e)
        return False

def setStatus(digitals):
    try:
        status_now = getStatus()
        
        if len(digitals) == len(status_now):

            for index, digital in enumerate(digitals):  
                if status_now[index] == 0 and digital == 1:
                    Pin(OUTPUTS[index]["port"], Pin.OUT).value(1)
                elif status_now[index] == 1 and digital == 0:
                    Pin(OUTPUTS[index]["port"], Pin.OUT).value(0)

            return True
        else:
            print("Error en setStatus: El numero de digitales no coincide con el de salidas.")
            return False

    except Exception as e:
        if system.DMM: print("Error en setStatus:", e)
        return False



def getStatus():
    if DMM: print("Obteniendo estado de salidas...")

    try:
        global OUTPUT_VALUES
        OUTPUT_VALUES.clear()

        for OUTPUT in OUTPUTS:
            value = Pin(OUTPUT["port"], Pin.OUT).value()
            OUTPUT_VALUES.append(value)

        if DMM: print("Valores de salidas adquiridos correctamente")

        return OUTPUT_VALUES

    except Exception as e:
        if DME: print("Error al configurar los valores de las salidas.")
        return False

# UTILIDADES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Funcion de restauracion de archivos de sistema desde respaldo
def restore(file):
    try:
        with open(FILE_DEFAULT_PATH+file+".bak", "r") as f:
            data = json.load(f)
            f.close()

        try:
            with open(FILE_SYSTEM_PATH+file+".json", "w") as f:
                json.dump(data, f)
                f.close()        

            if DMM: print("Archivo "+file+" restaurado correctamente.")
            return True
        
        except Exception as e:
            # Si ocurre un error inesperado en el Archivo Original
            if DME: print("Error al restaurar archivo original "+file)
            return False
                
    except Exception as e:
        # Si ocurre algun otro error no controlado en el archivo de respaldo.
        if DME: print("Error al restaurar archivo "+file)
        return False

# Carga la configuracion del sistema establecida en el archivo config.json
def loadConfiguration():
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            f.close()
        
        global INPUTS, OUTPUTS, MODE, NAME, SERVER, CONNECTION, TOKEN, EXCEPTION_TIME, CLIENT, RESET_TIME

        if cfg.get("inputs"): INPUTS = cfg["inputs"]
        if cfg.get("outputs"): OUTPUTS = cfg["outputs"]
        if cfg.get("mode"): MODE = cfg["mode"]
        if cfg.get("name"): NAME = cfg["name"]
        if cfg.get("server"): SERVER = cfg["server"]
        if cfg.get("connection"): CONNECTION = cfg["connection"]
        if cfg.get("token"): TOKEN = cfg["token"]
        if cfg.get("exception_time"): EXCEPTION_TIME = cfg["exception_time"]
        if cfg.get("client"): CLIENT = cfg["client"]
        if cfg.get("reset_time"): RESET_TIME = cfg["reset_time"]

        return True
        
    except Exception as e:
        if DME: print("Error al cargar la configuracion.")
        if DME: print("Intentando restaurar archivos de configuracion...")
        #if checkJson():
        res = restore("config")
        if res: ld = loadConfiguration()
        if ld: return True
        return False

# Carga la lista de sensores disponibles desde el archivo sensors.json
def loadSensors():
    try:
        with open(SENSORS_FILE, "r") as f:
            data = json.load(f)
            f.close()
        
        global SENSORS
        SENSORS = data

        return True
        
    except Exception as e:
        if DME: print("Error al cargar los sensores.")
        if DME: print("Intentando restaurar archivos de sensores...")
        res = restore("sensors")
        if res: ld = loadSensors()
        if ld: return True
        return False

# Carga las acciones asignadas al dispositivo desde el archivo actions.json
def loadActions():
    try:
        with open(ACTIONS_FILE, "r") as f:
            data = json.load(f)
            global ACTIONS
            ACTIONS = data
            f.close()
        return True
        
    except Exception as e:
        if DME: print("Error al cargar las acciones. Se restaurara el archivo de acciones.")
        rs = restore("actions")
        if rs: ld = loadActions()
        if ld: return True
        return False

# Carga el estado del sistema desde el archivo status.json
def loadStatus():
    try:
        with open(STATUS_FILE, "r") as f:
            data = json.load(f)
            global STATUS
            STATUS = data
            f.close()
        return True
        
    except Exception as e:
        if DME: print("Error al cargar el estado del sistema. Se restaurara el archivo de estado.")
        rs = restore("status")
        if rs: ld = loadStatus()
        if ld: return True
        return False

# Cargo la configuracion de red wifi desde el archivo wifi.json
def loadWifi():
    try:
        with open(WIFI_FILE, "r") as f:
            data = json.load(f)
            global WIFI_CREDENTIALS
            WIFI_CREDENTIALS = data
            f.close()
        return True
        
    except Exception as e:
        if DME: print("Error al cargar la configuracion de red wifi.")
        if DME: print("Intentando restaurar archivos de configuracion de red wifi...")
        res = restore("wifi")
        if res: ld = loadWifi()
        if ld: return True
        return False

def loadCors():
    try:
        with open(CORS_FILE, "r") as f:
            data = json.load(f)
            global CORS
            CORS = data
            f.close()
        return True
        
    except Exception as e:
        if DME: print("Error al cargar la configuracion de Origenes Permitidos")
        if DME: print("Intentando restaurar archivos de configuracion de Origenes...")
        res = restore("cors")
        if res: ld = loadCors()
        if ld: return True
        return False

# Carga las alarmas del sistema
def loadAlarms():
    try:
        with open(ALARMS_FILE, "r") as f:
            data = json.load(f)
            global ALARMS
            ALARMS = data
            f.close()
        return True
        
    except Exception as e:
        if DME: print("Error al cargar las alarmas del sistema.")
        if DME: print("Intentando restaurar archivos de alarmas...")
        res = restore("alarms")
        if res: ld = loadAlarms()
        if ld: return True
        return False

def loadDevices():
    try:
        with open(DEVICES_FILE, "r") as f:
            data = json.load(f)
            global DEVICES
            DEVICES = data
            f.close()
        return True
        
    except Exception as e:
        if DME: print("Error al cargar los dispositivos en la red.")
        res = restore("devices")
        if res: ld = loadDevices()
        if ld: return True
        return False

# Funccion de Inicio del sistema
def start():
    if DMM: print("Iniciando sistema...")

    try:
        # Carga de la hora del dispositivo
        time = loadCurrentTime()
        # Carga de configuracion
        cfg = loadConfiguration()
        # Carga la lista de sensores disponibles
        sns = loadSensors()
        # Carga la lista de acciones asignadas al dispositivo
        act = loadActions()
        # Carga el Estado del Sistema, El modo en que se encuentra
        sts = loadStatus()
        # Carga la configuracion de red wifi
        wfi = loadWifi()
        # Carga de Network
        dvs = loadDevices()
        # Carga CORS
        # cors = loadCors()
        
        if cfg and sns and act and sts and wfi and dvs and time:
            if DMM: print("Sistema iniciado correctamente.")
            return True
        else:
            if DME: print("Error al iniciar el sistema.")
            return False
        
    except Exception as e:
        if DME: print("Error al iniciar el sistema.")
        if DME: print(e)
        return False

# Reinicio del Sistema
def restart():
    if DMM: print("Reiniciando sistema...")

    try:
        if save():
            if DMM: print("Guardado correctamente.")
            if DMM: print("Reiniciando...")
            import machine
            machine.reset()
            return True
        else:
            if DME: print("Error al guardar el estado del sistema.")
            return False

    except Exception as e:
        if DME: print("Error al reiniciar el sistema.")
        if DME: print(e)
        return False

def save():
    if DMM: print("Guardando estado del sistema...")

    CONFIGURATION = {}

    try:
        CONFIGURATION["inputs"] = INPUTS
        CONFIGURATION["outputs"] = OUTPUTS
        CONFIGURATION["mode"] = MODE
        CONFIGURATION["name"] = NAME
        CONFIGURATION["server"] = SERVER
        CONFIGURATION["connection"] = CONNECTION
        CONFIGURATION["token"] = TOKEN
        CONFIGURATION["exception_time"] = EXCEPTION_TIME
        CONFIGURATION["client"] = CLIENT
        CONFIGURATION["reset_time"] = RESET_TIME

        with open(CONFIG_FILE, "w") as f:
            json.dump(CONFIGURATION, f)
            f.close()

        with open(STATUS_FILE, "w") as f:
            json.dump(STATUS, f)
            f.close()

        with open(SENSORS_FILE, "w") as f:
            json.dump(SENSORS, f)
            f.close()

        with open(ACTIONS_FILE, "w") as f:
            json.dump(ACTIONS, f)
            f.close()

        with open(WIFI_FILE, "w") as f:
            json.dump(WIFI_CREDENTIALS, f)
            f.close()

        with open(TIMESTAMP_FILE, "w") as f:
            json.dump(TIMESTAMP, f)
            f.close()

        with open(ALARMS_FILE, "w") as f:
            json.dump(ALARMS, f)
            f.close()

        with open(DEVICES_FILE, "w") as f:
            json.dump(DEVICES, f)
            f.close()

        if DMM: print("Estado del sistema guardado correctamente.")
        return True

    except Exception as e:
        if DME: print("Error al guardar el estado del sistema.")
        if DME: print(e)
        return False

def toggleOutput(index):
    try:
        OUTPUT = OUTPUTS[index]
        value = not Pin(OUTPUT["port"], Pin.OUT).value()
        Pin(OUTPUT["port"], Pin.OUT).value(value)
        return True
    except Exception as e:
        if DME: print("Error al cambiar el estado de la salida.")
        return False

def holdOutput(index, hold):
    try:
        OUTPUTS[index]["hold"] = int(hold)
        return True
    except Exception as e:
        if DME: print("Error al cambiar el estado de holding.")
        return False

def wait(ms):
    utime.sleep_ms(ms)

def getTime():
    try:
        with open(TIMESTAMP_FILE, 'r') as f:
            data = json.load(f)
            f.close()
    
        return data
    except Exception as e:
        if DME: print("Error al obtener la hora del sistema.")
        return False

def activateOutput(id):
    Pin(int(OUTPUTS[id]["port"]), Pin.OUT).value(1)

def deactivateOutput(input):
    Pin(int(OUTPUTS[id]["port"]), Pin.OUT).value(0)

def loadCurrentTime():
    try:
        data = getTime()
        if data:
            stored = utime.mktime((int(data["year"]), int(data["month"]), int(data["day"]), int(data["hour"]), int(data["minute"]), 0, 0, 0))
            runing = utime.time()

            p_stored = utime.localtime(stored)
            p_runing = utime.localtime(runing)

            if DMM: print("El tiempo actual es: " + str(runing) + " | " + str(p_runing) +"\nEl Tiempo Guardado es: " + str(stored) + " | " + str(p_stored))

            if runing < stored:
                if DMM: print("Actualizando tiempo")
                rtc = RTC()
                rtc.datetime((int(p_stored[0]), int(p_stored[1]), int(p_stored[2]), 0, int(p_stored[3]), int(p_stored[4]), 2 , 0))

            return True
        else:
            res = restore("timestamp")
            if res: ld = loadCurrentTime()
            if ld: return True
            return False

    except Exception as e:
        if DME: print("Error al obtener la hora del sistema.")
        return False

def storeCustomTime(date):
    try:
        if date.get("year") and date.get("month") and date.get("day") and date.get("hour") and date.get("minute") and date.get("second"):      
            rtc = RTC()
            rtc.datetime((int(date["year"]), int(date["month"]), int(date["day"]), 0, int(date["hour"]), int(date["minute"]), int(date["second"]), 0))

            if DMM: print("Fecha y hora establecida correctamente." + str(utime.time()))

            with open(TIMESTAMP_FILE, "w") as f:
                json.dump(date, f)
                f.close()
            
            if DMM: print("Hora almacenada.")

            global TIMESTAMP
            TIMESTAMP = date

            return True
        
        else:
            return False

    except Exception as e:
            if DME: print("Error al obtener la hora del sistema.")
            return False