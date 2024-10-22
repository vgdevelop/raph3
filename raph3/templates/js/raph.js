let DEVICES = [];
let NETWORK = [];
let ACTIONS = [];
let WEATHER = [];


document.addEventListener('DOMContentLoaded', () => {
    cookieHandler();
    syncDevicesTime();
    
    
    setInterval(updateDevices, 5000);
});

// Control de carga de la aplicacion
window.addEventListener('load', () => {
   
    
    //displayApp();

});

// Control de Botones de la aplicación
document.querySelectorAll('.app-button-menu').forEach(button => {
    button.addEventListener('click', () => {
        // Obtener el target del botón presionado
        const target = button.getAttribute('data-target');
        
        // Cambia el color del botón presionado
        document.querySelectorAll('.app-button-menu').forEach(btn => {
            btn.style.backgroundColor = 'var(--bg-color)';
        });

        button.style.backgroundColor = '#007afa';


        // Setea la cookie de la pagina
        setCookie('page', target, 1);
        
        // Cerrar todos los divs
        document.querySelectorAll('.content').forEach(div => {
            div.style.display = 'none';
        });

        // Abrir el div correspondiente
        const targetDiv = document.getElementById(target);
        if (targetDiv) {
            targetDiv.style.display = 'flex';
        }
    });
});

// Funcion de obtencion de cookies
function getCookie(name) {
    const nameEQ = name + '=';
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}

// Funcion de escritura de cookies
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = name + '=' + value + ';expires=' + expires.toUTCString();
}

// Funcion de borrado de cookies
function deleteCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

// Funcion de limpieza de cookies
function clearCookies() {
    document.cookie.split(';').forEach(cookie => {
        document.cookie = cookie + ";expires=Thu, 01 Jan 1970 00:00:01 GMT;";
    });
}

// Comprobacion de dispositivo Raph - API PING
async function getUrlData(url) {
    try {
        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            data.ip = url.split('//')[1].split('/')[0];
            return data; // Devuelve el dispositivo encontrado
        }
    } catch (error) {
        // console.error(`No se pudo conectar a ${url}:`, error);
    }
    return false; // Si no responde o hay error
}

// Obtencion de los datos de los dispositivos

async function scanNetwork() {
    // Muestra el Loader con el texto
    displayLoader('Buscando dispositivos...');

    DEVICES = []; // Limpia la lista de dispositivos
    NETWORK = []; // Limpia la lista de dispositivos

    // Elimina la cookie network
    let network = getCookie('network');
    if (network) {
        deleteCookie('network'); 
    } 

    // Agrega cada promesa realizada a la lista
    const promises = [];
    for (let i = 1; i <= 254; i++) {
        promises.push(getUrlData("http://192.168.1."+i+"/api/ping"));
    }

    // Guarda los resultados de las promesas en la lista
    const results = await Promise.all(promises);
    results.forEach(device => {
        if (device) {
            // Almacena los dispositivos encontrados en la lista
            device_data = {"ip": device.ip, "name": device.name, "token": device.token};
            NETWORK.push(device_data);
        }
    });


    setCookie('network', JSON.stringify(NETWORK), 1);

    await updateDevices();
    await displayApp();

}

async function syncDevicesTime() {
    // Muestra el Loader con el texto
    displayLoader('Sincronizando dispositivos...');

    for (let i = 0; i < NETWORK.length; i++) {
        await syncDeviceTime(NETWORK[i].ip);
    }

}

async function syncDeviceTime(device_ip) {
    const now = new Date();

    var details = {
        "date_now": now.getFullYear() + "-" + now.getMonth() + "-" + now.getDate(),
        "time_now": now.getHours()+":" + now.getMinutes()
        };
    
    var formBody = [];
    for (var property in details) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(details[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    
    await fetch("http://"+device_ip+'/api/timestamp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formBody
    });

    console.log(details)
}

async function syncNetwork() {
    // Muestra el Loader con el texto
    displayLoader('Sincronizando dispositivos...');

    for (let i = 0; i < NETWORK.length; i++) {
        await syncDeviceNetwork(NETWORK[i].ip);
    }

}

async function syncDeviceNetwork(device_ip) {
    await fetch("http://"+device_ip+'/api/network', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(NETWORK)
    });
}


// ##### Funciones de API ##### //

// Actualiza los dispositivos que se encuentran en la variable NETWORK
// Almacena estos dispositivos en la variable DEVICES
async function updateDevices() {

    const status_promises = []; // Lista de promesas del estado de los dispositivos

    // Agrega cada promesa realizada a la lista
    for (let i = 0; i < NETWORK.length; i++) {
        status_promises.push(getUrlData("http://"+NETWORK[i].ip+"/api/status"));
    }

    // Guarda los resultados de las promesas en la lista
    const results = await Promise.all(status_promises);

    DEVICES = results;

    
    await updateActions();
    await displayDevicesStatus(); 
    await displayDevicesOutputs();
    await displayNetwork();
    await displayConfiguration();
}

async function updateActions() {

    const actions_promises = []; // Lista de promesas del estado de los dispositivos

    // Agrega cada promesa realizada a la lista
    for (let i = 0; i < NETWORK.length; i++) {
        actions_promises.push(getUrlData("http://"+NETWORK[i].ip+"/api/actions"));
    }

    // Guarda los resultados de las promesas en la lista
    const results = await Promise.all(actions_promises);

    ACTIONS = results;

    await unifyDevicesActions();

    await displayDevicesActions(); 
}


function cookieHandler() {
    // Comprueba si existe la cookie de network
    let network = getCookie('network');
    if (network) {
        NETWORK = JSON.parse(network); // Dumpea los datos de la cookie en la memoria 
        updateDevices();
    } else {
        // Si no se encuentra seteada la cookie network
        scanNetwork();
    }

    // Comprueba si existe la cookie page para cargar el div correspondiente
    let page = getCookie('page');
    if (page) {
        const targetDiv = document.getElementById(page);
        if (targetDiv) {
            targetDiv.style.display = 'flex';
            
            // Activa el boton correspondiente al div cargado
            document.querySelectorAll('.app-button-menu').forEach(button => {
                if (button.getAttribute('data-target') === page) {
                    button.style.backgroundColor = '#007afa';
                }
            });
        }
    } else {
        // Si no se encuentra seteada la cookie page
        document.getElementById('home-content').style.display = 'flex';
        document.getElementById('button-home').style.backgroundColor = '#007afa';
    }
}

async function toggleDeviceAction(device_ip, action_id) {
    displayLoader('Cambiando estado de la accion programada...');
    var details = {
        'id': action_id,
        'token': 'YourTokenHere'
    };
    
    var formBody = [];
    for (var property in details) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(details[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    
    await fetch("http://"+device_ip+'/api/action/toggle', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formBody
    });

    await updateActions();
    await displayApp();
};

async function deleteDeviceAction(device_ip, action_id) {
    displayLoader('Eliminando accion programada...');
    var details = {
        'id': action_id,
        'token': 'YourTokenHere'
    };
    
    var formBody = [];
    for (var property in details) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(details[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    
    await fetch("http://"+device_ip+'/api/action/delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formBody
    });

    await updateActions();
    await displayApp();
}

async function getWeather(lat, lon) {
    var api_url = "https://api.open-meteo.com/v1/forecast?latitude="+lat+"&longitude="+lon+"&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,rain,surface_pressure,cloud_cover,visibility,evapotranspiration,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_10m,wind_direction_10m,wind_gusts_10m,soil_temperature_0cm,soil_moisture_0_to_1cm";
      
    let data = await fetch(api_url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      }
    });

    WEATHER = await data.json();

    return WEATHER;

}



// Modificadores de la GUI

async function displayApp() {
    document.getElementById('master-content').style.display = 'flex';
    document.getElementById('loader').style.display = 'none';
}


function displayLoader(message) {
    document.getElementById('master-content').style.display = 'none';
    document.getElementById('loader').textContent = message;
    document.getElementById('loader').style.display = 'flex';
}

async function displayDevicesStatus() {

    const contenedor = document.getElementById('home-content'); // Contenedor donde se agregarán los devices
    contenedor.innerHTML = '';

    DEVICES.forEach(device => {
        // Crear contenedor principal
        const deviceContainer = document.createElement('div');
        deviceContainer.className = 'col-4 device-home-container';

        // Crear fila
        const row = document.createElement('div');
        row.className = 'row';

        // Crear cabecera del device
        const headerCol = document.createElement('div');
        headerCol.className = 'col-12';
        const headerRow = document.createElement('div');
        headerRow.className = 'row';
        const header = document.createElement('div');
        header.className = 'col-12 device-home-header';
        const headerLink = document.createElement('a');
        headerLink.id = `device${device.id}-name`;
        headerLink.className = 'is-center home-device-name';
        headerLink.textContent = device.name;

        // Estructura de cabecera
        header.appendChild(headerLink);
        headerRow.appendChild(header);
        headerCol.appendChild(headerRow);
        row.appendChild(headerCol);

        inputs = device["inputs"];

        // Crear entradas de estado
        inputs.forEach(input => {
            const inputCol = document.createElement('div');
            inputCol.className = 'col-12';
            const inputRow = document.createElement('div');
            inputRow.className = 'row';
            const inputCard = document.createElement('div');
            inputCard.className = 'col-12 card device-home-inputs';
            const inputLink = document.createElement('a');
            inputLink.className = 'device-input-status';
            inputLink.textContent = input["value"];

            // Estructura de input
            inputCard.appendChild(inputLink);
            inputRow.appendChild(inputCard);
            inputCol.appendChild(inputRow);
            row.appendChild(inputCol);
        });

        // Agregar la fila al contenedor del device
        deviceContainer.appendChild(row);
        // Agregar el device al contenedor principal
        contenedor.appendChild(deviceContainer);
    });

    await displayApp();

}

async function displayDevicesOutputs() {
    // Seleccionar el contenedor principal donde se añadirá el nuevo contenido
    const container = document.getElementById('device-container'); // Cambia 'main-container' al ID de tu contenedor
    container.innerHTML = '';

    DEVICES.forEach(device => {

        // Crear el div principal con la clase 'col-12 card device-card'
        var deviceCard = document.createElement('div');
        deviceCard.className = 'col-12 card device-card';

        // Crear el div con la clase 'row device-row is-center'
        var deviceRow = document.createElement('div');
        deviceRow.className = 'row device-row is-center';
        deviceCard.appendChild(deviceRow);

        // Crear el header con el título
        var headerDiv = document.createElement('div');
        headerDiv.className = 'col-12 device-button-header';
        deviceRow.appendChild(headerDiv);

        var headerRow = document.createElement('div');
        headerRow.className = 'row is-center';
        headerDiv.appendChild(headerRow);

        var headerText = document.createElement('div');
        headerText.className = 'col-12 device-header is-center';
        headerText.innerHTML = '<b>'+device.name+'</b>';
        headerRow.appendChild(headerText);

        // Crear el contenido de los dispositivos
        var contentDiv = document.createElement('div');
        contentDiv.className = 'col-12 device-button-content';
        contentDiv.hidden = false; // Añadir el atributo 'hidden'
        deviceRow.appendChild(contentDiv);

        var contentRow = document.createElement('div');
        contentRow.className = 'row is-center';
        contentDiv.appendChild(contentRow);

        device["outputs"].forEach(output => {
            // Agregar la tercera sección de dispositivo: Riego
            var irrigationTypeDiv = document.createElement('div');
            irrigationTypeDiv.className = 'col-6 device-output-type';
            irrigationTypeDiv.textContent = output.name;
            contentRow.appendChild(irrigationTypeDiv);

            var irrigationStatusDiv = document.createElement('div');
            irrigationStatusDiv.className = 'col-6 device-output-status';
            if (output.value) {
                irrigationStatusDiv.textContent = "Encendido";
            } else {
                irrigationStatusDiv.textContent = "Apagado";
            }
            
            contentRow.appendChild(irrigationStatusDiv);

            var irrigationOffDiv = document.createElement('div');
            irrigationOffDiv.className = 'col-4 is-center device-button-off';
            
            var irrigationOffText = document.createElement('b');
            irrigationOffText.className = 'op-80';
            irrigationOffText.textContent = 'OFF';
            irrigationOffDiv.appendChild(irrigationOffText);
            contentRow.appendChild(irrigationOffDiv);

            var irrigationAutoDiv = document.createElement('div');
            irrigationAutoDiv.className = 'col-4 is-center device-button-auto';
            var irrigationAutoText = document.createElement('b');
            irrigationAutoText.className = 'op-80';
            irrigationAutoText.textContent = 'AUTO';
            irrigationAutoDiv.appendChild(irrigationAutoText);
            contentRow.appendChild(irrigationAutoDiv);

            var irrigationOnDiv = document.createElement('div');
            irrigationOnDiv.className = 'col-4 is-center device-button-on';
            var irrigationOnText = document.createElement('b');
            irrigationOnText.className = 'op-80';
            irrigationOnText.textContent = 'ON';
            irrigationOnDiv.appendChild(irrigationOnText);
            contentRow.appendChild(irrigationOnDiv);

            if (output.value ) {
                irrigationOnDiv.style.backgroundColor = '#007afa'; 
                irrigationOnDiv.style.color = 'white'; 
                irrigationOnDiv.style.opacity = 0.5; 
           }

            if (output.hold == 0) { irrigationOffDiv.style.backgroundColor = 'grey'; }
            if (output.hold == 1) { irrigationOnDiv.style.backgroundColor = 'grey'; }
            if (output.hold == 2) { irrigationAutoDiv.style.backgroundColor = 'grey'; }

            irrigationOnDiv.addEventListener('click', () => {
                sendHoldData(device.ip, output.id, 1);
            });

            irrigationOffDiv.addEventListener('click', () => {
                sendHoldData(device.ip, output.id, 0);
            });

            irrigationAutoDiv.addEventListener('click', () => {
                sendHoldData(device.ip, output.id, 2);
            });

        });
        

        // Añadir la card completa al contenedor principal
        container.appendChild(deviceCard);

        

    });


}

async function displayDevicesActions() {

    const container = document.getElementById('actions-content'); // El contenedor principal

    container.innerHTML = '';

    DEVICES.forEach((device, index) => {
        // Crear div principal con la clase col-12
        const deviceContainer = document.createElement('div');
        deviceContainer.classList.add('col-12', 'device-actions-container');
    
        // Crear fila con el nombre del dispositivo
        const rowTitle = document.createElement('div');
        rowTitle.classList.add('row', 'actions-data-row');
    
        const colTitle = document.createElement('div');
        colTitle.classList.add('col-12', 'is-center');
    
        const h2Title = document.createElement('h2');
        h2Title.textContent = device.name; 
    
        colTitle.appendChild(h2Title);
        rowTitle.appendChild(colTitle);
        deviceContainer.appendChild(rowTitle);
    
        // Crear fila con la descripción y acciones
        const rowActions = document.createElement('div');
        rowActions.classList.add('row', 'actions-data-row');

        device.actions.forEach(action => {
            const colDescription = document.createElement('div');
            colDescription.classList.add('col-10');
            colDescription.textContent = getActionMessage(action); 
        
            const colToggle = document.createElement('div');
            colToggle.classList.add('col-1', 'card', 'action-button');

            colToggle.id = 'at-device-' + device.ip + '-action-' + action.id;

            if (action.active) {
                colToggle.classList.add('action-button-toggle-on');
            } else {
                colToggle.classList.add('action-button-toggle-off');
            }

            colToggle.addEventListener('click', () => {
                toggleDeviceAction(device.ip, action.id);
            });
        
            const colDelete = document.createElement('div');
            colDelete.classList.add('col-1', 'card', 'action-button', 'action-button-delete');

            colDelete.addEventListener('click', () => {
                deleteDeviceAction(device.ip, action.id);
            });
        
            rowActions.appendChild(colDescription);
            rowActions.appendChild(colToggle);
            rowActions.appendChild(colDelete);
        });
    
        
    
        deviceContainer.appendChild(rowActions);
    
        // Crear fila para el botón de añadir acción
        const rowAddAction = document.createElement('div');
        rowAddAction.classList.add('row', 'actions-data-row');
    
        const colAdd = document.createElement('div');
        colAdd.classList.add('col-12', 'card', 'action-button', 'action-button-add');

        colAdd.addEventListener('click', () => {
            displayActionForm(device.ip);
        });
    
        rowAddAction.appendChild(colAdd);
        deviceContainer.appendChild(rowAddAction);
    
        // Finalmente, añadir el contenedor del dispositivo al contenedor principal
        container.appendChild(deviceContainer);
    });



}

function displayConfiguration() {
    const config_container = document.getElementById('config-content');

    config_container.innerHTML = '';

    for (let i = 0; i < NETWORK.length; i++) {
        let device_name = getDeviceByIp(NETWORK[i].ip).name;

        const col4 = document.createElement('div');
        col4.className = 'col-4 card is-center';
        col4.innerHTML = device_name;
        col4.addEventListener('click', () => {
            displayConfigurationForm(NETWORK[i].ip);
        })
        config_container.appendChild(col4);
        // create click event listener
        

    }


}

function displayNetwork() {
    const network_container = document.getElementById('network-switcher');
    network_container.innerHTML = '';

    for (let i = 0; i < NETWORK.length; i++) {
        let device_name = getDeviceByIp(NETWORK[i].ip).name;

        const col4 = document.createElement('div');
        col4.className = 'col-4 card network-device app-button is-center';
        col4.innerHTML = device_name;
        col4.addEventListener('click', () => {
            displayNetworkForm(NETWORK[i].ip);
        })
        network_container.appendChild(col4);
    }
}

// Crear y añadir los elementos del formulario
function createFormElement(tag, classes = [], attributes = {}, textContent = '') {
    const element = document.createElement(tag);
    classes.forEach(cls => element.classList.add(cls));
    for (const attr in attributes) {
        element.setAttribute(attr, attributes[attr]);
    }
    element.textContent = textContent;
    return element;
}



// Local Variables Data Adquireing
function getDeviceNameByIp(ip) {
    return DEVICES.find(device => device.ip === ip).name;
}

function getDeviceNameByToken(token) {
    return DEVICES.find(device => device.token === token).name;
}

function getDeviceActionsByIp(ip) {
    return ACTIONS.filter(action => action.ip === ip)[0];
}

function getDeviceOutputsByIp(ip) {
    return DEVICES.find(device => device.ip === ip).outputs;
}

function getDeviceInputsByIp(ip) {
    return DEVICES.find(device => device.ip === ip).inputs;
}

function getDeviceByToken(token){
    return DEVICES.find(device => device.token === token);
}

function getDeviceByIp(ip){
    return DEVICES.find(device => device.ip === ip);
}

function getActionMessage(action) {
    let device_write = getDeviceByToken(action.device_write);
    let device_read = getDeviceByToken(action.device_read);
    let days = [];

    for (let i = 0; i < action.days.length; i++) {
        if (action.days[i] == 0) {
            days.push("lunes");
        } else if (action.days[i] == 1) {
            days.push("martes");
        } else if (action.days[i] == 2) {
            days.push("miercoles");
        } else if (action.days[i] == 3) {
            days.push("jueves");
        } else if (action.days[i] == 4) {
            days.push("viernes");
        } else if (action.days[i] == 5) {
            days.push("sabado");
        } else if (action.days[i] == 6) {
            days.push("domingo");
        }
    }

     switch (action.type) {
        case 10:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará desde el " + action.date_start.day + "/" + action.date_start.month + "/" + action.date_start.year + " a las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta el " + action.date_end.day + "/" + action.date_end.month + "/" + action.date_end.year + " a las " + action.hour_end.hour + ":" + action.hour_end.minute;
            break;
        case 11:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará desde el " + action.date_start.day + "/" + action.date_start.month + "/" + action.date_start.year + " a las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta el " + action.date_end.day + "/" + action.date_end.month + "/" + action.date_end.year + " a las " + action.hour_end.hour + ":" + action.hour_end.minute + " si " + device_read.inputs[action.analog_read].name + " es "+ action.operator_start +" a " + action.value_start;
            break;
        case 12:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará desde el " + action.date_start.day + "/" + action.date_start.month + "/" + action.date_start.year + " a las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta el " + action.date_end.day + "/" + action.date_end.month + "/" + action.date_end.year + " a las " + action.hour_end.hour + ":" + action.hour_end.minute + " si " + device_read.inputs[action.analog_read].name + " se encuentra entre "+ action.value_start +" y " + action.value_end;
            break;
        case 13:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará desde el " + action.date_start.day + "/" + action.date_start.month + "/" + action.date_start.year + " a las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta el " + action.date_end.day + "/" + action.date_end.month + "/" + action.date_end.year + " a las " + action.hour_end.hour + ":" + action.hour_end.minute + " durante "+ action.duration + " minutos con espera de "+ action.wait + " minutos";
            break;
        case 14:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará desde el " + action.date_start.day + "/" + action.date_start.month + "/" + action.date_start.year + " a las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta el " + action.date_end.day + "/" + action.date_end.month + "/" + action.date_end.year + " a las " + action.hour_end.hour + ":" + action.hour_end.minute + " durante "+ action.duration + " minutos con espera de "+ action.wait + " minutos si "+ device_read.inputs[action.analog_read].name + " es "+ action.operator_start +" a " + action.value_start;
            break;
        case 15:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará desde el " + action.date_start.day + "/" + action.date_start.month + "/" + action.date_start.year + " a las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta el " + action.date_end.day + "/" + action.date_end.month + "/" + action.date_end.year + " a las " + action.hour_end.hour + ":" + action.hour_end.minute + " durante "+ action.duration + " minutos con espera de "+ action.wait + " minutos si "+ device_read.inputs[action.analog_read].name + " se encuentra entre "+ action.value_start +" y " + action.value_end;
            break;
        case 20:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " durante "+ action.duration + " minutos con espera de "+ action.wait + " minutos";
            break;
        case 21:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " si " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " es "+ action.operator_start +" a " + action.value_start;
            break;
        case 22:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " si " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " esta entre "+ action.value_start +" y " + action.value_end;
            break;
        case 23:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " desde las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta las " + action.hour_end.hour + ":" + action.hour_end.minute;
            break;
        case 24:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " desde las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta las " + action.hour_end.hour + ":" + action.hour_end.minute + " si " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " es "+ action.operator_start +" a " + action.value_start;
            break;
        case 25:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " desde las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta las " + action.hour_end.hour + ":" + action.hour_end.minute + " si " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " esta entre "+ action.value_start +" a " + action.value_end;
            break;
        case 211:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " durante " + action.duration + " minutos con espera de "+ action.wait + " minutos si " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " es "+ action.operator_start +" a " + action.value_start;
            break;
        case 221:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " durante " + action.duration + " minutos con espera de "+ action.wait + " minutos si " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " este entre "+ action.value_start +" y " + action.value_end;
            break;
        case 231:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " desde las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta las " + action.hour_end.hour + ":" + action.hour_end.minute + " durante " + action.duration + " minutos con espera de "+ action.wait + " minutos";
            break;
        case 241:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " desde las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta las " + action.hour_end.hour + ":" + action.hour_end.minute + " durante " + action.duration + " minutos con espera de "+ action.wait + " minutos si " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " es "+ action.operator_start +" a " + action.value_start;
            break;
        case 251:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará " + JSON.stringify(days) + " desde las " + action.hour_start.hour + ":" + action.hour_start.minute + " hasta las " + action.hour_end.hour + ":" + action.hour_end.minute + " durante " + action.duration + " minutos con espera de "+ action.wait + " minutos si " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " este entre "+ action.value_start +" y " + action.value_end;
            break;
        case 30:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará cuando " + device_read.inputs[action.analog_read].name + "en " + device_read["name"] + " sea "+ action.operator_start +" a " + action.value_start;
            break;
        case 31:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará cuando " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " este entre "+ action.value_start +" y " + action.value_end;
            break;
        case 32:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará durante "+ action.duration + " minutos con espera de "+ action.wait + " minutos cuando " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " sea "+ action.operator_start +" a " + action.value_start;
            break;
        case 33:
            return device_write["outputs"][action.digital_write].name + " en " + device_write["name"] + " se activará durante "+ action.duration + " minutos con espera de "+ action.wait + " minutos cuando " + device_read.inputs[action.analog_read].name + " en " + device_read["name"] + " este entre "+ action.value_start +" y " + action.value_end;
            break;
        default:
            return "Desconocido";
    }
}

async function unifyDevicesActions() {
    DEVICES.forEach(device => {
        device["actions"] = getDeviceActionsByIp(device.ip);
    });
}

