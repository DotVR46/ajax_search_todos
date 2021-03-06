const user_input = $("#user-input")
const todos_div = $('#replaceable-content')
const endpoint = '/'
const delay_by_in_ms = 200
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
    .done(response => {
        todos_div.fadeTo('slow', 0).promise().then(() => {
            todos_div.html(response['html_from_view'])
            todos_div.fadeTo('slow', 1)

        })
    })
}


user_input.on('keyup', function () {
    
    const request_parameters = {
        q: $(this).val()
    }
    

    
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})