$( document ).ready(function() {
    poll_update()
    pull_LED_list()
    pull_working()
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

function pull_LED_list() {

    $.getJSON('/api/0.1/selftest/application', function(response) {
        var LED_list = response.application.LED_list;
        
        $('#LED_list').val(LED_list);
    });
}

function input_LED_list(){

    var LED_list = document.getElementById("LED_list").value;
    console.log(LED_list)
    LED_array = LED_list.split(",");
    LED_array.forEach((item, index) => {
  LED_array[index] = item.trim()
})
    console.log(LED_array)

    $.ajax({
        type: "PUT",
        url: '/api/0.1/selftest/application',
        contentType: "application/json",
        data: JSON.stringify({'LED_list':LED_array})
    });
}


// runs LED test
function run_LED_test(){
    input_LED_list();
    var LED_value = document.getElementById("run_LED_test").value;
    console.log("Running LED test")
    $.ajax({
        type: "PUT",
        url: '/api/0.1/selftest/application',
        contentType: "application/json",
        data: JSON.stringify({'run_LEDs': true})
    });
}


function pull_working(){
    $.getJSON('/api/0.1/selftest/application', function(response) {
        var working = response.application.run_GPIO;
        
        if (working === true){ 
            if (working === false){
                working = working ? "yes" : "no";}}
        $('#working').html(working);
    })
}

//runs GPIO test
function run_GPIO_test(){
    // input_LED_list();
    var GPIO_value = document.getElementById("run_GPIO_test").value;
    console.log("Running GPIO test")
    $.ajax({
        type: "PUT",
        url: '/api/0.1/selftest/application',
        contentType: "application/json",
        data: JSON.stringify({'run_GPIO': true})
        
    });
    console.log("done PUT");
    pull_working();
}



