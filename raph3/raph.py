# ===================================================== #
# =================== RAPH APP MAIN =================== #
# ===================================================== #
# Control de Aplicacion Web =========================== #
# Executon Control ==================================== #
# ===================================================== #

from raph3 import system
from raph3 import wifi
from raph3.action import *
from raph3.action import Action
from machine import Pin, ADC, RTC
import asyncio
import utime
import urequests

from microdot.microdot import Microdot, Response, send_file, redirect
from microdot.cors import CORS

app = Microdot()

# WEB APLICATION STARTING SYSTEM <============================ #
def run():
    try:
        if system.start():
            # Comprubea el modo de inicio (AP / STA) dependiendo de las credenciales ingresadas
            if system.WIFI_CREDENTIALS.get("ssid") and system.WIFI_CREDENTIALS["ssid"]:
                if system.DMM: print("Se detectaron credenciales WiFi.")
                if wifi.connect(system.WIFI_CREDENTIALS["ssid"], system.WIFI_CREDENTIALS["password"]):
                    if system.DMM: print("Stremeando en la Red.")
                else:
                    if system.DMM: print("Error en la conexion WiFi.")
                    if wifi.stream():
                        if system.DMM: print("Stremeando en modo AP")
            else:
                if system.DMM: print("No se detectaron credenciales WiFi.")
                if wifi.stream():
                    if system.DMM: print("Stremeando en modo AP")

            setCors()
            
            startup_routes()
            shared_routes()

            resources_routes()

            return True
        
        
        return False

    except Exception as e:
        if system.DMM: print("Error al conectar o crear la red WiFi:", e)
        return False

def stop():
    app.shutdown()

# WEB ROUTES FOR API REST <=================================== #
def startup_routes():

    ########## DATA GET ##########

    # API - Devices in Network
    @app.get("/api/network")
    async def get_network(request):
        await asyncio.sleep(1)
        return system.DEVICES
    
    # API - Device Status
    @app.get("/api/status")
    async def status(request):
        await asyncio.sleep(1)
        inputs_data = []
        outputs_data = []

        inputs_values = system.getValues()
        outputs_values = system.getStatus()

        # SENSORS - Sensor List
        for index, sensor in enumerate(system.INPUTS):
            sensor["id"] = index
            sensor["value"] = inputs_values[index]
            sensor["name"] = system.SENSORS[sensor["type"]]["name"]
            sensor["model"] = system.SENSORS[sensor["type"]]["model"]
            inputs_data.append(sensor)
        
        # OUTPUTS - Output List
        for index, output in enumerate(system.OUTPUTS):
            output["value"] = outputs_values[index]
            output["name"] = output["type"]
            output["id"] = index
            outputs_data.append(output)

        return json.dumps({"name": system.NAME, "server": system.SERVER, "connection": system.CONNECTION, "token": system.TOKEN, "network": system.NETWORK, "inputs": inputs_data, "outputs": outputs_data})
       
    # API - Actions List
    @app.get("/api/actions")
    async def actions(request):
        await asyncio.sleep(1)
        return json.dumps(system.ACTIONS)

    # API - Identifier
    @app.get("/api/ping")
    async def api_ping(request):
        await asyncio.sleep(1)
        return json.dumps({"device": "raph3", "name": system.NAME, "token": system.TOKEN, "ip": system.IP_ADDRESS})

    # API - Alarms Get
    @app.get("/api/alarms")
    async def alarms(request):
        await asyncio.sleep(1)
        return json.dumps(system.ALARMS)

    # API - Test
    @app.get("/api/test")
    async def apitest(request):
        await asyncio.sleep(1)

        data = getApiData("http://192.168.1.100")

        return json.dumps(data)

    ########## DATA POST ##########

    # API - Network Configuration
    @app.post("/api/wifi")
    async def wifi(request):
        try:
            await asyncio.sleep(1)
            if request.form.get("ssid") and request.form.get("password"):
                system.WIFI_CREDENTIALS["ssid"] = request.form.get("ssid")
                system.WIFI_CREDENTIALS["password"] = request.form.get("password")
                system.save()
                if system.DMM: print("Credenciales de WiFi Guardadas...")
                return json.dumps({"status": "ok"})
            else:
                return json.dumps({"status": "error"})
        except Exception as e:
            if system.DMM: print("Error en wifi:", e)
            return False

    # API - Device Timestamp
    @app.get("/api/timestamp")
    async def timestampGet(request):
        await asyncio.sleep(1)
        date = utime.localtime()
        return json.dumps({"year": int(date[0]), "month": int(date[1]), "day": int(date[2]), "hour": int(date[3]), "minute": int(date[4]), "second": int(date[5])})


    # POST - Ruta del editor de acciones
    @app.post("/editor")
    async def editor(request):
        await asyncio.sleep(1)
        ac = {}

        # Dispositivo unico de escritura
        ac["device_write"] = system.TOKEN
        
        if request.form.get("value_end"):
            ac["operator_end"] = "<"
        
        # Dispositivo unico de Lectura
        if request.form.get("device_read"):
            ac["device_read"] = request.form.get("device_read")
        else:
            ac["device_read"] = system.TOKEN

        # Nombre
        if request.form.get("name"): ac["name"] = request.form.get("name")

        # digital_write
        if request.form.get("digital_write"): ac["digital_write"] = request.form.get("digital_write")

        # Analog Read
        if request.form.get("analog_read"): ac["analog_read"] = request.form.get("analog_read")

        # Operator Start
        if request.form.get("operator_start"): ac["operator_start"] = request.form.get("operator_start")

        # Value Start
        if request.form.get("value_start"): ac["value_start"] = request.form.get("value_start")

        # Operator End
        if request.form.get("operator_end"): ac["operator_end"] = request.form.get("operator_end")

        # Value End
        if request.form.get("value_end"): ac["value_end"] = request.form.get("value_end")

        if request.form.get("api_url") and request.form.get("api_target") and request.form.get("api_operator") and request.form.get("api_value"):
            ac["api_url"] = request.form.get("api_url")
            ac["api_target"] = request.form.get("api_target")
            ac["api_operator"] = request.form.get("api_operator")
            ac["api_value"] = request.form.get("api_value")

        if request.form.get("duration") and request.form.get("wait"):
            ac["duration"] = request.form.get("duration")
            ac["wait"] = request.form.get("wait")

        # Sobreescrituras
        if request.form.get("date_start"):
            ac["date_start"] = {"year": int(request.form.get("date_start").split("-")[0]), "month": int(request.form.get("date_start").split("-")[1]), "day": int(request.form.get("date_start").split("-")[2])}

        if request.form.get("date_end"):
            ac["date_end"] = {"year": int(request.form.get("date_end").split("-")[0]), "month": int(request.form.get("date_end").split("-")[1]), "day": int(request.form.get("date_end").split("-")[2])}
        
        if request.form.get("hour_start"):
            ac["hour_start"] = {"hour": int(request.form.get("hour_start").split(":")[0]), "minute": int(request.form.get("hour_start").split(":")[1])}
        
        if request.form.get("hour_end"):
            ac["hour_end"] = {"hour": int(request.form.get("hour_end").split(":")[0]), "minute": int(request.form.get("hour_end").split(":")[1])}
        

        # Comprobacion de Dias
        if request.form.get("lunes") or request.form.get("martes") or request.form.get("miercoles") or request.form.get("jueves") or request.form.get("viernes") or request.form.get("sabado") or request.form.get("domingo"):
            ac["days"] = []
            if request.form.get("lunes"): ac["days"].append(0)
            if request.form.get("martes"): ac["days"].append(1)
            if request.form.get("miercoles"): ac["days"].append(2)
            if request.form.get("jueves"): ac["days"].append(3)
            if request.form.get("viernes"): ac["days"].append(4)
            if request.form.get("sabado"): ac["days"].append(5)
            if request.form.get("domingo"): ac["days"].append(6)            

        action = Action()
        action.fill(ac)
        action.save()

        system.loadActions()

        return redirect("/")

        # if form_type:
        #     form["type"] = form_type
        #     form["active"] = 1 
        #     ACTIONS.append(form)
        #     with open(ACTIONS_FILE, "w") as f:
        #         json.dump(ACTIONS, f)
        #         f.close()

        #     with open(AP_TEMPLATE_PATH + "/app.css", "r") as f:
        #         css = f.read()
        #         f.close()
        
    @app.post("/api/network")
    async def network(request):
        print("NETWORK!!!")
        await asyncio.sleep(1)
        data_array = request.json

        if isinstance(data_array, list):
            need_update = False
            # Procesa cada objeto en el array
            for item in data_array:
                if item.get('name') and item.get('token') and item.get('ip'):
                    device_check = getDeviceByToken(item.get('token'))

                    if device_check is False:
                        if "id" in item: del item["id"]
                        system.DEVICES.append(item)
                        need_update = True
                        if system.DMD: print("Dispositivo "+str(item.get("name")+" Agregado"))

                    else:
                        old = system.DEVICES[device_check["id"]]
                        
                        if item.get('name') != old["name"] or item.get('token') != old["token"] or item.get('ip') != old["ip"]:
                            if "id" in item: del item["id"]

                            system.DEVICES[device_check["id"]] = item
                            need_update = True
                            if system.DMD: print("Dispositivo "+str(item.get("name")+" Actualizado"))
            
            if need_update: system.save()

            return json.dumps({"status": "success", "message": "Correcto"})
        else:
            return json.dumps({"status": "error", "message": "Formato Incorrecto"})

    # API - Ruta de activacion / Desactivacion de Acciones
    @app.post("/api/action/toggle")
    async def action_toggle(request):
        await asyncio.sleep(1)
        if request.form.get("id"):
            action = Action()
            if action.load(int(request.form.get("id"))):
                if action.toggle(int(request.form.get("id"))):
                    system.loadActions()
                    return json.dumps({"status": "success", "message": "Accion Activada"})

        return json.dumps({"status": "error", "message": "Error al activar la Accion"})

        # API - Ruta de activacion / Desactivacion de Acciones
    
    # API - Ruta de Eliminacion de Accion
    @app.post("/api/action/delete")
    async def action_delete(request):
        await asyncio.sleep(1)

        # Comprobacion si la accion indicada existe.
        if request.form.get("id"):
            if system.ACTIONS[int(request.form.get("id"))]:

                system.ACTIONS.pop(int(request.form.get("id")))

                with open(system.ACTIONS_FILE, "w") as f:
                    json.dump(system.ACTIONS, f)
                    f.close()

            else:
                return json.dumps({"status": "error", "message": "La acción indicada no existe."})

        return json.dumps({"status": "error", "message": "Debe especificar una accion"})
            
    # API - Ruta de Holding
    @app.post("/api/output/hold")
    async def output_hold(request):
        await asyncio.sleep(1)
        if system.DMD: print("Señal de Hold Detectada desde la WEB...")
        
        if request.form.get("id") and request.form.get("hold"):
            if system.holdOutput(int(request.form.get("id")), int(request.form.get("hold"))):
                return json.dumps({"status": "success", "message": "Modificaciones de Holding seteadas Correctamente"})
            else:
                return json.dumps({"status": "error", "message": "Se requieren los enteros de ID del dispositivo y HOLD de estado"})

        return json.dumps({"status": "error", "message": "Error al activar el Output"})

    # API - Ruta de Activacion / Desactivacion de Outputs
    @app.post("/api/output/toggle")
    async def output_toggle(request):
        await asyncio.sleep(1)
        if request.form.get("id"):
            if system.toggleOutput(int(request.form.get("id"))):
                if system.DMD: print("Señal de Toggle Detectada desde la WEB...")
                if system.getStatus():
                    return json.dumps({"status": "success", "message": "Output Activado"})

        return json.dumps({"status": "error", "message": "Error al activar el Output"})

    @app.post("/mode")
    async def mode(request):
        await asyncio.sleep(1)

        if request.form.get("mode"):
            if request.form.get("mode") == "maker":
                system.STATUS["mode"] = "maker"
                system.restart()
            elif request.form.get("mode") == "editor":
                system.STATUS["mode"] = "startup"
                system.restart()
            elif request.form.get("mode") == "standalone":
                system.STATUS["mode"] = "standalone"
                system.restart()

    @app.post("/api/timestamp")
    async def timestampPost(request):
        await asyncio.sleep(1)
        try:
            if request.form.get("date_now") and request.form.get("time_now"):
                string_date = request.form.get("date_now").split("-")
                string_time = request.form.get("time_now").split(":")
                date = {"year": int(string_date[0]), "month": int(string_date[1]), "day": int(string_date[2]), "hour": int(string_time[0]),"minute": int(string_time[1]), "second": int(string_time[2])}
                
                if system.storeCustomTime(date):
                    return json.dumps({"status": "ok", "message": "Fecha almacenada correctamente"})
                else:
                    return json.dumps({"status": "error", "message": "Ha ocurrido un error procesando la fecha"})

            else:
                return json.dumps({"status": "error", "message": "Formato incorrecto"})
        except Exception as e:
            if system.DMM: print("Error en timestampPost:", e)
            return False

    # API - Configuration
    @app.post("/api/configuration")
    async def configuration(request):
        await asyncio.sleep(1)
        # Requests: name, exception_time, reset_time, mode, domain, port protocol, time_sync, scope
        if request.form.get("name"): system.NAME = request.form.get("name")
        if request.form.get("exception_time"): system.EXCEPTION_TIME = request.form.get("exception_time")
        if request.form.get("reset_time"): system.RESET_TIME = request.form.get("reset_time")
        if request.form.get("mode"): system.MODE = request.form.get("mode")
        if request.form.get("domain"): system.SERVER["domain"] = request.form.get("domain")
        if request.form.get("port"): system.SERVER["port"] = request.form.get("port")
        if request.form.get("protocol"): system.SERVER["protocol"] = request.form.get("protocol")
        if request.form.get("time_sync"): system.CLIENT["time_sync"] = request.form.get("time_sync")
        if request.form.get("scope"): system.CLIENT["scope"] = request.form.get("scope")
        if request.form.get("token"): system.TOKEN = request.form.get("token")

        system.save()

        return redirect("/")

    # API - Configuration
    @app.post("/api/config")
    async def config(request):
        await asyncio.sleep(1)
        # Requests: name, exception_time, reset_time, mode, domain, port protocol, time_sync, scope
        if request.form.get("name"): system.NAME = request.form.get("name")
        if request.form.get("token"): system.TOKEN = request.form.get("token")

        system.save()

        print("La configuracion del Dispositivo ha cambiado")

        return json.dumps({"status": "success", "message": "Configuracion editada correctamente"})

    # API - Alarms Post
    @app.post("/api/alarms")
    async def alarms(request):
        await asyncio.sleep(1)
        if request.form.get("name") and request.form.get("active") and request.form.get("trigger") and request.form.get("operator") and request.form.get("value") and request.form.get("type"):
            data = {}
            data["name"] = request.form.get("name")
            data["active"] = request.form.get("active")
            data["trigger"] = request.form.get("trigger")
            data["operator"] = request.form.get("operator")
            data["value"] = request.form.get("value")
            data["type"] = request.form.get("type")
            system.ALARMS.append(data)
            system.save()
            return json.dumps({"status": "ok"})
        else:
            return json.dumps({"status": "error"})

# WEB ROUTES FOR RESOURCES <=================================== #

def resources_routes():

    @app.get("/res/sensors")
    async def get_sensors(request):
        await asyncio.sleep(1)
        return system.SENSORS
    
    @app.post("/res/sensors")
    async def post_sensors(request):
        await asyncio.sleep(1)
        sensors_list = []

        data_array = request.json

        if isinstance(data_array, list):
            
            for item in data_array:
                if item.get('name') and item.get('model') and item.get('type') and item.get('math'):
                    sensors_list.append(item)
                else:
                    return json.dumps({"status": "error", "message": "Datos insuficientes o erroneos"})
        
        else:
            return json.dumps({"status": "error", "message": "El formato de la solicitud no es correcto"})


        for index, sensor in enumerate(sensors_list):
            print(str(sensor))

        return json.dumps({"status": "success", "message": "Recurso Sensores modificado Correctamente"})

    @app.post("/res/outputs")
    async def post_outputs(request):
        await asyncio.sleep(1)

        data_array = request.json

        if isinstance(data_array, list):

            outputs_list = []
            
            for item in data_array:

                if item.get('name') and item.get('type') and item.get('port'):
                    outputs_list.append(item)
                else:
                    return json.dumps({"status": "error", "message": "Datos insuficientes o erroneos"})

            return outputs_list
        else:
            return json.dumps({"status": "error", "message": "El Formato de la solicitud es incorrecto"})

    @app.post("/res/inputs")
    async def post_inputs(request):
        await asyncio.sleep(1)

        data_array = request.json

        if isinstance(data_array, list):

            inputs_list = []
            
            for item in data_array:

                if item.get('name') and item.get('type') and item.get('port'):
                    inputs_list.append(item)
                else:
                    return json.dumps({"status": "error", "message": "Datos insuficientes o erroneos"})

            return inputs_list
        else:
            return json.dumps({"status": "error", "message": "El Formato de la solicitud es incorrecto"})

# GUI ROUTES  <=================================== #         
def shared_routes():
    @app.get("/")
    async def index(request):
        await asyncio.sleep(1)
        return send_file(system.FILE_TEMPLATE_PATH+'app.html')

    # CSS Routes

    @app.get("/css/app.css")
    async def appcss(request):
        await asyncio.sleep(1)
        return send_file(system.FILE_TEMPLATE_PATH+'/css/app.css')

    @app.get("/css/grid.css")
    async def gridcss(request):
        await asyncio.sleep(1)
        return send_file(system.FILE_TEMPLATE_PATH+'/css/grid.css')

    # Javascrip Routes

    @app.get("/js/raph.js")
    async def raphjs(request):
        await asyncio.sleep(1)
        return send_file(system.FILE_TEMPLATE_PATH+'/js/raph.js')

    @app.get("/js/form.js")
    async def formjs(request):
        await asyncio.sleep(1)
        return send_file(system.FILE_TEMPLATE_PATH+'/js/form.js')
    
def sendToServer():
    try:
        if system.DMM: print("Enviando datos al servidor...")

        # Envia un mensaje al servidor con los datos actuales en el dispositivo
        # Siempre y cuando los valores establecidos en el json sean los correspondientes.

    except Exception as e:
        if system.DMM: print("Error en sendToServer:", e)

def checkActionDate(action):
    if system.DMM: print("Comprobando si la fecha se encuentra en el rango establecido...")

    try:            
        hour_start = utime.mktime([action["date_start"]["year"], action["date_start"]["month"], action["date_start"]["day"], action["hour_start"]["hour"], action["hour_start"]["minute"], 0, 0, 0])
        hour_end = utime.mktime([action["date_end"]["year"], action["date_end"]["month"], action["date_end"]["day"], action["hour_end"]["hour"], action["hour_end"]["minute"], 0, 0, 0])
    
        diff_start = utime.time() - hour_start
        diff_end = utime.time() - hour_end

        if system.DMM: print("se ejecuta desde: " + str(hour_start) + " hasta " + str(hour_end) + "| Actual: "+ str(utime.time()))
        
        if diff_start >= 0 and diff_end <= 0:
            return True
        

        return False

    except Exception as e:
        if system.DME: print("Error al comprobar si la fecha se encuentra en el rango establecido.")
        return False

def checkActionValue(action):
    if system.DMM: print("Comprobando si el valor se encuentra en el rango establecido...")

    try:
        if action.get("device_read") == system.TOKEN:
            value = system.getValues()[int(action["analog_read"])]
        else:
            print("NIOOOOOOOOOOOOOOOOOOOOOOOOOOO")

        if action.get("operator_start") and action.get("value_start") and not action.get("operator_end") and not action.get("value_end"): 
            if action["operator_start"] == ">":
                if int(value) > int(action["value_start"]):
                    return True
            elif action["operator_start"] == "<":
                if int(value) < int(action["value_start"]):
                    return True
            elif action["operator_start"] == "=":
                if int(value) == int(action["value_start"]):
                    return True

        elif action.get("operator_start") and action.get("value_start") and action.get("operator_end") and action.get("value_end"):
            if action["operator_start"] == ">" and action["operator_end"] == "<":
                if int(value) > int(action["value_start"]) and int(value) < int(action["value_end"]):
                    return True
            elif action["operator_start"] == "<" and action["operator_end"] == ">":
                if int(value) < int(action["value_start"]) and int(value) > int(action["value_end"]):
                    return True            

        return False
        
    except Exception as e:
        if system.DME: print("Error al comprobar si el valor se encuentra en el rango establecido.")
        return False

# Comprueba el dia de la semana con la libreria utime 
def checkActionWeekday(action):
    try:
        if action.get("days"):
            today = utime.localtime()[6]
            if today in action['days']:
                return True
        
        return False

    except Exception as e:
        if system.DME: print("Error al comprobar si el dia se encuentra en el rango establecido.")
        return False

def checkActionTime(action):
    try:
        if system.DMS: print("Comprobando si la hora actual coincide con el rango establecido...")

        if action.get("hour_start") and action.get("hour_end"):

            # Tupple (2024, 8, 27, 18, 26, 19, 1, 240)
            time_now = utime.localtime() # Hora local del dispositivo

            s_hour_start = action["hour_start"]["hour"]
            s_minute_start = action["hour_start"]["minute"]
            s_hour_end = action["hour_end"]["hour"]
            s_minute_end = action["hour_end"]["minute"]   

            # timestamp de la hora actual 
            RTT = utime.mktime(tuple(time_now))
            # timestamp de la hora de inicio indicada
            STS = utime.mktime([time_now[0], time_now[1], time_now[2], s_hour_start, s_minute_start, 0, 0, 0])
            # timestamp de la hora de fin indicada 
            STE = utime.mktime([time_now[0], time_now[1], time_now[2], s_hour_end, s_minute_end, 0, 0, 0])

            if RTT >= STS and RTT <= STE:
                return True
            else:
                return False
    
        else:
            if system.DMS: print("La acción no posee una hora indicada la cual comparar.")
            return False

    except Exception as e:
        if system.DME: print("Error al comprobar si la hora se encuentra en el rango establecido.")
        return False

def setStatus(digitals):
    try:
        status_now = system.getStatus()
        
        if len(digitals) == len(system.OUTPUTS):
            for index, output in enumerate(system.OUTPUTS):

                if digitals[index] == 1 and status_now[index] == 0:
                    Pin(system.OUTPUTS[index]["port"], Pin.OUT).value(1)
                elif digitals[index] == 0 and status_now[index] == 1:
                    Pin(system.OUTPUTS[index]["port"], Pin.OUT).value(0)
            return True
        else:
            return False
    except Exception as e:
        if system.DME: print("Error al establecer el estado de las salidas digitales.")
        return False

async def executeSchedule():
    if system.DMM: print("Ejecutando cronograma...")
    try:
        while True:
            if system.DMS: print("Ejecutando cronograma.\n  Hora de inicio: "+str(utime.localtime()[3])+":"+str(utime.localtime()[4])+":"+str(utime.localtime()[5]))
            if system.DMD: print("Ejecutando cronograma.")

            sync()

            # Configura el estado de las salidas digitales dentro del sistema en estado apagado
            digitals = []
            for output in system.OUTPUTS:
                digitals.append(0)

            for index, action in enumerate(system.ACTIONS):
                print("comprobando acción de: "+action["name"])
                # comprobacion de activacion de estado
                status_now = system.getStatus()

                # Comprobacion y resolucion de excepciones
                # Si la acción posee Duracion
                if action.get("duration") and action.get("wait"):
                    
                    if action.get("last_start"):
                        time_now = utime.time()
                        last_start = utime.mktime(action["last_start"])
                        wait = int(action["wait"]) * 60
                        duration = int(action["duration"]) * 60

                        tn = utime.localtime()


                        # Fix del tiempo de ejecucion despues de desync
                        if time_now > last_start + duration:
                            new_action = system.ACTIONS[index]
                            new_action.pop("last_start")
                            new_action["last_end"] = [tn[0], tn[1], tn[2], tn[3], tn[4], 0, 0, 0]



                        # Si la hora actual del dispositivo es menor a la de cuando se inicio por por primera vez la accion
                        # Significa que el dispositivo se reinicio y posee una hora desactualizada
                        # Restaura los datos de inicio de la accion
                        if time_now < last_start:
                            print("La hora del dispositivo ha disminuido, Restaurando acción")
                            new_action = system.ACTIONS[index]
                            new_action.pop("last_start")
                            system.ACTIONS[index] = new_action
                            system.save()



                    elif action.get("last_end"):
                        print("last_end")
                    else:
                        print("nada")

                # Si la accion se encuentra activa
                if action["active"] and system.OUTPUTS[int(action["digital_write"])]["hold"] == 2:
                    if action["type"] == 10:
                        if system.DMD: print("Testing Type 10")
                        trigger = checkActionDate(action)
                        if trigger:
                            digitals[int(action["digital_write"])] = 1
                    elif action["type"] == 11:
                        if system.DMD: print("Testing Type 11")
                        trigger_date = checkActionDate(action)
                        trigger_value = checkActionValue(action)

                        if trigger_value and trigger_date:
                            digitals[int(action["digital_write"])] = 1               
                    elif action["type"] == 12:
                        if system.DMD: print("Testing Type 12")
                        trigger_date = checkActionDate(action)
                        trigger_value = checkActionValue(action)

                        if trigger_value and trigger_date:
                            digitals[int(action["digital_write"])] = 1
                    elif action["type"] == 13:
                        if system.DMD: print("Testing Type 13")
                        # Si la Accion se esta ejecutando
                        if action.get("last_start"):

                            time_now = utime.time()
                            last_start = utime.mktime(action["last_start"])
                            duration = int(action["duration"]) * 60

                            # Si la hora actual es menor el la hora de inicio + la duración
                            if time_now <= last_start + duration:
                                trigger_date = checkActionDate(action)

                                if trigger_date:
                                    digitals[int(action["digital_write"])] = 1

                        # Si la accion ya se ha ejecutado
                        elif action.get("last_end"):
                            
                            time_now = utime.time()
                            last_end = utime.mktime(action["last_end"])
                            wait = int(action["wait"]) * 60

                            # Si la hora actual es mayor al la hora de fin + el tiempo de espera
                            if time_now >= last_end + wait:
                                trigger_date = checkActionDate(action)

                                if trigger_date:
                                    digitals[int(action["digital_write"])] = 1

                        # Si la accion no se ha ejecutado nunca
                        else:
                            trigger_date = checkActionDate(action)

                            if trigger_date:
                                digitals[int(action["digital_write"])] = 1                                      
                    elif action["type"] == 14 or action["type"] == 15:
                        if system.DMD: print("Testing Type 14 or 15")
                        value = system.getValues()[int(action["analog_read"])]
                        # Si la Accion se esta ejecutando
                        if action.get("last_start"):
                            time_now = utime.time()
                            last_start = utime.mktime(action["last_start"])
                            duration = int(action["duration"]) * 60

                            # Si la hora actual es menor el la hora de inicio + la duración
                            if time_now <= last_start + duration:
                                trigger_date = checkActionDate(action)
                                trigger_value = checkActionValue(action)

                                if trigger_date:
                                    digitals[int(action["digital_write"])] = 1

                        # Si la accion ya se ha ejecutado
                        elif action.get("last_end"):
                            time_now = utime.time()
                            last_end = utime.mktime(action["last_end"])
                            wait = int(action["wait"]) * 60

                            # Si la hora actual es mayor al la hora de fin + el tiempo de espera
                            if time_now >= last_end + wait:
                                trigger_date = checkActionDate(action)
                                trigger_value = checkActionValue(action)

                                if trigger_value and trigger_date:
                                    digitals[int(action["digital_write"])] = 1

                        # Si la accion no se ha ejecutado nunca
                        else:
                            trigger_date = checkActionDate(action)
                            trigger_value = checkActionValue(action)

                            if trigger_value and trigger_date:
                                digitals[int(action["digital_write"])] = 1
                    elif action["type"] == 30 or action["type"] == 31:
                        if system.DMD: print("Testing Type 30 or 31")
                        trigger_value = checkActionValue(action)

                        if trigger_value:
                            digitals[int(action["digital_write"])] = 1
                    elif action["type"] == 32 or action["type"] == 33:
                        if system.DMD: print("Testing Type 32 or 33")
                        # Si la Accion se esta ejecutando
                        if action.get("last_start"):

                            time_now = utime.time()
                            last_start = utime.mktime(action["last_start"])
                            duration = int(action["duration"]) * 60

                            # Si la hora actual es menor el la hora de inicio + la duración
                            if time_now <= last_start + duration:
                                trigger_value = checkActionValue(action)

                                if trigger_value:
                                    digitals[int(action["digital_write"])] = 1

                        # Si la accion ya se ha ejecutado
                        elif action.get("last_end"):
                            
                            time_now = utime.time()
                            last_end = utime.mktime(action["last_end"])
                            wait = int(action["wait"]) * 60

                            # Si la hora actual es mayor al la hora de fin + el tiempo de espera
                            if time_now >= last_end + wait:
                                trigger_value = checkActionValue(action)

                                if trigger_value:
                                    digitals[int(action["digital_write"])] = 1

                        # Si la accion no se ha ejecutado nunca
                        else:
                            trigger_value = checkActionValue(action)

                            if trigger_value:
                                digitals[int(action["digital_write"])] = 1 
                    elif action["type"] == 20:
                        # Si la Accion se esta ejecutando
                        if action.get("last_start"):
                            time_now = utime.time()
                            last_start = utime.mktime(action["last_start"])
                            duration = int(action["duration"]) * 60

                            # Si la hora actual es menor el la hora de inicio + la duración
                            if time_now <= last_start + duration:
                                trigger_day = checkActionWeekday(action)

                                if trigger_day:
                                    digitals[int(action["digital_write"])] = 1

                        # Si la accion ya se ha ejecutado
                        elif action.get("last_end"):
                            time_now = utime.time()
                            last_end = utime.mktime(action["last_end"])
                            wait = int(action["wait"]) * 60
                            
                            # Si la hora actual es mayor al la hora de fin + el tiempo de espera
                            if time_now >= last_end + wait:
                                trigger_day = checkActionWeekday(action)

                                if trigger_day:
                                    digitals[int(action["digital_write"])] = 1

                        # Si la accion no se ha ejecutado nunca
                        else:
                            trigger_day = checkActionWeekday(action)

                            if trigger_day:
                                digitals[int(action["digital_write"])] = 1                            
                    elif action["type"] == 21 or action["type"] == 22:
                        if system.DMD: print("Testing Type 21 or 22")
                        trigger_day = checkActionWeekday(action)
                        if trigger_day:
                            trigger_value = checkActionValue(action)
                            if trigger_value:
                                digitals[int(action["digital_write"])] = 1
                    elif action["type"] == 23:
                        if system.DMD: print("Testing Type 23")
                        trigger_day = checkActionWeekday(action)
                        if trigger_day:
                            trigger_time = checkActionTime(action)
                            if trigger_time:
                                digitals[int(action["digital_write"])] = 1
                    elif action["type"] == 24 or action["type"] == 25:
                        if system.DMD: print("Testing Type 24 or 25")
                        trigger_day = checkActionWeekday(action)
                        if trigger_day:
                            trigger_time = checkActionTime(action)
                            if trigger_time:
                                trigger_value = checkActionValue(action)
                                if trigger_value:
                                    digitals[int(action["digital_write"])] = 1
                    elif action["type"] == 211 or action["type"] == 221:
                        if system.DMD: print("Testing Type 211 or 221")
                        # Si la Accion se esta ejecutando
                        if action.get("last_start"):
                            if system.DMD: print("La accion posee last_start")

                            time_now = utime.time()
                            last_start = utime.mktime(action["last_start"])
                            duration = int(action["duration"]) * 60

                            # Si la hora actual es menor el la hora de inicio + la duración
                            if time_now <= last_start + duration:
                                if system.DMD: print("El tiempo actual se encuentra en el rango de ejecucion de la accion, SALIDA ACTIVADA")
                                
                                trigger_day = checkActionWeekday(action)

                                if trigger_day:
                                    trigger_value = checkActionValue(action)
                                    if trigger_value:
                                        digitals[int(action["digital_write"])] = 1
                            else:
                                if system.DMD: print("El tiempo actual no se encuentra en el rango de ejecucion de la accion, SALIDA DESACTIVADA")
                        
                        # Si la accion ya se ha ejecutado
                        elif action.get("last_end"):
                            if system.DMD: print("La accion posee last_end")
                            
                            time_now = utime.time()
                            last_end = utime.mktime(action["last_end"])
                            wait = int(action["wait"]) * 60

                            # INFORMATION GATHERING 
                            if system.DMD: print("time_now: "+str(time_now))
                            if system.DMD: print("last_end: "+str(last_end ))
                            if system.DMD: print("wait: "+str(wait))

                            # Si la hora actual es mayor al la hora de fin + el tiempo de espera
                            if time_now >= last_end + wait:
                                if system.DMD: print("El tiempo actual es mayor o igual a: last_end + wait")
                                trigger_day = checkActionWeekday(action)

                                if trigger_day:
                                    trigger_value = checkActionValue(action)
                                    if trigger_value:
                                        digitals[int(action["digital_write"])] = 1
                                        if system.DMD: print("APLICANDO SALIDA DIGITAL")
                            else:
                                if system.DMD: print("NO APLICA POR ALGUNA RAZON")

                        # Si la accion no se ha ejecutado nunca
                        else:
                            if system.DMD: print("La accion no se ha ejecutado nunca")
                            trigger_day = checkActionWeekday(action)

                            if trigger_day:
                                trigger_value = checkActionValue(action)
                                if trigger_value:
                                    digitals[int(action["digital_write"])] = 1            
                    elif action["type"] == 231:
                        if system.DMD: print("Testing Type 231")
                        # Si la Accion se esta ejecutando
                        if action.get("last_start"):

                            time_now = utime.time()
                            last_start = utime.mktime(action["last_start"])
                            duration = int(action["duration"]) * 60

                            # Si la hora actual es menor el la hora de inicio + la duración
                            if time_now <= last_start + duration:
                                trigger_day = checkActionWeekday(action)
                                if trigger_day:
                                    trigger_time = checkActionTime(action)
                                    if trigger_time:
                                        digitals[int(action["digital_write"])] = 1
                            else:
                                print("Algo mal esta pasando")

                        # Si la accion ya se ha ejecutado
                        elif action.get("last_end"):
                            
                            time_now = utime.time()
                            last_end = utime.mktime(action["last_end"])
                            wait = int(action["wait"]) * 60

                            # Si la hora actual es mayor al la hora de fin + el tiempo de espera
                            if time_now >= last_end + wait:
                                trigger_day = checkActionWeekday(action)

                                if trigger_day:
                                    trigger_time = checkActionTime(action)
                                    if trigger_time:
                                        digitals[int(action["digital_write"])] = 1
                            
                            else:
                                print("Algo mal esta pasando 2")

                        # Si la accion no se ha ejecutado nunca
                        else:
                            trigger_day = checkActionWeekday(action)

                            if trigger_day:
                                trigger_time = checkActionTime(action)
                                if trigger_time:
                                    digitals[int(action["digital_write"])] = 1

                    elif action["type"] == 241 or action["type"] == 251:
                        if system.DMD: print("Testing Type 241 or 251")
                        # Si la Accion se esta ejecutando
                        if action.get("last_start"):

                            time_now = utime.time()
                            last_start = utime.mktime(action["last_start"])
                            duration = int(action["duration"]) * 60

                            # Si la hora actual es menor el la hora de inicio + la duración
                            if time_now <= last_start + duration:
                                trigger_day = checkActionWeekday(action)
                                if trigger_day:
                                    trigger_time = checkActionTime(action)
                                    if trigger_time:
                                        trigger_value = checkActionValue(action)
                                        if trigger_value:
                                            digitals[int(action["digital_write"])] = 1

                        # Si la accion ya se ha ejecutado
                        elif action.get("last_end"):
                            
                            time_now = utime.time()
                            last_end = utime.mktime(action["last_end"])
                            wait = int(action["wait"]) * 60

                            # Si la hora actual es mayor al la hora de fin + el tiempo de espera
                            if time_now >= last_end + wait:
                                trigger_day = checkActionWeekday(action)

                                if trigger_day:
                                    trigger_time = checkActionTime(action)
                                    if trigger_time:
                                        trigger_value = checkActionValue(action)
                                        if trigger_value:
                                            digitals[int(action["digital_write"])] = 1

                        # Si la accion no se ha ejecutado nunca
                        else:
                            trigger_day = checkActionWeekday(action)

                            if trigger_day:
                                trigger_time = checkActionTime(action)
                                if trigger_time:
                                    trigger_value = checkActionValue(action)
                                    if trigger_value:
                                        digitals[int(action["digital_write"])] = 1

                    stn = int(status_now[int(action["digital_write"])])
                    dtn = int(digitals[int(action["digital_write"])])

                    if action.get("last_start"):
                        # Si la salida esta ENCENDIDA y se indica APAGADO
                        if stn == 1 and dtn == 0:
                            action_rec = system.ACTIONS[index]
                            tn = utime.localtime()
                            action_rec.pop("last_start")
                            action_rec["last_end"] = [tn[0], tn[1], tn[2], tn[3], tn[4], 0, 0, 0]
                            system.ACTIONS[index] = action_rec
                            with open(system.ACTIONS_FILE, "w") as f:
                                json.dump(system.ACTIONS, f)
                                f.close()
                            
                    elif action.get("last_end"):
                        # Si la salida esta APAGADA y se indica ENCENDIDO
                        if stn == 0 and dtn == 1:
                            action_rec = system.ACTIONS[index]
                            tn = utime.localtime()
                            action_rec.pop("last_end")
                            action_rec["last_start"] = [tn[0], tn[1], tn[2], tn[3], tn[4], 0, 0, 0]
                            system.ACTIONS[index] = action_rec
                            with open(system.ACTIONS_FILE, "w") as f:
                                json.dump(system.ACTIONS, f)
                                f.close()
                        
                    else:
                        # Si la salida esta APAGADA y se indica ENCENDIDO
                        if stn == 0 and dtn == 1:
                            action_rec = system.ACTIONS[index]
                            tn = utime.localtime()
                            action_rec["last_start"] = [tn[0], tn[1], tn[2], tn[3], tn[4], 0, 0, 0]
                            system.ACTIONS[index] = action_rec
                            with open(system.ACTIONS_FILE, "w") as f:
                                json.dump(system.ACTIONS, f)
                                f.close()

            # Final de la ejecucion de las acciones
            # utime.sleep_ms(100)
            print(digitals)

            # Sobreescritura por comportamiento de Holding
            for ind, output in enumerate(system.OUTPUTS):
                if output["hold"] == 0:
                    digitals[ind] = 0
                elif output["hold"] == 1:
                    digitals[ind] = 1

            setStatus(digitals)

            # return True
            await asyncio.sleep(5)

        asyncio.sleep(5)   
    except Exception as e:
        if system.DME: print("Error al ejecutar el cronograma.")
        if system.DME: print(e)
        return False

def setCors():
    local_address = wifi.getAddress()
    system.IP_ADDRESS = local_address
    ar = local_address.split(".")

    system.CORS = [f"http://"+ar[0]+"."+ar[1]+"."+ar[2]+"."+str(i) for i in range(1, 256)]
    CORS(app, allowed_origins=system.CORS, allow_credentials=False)

# Funciones de de Sincronización
def sync():
    if system.DMM: print("SINCRONIZANDO...")
    try:
        
        # Comprobacion de estado de coneccion con la red wifi
        if not wifi.is_connected():
            if (wifi.connect(system.WIFI_CREDENTIALS["ssid"], system.WIFI_CREDENTIALS["password"])):
                if system.DMM: print("Sync - "+system.WIFI_CREDENTIALS["ssid"]+" - OK")
            else:
                if system.DMM: print("El dispositivo se ha desconectado de "+system.WIFI_CREDENTIALS["ssid"]+", intentando reconección en "+system.EXEPTION_TIME+" segundos.")
        else:
            if system.DMM: print("Link OK!")       

    except Exception as e:
        if system.DME: print("Error en sincronizacion.")
        asyncio.sleep(1)

# Obtiene el estado de los dispositivos establecidos en la red (system.DEVICES)
def syncDevicesStatus():
    try:
        for index, device in enumertate(system.DEVICES):
            device_status = getApiData("http://"+device["ip"]+"/api/status")
            
            if device_status:
                system.DEVICES[index]["inputs"] = device_status["inputs"]
                system.DEVICES[index]["outputs"] = device_status["outputs"]

                print(system.DEVICES[index]["inputs"])
                print(system.DEVICES[index]["outputs"])
                
            else:
                print("No se encuentra el dispositivo en la red")
            

    except Exception as e:
        if system.DME: print("Error en sincronizacion de red.")
        asyncio.sleep(1)

def getDeviceStatus(ip):
    try:
        device_status = getApiData("http://"+str(ip)+"/api/status")

        if device_status:
            return device_status
        else:
            return False

    except Exception as e:
        if system.DME: print("Error obteniendo el estado del dispositivo.")
        return False

def getDeviceByToken(token):
    try:
        for index, device in enumerate(system.DEVICES):
            if device["token"] == token:
                device["id"] = index
                return device
        return False

    except Exception as e:
        if system.DME: print("Error obteniendo el dispositivo.")
        return False

def getApiData(url):
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            if system.DMM: print("Datos obtenidos correctamente de "+url)
            return response.json()
        else:
            print(f'Error al hacer ping a {url}: {response.status_code}')
        response.close()
    except Exception as e:
        print(f'No se pudo contactar con {url}: {e}')

# Physical Firewall Button confirmation
def confirmButton():
    active = Pin(system.RESET_PIN, Pin.IN).value()
    return active

def checkConfirm():
    try:
        counter = 0
        while counter < system.EXCEPTION_TIME:
            status = confirmButton()

            if status:
                return True
            else:
                counter += 1
            
        utime.sleep(1)
        
        return False

    except Exception as e:
        if system.DME: print("Error de verificacion de escritura fisica:", e)
        return False