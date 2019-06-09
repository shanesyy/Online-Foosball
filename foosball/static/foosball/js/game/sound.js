var soundObj = function() {
	this.prepare;
	this.start;
	this.ballKick;
	this.ballWall;
	this.goal;
	this.goalSuccess;
	this.goalMiss;
	this.gameOver;
	this.gameWin;
}

soundObj.prototype.init = function() {
	// prepare
	this.prepare = document.createElement("AUDIO");
    this.prepare.src = audioPrepareSrc;
    this.prepare.setAttribute("id", "audioPrepare");
    this.prepare.setAttribute("preload", "auto");
    this.prepare.setAttribute("controls", "none");
    this.prepare.style.display = "none";
    document.body.appendChild(this.prepare);

	// start
	this.start = document.createElement("AUDIO");
    this.start.src = audioStartSrc;
    this.start.playbackRate = 2;
    this.start.setAttribute("id", "audioStart");
    this.start.setAttribute("preload", "auto");
    this.start.setAttribute("controls", "none");
    this.start.style.display = "none";
    document.body.appendChild(this.start);

	// ball_kick
	this.ballKick = document.createElement("AUDIO");
    this.ballKick.src = audioBallKickSrc;
    this.ballKick.playbackRate = 2;
    this.ballKick.setAttribute("id", "audioBallKick");
    this.ballKick.setAttribute("preload", "auto");
    this.ballKick.setAttribute("controls", "none");
    this.ballKick.style.display = "none";
    document.body.appendChild(this.ballKick);

    // ball_wall
    this.ballWall = document.createElement("AUDIO");
    this.ballWall.src = audioBallKickSrc;
    this.ballWall.setAttribute("id", "audioBallWall");
    this.ballWall.setAttribute("preload", "auto");
    this.ballWall.setAttribute("controls", "none");
    this.ballWall.style.display = "none";
    document.body.appendChild(this.ballWall);

    // goal
    this.goal = document.createElement("AUDIO");
    this.goal.src = audioGoalSrc;
    this.goal.setAttribute("id", "audioGoal");
    this.goal.setAttribute("preload", "auto");
    this.goal.setAttribute("controls", "none");
    this.goal.style.display = "none";
    document.body.appendChild(this.goal);

    // goal_success
    this.goalSuccess = document.createElement("AUDIO");
    this.goalSuccess.src = audioGoalSuccessSrc;
    this.goalSuccess.setAttribute("id", "audioGoalSuccess");
    this.goalSuccess.setAttribute("preload", "auto");
    this.goalSuccess.setAttribute("controls", "none");
    this.goalSuccess.style.display = "none";
    document.body.appendChild(this.goalSuccess);

    // goal_miss
    this.goalMiss = document.createElement("AUDIO");
    this.goalMiss.src = audioGoalMissSrc;
    this.goalMiss.setAttribute("id", "audioGoalMiss");
    this.goalMiss.setAttribute("preload", "auto");
    this.goalMiss.setAttribute("controls", "none");
    this.goalMiss.style.display = "none";
    document.body.appendChild(this.goalMiss);

    // game_over
    this.gameOver = document.createElement("AUDIO");
    this.gameOver.src = audioGameOverSrc;
    this.gameOver.setAttribute("id", "audioGameOver");
    this.gameOver.setAttribute("preload", "auto");
    this.gameOver.setAttribute("controls", "none");
    this.gameOver.style.display = "none";
    document.body.appendChild(this.gameOver);

    // game_win
    this.gameWin = document.createElement("AUDIO");
    this.gameWin.src = audioGameWinSrc;
    this.gameWin.setAttribute("id", "audioGameWin");
    this.gameWin.setAttribute("preload", "auto");
    this.gameWin.setAttribute("controls", "none");
    this.gameWin.style.display = "none";
    document.body.appendChild(this.gameWin);
}


soundObj.prototype.playSound = function(id) {
	var curSound = document.getElementById(id);
	curSound.play();
}
