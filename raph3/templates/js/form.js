const action_field_list = [ "date_start", "hour_start", "date_end", "hour_end", "device_read", "analog_read", "operator_start", "value_start", "value_end", "duration", "wait"]; 


function displayActionForm(device_ip) {

    let device_outputs = getDeviceOutputsByIp(device_ip);
    let device_inputs = getDeviceInputsByIp(device_ip);
    let device_name = getDeviceNameByIp(device_ip);

    const formContent = document.getElementById('form-content');

    formContent.innerHTML = '';

    document.querySelectorAll('.content').forEach(div => {
        div.style.display = 'none';
    });

    formContent.style.display = 'flex';

    let formulario = 
        `
            <div class="form row">
    
                <div class="col-12  title">
                    <h3 style="text-align: center" class="form-text">Agregar Acción a ${device_name}</h3>
                </div>
                
                
                <div class="col-6 ">
                    <input class="form-input" type="text" name="name" id="name" value="" placeholder="Detalle de la acción">
                </div>
    
                <div class="col-6 ">
                    <select class="form-input" name="digital_write" id="digital_write">
                        <option value="">Salida Digital ...</option>
                    </select>
                </div>

                <div class="col-12  selection_type">
                    <select class="form-input" id="action_type">
                        <option value="">Modo Manual ...</option>
                        <option value="10">10 - Fecha y Hora</option>
                        <option value="11">11 - Fecha y Hora + Lectura</option>
                        <option value="12">12 - Fecha y Hora + Rango</option>
                        <option value="13">13 - Fecha y Hora + Duración</option>
                        <option value="14">14 - Fecha y Hora + Lectura + Duración</option>
                        <option value="15">15 - Fecha y Hora + Rango + Duración</option>
                        <option value="201">201 - Rutina Semanal + Duración</option>
                        <option value="21">21 - Rutina Semanal + Lectura</option>
                        <option value="22">22 - Rutina Semanal + Rango</option>
                        <option value="23">23 - Rutina Semanal + Hora</option>
                        <option value="24">24 - Rutina Semanal + Lectura + Hora</option>
                        <option value="25">25 - Rutina Semanal + Rango + Hora</option>
                        <option value="211">211 - Rutina Semanal + Lectura + Duración</option>
                        <option value="221">221 - Rutina Semanal + Rango + Duración</option>
                        <option value="231">231 - Rutina Semanal + Hora + Duración"></option>
                        <option value="241">241 - Rutina Semanal + Hora + Lectura + Duración</option>
                        <option value="251">251 - Rutina Semanal + Hora + Rango + Duración</option>
                        <option value="30">30 - Lectura Analogica</option>
                        <option value="31">31 - Rango</option>
                        <option value="32">32 - Lectura + Duración</option>
                        <option value="33">33 - Rango + Duración</option>
                    </select>
                </div>
    
                <div class="col-3 " id="field_device_read" hidden>
                    <select class="form-input" name="device_read" id="device_read">
                        <option value="">Dispositovo de Lectura ...</option>
                        <option value="-1">Este Dispositivo</option>
                        <option value="" style="color: grey;" disabled>Otro Dispositivo</option>
                    </select>
                </div>
    
                <div class="col-3 " id="field_analog_read">
                    <select class="form-input" name="analog_read" id="analog_read">
                        <option value="">Tipo de Sensor ...</option>
                    </select>
                </div>
    
                <div class="col-3 " id="field_operator_start">
                    <select class="form-input" name="operator_start" id="operator_start">
                        <option value="">Operador ...</option>
                        <option value=">">Mayor a ...</option>
                        <option value="<">Menor a ...</option>
                        <option value="=">Igual a ...</option>
                    </select>
                </div>
    
                <div class="col-3 " id="field_value_start">
                    <input class="form-input" type="number" name="value_start" id="value_start" value="" placeholder="Valor de Inicio">
                </div>
    
                <div class="col-3 " id="field_value_end">
                    <input class="form-input" type="number" name="value_end" id="value_end" value="" placeholder="Valor de Final">
                </div>
    
                <div class="col-3 " id="field_date_start">
                    <input class="form-input" type="date" name="date_start" id="date_start" value="" placeholder="Fecha de Inicio">
                </div>
    
                <div class="col-3 " id="field_hour_start">
                    <input class="form-input" type="time" name="hour_start" id="hour_start" value="" placeholder="Hora de Inicio">
                </div>
    
                <div class="col-3 " id="field_date_end">
                    <input class="form-input" type="date" name="date_end" id="date_end" value="" placeholder="Fecha de Fin">
                </div>
    
                <div class="col-3 " id="field_hour_end">
                    <input class="form-input" type="time" name="hour_end" id="hour_end" value="" placeholder="Hora de Fin">
                </div>

                <div class="col-12">
                    <div class="row">


                        <div class=" col-1 days form-text" id="field_lunes">
                            <label class="days" for="lunes">L</label>&nbsp;
                            <input class="form-input" type="checkbox" id="lunes" name="lunes" value="0"> 
                        </div>
            
                        <div class=" col-1 days form-text" id="field_martes">
                            <label class="days" for="martes">M</label>&nbsp;
                            <input class="form-input" type="checkbox" id="martes" name="martes" value="1"> 
                        </div>
            
                        <div class=" col-1 days form-text" id="field_miercoles">
                            <label class="days" for="miercoles">M</label>&nbsp;
                            <input class="form-input" type="checkbox" id="miercoles" name="miercoles" value="2"> 
                        </div>
            
                        <div class=" col-1 days form-text" id="field_jueves">
                            <label class="days" for="jueves">J</label>&nbsp;
                            <input class="form-input" type="checkbox" id="jueves" name="jueves" value="3"> 
                        </div>
            
                        <div class=" col-1 days form-text" id="field_viernes">
                            <label class="days" for="viernes">V</label>&nbsp;
                            <input class="form-input" type="checkbox" id="viernes" name="viernes" value="4"> 
                        </div>
            
                        <div class=" col-1 days form-text" id="field_sabado">
                            <label class="days" for="sabado">S</label>&nbsp;
                            <input class="form-input" type="checkbox" id="sabado" name="sabado" value="5"> 
                        </div>
            
                        <div class=" col-1 days form-text" id="field_domingo">
                            <label class="days" for="domingo">D</label>&nbsp;
                            <input class="form-input" type="checkbox" id="domingo" name="domingo" value="6">
                        </div>

                    </div>
                </div>
    
                
                <div class="col-6 " id="field_wait">
                    <input class="form-input" type="number" name="wait" id="wait" value="" placeholder="Tiempo de Espera en minutos">
                </div>
    
                <div class="col-6 " id="field_duration">
                    <input class="form-input" type="number" name="duration" id="duration" value="" placeholder="Duración en minutos">
                </div>

    
                <div class="col-6 " id="field_api_url" hidden>
                    <input class="form-input" type="text" name="api_url" id="api_url" value="" placeholder="API Url">
                </div>
    
                <div class="col-6 " id="field_api_target" hidden>
                    <input class="form-input" type="text" name="api_target" id="api_target" value="" placeholder="API Target">
                </div>
    
                <div class="col-6 " id="field_api_operator" hidden>
                    <input class="form-input" type="text" name="api_operator" id="api_operator" value="" placeholder="API Operator">
                </div>
    
                <div class="col-6 " id="field_api_value" hidden>
                    <input class="form-input" type="number" name="api_value" id="api_value" value="" placeholder="API Value">
                </div>
    
                <div class="col-12 form-button-container">
                    <button class="form-button" id="form-cancel">Cancelar</button>
                    <button class="form-button" id="form-button">Guardar</button>
                </div>
                
            </div>
        `;

    const formContainer = document.createElement('div');
    formContainer.className = 'col-12';

    formContainer.innerHTML = formulario;

    formContent.appendChild(formContainer);

    const outputs_selector = document.getElementById('digital_write');

    for (let i = 0; i < device_outputs.length; i++) {
        outputs_selector.innerHTML += `<option value="${device_outputs[i].id}">${device_outputs[i].name}</option>`
    }

    const inputs_selector = document.getElementById('analog_read');

    for (let i = 0; i < device_inputs.length; i++) {
        inputs_selector.innerHTML += `<option value="${device_inputs[i].id}">${device_inputs[i].name}</option>`
    }

    attachActionModifier();
    attachActionSend(device_ip);

}

function attachActionModifier() {
    document.getElementById("action_type").addEventListener("change", (event) => {
        action_type = event.target.value;
        hideActionFields();
    
        const date_start = document.getElementById('field_date_start');
        const date_end = document.getElementById('field_date_end');
        const hour_start = document.getElementById('field_hour_start');
        const hour_end = document.getElementById('field_hour_end');
        const device_read = document.getElementById('field_device_read');
        const analog_read = document.getElementById('field_analog_read');
        const operator_start = document.getElementById('field_operator_start');
        const value_start = document.getElementById('field_value_start');
        const value_end = document.getElementById('field_value_end');
        const duration = document.getElementById('field_duration');
        const wait = document.getElementById('field_wait');
        const days = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]; 
        
        // Muestra los campos seleccionados en base al indice requerido
        switch (action_type) {
            case "10":
                show_10();
                break;
            case "11":
                show_11();
                break;
            case "12":
                show_12();
                break;
            case "13":
                show_13();
                break;
            case "14":
                show_14();
                break;
            case "15":
                show_15();
                break;
            case "201":
                show_201();
                break;
            case "21":
                show_21();
                break;
            case "22":
                show_22();
                break;
            case "23":
                show_23();
                break;
            case "24":
                show_24();
                break;
            case "25":
                show_25();
                break;
            case "211":
                show_211();
                break;
            case "221":
                show_221();
                break;
            case "231":
                show_231();
                break;
            case "241":
                show_241();
                break;
            case "251":
                show_251();
                break;
            case "30":
                show_30();
                break;
            case "31":
                show_31();
                break;
            case "32":
                show_32();
                break;
            case "33":
                show_33();            
                break;
            default:
                show_all_fields();
                break;
    
        }
    
    });
}

function attachActionSend(device_ip) {
    document.getElementById("form-button").addEventListener("click", (event) => {
        let form_data = getFormData();
        sendFormData(device_ip, form_data);
        
    });
    document.getElementById("form-cancel").addEventListener("click", (event) => {
        clearFormFields();
        
    });
}

function getFormData(){
    // Lee los valores del formulario
    let days = [];
    let name = document.getElementById('name').value;
    let digital_write = document.getElementById('digital_write').value;
    let analog_read = document.getElementById('analog_read').value;
    let operator_start = document.getElementById('operator_start').value;
    let value_start = document.getElementById('value_start').value;
    let value_end = document.getElementById('value_end').value;
    let date_start = document.getElementById('date_start').value;
    let date_end = document.getElementById('date_end').value;
    let hour_start = document.getElementById('hour_start').value;
    let hour_end = document.getElementById('hour_end').value;
    let device_read = document.getElementById('device_read').value;
    let duration = document.getElementById('duration').value;
    let wait = document.getElementById('wait').value;

    let lunes = document.getElementById('lunes').checked;
    let martes = document.getElementById('martes').checked;
    let miercoles = document.getElementById('miercoles').checked;
    let jueves = document.getElementById('jueves').checked;
    let viernes = document.getElementById('viernes').checked;
    let sabado = document.getElementById('sabado').checked;
    let domingo = document.getElementById('domingo').checked;

    

    let form_data = {};

    form_data.name = name;
    form_data.digital_write = digital_write;
    form_data.analog_read = analog_read;
    form_data.operator_start = operator_start;
    form_data.value_start = value_start;
    form_data.value_end = value_end;
    form_data.date_start = date_start;
    form_data.date_end = date_end;
    form_data.hour_start = hour_start;
    form_data.hour_end = hour_end;
    form_data.device_read = device_read;
    form_data.duration = duration;
    form_data.wait = wait;
    if (lunes) { form_data.lunes = lunes; }
    if (martes) { form_data.martes = martes; }
    if (miercoles) { form_data.miercoles = miercoles; }
    if (jueves) { form_data.jueves = jueves; }
    if (viernes) { form_data.viernes = viernes; }
    if (sabado) { form_data.sabado = sabado; }
    if (domingo) { form_data.domingo = domingo; }
    
    return form_data;

}

async function sendFormData(device_ip, action_data) {
    displayLoader('Enviando accion...');
    var details = action_data;
    
    var formBody = [];
    for (var property in details) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(details[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    
    await fetch('http://'+device_ip+'/editor', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formBody
    });

    await updateActions();
    //document.getElementById("button-actions").click();
    await displayApp();
    clearFormFields();
}

async function sendHoldData(device_ip, device_output, hold) {
    let dev_name = getDeviceNameByIp(device_ip);
    let dev_outputs = getDeviceOutputsByIp(device_ip);

    if (hold == 0) { displayLoader('Desactivando '+dev_outputs[device_output].name+' en '+dev_name); }
    if (hold == 1) { displayLoader('Activando '+dev_outputs[device_output].name+' en '+dev_name); }
    if (hold == 2) { displayLoader('Automatizando '+dev_outputs[device_output].name+' en '+dev_name); }
    
    var details = {"hold": hold, "id": device_output};
    
    var formBody = [];
    for (var property in details) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(details[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    
    await fetch('http://'+device_ip+'/api/output/hold', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formBody
    });

    await updateDevices();
  
}

function show_10(){
    date_start.style.display = "block";
    date_end.style.display = "block";
    hour_start.style.display = "block";
    hour_end.style.display = "block";
};

function show_11(){
    date_start.style.display = "block";
    date_end.style.display = "block";
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
};

function show_12(){
    date_start.style.display = "block";
    date_end.style.display = "block";
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
};

function show_13(){
    date_start.style.display = "block";
    date_end.style.display = "block";
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_14(){
    date_start.style.display = "block";
    date_end.style.display = "block";
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_15(){
    date_start.style.display = "block";
    date_end.style.display = "block";
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_201(){
    show_days();
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_21(){
    show_days();
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
};

function show_22(){
    show_days();
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
};

function show_23(){
    show_days();
    hour_start.style.display = "block";
    hour_end.style.display = "block";
};

function show_24(){
    show_days();
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
};

function show_25(){
    show_days();
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
};

function show_211(){
    show_days();
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_221(){
    show_days();
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_231(){
    show_days();
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_241(){
    show_days();
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_251(){
    show_days();
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_30(){
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
};

function show_31(){
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
};

function show_32(){
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
};

function show_33(){
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";
} 

function hideActionFields(){
    // Oculta los campos de configuracion de las acciones a traves de un each
    action_field_list.forEach(element => {
        document.getElementById(element).style.display = 'none';
    });
    
    hide_days();
    
};

function show_days(){
    // Muestra los dias
    document.getElementById('field_lunes').style.display = 'block';
    document.getElementById('field_martes').style.display = 'block';
    document.getElementById('field_miercoles').style.display = 'block';
    document.getElementById('field_jueves').style.display = 'block';
    document.getElementById('field_viernes').style.display = 'block';
    document.getElementById('field_sabado').style.display = 'block';
    document.getElementById('field_domingo').style.display = 'block';
};

function hide_days(){
    // Oculta los dias
    document.getElementById('field_lunes').style.display = 'none';
    document.getElementById('field_martes').style.display = 'none';
    document.getElementById('field_miercoles').style.display = 'none';
    document.getElementById('field_jueves').style.display = 'none';
    document.getElementById('field_viernes').style.display = 'none';
    document.getElementById('field_sabado').style.display = 'none';
    document.getElementById('field_domingo').style.display = 'none';
};

function show_all_fields(){
    // Muestra todos los campos de configuracion
    
    date_start.style.display = "block";
    date_end.style.display = "block";
    hour_start.style.display = "block";
    hour_end.style.display = "block";
    device_read.style.display = "block";
    analog_read.style.display = "block";
    operator_start.style.display = "block";
    value_start.style.display = "block";
    value_end.style.display = "block";
    duration.style.display = "block";
    wait.style.display = "block";

    show_days();
};

function clearFormFields() {
    // Limpia todos los valores del formulario

    document.getElementById('action_type').value = '';
    document.getElementById('name').value = '';
    document.getElementById('digital_write').value = '';
    document.getElementById('analog_read').value = '';
    document.getElementById('operator_start').value = '';
    document.getElementById('value_start').value = '';
    document.getElementById('value_end').value = '';
    document.getElementById('date_start').value = '';
    document.getElementById('date_end').value = '';
    document.getElementById('hour_start').value = '';
    document.getElementById('hour_end').value = '';
    document.getElementById('device_read').value = '';
    document.getElementById('duration').value = '';
    document.getElementById('wait').value = '';
    document.getElementById('lunes').checked = false;
    document.getElementById('martes').checked = false;
    document.getElementById('miercoles').checked = false;
    document.getElementById('jueves').checked = false;
    document.getElementById('viernes').checked = false;
    document.getElementById('sabado').checked = false;
    document.getElementById('domingo').checked = false;

    show_all_fields();
    document.getElementById('button-actions').click();
}

async function sendConfig(device_ip) {

    const name = document.getElementById('cfg-name').value;
    // const token = document.getElementById('cfg-token').value;
    displayLoader('Enviando configuración...');
    
    var details = {
        name: name
    };
    
    var formBody = [];
    for (var property in details) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(details[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    
    await fetch('http://'+device_ip+'/api/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formBody
    });

    clearConfigForm();
    // await updateDevices();
    await displayApp();

    
}

function displayConfigurationForm(device_ip) {

    let device = getDeviceByIp(device_ip);

    const conf_content = document.getElementById('config-form-content');
    conf_content.style.display = 'flex';

    const content = document.getElementById('form-config');
    content.innerHTML = '';

    // Creamos el formulario
    const form = document.createElement('div');
    form.className = 'row card network-card';
    
    // Título del formulario
    const titleDiv = document.createElement('div');
    titleDiv.className = 'col-12';
    const title = document.createElement('h6');
    title.className = 'is-left network-text';
    title.textContent = 'Nombre del Dispositivo';
    titleDiv.appendChild(title);
    form.appendChild(titleDiv);

    // Campo "Nombre"
    const nameDiv = document.createElement('div');
    nameDiv.className = 'col-6';
    const nameInput = document.createElement('input');
    nameInput.className = 'form-input';
    nameInput.type = 'text';
    nameInput.name = 'name';
    nameInput.value = device.name;
    nameInput.id = 'cfg-name';
    nameInput.placeholder = 'Ej: Sala';
    nameDiv.appendChild(nameInput);
    form.appendChild(nameDiv);

    // Botón "Establecer"
    const buttonDiv = document.createElement('div');
    buttonDiv.className = 'col-6 is-right';

    const cancel = document.createElement('button');
    cancel.className = 'card form-button-cancel';
    cancel.id = 'cancel-config';
    cancel.textContent = 'Cancelar';
    cancel.addEventListener('click', () => {
        clearConfigForm();
    });

    buttonDiv.appendChild(cancel);
    form.appendChild(buttonDiv);

    

    const button = document.createElement('button');
    button.className = 'card form-button';
    button.id = 'set-config';
    button.textContent = 'Establecer';
    button.addEventListener('click', () => {
        sendConfig(device_ip);
    });
    buttonDiv.appendChild(button);

    



    // Añadimos el formulario al contenedor
    content.appendChild(form);


}


function clearConfigForm() { 
    const config_form = document.getElementById('form-config');
    config_form.innerHTML = '';
    
}

function displayNetworkForm(device_ip) { 
    const device = getDeviceByIp(device_ip);
    // Crear el contenedor principal
    const container = document.getElementById('network-wifi');
    container.innerHTML = '';

    // Título
    const titleRow = document.createElement('div');
    titleRow.className = 'row';
    const titleCol = document.createElement('div');
    titleCol.className = 'col-12';
    const title = document.createElement('h4');
    title.className = 'network-text is-center';
    title.textContent = 'Conectividad de ' + device.name;
    titleCol.appendChild(title);
    titleRow.appendChild(titleCol);
    container.appendChild(titleRow);

    // Sección "Red Local"
    const localNetworkRow = document.createElement('div');
    localNetworkRow.className = 'row card network-card';
    const localNetworkCol = document.createElement('div');
    localNetworkCol.className = 'col-12';
    localNetworkCol.textContent = 'Red Local';
    localNetworkRow.appendChild(localNetworkCol);

    const wifiSSIDCol = document.createElement('div');
    wifiSSIDCol.className = 'col-4';
    const wifiSSIDInput = document.createElement('input');
    wifiSSIDInput.type = 'text';
    wifiSSIDInput.id = 'wifi_ssid';
    wifiSSIDInput.placeholder = 'SSID';
    wifiSSIDCol.appendChild(wifiSSIDInput);

    const wifiPasswordCol = document.createElement('div');
    wifiPasswordCol.className = 'col-4';
    const wifiPasswordInput = document.createElement('input');
    wifiPasswordInput.type = 'text';
    wifiPasswordInput.id = 'wifi_password';
    wifiPasswordInput.placeholder = 'Contraseña';
    wifiPasswordCol.appendChild(wifiPasswordInput);

    const wifiButtonCol = document.createElement('div');
    wifiButtonCol.className = 'col-4';
    const wifiButton = document.createElement('button');
    wifiButton.className = 'form-button app-button';
    wifiButton.id = 'set_wifi';
    wifiButton.textContent = 'Establecer';
    wifiButtonCol.appendChild(wifiButton);

    localNetworkRow.appendChild(wifiSSIDCol);
    localNetworkRow.appendChild(wifiPasswordCol);
    localNetworkRow.appendChild(wifiButtonCol);
    container.appendChild(localNetworkRow);

    // Sección "Access Point"
    const accessPointRow = document.createElement('div');
    accessPointRow.className = 'row card network-card';
    const accessPointCol = document.createElement('div');
    accessPointCol.className = 'col-12';
    accessPointCol.textContent = 'Access Point';
    accessPointRow.appendChild(accessPointCol);

    const apSSIDCol = document.createElement('div');
    apSSIDCol.className = 'col-4';
    const apSSIDInput = document.createElement('input');
    apSSIDInput.type = 'text';
    apSSIDInput.id = 'ap_ssid';
    apSSIDInput.placeholder = 'Nombre para la Red';
    apSSIDCol.appendChild(apSSIDInput);

    const apPasswordCol = document.createElement('div');
    apPasswordCol.className = 'col-4';
    const apPasswordInput = document.createElement('input');
    apPasswordInput.type = 'text';
    apPasswordInput.id = 'ap_password';
    apPasswordInput.placeholder = 'Contraseña para la Red';
    apPasswordCol.appendChild(apPasswordInput);

    const apButtonCol = document.createElement('div');
    apButtonCol.className = 'col-4';
    const apButton = document.createElement('button');
    apButton.className = 'form-button app-button';
    apButton.id = 'set_ap';
    apButton.textContent = 'Establecer';
    apButtonCol.appendChild(apButton);

    accessPointRow.appendChild(apSSIDCol);
    accessPointRow.appendChild(apPasswordCol);
    accessPointRow.appendChild(apButtonCol);
    container.appendChild(accessPointRow);



}