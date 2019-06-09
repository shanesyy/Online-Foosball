var countObj = function() {
	this.x = canWidth * 0.5;
	this.y = canHeight * 0.5;
	this.value = 0;
	this.font = "60px Arial";
	this.roundFlag = true;
	this.startImg = new Image();
	// this.img = new Image();
	// this.halfWidth = 20;
};

countObj.prototype.init = function(counts) {
	this.value = counts + 1;
	this.roundFlag = true;
	this.startImg.src = startImgSrc;
};

countObj.prototype.draw = function() {
	ctx1.font = this.font;
	if (this.roundFlag) {
		ctx1.fillText("Round " + round, this.x, this.y);
		this.roundFlag = false;
	}
	else if (this.value > 0) {
		ctx1.fillText(this.value, this.x, this.y);
	}
	else if (this.value == 0){
		// ctx1.fillText("Start!", this.x, this.y);
		var startImgWidth = 120;
		var startImgHeight = 60;
		ctx1.drawImage(this.startImg, this.x - startImgWidth * 0.5, this.y - startImgHeight * 0.5, startImgWidth, startImgHeight);
		sound.playSound("audioStart");
	}
	this.value -= 1;
};

countObj.prototype.reset = function(counts) {
	this.value = counts;
};
