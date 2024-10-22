# ===================================================== #
# =================== ACTIONS CLASS =================== #
# ===================================================== #
# Device action control class.========================= #
# CRUD functions for the action database ============== #
# Small variable control ============================== #
# ===================================================== #

import json
import os

# ACTIONS DATABASE <=================================== #
ACTIONS_FILE = "/raph3/files/actions.json"

# DEBUG MESSAGES
ADM = True # Action Debug Messages
ADE = True # Action Debug Errors
ADS = True # Action Debug System

# Action Variables Middleware for Variables
FILLABLES = ["description", "name", "date_start", "date_end", "hour_start", "hour_end", "device_read", "analog_read", "operator_start", "value_start", "device_write", "digital_write", "operator_end", "value_end", "hour_start", "hour_end", "days", "duration", "wait", "last", "api_url", "api_target", "api_operator", "api_value", "active"]

# SECURITY MIDDLEWARES
# SOON

class Action:
    def __init__(self):
        self.description = False
        self.type = False
        self.name = False
        self.date_start = False
        self.date_end = False
        self.hour_start = False
        self.hour_end = False
        self.device_read = False
        self.analog_read = False
        self.operator_start = False
        self.value_start = False
        self.device_write = False
        self.digital_write = False
        self.operator_end = False
        self.value_end = False
        self.hour_start = False
        self.hour_end = False
        self.days = False
        self.duration = False
        self.wait = False
        self.last = False
        self.api_url = False
        self.api_target = False
        self.api_operator = False
        self.api_value = False
        self.active = False

    # Guarda la accion en el archivo de acciones
    def save(self):
        try:
            self.type = self.getActionType()
            print(self.type)

            if self.type not in [False, None]:
                print("Hasta aca vamos bien, llego el tipo de accion designada")
                # Comprueba si el archivo de acciones existe, si no existe lo crea en Exception
                os.stat(ACTIONS_FILE)
                # Abre el archivo de acciones como json_file
                with open(ACTIONS_FILE, "r") as file:
                    json_file = json.load(file)
                    file.close()

                # Comprueba si el archivo es una lista, si no lo es, la convierte en una lista
                if type(json_file).__name__ != "list": json_file = []

                action = {} # Crea un diccionario vacio para guardar los datos de la accion

                # Recorre los datos de la accion y los guarda en el diccionario
                for key, data in self.__dict__.items():
                    action[key] = data

                # Comprueba si la accion ya existe en el archivo de acciones
                if action in json_file:
                    if ADM: print("La accion ya existe en el archivo de acciones")
                else:
                    # Agrega la accion a la lista de acciones
                    json_file.append(action)

                    # Guarda la lista de acciones en el archivo de acciones
                    with open(ACTIONS_FILE, "w") as file:
                        json.dump(json_file, file)
                        file.close()
                    if ADM: print("Saved...")
            else:
                if ADE: print("No se puede guardar la accion, no se ha definido el tipo")
                return False

        except Exception as e:
            print(e)
            if ADE: print("No se encontro el archivo de acciones, se ha creado uno nuevo")
            # self.save()
    
    # Obtiene todas las acciones del archivo de acciones
    def getAll(self):
        try:
            # Comprueba si el archivo de acciones existe, si no existe lo crea en Exception
            os.stat(ACTIONS_FILE)
            # Abre el archivo de acciones como json_file
            with open(ACTIONS_FILE, "r") as file:
                json_file = json.load(file)
                file.close()

            return json_file

        except Exception as e:
            if ADE: print("No se encontro el archivo de acciones, se ha creado uno nuevo")
            return []
            
    # Metofo de comprobacion de tipo de accion
    def getActionType(self):
        if ADS: print("Comprobando acciones...")

        if self.device_write and self.digital_write:
            
            #  #################### SELECTED DAY OR RANGE OF DAYS ##################### 
            if self.date_start and self.hour_start and self.date_end and self.hour_end:
                
                #  TYPE 010
                
                #  #################### SELECTED DAY OR RANGE OF DAYS IN SOME VALUE ##################### 
                if self.device_read and self.analog_read and self.operator_start and self.value_start:
                    
                    if self.operator_end and self.value_end:
                        # RANGE OF DAYS WHEN SOME RANGE
                        if self.duration and self.wait:
                            return 15 # Duration and Delay
                        else:
                            return 12
                    else:
                        # RANGE OF DAYS WHEN SOME VALUE
                        if self.duration and self.wait:
                            return 14 # Duration and Delay
                        else:
                            return 11
                    return False

                #  #################### SELECTED DAY OR RANGE OF DAYS WITH DURATION AND DELAY ##################### 

                if self.duration and self.wait:
                    return 13
                else:
                    return 10
                # #################### SOME DAYS OF THE WEEK ####################//
            #  #################### DIAS DE LA SEMANA ##################### 
            elif self.days:

                # Lectura Analogica
                if self.device_read and self.analog_read and self.operator_start and self.value_start:
                    if self.operator_end and self.value_end: 
                        if self.duration and self.wait: 
                            if self.hour_start and self.hour_end:
                                return 251
                            else:
                                return 221 # Dias - Rango - Duracion - Espera
                        else:
                            if self.hour_start and self.hour_end:
                                return 25
                            else:
                                return 22
                        
                    else:
                        if self.duration and self.wait:
                            if self.hour_start and self.hour_end:
                                return 241
                            else:
                                return 211 # Dias - Valor - Duracion - Espera
                        else:
                            if self.hour_start and self.hour_end:
                                return 24
                            else:
                                return 21
                        
                # Si no es una lectura analogica       
                elif self.hour_start and self.hour_end:

                    if self.device_read and self.analog_read and self.operator_start and self.value_start:
                        if self.operator_end and self.value_end:
                            if self.duration and self.wait:
                                return 251 
                            else:
                                return 25
                        else:
                            if self.duration and self.wait:
                                return 241
                            else:
                                return 24
                    else:
                        if self.duration and self.wait:
                            return 231
                        else:
                            return 23
                    

                return 20       

                # #################### ANALOG READING ####################//
            #  #################### LECTURA ANALOGICA #####################
            elif self.device_read and self.analog_read and self.operator_start and self.value_start:
                # TYPE 030
                if self.operator_end and self.value_end:
                    if self.duration and self.wait:
                        return 33
                    else:
                        return 31
                else:
                    if self.duration and self.wait:
                        return 32
                    else:
                        return 30

                # #################### API EVENT ####################//
            #  #################### EVENTO API #####################
            elif self.api_url and self.api_target and self.api_operator and self.api_value:
                # TYPE 040
                return 40
            
        else:
            return False

        return False

    # Sistema Anti-Inject
    def fill(self, data):
        try:
            # Setea solo los atributos que estan en la lista de atributos permitidos
            for index, d in enumerate(data):
                if d in FILLABLES:
                    setattr(self, d, data[d])
                else:
                    if ADM: print("No se puede llenar el campo: " + d)
            
            action_type = self.getActionType()
            # Comprubea si los datos introducidos son suficientes para llenar la accion
            if action_type:
                setattr(self, "type", action_type)
                if ADM: print("Accion llenada correctamente")
                return True
            else:
                if ADE: print("No se puede llenar la accion, no se ha definido el tipo")
                return False

        except Exception as e:
            if ADE: print("Error al llenar los campos de la accion: " + str(e))
            return False

    def load(self, index):
        try:
            actions = self.getAll()
            action = actions[index]
            for key, data in action.items():
                setattr(self, key, data)
            return True
        except Exception as e:
            if ADE: print("Error al cargar la accion: " + str(e))
            return False

    def toggle(self, index):
        try:
            actions = self.getAll()
            action = actions[index]
            action["active"] = not action["active"]
            actions[index] = action
            with open(ACTIONS_FILE, "w") as file:
                json.dump(actions, file)
                file.close()

            return True
        except Exception as e:
            if ADE: print("Error al cambiar el estado de la accion: " + str(e))
            return False

    def delete(self, index):
        try:
            actions = self.getAll()
            actions.pop(index)
            with open(ACTIONS_FILE, "w") as file:
                json.dump(actions, file)
                file.close()

            return True
        except Exception as e:
            if ADE: print("Error al cambiar el estado de la accion: " + str(e))
            return False

