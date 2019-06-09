jQuery("document").ready(function(){
    $("#rooms").on("click", "button", function(event){
        var id = $(this).attr('name');
        console.log(id);
        applyRoom(id);
    });
    // document.getElementById("start").disabled = true;
    $('#start').click(function (e) {
      e.preventDefault();
      if ($(this).hasClass('disabled'))
        return false; // Do something else in here if required
      else
        gameroomSocket.send(JSON.stringify({'start': true}));
        // window.location.href = $(this).attr('href');
    });
});

function update() {
    $.ajax({
        url: "/foosball/update_page",
        type: "POST",
        data: "cur_page="+window.location.href+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: updateHelper
    });
}

function updateHelper(response) {
    var leaders = JSON.parse(response['leaders']);
    var leader_board = document.getElementById("leaders");
    // var rooms = JSON.parse(response['rooms']);
    // var room_div = document.getElementById("rooms");
    
    while (leader_board.hasChildNodes()) {
        leader_board.removeChild(leader_board.firstChild);
    }
    $(leaders).each(function(){
        $("#leaders").append(this.html);
    });
    
    if (response['rooms']) {
        var rooms = JSON.parse(response['rooms']);
        var room_div = document.getElementById("rooms");
        while (room_div.hasChildNodes()) {
            room_div.removeChild(room_div.firstChild);
        }
        $(rooms).each(function(){
            $("#rooms").append(this.html);
        });
    }
    if (response['url']) {
        window.location=response['url'];
    }

    if(response['applicants']){
        $("#leaders a").attr('href','')
        $("#leaders a").attr('disabled',true)
        $("#follower a").attr('href','')
        $("#follower a").attr('disabled',true)
        var applicants = JSON.parse(response['applicants']);
        var waitlist_div = document.getElementById('waitlist');
        while(waitlist_div.hasChildNodes()){
            waitlist_div.removeChild(waitlist_div.firstChild);
        }
        $(applicants).each(function(){
            $("#waitlist").append(this.html);
        })

    }

    if (response['players']) {
        var players = JSON.parse(response['players']);
        var canStart = JSON.parse(response['can_start']);
        if (players == "room_closed") {
            window.location="/foosball/home"
        }
        else {
            if (canStart) {
                if ($('#start').hasClass('disabled'))
                    $('#start').removeClass('disabled');
                // $('#start').removeAttr('disabled');
                // document.getElementById("start").disabled = false;
            }
            else {
                if (!$('#start').hasClass('disabled'))
                    $('#start').addClass('disabled');
                // document.getElementById("start").disabled = true;
                // $('#start').attr('disabled', 'disabled');
            }
            
            var player_div = document.getElementById("players");
            while (player_div.hasChildNodes()) {
                player_div.removeChild(player_div.firstChild);
            }
            $(players).each(function(){
                $("#players").append(this.html);
            });
        }
    }
}

// function joinRoom(id) {
//     $.ajax({
//         url: "/foosball/join_room/"+id,
//         type: "POST",
//         data: "csrfmiddlewaretoken="+getCSRFToken(),
//         dataType: "json",
//         success: function(response) {
//             window.location=response['url'];
//         }
//     });
// }

function applyRoom(id){
    $.ajax({
        url: "/foosball/apply_room/"+id,
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: function(response){
            $("#messageModal").modal();
            console.log(response['message']);
            $("#message").text(response['message']);            
        }

    })
}

function accept(id) {
    $.ajax({
        url: "/foosball/accept/"+id,
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: function(response) {
            window.location=response['url'];
        }
    });
}

function selectTeam(){
    var idx = $('.carousel-inner li.active').index();
    var index = $('.carousel-inner').find('.active').index();
    console.log(index);
    $.ajax({
        url: "/foosball/select_team/"+index,
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: updateHelper
    });
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

window.onload = update;
window.setInterval(update, 1000);