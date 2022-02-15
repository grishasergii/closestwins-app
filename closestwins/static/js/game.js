var socket;

function start_question_round_countdown(duration_seconds, display, send_to_socket) {
    var interval = setInterval(function() {
        display.text(duration_seconds);
        duration_seconds -= 1;
        if (duration_seconds < 0){
            clearInterval(interval);
            var answer = {};
            if (marker_answer) {
                answer["latitude"] = marker_answer.getGeometry().lat;
                answer["longitude"] = marker_answer.getGeometry().lng;
            }
            send_to_socket({
                "action": "submit_room_round_answer",
                "answer": answer,
                "question_id": question_id
            });
            display.text("Boom");
        }
    }, 1000);
}

function start_next_question_countdown(duration_seconds, display, send_to_socket) {
    var interval = setInterval(function() {
        display.text(duration_seconds);
        duration_seconds -= 1;
        if (duration_seconds < 0){
            clearInterval(interval);
            send_to_socket({
                "action": "get_room_question"
            });
            display.text("Boom");
        }
    }, 1000);
}

function clear_map(map) {
    map.removeObjects(map.getObjects ());
    map.setCenter({lat:50.4501, lng:30.5234});
    map.setZoom(3);
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
            // clear current answer marker and the map
            marker_answer = null;
            clear_map(map);
            $("leaderboard").html("");

            question_id = message_data["question_id"];
            $("#city-name").text(message_data["city_name"]);
            $("#question-number").text(message_data["question_number_out_of_total"]);
            start_question_round_countdown(round_duration_seconds, $("#timer"), send_to_socket);
        }

        if (message_type === "round_result") {
            var map_objects = [];

            // correct answer marker
            var correct_answer = message_data["correct_answer"];
            var icon = new H.map.Icon('https://img.icons8.com/color/48/000000/marker--v1.png');
            var point_correct_location = {lat: correct_answer["latitude"], lng: correct_answer["longitude"]};
            var marker_true = new H.map.Marker(
                point_correct_location,
                {icon: icon}
            );
            map_objects.push(marker_true);

            // correct answer circle
            var circle = new H.map.Circle(
                point_correct_location,
                10000,
                {
                    style: {
                        strokeColor: "rgba(55, 85, 170, 0.6)",
                        fillColor: "rgba(0, 128, 0, 0.1)",
                        lineWidth: 2
                    }
                }
            );
            map_objects.push(circle);

            // render user answers
            message_data["user_answers"].forEach((answer) => {
                if (jQuery.isEmptyObject(answer["location"])){ return; }

                // marker answer
                var point = {lat: answer["location"]["latitude"], lng: answer["location"]["longitude"]};
                var marker = new H.map.Marker(point);
                map_objects.push(marker);

                // line between marker answer and correct location
                var line_string = new H.geo.LineString();
            	line_string.pushPoint(point);
            	line_string.pushPoint(point_correct_location);
            	var polyline = new H.map.Polyline(line_string, {style: {lineWidth: 2, strokeColor: 'black', lineDash: [2, 4]}});
            	map_objects.push(polyline);
            });

            var users_scores = "";
            message_data["leaderboard"].forEach(element => users_scores += `<li>${element["connection_id"]}: ${element["distance_presentation"]}</li>`);
            $("#leaderboard").html(users_scores);

            group = new H.map.Group();
	        group.addObjects(map_objects);
	        map.addObject(group);
            map.getViewModel().setLookAtData({
                bounds: group.getBoundingBox()
            });

            start_next_question_countdown(5, $("#timer"), send_to_socket);
        }
    };
}
