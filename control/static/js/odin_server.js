$( document ).ready(function() {

    update_api_adapters();
    poll_update()
});

function poll_update() {
    update_background_task();
    setTimeout(poll_update, 500);   
}

function update_api_adapters() {

    $.getJSON('/api/adapters/', function(response) {
        adapter_list = Object.keys(response.adapters).join(", ")
        $('#api-adapters').html(adapter_list);
    });
}

function update_background_task() {

    $.getJSON('/api/0.1/selftest/application', function(response) {
        var pattern_trigger = response.application.run_LEDs;
        pattern_trigger = pattern_trigger ? "yes" : "no";
        $('#pattern_running').html(pattern_trigger);
    });
}

function change_enable() {
    var enabled = $('#task-enable').prop('checked');
    console.log("Enabled changed to " + (enabled ? "true" : "false"));
    $.ajax({
        type: "PUT",
        url: '/api/workshop/background_task',
        contentType: "application/json",
        data: JSON.stringify({'enable': enabled})
    });
}

function run_LED_test(){
    var LED_value = document.getElementById("run_LED_test").value;
    console.log("Running LED test")
    $.ajax({
        type: "PUT",
        url: '/api/0.1/selftest/application ',
        contentType: "application/json",
        data: JSON.stringify({'run_LEDs': true})
    });
}