Raph3: Automatización Simple para Todos

Plataforma de automatización diseñada específicamente para técnicos en electrónica y usuarios con conocimientos básicos. Nuestro objetivo es facilitar la automatización del hogar y la industria, ofreciendo una solución accesible y fácil de usar para todos.

¿Qué es Raph3?

Raph3 es un proyecto open source que permite a los usuarios programar y controlar secuencias lógicas a través de una interfaz intuitiva. Ya sea que desees automatizar tu hogar o gestionar procesos industriales, Raph3 simplifica la programación de acciones utilizando formularios claros y comprensibles, lo que elimina la necesidad de escribir código.

Características Principales

Interfaz de Usuario Amigable: Accede, controla y programa dispositivos conectados a la red desde cualquier dispositivo. Nuestra interfaz está diseñada para ser intuitiva, permitiendo a los usuarios realizar configuraciones en simples pasos.

Flexibilidad en la Programación: La plataforma ofrece una amplia gama de opciones de programación a través de una clase de acciones. Los usuarios pueden configurar activaciones de forma sencilla con solo unos clics.

Condiciones Personalizables: Raph3 permite programar acciones en base a diversas condiciones, como:
Fecha y hora
Lecturas de sensores
Rangos de valores
Duración de activación
Días de la semana
y explorando mas!

Algunas combinaciones posibles incluyen activaciones programadas por fecha y hora, con condiciones adicionales como lecturas y rangos.

Detalles Técnicos

Raph3 se encuentra actualmente en fase beta y funciona a través de HTTP, sin almacenar datos de ningún tipo. Está diseñada específicamente para microcontroladores que utilizan MicroPython, como Raspberry PicoW, ESP32, etc.

Almacenamiento de Datos: Existe la posibilidad de almacenar datos de sensores en un servidor en la red, siempre que se habilite CORS en los dispositivos.

Beneficios Clave

Accesibilidad: No necesitas ser un experto en programación para utilizar Raph3. Nuestra plataforma está diseñada para ser comprensible para todos, desde entusiastas de la electrónica hasta usuarios ocasionales.

Automatización Eficiente: Optimiza tus rutinas diarias y mejora la eficiencia de tus procesos con un sistema que se adapta a tus necesidades.

Comunidad  Al ser un proyecto open source, invitamos a la comunidad a contribuir y mejorar Raph3. Tu participación es esencial para hacer de esta herramienta algo aún más robusto y útil.

¿Cómo Empezar?

Open Source: explora el código, contribuye al desarrollo y aprende más sobre cómo Raph3 puede transformar tu experiencia con la automatización. Te invitamos a ser parte de este emocionante viaje hacia la automatización personal, donde cada uno puede crear sus propios proyectos de automatización sin necesidad de escribir codigo. Comienza hoy mismo y descubre todo lo que puedes lograr.

Metas del Proyecto

Incorporar funcionalidad de red mesh para mejorar la conectividad entre dispositivos.
Implementar más protocolos de comunicación como HTTPS, MQTT y WebSockets.
Desarrollar un asistente basado en inteligencia artificial para optimizar los procesos y permitir el control por voz.
Integrar compatibilidad con asistentes de voz como Alexa y Google Assistant.
Ampliar la compatibilidad con una variedad de sensores y motores para diversas aplicaciones.
Implementar funcionalidades como el cambio de colores en luces RGB y la posibilidad de compartir tareas programadas.

COPYRIGHT miguelgrinberg for MICRODOT & CORS
Thanks you for your contribution to this open source world!
https://github.com/miguelgrinberg

___________________________________________________________________________________________________________________________

NOTA: Si has llegado hasta aquí seguramente buscaras el codigo!, tranquilo esto aun esta en desarrollo!, pronto lo hare, de momento trabajo en ello pero dejare algunos detalles de uso interno a continuacion:

https://drive.google.com/drive/folders/1M9172nwRUJD5QJ2YUZqAqV_tzyYwS6S6?usp=drive_link

Carpeta Raph3 contiene el codigo para el dispositivo microcontrolador, front end es una copia no exacta de la aplicacion web que el dispositivo tiene integrada.

La misma contiene la siguiente Extructura:

Carpeta microdot: pequeño framework que se utiliza para crear el servicio web.
Carpeta raph3: codigo del proyecto para los microcontroladores raspberry picow y picowh (pronto más)

  -default: contiene los valores de fabrica que se utilizan dentro de la aplicación, no debes modificarlos, si lo haces ten en
   cuenta que si ocurre un error inexperado el dispositivo se parará y no funcionara hasta que se reinicie de forma manual.

  -files: actions.json - Base de datos de las acciones que se establecen en el dispositivo, no tocar, generar desde la aplicacion.
          alarms.json - Base de datos para alarmas, aun no funcional.
          config.json - Archivo de configuracion manual del dispositivo
          devices.json - Dispositivos en la red, se generan automaticamente cuando se ingresa a la aplicacion web.
          sensors.json - Lista de los sensores disponibles a utilizar en la aplicacion, obviamente pueden agregarse mas de manera                          manual, se detalla mas adelante como funciona.
          status.json - archivo interno.
          timestamp.json - hora del dispositivo.
          wifi.json - Archivo de configuracion de la red wifi ed forma manual.
          
  -templates: Interfaz grafica de la aplicacion.

  -action.py: Clase de acciones.
  -raph.py: Backend
  -system.py: Control del sistema electronico.
  -wifi.py: control de la red wifi.

Configuracion Manual:
1- en wifi.json pon las credenciales de tu red local a utilizar. En caso de no tener una red local inalambrica el dispositivo
   te proporcionara una si las credenciales en este archivo no son correctas para que puedas volver a configurar la misma.
   Para cambiar la contraseña por defecto de la red que crea el dispositivo debes modificar el archivo wify.py en las lineas
   9 y 10, AP_SERVER_SSID y AP_SERVER_PASSWORD. Esto cambiara a medida que vaya trabajando en esa sección del proyecto.

2- en config.json cambia lo siguiente a tu gusto:
   "name": Nombre del dispositivo
   "token": Identificacion unica dentro de la red del dipositivo, pon lo que quieras pero que no se repita en otros dispositivos.
   "outputs": Salidas.
              "name": Nombre de la salida ejempli "Riego"
              "type": Lo que gustes.
              "port": Numero de puerto que se activará, a donde esta soldado basicamente.
              "hold": 0 = siempre apagado, 1 = siempre activado, 2 = automatico, sigue las acciones programdas. Se actualiza                               cuando se presionan los botones en la aplicacion web.
              "id": identidicacion interna a modo de index. 0,1,2,3,4, etc.
              "value": Estado actual de la salida. No es necesario que se ponga en su primer uso al igual que hold.
    "inputs": Sensores.
              "value": ultimo valor recibido, no es necesario en la configuracion.
              "type": 0, identificador del tipo de sensor que se utiliza para esta entrada, debe ser igual al que este en                                 sensors.json para leer los valores correctamente, pronto se realizará desde la acplicacion.
              "port": 27, Puerto fisico que utiliza del microcontrolador
              "name": "Humedad", // nombre del tipo de sensor, el mismo que en sensors.json
              "id": 0, // identificacio unica dentro de esta base de datos.
              "model": // Modelo del sensor, mismo que el nombre.

    "exception_time": Controla la velocidad en que se realiza la secuencia logica, puedes ponerlo en 0.1 como minimo, lo cual         será muy rapido pero no necesariamente lo mejor, para evitar saturaciones, utilizo 5.

Luego enciende el dispositivo y accede a el desde la red a través de su direccion de ip otorgada por el router y agrega las acciones que desees que el dispositivo realize desde su aplicacion web actual.

Hasta el momento es todo lo que necesitas hacer, obviamente la idea es que no sea necesario programar nada de esto de forma manual, pero de momento es lo que tengo!
              

