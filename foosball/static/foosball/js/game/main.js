document.body.onload = game;
var gameSocket;
var can0;
var ctx0;
var can1;
var ctx1;

var sound;

var lastTime = Date.now();
var timeDelta = 0;

var bgFieldImg = new Image();
var bgArenaImg = new Image();
var winImg = new Image();
var loseImg = new Image();

var canWidth;
var canHeight;

var tWidth;
var tHeight;

var paddle;
var leftDirection;
var rightDirection;

var ball;
var counts;

var start = false;
var round = leftScore + rightScore + 1;

var comeBack = false;

function game() {
    init();
    if (firstIn == 1) {
        initGameState();
        countDownBFGame();
    }
    gameLoop();
};

function init() {
    can0 = document.getElementById("canvas0");
    ctx0 = can0.getContext("2d");
    can1 = document.getElementById("canvas1"); // draw text
    ctx1 = can1.getContext("2d");
    ctx1.textAlign = "center";
    ctx1.font = "60px Arial";

    sound = new soundObj();
    sound.init();

    canWidth = can0.width;
    canHeight = can0.height;

    tWidth = 800;
    tHeight = 400;
    gHeight = tHeight - 90;

    leftDirection = 0;
    rightDirection = 0;

    paddle = new paddleObj();

    bgArenaImg.src = bgArenaSrc;
    bgArenaImg.onload = function() {
        drawArena();
    }
    bgFieldImg.src = bgFieldSrc;
    bgFieldImg.onload = function() {
        drawBackground();
    }

    winImg.src = winImgSrc;
    loseImg.src = loseImgSrc;
    ball = new ballObj();

    counts = new countObj();
    counts.init(3);

    gameSocket = new WebSocket('ws://'+window.location.host+'/ws/foosball/game/'+roomId+'/');
    
    gameSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        if (data['type'] == 'paddle_data') {
            if (data['from'] == leftPlayer){
                leftDirection = data['direction'];
            }
            else if (data['from'] == rightPlayer){
                rightDirection = data['direction'];
            }
        }
        else if (data['type'] == 'ball_data') {
            ball.x = data['x'];
            ball.y = data['y'];
            ball.angle = data['angle'];
            var collisionPaddleIdx = data['paddle_idx'];
            ball.collisionWithPaddle(collisionPaddleIdx);
        }
        else if (data['type'] == 'goal_data') {
            document.getElementById("left-score").innerHTML = data['left_score'];
            document.getElementById("right-score").innerHTML = data['right_score'];
            round = data['left_score'] + data['right_score'] + 1;
            ball.init(data['angle']);

            sound.playSound("audioGoal");
            if (data['side'] == side) {
            	sound.playSound("audioGoalSuccess");
            } else {
				sound.playSound("audioGoalMiss");
            }
            if (data['is_alone']) {
                comeBack = false;
                counts.init(10);
                countDown4Reconnection();
            }
            else {
                reset(3);
            }
        }
        else if (data['type'] == 'enter') {
            if (data['from'] != side) {
                sendSyncData();
            }
        }
        else if (data['type'] == 'game_over') {
            document.getElementById("left-score").innerHTML = data['left_score'];
            document.getElementById("right-score").innerHTML = data['right_score'];
            sound.playSound("audioGoal");
            if (data['side'] == side) {
                ctx1.drawImage(winImg, canWidth * 0.5 - 150, canHeight * 0.5 - 30, 300, 60);
                sound.playSound("audioGameWin");
            }
            else {
                ctx1.drawImage(loseImg, canWidth * 0.5 - 150, canHeight * 0.5 - 30, 300, 60);
                sound.playSound("audioGameOver");
            }
        }
        else if (data['type'] == 'sync_data') {
            if (data['counts'] <= -1) {
                ball.init(data['ball_dir']);
                paddle.init();
                ball.x = data['ball_x'];
                ball.y = data['ball_y'];
                ball.speed = data['ball_spd'];
                paddle.poleY = data['paddle_y'];
                start = true;
            }
            else {
                if (data['side'] == side)
                    comeBack = true;
                ball.init(data['angle']);
                reset(3);
            }
        }
    }

    gameSocket.onclose = function(e) {
        console.log('Game socket closed.');
    }

    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("keyup", onKeyUp);
}

function initGameState() {
    paddle.init();
    ball.init(initAngle);
}

function countDownBFGame() {
    window.removeEventListener("keydown", onKeyDown);
    window.removeEventListener("keyup", onKeyUp);
    var x = setInterval(function() {
        ctx1.clearRect(0, 0, canWidth, canHeight);
        if (comeBack) {
            clearInterval(x);
            comeBack = false;
        }
        else if (counts.value > -1) {
            counts.draw();
        }
        else if (counts.value <= -1) {      
            clearInterval(x);
            window.addEventListener("keydown", onKeyDown);
            window.addEventListener("keyup", onKeyUp);
            start = true;
        }
    }, 1000);
}

function countDown4Reconnection() {
    window.removeEventListener("keydown", onKeyDown);
    window.removeEventListener("keyup", onKeyUp);
    var x = setInterval(function() {
        ctx1.clearRect(0, 0, canWidth, canHeight);
        if (comeBack) {
            clearInterval(x);
            comeBack = false;
        }
        else if (counts.value > 0){
            counts.draw();
        }
        else if (counts.value <= 0) {
            clearInterval(x);
            ctx1.drawImage(winImg, canWidth * 0.5 - 150, canHeight * 0.5 - 30, 300, 60);
            sound.playSound("audioGameWin");
            sendGameOver();
        }
    }, 1000);
}

function reset(count) {
    paddle.init();
    leftDirection = 0;
    rightDirection = 0;
    counts.init(count);
    countDownBFGame();
}

function gameLoop() {
    window.myRequestAnimationFrame(gameLoop);
    ctx0.clearRect(0, 0, canWidth, canHeight);
    drawBackground();
    if(start) {
        updateBallPosition();
        ball.draw();
        updatePaddlePosition();
        ball.collisionCheck();
    }
    paddle.draw();
    drawArena();
    var curTime = Date.now();
    timeDelta = curTime - lastTime;
    if (timeDelta > 50) {
        timeDelta = 50;
    }
    lastTime = curTime;
}

function onKeyDown(e) {
    e.preventDefault();
    if (e.keyCode === 87) {
        sendDirData(-1);
    } else if (e.keyCode === 83) {
        sendDirData(1);
    }
}

function onKeyUp(e) {
    e.preventDefault();
    if (e.keyCode === 83 || e.keyCode === 87) {
        sendDirData(0);
    }
}

function sendDirData(dir) {
    gameSocket.send(JSON.stringify({
        'type':'paddle_data',
        'direction': dir,
        })
    );
}

function sendBallData(ballObj, paddle_idx) {
    gameSocket.send(JSON.stringify({
        'type': 'ball_data',
        'x': ballObj.x,
        'y': ballObj.y,
        'angle': ballObj.angle,
        'paddle_idx': paddle_idx,
        })
    );
}

function sendGameOver() {
    gameSocket.send(JSON.stringify({
        'type': 'game_over',
        })
    );
}

function sendGoalData(goalSide) {
    start = false;
    gameSocket.send(JSON.stringify({
        'type': 'goal_data',
        'goal_side': goalSide,
        })
    );
}

function sendSyncData() {
    gameSocket.send(JSON.stringify({
        'type': 'sync_data',
        'ball_x': ball.x,
        'ball_y': ball.y,
        'ball_dir': ball.angle,
        'ball_spd': ball.speed,
        'paddle_y': paddle.poleY,
        'counts': counts.value,
        'side': side,
        })
    );
}

function updatePaddlePosition() {
    for (var i = 0; i < paddle.poleNum; i++) {
        if (paddle.poleTeam[i] == 0) {
            paddle.poleY[i] += leftDirection * paddle.speed * timeDelta;
        }
        else {
            paddle.poleY[i] += rightDirection * paddle.speed * timeDelta;
        }
        if (paddle.poleY[i] <= paddle.poleYUpRange[i])
            paddle.poleY[i] = paddle.poleYUpRange[i];
        else if (paddle.poleY[i] >= paddle.poleYDownRange[i])
            paddle.poleY[i] = paddle.poleYDownRange[i];
    }
    paddle.calPaddleYPos();
}

function updateBallPosition() {
    ball.x += Math.cos(ball.angle) * ball.speed * timeDelta;
    ball.y -= Math.sin(ball.angle) * ball.speed * timeDelta;
    ball.lastKickTime += timeDelta;
    ball.speed -= ball.lastKickTime * 0.0000001;
    if (ball.speed < 0.05) ball.speed = 0.05;
}
