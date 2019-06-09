var paddleObj = function() {
	this.x = [];
	this.y = [];
	this.num = 22;
	this.numPerTeam = 11;
	this.left = new Image();
	this.right = new Image();
	this.interval = canWidth / 8;
	this.speed = 0.1;
	this.width = 8;
	this.height = 30;
}

paddleObj.prototype.init = function() {
	this.initPosition();
	this.left.src = leftPlayerSrc;
	this.right.src = rightPlayerSrc;
};

paddleObj.prototype.initPosition = function() {
	this.x[0] = this.interval * 0.5;
	this.y[0] = canHeight * 0.5;
	for (var i = 1; i < 3; i++) {
		this.x[i] = this.interval * 1.5;
		this.y[i] = canHeight / 3 * i;
	}
	for (var i = 3; i < 8; i++) {
		this.x[i] = this.interval * 3.5;
		this.y[i] = canHeight / 6 * (i - 2);
	}
	for (var i = 8; i < 11; i++) {
		this.x[i] = this.interval * 5.5;
		this.y[i] = canHeight / 4 * (i - 7);
	}
	for (var i = 11; i< 22; i++) {
		this.x[i] = canWidth - this.x[21 - i];
		this.y[i] = this.y[21 - i];
	}
};

paddleObj.prototype.draw = function() {
	// draw player
	for (var i = 0; i< this.num; i++) {
		var img = (i > 10) ? this.right : this.left;
		ctx0.drawImage(img, this.x[i]-this.width*0.5, this.y[i]-this.height*0.5, this.width, this.height);
	}
};