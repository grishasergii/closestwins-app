var socket;

// Connect to the WebSocket and setup listeners
function setupWebSocket(endpoint, room_id, user_name) {
    socket = new WebSocket(endpoint + "?room=" + room_id + "&username=" + encodeURIComponent(user_name));

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
            message_data["users"].forEach(element => users_list += `<li>${element["user_name"]}</li>`);
            $("#users-in-the-lobby").html(users_list);
        }
    };
}
