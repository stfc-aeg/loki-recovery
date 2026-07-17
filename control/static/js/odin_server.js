$( document ).ready(function() {
    poll_update()
    pull_LED_list()
});

function poll_update() {
   pull_variables();
    setTimeout(poll_update, 500);   
}


function pull_LED_list() {

    $.getJSON('/api/0.1/selftest/application', function(response) {
        var LED_list = response.application.LED_list;
        
        $('#LED_list').val(LED_list);
    });
}


function pull_variables(){
    $.getJSON('/api/0.1/selftest/application', function(response) {
// Presents whether the GPIO test has been successful        
        var working = response.application.run_GPIO;        
        $('#working').html(working ? "yes" : "no");
// Presents whether the LED test is running
        var pattern_trigger = response.application.run_LEDs;
        $('#pattern_running').html(pattern_trigger ? "yes" : "no");

})
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
}



function do_gpio_test() {
    var selected_option = $("input[name='gpio_test_option']:checked").val();
    console.log("GPIO test with selected option " + selected_option);
    
    selected_option = selected_option.split(",");
    selected_option.forEach((item, index) => {
  selected_option[index] = item.trim()
})
    console.log(selected_option)
    
    $.ajax({
        type: "PUT",
        url: '/api/0.1/selftest/application',
        contentType: "application/json",
        data: JSON.stringify({which_pins:selected_option})
    });
}

