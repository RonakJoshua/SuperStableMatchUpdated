const cvs = document.querySelector('canvas');
const c = cvs.getContext('2d');
let yval = 50

cvs.width = window.innerWidth;
cvs.height = window.innerHeight;

window.addEventListener('resize', function () {
  cvs.width = window.innerWidth;
  cvs.height = window.innerHeight;
});

$.ajax({
    url: "/get-matches",
    type: "POST",
    data: {},
    success: function(response) {
       //response.map stores the map array
       for (var [v1, v2, v3] of response.map){
          console.log(v1)
          console.log(v2)
          console.log(v3)
       }
    }
});


function myFunc(vars) {
    let n = vars
    return vars
}

function draw() {

    if (!cvs.getContext) {
        return;
    }

    // set line stroke and line width
    c.strokeStyle = 'red';
    c.fillStyle = 'red';
    c.lineWidth = 5;

    // draw a red line
    c.beginPath();
    c.moveTo(100, 100);
    c.lineTo(300, 500);
    c.stroke();
    c.closePath();

    for (let i = 0; i < n; i++) {
        c.beginPath();
        c.arc(50, 50+(i*40), 20, 0, 2*Math.PI)
        c.fill();
        c.closePath();
    }

    c.beginPath();
    c.arc(20, 50, 20, 0, 2*Math.PI)
    c.fill();

}
draw();