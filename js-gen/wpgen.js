

    

var steps=40.0;
var canvas = $('canvas');
var width = document.body.clientWidth;
var height = document.body.clientHeight;
canvas.width=width;
canvas.height=height;
var ctx = canvas.getContext('2d');
var img = ctx.getImageData(0,0,width, height);
var pdata= img.data;
var data=[];
var resetImg  = false; 

function $(id)
{
  return document.getElementById(id);
}

function basepoints(d=30) {
    var points=[]
    for (var t=0.0;t<steps;t++){       
        var x=(width/steps)*t;
        var y=Math.sin(x/40)*d;
        points.push(new THREE.Vector2(x,y));
    }
    return points;
}


// lets agree on 0-based counting
function setPixel(x,y,color) {
    x=Math.floor(x);
    y=Math.floor(y);
    var offset=(y*width+x)*4;
    var max = data[offset];
    data[offset++]=color[0];
    if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]=color[1];
    if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]=color[2];
    if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]=color[3];
    if (data[offset-1]>max){ max = data[offset-1];}
    return max;
}

function addToPixel(x,y,color) {
    x=Math.floor(x);
    y=Math.floor(y);
    var offset=(y*width+x)*4;
    //var max = data[offset];
    var max=0.0;
    data[offset++]=color[0];
    // if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]=color[1];
    // if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]=color[2];
    // if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]+=color[3];
    if (data[offset-1]>max){ max = data[offset-1];}
    console.log(max);
    return max;
}

function getPixel(x,y){
    x=Math.floor(x);
    y=Math.floor(y);
    var offset=(y*width+x)*4;
    var idx=0;
    var rgb=[];
    rgb[offset + idx]=data[offset + idx++];
    rgb[offset + idx]=data[offset + idx++];
    rgb[offset + idx]=data[offset + idx++];
    rgb[offset + idx]=data[offset + idx++];
    return rgb;
}

function makeArr(startValue, stopValue, cardinality) {
    var arr = [];
    var step = (stopValue - startValue) / (cardinality - 1);
    for (var i = 0; i < cardinality; i++) {
      arr.push(startValue + (step * i));
    }
    return arr;
  }

function drawline_spread(points,spread,c) {
    var max=0.0;
    var bucket=255.0;
    var d=40.0;
    var stepsize=1;
    var snum=d/stepsize;
    var gradient=bucket/snum;
    console.log(points.length);
    for (var i=1;i<points.length;i++){
        d=spread[i].y**2;
        snum=d/stepsize;
        gradient=bucket/snum;
    
        var p=points[i];
        var l=points[i-1];
        var v={};
        v.x=p.x-l.x;
        v.y=p.y-l.y;
        var r={};
        r.x=-v.y;
        r.y=v.x;
        
        //var val=setPixel(p.x,p.y+height/2,[255,0,0,gradient]); 
        //if (val>max) {max=val;}
        for (var t=-(d/2);t<(d/2);t+=stepsize){
            var val=addToPixel(p.x+t*r.x,p.y+t*r.y+height/2,[255,0,0,gradient]);
            //console.log(gradient);
            //var val=setPixel(p.x+t*r.x,p.y+t*r.y+height/2,[255,0,0,200]);  
            if (val>max) {max=val;}  
        }
        //console.log(max);

        
    
    }
    return max
}

function drawline(points,c) {
    var max = 0;
    points.forEach(function (item){
        var v=setPixel(item.x,item.y+height/2,c);
        if (v>max) max=v;
    });
    return max;
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
      var spread=basepoints(20);
      var max=0.0;

      var iterations=1;
      for (var t=0;t<iterations;t++) {
          for (var s=0;s<p.length;s++){
              p[s].y+=(Math.random()-0.5)*((p.length/2-Math.abs(s-p.length/2))^2);
              //p[s].x+=(Math.random()-0.5);
          }
        var curve = new THREE.SplineCurve(p);   
        var spreadcurve= new THREE.SplineCurve(spread)
        var points = curve.getPoints(width*10);
        var spoints = spreadcurve.getPoints(width*10);
        var v=drawline_spread(points,spoints,[255,0,0,Math.floor(255-((t/iterations)*255))]);
        //drawline(points,[255,0,0,Math.floor(255-((t/iterations)*255))])
        if (v>max) max=v;
      }
    //drawrandom();
      for (var t=0;t<pdata.length;t++){
          pdata[t]=Math.floor((data[t]/max)*255);
      }
      console.log("max");
      console.log(max);
    ctx.putImageData(img,0,0);
	


}

main();

