var socket;

function start_countdown(duration_seconds, display, send_to_socket) {
    var interval = setInterval(function() {
        display.text(duration_seconds);
        duration_seconds -= 1;
        if (duration_seconds < 0){
            clearInterval(interval);
            send_to_socket({
                "action": "submit_room_round_answer",
            });
            display.text("Boom")
        }
    }, 1000);
}

// Connect to the WebSocket and setup listeners
function setupWebSocket(endpoint, room_id, round_duration_seconds) {
    socket = new ReconnectingWebSocket(endpoint + "?room=" + room_id);

    socket.onopen = function(event) {
        console.log("Socket is open!");

        console.log("Ask for users in the room");
        socket.send(JSON.stringify({
            "action": "get_users_in_the_room",
            "room_id": room_id
        }));

        console.log("Ask for first question");
        socket.send(JSON.stringify({
            "action": "get_room_question",
            "room_id": room_id
        }));
    };

    function send_to_socket(data) {
        data["room_id"] = room_id;
        console.log(`Send to socket ${data}`);
        socket.send(JSON.stringify(data));
    }

    socket.onmessage = function(message) {
        console.log('Message from server ', message.data);
        message_data = JSON.parse(message.data);
        var message_type = message_data["message_type"];

        if (message_type === "users_in_the_room") {
            var users_list = "";
            message_data["users"].forEach(element => users_list += `<li>${element}</li>`);
            $("#users-in-the-room").html(users_list);
        }

        if (message_type === "question") {
            $("#city-name").text(message_data["city_name"]);
            start_countdown(round_duration_seconds, $("#timer"), send_to_socket);
        }

        if (message_type === "round_result") {
            console.log("round result ok");
        }
    };
}
