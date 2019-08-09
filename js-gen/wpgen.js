

    

var steps=40.0;
var canvas = $('canvas');
var width = document.body.clientWidth;
var height = document.body.clientHeight;
canvas.width=width;
canvas.height=height;
var ctx = canvas.getContext('2d');
var img = ctx.getImageData(0,0,width, height);
var data= img.data;
var resetImg  = false; 

function $(id)
{
  return document.getElementById(id);
}

function basepoints() {
    var points=[]
    for (var t=0.0;t<steps;t++){       
        var x=(width/steps)*t;
        var y=Math.sin(x/40)*30;
        points.push(new THREE.Vector3(x,y,0.0));
    }
    return points;
}


// lets agree on 0-based counting
function setPixel(x,y,color) {
    x=Math.floor(x);
    y=Math.floor(y);
    var offset=(y*width+x)*4;
    data[offset++]=color[0];
    data[offset++]=color[1];
    data[offset++]=color[2];
    data[offset++]=color[3];
}

function drawline(points,c) {
    points.forEach(function (item){
        setPixel(item.x,item.y+height/2,c);
    });
}

function drawrandom() {
    for (var i=0;i<10000;i++){
        setPixel(Math.floor(Math.random() * (width)), Math.floor(Math.random() * (height)),[255,0,0,255]);
    }   
}

function main() {

    if ( resetImg ) {
        resetImg = false;
    
        canvas = $('canvas');
        canvas.width  =width;
        canvas.height = height;
    
        ctx = canvas.getContext('2d');
        img = ctx.createImageData(canvas.width, 1);
        
      }
      var p = basepoints();

      var iterations=150;
      for (var t=0;t<iterations;t++) {
          for (var s=0;s<p.length;s++){
              p[s].y+=(Math.random()-0.5)*((p.length/2-Math.abs(s-p.length/2))^2);
              //p[s].x+=(Math.random()-0.5);
          }
        var curve = new THREE.SplineCurve(p);   
        var points = curve.getPoints(width*10);
        drawline(points,[255,0,0,Math.floor(255-((t/iterations)*255))]);
      }
    //drawrandom();
    ctx.putImageData(img,0,0);
	


}

main();

