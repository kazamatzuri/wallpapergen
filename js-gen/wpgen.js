

    

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
        var z= Math.sin(x/30)*25;
        points.push(new THREE.Vector3(x,y,z));
    }
    return points;
}


// lets agree on 0-based counting
function setPixel(x,y,color) {
    x=Math.floor(x);
    y=Math.floor(y);
    var offset=(y*width+x)*4;
    var max = data[offset];
    data[offset++]+=color[0];
    if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]+=color[1];
    if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]+=color[2];
    if (data[offset-1]>max){ max = data[offset-1];}
    data[offset++]+=color[3];
    if (data[offset-1]>max){ max = data[offset-1];}
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
    var max=0;
    var bucket=100;
    console.log(points.length);
    for (var i=1;i<points.length;i++){
        var sp=points[i];
        var lp=points[i-1];
        var px=lp.x;
        var py=lp.y;
        var x = sp.x;
        var y = sp.y;
        var s = spread[i];            
        if ((x - px) != 0) {
            var length = Math.sqrt((x - px) ** 2 + (y - py) ** 2)
            var dx = -(y - py) / length
            var dy = (x - px) / length               
            //going to spread <bucket> amount of color
            var tx1 = x + s * dx;
            var ty1=y + s * dy;
            var tx2=x - s * dx;
            var ty2 = y - s * dy;
            var num=Math.round(Math.sqrt((tx1-tx2)**2+(ty1-ty2)**2)/0.5)
            if (num==NaN) {
                num=1;
            }
            var color_gradient=bucket/num;
            var xr=makeArr(tx1,tx2,num);
            var yr=makeArr(ty1,ty2,num);
            for (var i; i<num-1; i++){
                var tx=xr[i]; 
                var ty=yr[i];
                // avoid oob errors
                if ((tx >= 0) & (tx < width) & (ty >= 0) & (ty < height))
                    {   
                        //TODO: getpixel
                        var c = getPixel(tx,ty);
                        var newc=[255,255,255,255];                     
                        //self.img_data[int(tx), int(ty)] = newc
                        var v=setPixel(tx,ty+(height/2),newc);
                        if (v>max) max=v; 
                }
            }   
        }
    
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
      var spread=[];
      var max=0;

      var iterations=5;
      for (var t=0;t<iterations;t++) {
          for (var s=0;s<p.length;s++){
              p[s].y+=(Math.random()-0.5)*((p.length/2-Math.abs(s-p.length/2))^2);
              spread[s]=p[s].z;
              //p[s].x+=(Math.random()-0.5);
          }
        var curve = new THREE.SplineCurve(p);   
        var points = curve.getPoints(width*10);
        var v=drawline_spread(points,spread,[255,0,0,Math.floor(255-((t/iterations)*255))]);
        if (v>max) max=v;
      }
    //drawrandom();
    //   for (var t=0;t<data.length;t++){
    //       data[t]=(data[t]/max)*155;
    //   }
      console.log(max);
    ctx.putImageData(img,0,0);
	


}

main();

