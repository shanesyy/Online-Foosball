var collection;
var adsObj = function() {
    this.ad_width = 150;

    // code for closing left ad
    this.close_left_ad_str = '<div onClick="closeLeft();" style="color:gray;font-size:9pt;cursor:hand;text-align:center;width:100%;background-color: #efefef;line-height:200%">Close</div>';
    // code for closing right ad
    this.close_right_ad_str = '<div onClick="closeRight();" style="color:gray;font-size:9pt;cursor:hand;text-align:center;width:100%;background-color: #efefef;line-height:200%">Close</div>';

    this.close_web_ad_str = '<div onClick="closeWebAd();" style="color:gray;font-size:9pt;cursor:hand;text-align:center;width:100%;background-color: #efefef;line-height:200%">Close</div>';

    // code for left ad
    this.left_ad_str = "<embed src="+ leftAdSrc +" width='150' height='300' quality='high' wmode='window'></embed>" + this.close_left_ad_str;
    // code for right ad
    this.right_ad_str = "<embed src="+ rightAdSrc +" width='150' height='300' quality='high' wmode='window'></embed>" + this.close_right_ad_str;
    this.web_ad_str = "<embed src="+ webAdSrc +" width='200' height='200' quality='high' wmode='window'></embed>" + this.close_web_ad_str;

    this.delta = 0.8;

    this.items;
    this.closeB = false;
}


adsObj.prototype.init = function() {
    this.items = [];
    this.addItem('right_ad', 90, 40, this.right_ad_str);
    this.addItem('left_ad', 1, 40, this.left_ad_str);
    this.addItem('web_ad', 87, 20, this.web_ad_str);
    collection = this.items;
}

adsObj.prototype.addItem = function (id, x, y, content) {
    document.write('<DIV id=' + id + ' style="Z-INDEX: 10; POSITION: absolute;   width:' + this.ad_width + 'px; height:300px; left:' + (typeof (x) == 'string' ? eval(x) : x) + '%' + ';top:' + (typeof (y) == 'string' ? eval(y) : y) + '%' + '">' + content + '</DIV>');

    var newItem = {};
    newItem.object = document.getElementById(id);
    newItem.x = x;
    newItem.y = y;

    this.items[this.items.length] = newItem;
}


function closeLeft() {
    //document.getElementById("left_ad").style.display=="none";
    collection[1].object.style.display = 'none';
    closeB = true;
    return;
}

function closeRight() {
    //document.getElementById("right_ad").style.display=="none";
    collection[0].object.style.display = 'none';
    closeB = true;
    return;
}

function closeWebAd() {
    collection[2].object.style.display = 'none';
    closeB = true;
    return;
}

console.log("ad");
var ads = new adsObj();
ads.init();
