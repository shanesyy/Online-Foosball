var paddleObj = function() {
	this.x = [];
	this.y = [];
	this.poleX = [];
	this.poleY = [];
	this.poleTeam = [0, 0, 1, 0, 1, 0, 1, 1];
	this.poleNum = 8;
	this.poleYUpRange = [];
	this.poleYDownRange = [];
	this.poleNum = 8;
	this.num = 20;
	this.numPerTeam = 10;
	this.leftStick = new Image();
	this.rightStick = new Image();
	this.left = new Image();
	this.right = new Image();
	this.leftOnColl = new Image();
	this.rightOnColl = new Image();
	this.paddlesCollisionState = new Array(this.num).fill(0); // double indicates states of paddle on collision
	this.interval = 94.5;
	this.speed = 0.18;
	this.width = 20;
	this.height = 26;
	this.collHeight = 32;
	this.collWidth = 46;
	this.playerCollWidth = 100;
	this.playerCollHeight = 70;
	this.collDrawSpeed = 1;
	this.yDelta = (canHeight - gHeight) * 0.5;
}

paddleObj.prototype.init = function() {
	this.initPole();
	this.calPaddleXPos();
	this.calPaddleYPos();
	this.initSrc();
};

paddleObj.prototype.initSrc = function() {
	this.left.src = leftPlayerSrc;
	this.right.src = rightPlayerSrc;
	this.leftOnColl.src = leftOnCollPlayerSrc;
	this.rightOnColl.src = rightOnCollPlayerSrc;
	this.leftStick.src = leftStickSrc;
	this.rightStick.src = rightStickSrc;
}

paddleObj.prototype.initPole = function() {
	var delta = (canWidth - 7 * this.interval) / 2
	for (var i = 0; i < this.poleNum; i++) {
		this.poleX[i] = delta + i * this.interval;
		this.poleY[i] = canHeight * 0.5;
	}
	this.calPoleRange();
};

paddleObj.prototype.calPaddleYPos = function() {
	this.y[0] = this.poleY[0];
	for (var i = 1; i < 3; i++) {
		this.y[i] = this.poleY[1] + gHeight / 4 * (2 * i - 3);
	}
	for (var i = 10; i < 13; i++) {
		this.y[i] = this.poleY[2] + gHeight / 3 * (i - 11);
	}
	for (var i = 3; i < 7; i++) {
		this.y[i] = this.poleY[3] + gHeight / 8 * (2 * i - 9);
	}
	for (var i = 13; i < 17; i++) {
		this.y[i] = this.poleY[4] + gHeight / 8 * (2 * i - 29);
	}
	for (var i = 7; i < 10; i++) {
		this.y[i] = this.poleY[5] + gHeight / 3 * (i - 8);
	}
	for (var i = 17; i < 19; i++) {
		this.y[i] = this.poleY[6] + gHeight / 4 * (2 * i - 35);
	}
	this.y[19] = this.poleY[7];
}

paddleObj.prototype.calPaddleXPos = function() {
	this.x[0] = this.poleX[0];
	for (var i = 1; i < 3; i++) {
		this.x[i] = this.poleX[1];
	}
	for (var i = 10; i < 13; i++) {
		this.x[i] = this.poleX[2];
	}
	for (var i = 3; i < 7; i++) {
		this.x[i] = this.poleX[3];
	}
	for (var i = 13; i < 17; i++) {
		this.x[i] = this.poleX[4];
	}
	for (var i = 7; i < 10; i++) {
		this.x[i] = this.poleX[5];
	}
	for (var i = 17; i < 19; i++) {
		this.x[i] = this.poleX[6];
	}
	this.x[19] = this.poleX[7];
}

paddleObj.prototype.calPoleRange = function() {
	this.poleYUpRange[0] = gHeight / 4 + this.height * 0.5 + this.yDelta;
	this.poleYUpRange[1] = gHeight / 4 + this.height * 0.5 + this.yDelta;
	this.poleYUpRange[2] = gHeight / 3 + this.height * 0.5 + this.yDelta;
	this.poleYUpRange[3] = 3 * gHeight / 8 + this.height * 0.5 + this.yDelta;
	for (var i = 4; i < 8; i++) {
		this.poleYUpRange[i] = this.poleYUpRange[7 - i];
	}
	for (var i = 0; i < 8; i++) {
		this.poleYDownRange[i] = canHeight - this.poleYUpRange[i];
	}
}


paddleObj.prototype.draw = function() {
	// draw sticks
	for (var i = 0; i < this.poleNum; i++) {
		var img = (this.poleTeam[i] == 0) ? this.leftStick : this.rightStick;
		// console.log("draw stick" + this.poleX[i] + " " + this.poleY[i] + "\n");
		var top_left_x = this.poleX[i] - this.width*0.5 - this.poleTeam[i] * 3;
		var top_left_y = this.poleY[i] - 250 - this.poleTeam[i] * 50;
		ctx0.drawImage(img, top_left_x, top_left_y);
	}
	// draw players
	for (var i = 0; i< this.num; i++) {
		if (this.paddlesCollisionState[i] <= 0.0) {
			var img = (i >= this.numPerTeam) ? this.right : this.left;
			ctx0.drawImage(img, this.x[i]-this.width*0.5, this.y[i]-this.height*0.5, this.width, this.height);
		} else {
			var curState = 4 - this.paddlesCollisionState[i];
			var img = (i >= this.numPerTeam) ? this.rightOnColl : this.leftOnColl;
			var deltaX = 0;
			if (i >= this.numPerTeam) {
				deltaX = -6;
			} 
			//var curState = parseInt(this.paddlesCollisionState[i], 10);
			var startX = this.x[i] - this.collWidth * 0.5 + deltaX;
			ctx0.drawImage(img, curState * this.playerCollWidth, 0, this.playerCollWidth, this.playerCollHeight, startX, this.y[i]-this.height*0.5, this.collWidth, this.collHeight);
			this.paddlesCollisionState[i] -= this.collDrawSpeed;
		}	
	}
};