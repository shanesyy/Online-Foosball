var roomId = window.location.href.split("/").slice(-1);
// console.log(window.location.href, roomId);
var gameroomSocket = new WebSocket('ws://'+window.location.host+'/ws/foosball/gameroom/'+roomId+'/');

gameroomSocket.onmessage = function(e) {
	var data = JSON.parse(e.data);
	// console.log(window.location.href, data);
	window.location="/foosball/game/"+roomId;
}

gameroomSocket.onclose = function(e) {
	console.log('Gameroom socket closed.');
}

