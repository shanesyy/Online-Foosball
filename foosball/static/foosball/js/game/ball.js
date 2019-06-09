var ballObj = function() {
	this.x = 0;
	this.y = 0;
	this.angle = 0;
	this.speed = 0;
	this.maxSpeed = 0.3;
	this.lastKickTime = 0
	this.img = new Image();
	this.r = 10;
	this.curDrawState;
	this.drawLoopCount;
	this.ballPicD = 32;
}

ballObj.prototype.init = function(initAngle) {
	this.x = canWidth * 0.5;
	this.y = canHeight - this.r;

	this.angle = initAngle;
	this.speed = 0.25;
	this.img.src = ballImgSrc;

	this.curDrawState = 0;
	this.drawLoopCount = 0;
}

ballObj.prototype.draw = function() {
        ctx0.translate(this.x, this.y);
        ctx0.rotate(-this.angle);
        ctx0.drawImage(this.img, 0, this.ballPicD * this.curDrawState, this.ballPicD, this.ballPicD, -this.r, -this.r, this.r * 2, this.r * 2);
        ctx0.rotate(this.angle);
        ctx0.translate(-this.x, -this.y);

        if (this.speed > 0.85 * this.maxSpeed) {
            this.drawLoopCount = (this.drawLoopCount + 3) % 14;
            this.curDrawState = this.drawLoopCount % 7;
        } else if (this.speed  <= 0.07) {
            this.drawLoopCount = (this.drawLoopCount + 1) % 14;
            this.curDrawState = parseInt(this.drawLoopCount / 2, 10) % 7;
        } else {
            this.drawLoopCount = (this.drawLoopCount + 1) % 14;
            this.curDrawState = this.drawLoopCount % 7;
        }
}

ballObj.prototype.reset = function() {
	this.lastKickTime = 0;
	this.speed = this.maxSpeed;
}

ballObj.prototype.collisionWithPaddle = function(i) {
	var ratio = this.speed / this.maxSpeed * 0.6;
	this.reset();

	paddle.paddlesCollisionState[i] = 4.0;

	if(i < paddle.numPerTeam) { // the left side
		if (this.angle < - Math.PI/2) {
			if (this.angle < -2.88) {   // almost horizonal
                this.angle = (- Math.PI - this.angle) * ratio - leftDirection * 0.26;
			} else {
			    this.angle = (- Math.PI - this.angle) * ratio;
			}

		} 
		if (this.angle > Math.PI/2) {
			if (this.angle > 2.88) {    // almost horizonal
			    this.angle = (Math.PI - this.angle) * ratio - leftDirection * 0.26;
			} else {
			    this.angle = (Math.PI - this.angle) * ratio;
			}
		}
	} else {    // the right side
		if (0 < this.angle && this.angle < Math.PI/2) {
		    if (this.angle < 0.26) {    // almost horizonal
		        this.angle = Math.PI - this.angle * ratio + rightDirection * 0.26;
		    } else {
		        this.angle = Math.PI - this.angle * ratio;
		    }
		} 
		if (-Math.PI/2 < this.angle && this.angle < 0) {
		    if (this.angle > -0.26) {   // almost horizonal
		        this.angle = Math.PI - this.angle * ratio + rightDirection * 0.26;
		    } else {
		        this.angle = - Math.PI - this.angle * ratio;
		    }

		}
	}

	sound.playSound("audioBallKick");
}



ballObj.prototype.collisionWithPaddleCheck = function() {
	for (var i = 0; i < paddle.num; i++) {
		var deltaX = (i >= paddle.numPerTeam)? -paddle.width * 0.5 : paddle.width * 0.5
		if (calDistance2(this.x, this.y, paddle.x[i] + deltaX, paddle.y[i]) < 250) {
			// this.collisionWithPaddle(i);
			sendBallData(this, i);
			return true;
		}
	}
	return false;
}

ballObj.prototype.collisionWithWallCheck = function() {
	var gUpBound = (canHeight - gHeight) * 0.5;
	var gDownBound = canHeight - gUpBound;
	var gLeftBound = 45;
	var gRightBound = canWidth - gLeftBound;
	var halfHeight = 75;
	if (((this.y - this.r - 5) <= gUpBound && Math.sin(this.angle) >= 0) ||
		((this.y + this.r + 5) >= gDownBound && Math.sin(this.angle) <= 0)) {
		this.angle = - this.angle;
		sound.playSound("audioBallWall");
	}
	else if (((this.x - this.r - 5) <= gLeftBound && Math.cos(this.angle) <= 0) ||
		((this.x + this.r + 5) >= gRightBound && Math.cos(this.angle) >= 0)) {
		if (this.y >= 0.5 * canHeight - halfHeight && this.y <= 0.5 * canHeight + halfHeight){
			var goalSide = (this.x > canWidth * 0.5)? 'left' : 'right';
			sendGoalData(goalSide);
		}
		else {
			this.angle = (this.angle > 0)? Math.PI - this.angle : -Math.PI - this.angle;
			sound.playSound("audioBallWall");
		}
	}	
}

ballObj.prototype.collisionCheck = function() {
	if (this.lastKickTime > 150) {
		if (!this.collisionWithPaddleCheck())
			this.collisionWithWallCheck();
	}
}
