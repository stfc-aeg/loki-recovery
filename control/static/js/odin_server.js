$( document ).ready(function() {
    poll_update()
});

function poll_update() {
   is_LED_test_running();
    setTimeout(poll_update, 500);   
}

// Presents whether the LED test is running
function is_LED_test_running() {

    $.getJSON('/api/0.1/selftest/application', function(response) {
        var pattern_trigger = response.application.run_LEDs;
        pattern_trigger = pattern_trigger ? "yes" : "no";
        $('#pattern_running').html(pattern_trigger);
    });
}


// runs LED test
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