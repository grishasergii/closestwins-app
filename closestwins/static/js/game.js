var socket;

function start_countdown(duration_seconds, display) {
    var interval = setInterval(function() {
        display.text(duration_seconds);
        duration_seconds -= 1;
        if (duration_seconds < 0){
            clearInterval(interval);
            display.text("Boom")
        }
    }, 1000);
}

// Connect to the WebSocket and setup listeners
function setupWebSocket(endpoint, room_id) {
    socket = new ReconnectingWebSocket(endpoint + "?room=" + room_id);

    socket.onopen = function(event) {
        console.log("Socket is open!");
        body = {
            "action": "get_users_in_the_room",
            "room_id": room_id
        };
        socket.send(JSON.stringify(body));
    };

    socket.onmessage = function(message) {
        console.log('Message from server ', message.data);
        message_data = JSON.parse(message.data);
        var message_type = message_data["message_type"];

        if (message_type === "users_in_the_room") {
            var users_list = "";
            message_data["users"].forEach(element => users_list += `<li>${element}</li>`);
            $("#users-in-the-room").html(users_list);
        }


    };
}
