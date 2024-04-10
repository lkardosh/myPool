let myTracker = false;
let xVar=0;
let yVar=0;
let clickX=0;
let clickY=0;

function pageToSvgCoordinates(svgElement, pageX, pageY) {
    var point = svgElement.createSVGPoint();
    point.x = pageX;
    point.y = pageY;
    
    // Convert coordinates to the SVG coordinate system
    var svgP = point.matrixTransform(svgElement.getScreenCTM().inverse());
    
    return { x: svgP.x, y: svgP.y };
}


function sillyClick(event) {
    myTracker =true;
    clickX=event.pageX;
    clickY=event.pageY;
    // console.log(clickX, clickY)
    var svg = document.getElementById("insideSvg"); // Replace "yourSvgId" with your SVG element ID
    var svgCoords = pageToSvgCoordinates(svg, clickX, clickY);
    clickX = svgCoords.x;
    clickY = svgCoords.y;
}

function onDocumentReady() {

    $("#myBox").mousemove(
        function(event) {
            if (myTracker==true){
                xVar=event.pageX;
                yVar=event.pageY;
                // console.log("coords before", xVar, yVar);
                var svg = document.getElementById("insideSvg"); // Replace "yourSvgId" with your SVG element ID
                var svgCoord2 = pageToSvgCoordinates(svg, xVar, yVar);
                xVar=svgCoord2.x;
                yVar=svgCoord2.y;

                // // Change its attributes
                myLine.setAttribute("x2", xVar);  // Change x2 attribute
                myLine.setAttribute("y2", yVar);

            }
        }
            // implement Trackerrrrr
            // draw pretty line from ball to mouse
        
    );

    function scaryDisplay(data) {
        // Parse the JSON data
        // console.log("Received data: ", data)
        // console.log(data.number)

        let mySvg = document.getElementById("svgContain");

        //my display stuff
        function displaySvg(data, index){
            // console.log("hehheheha");
            if(data.isWinner == "True" && data.svgs=="None"){
                console.log("gets here")
                
                let myCurrent= document.getElementById("theCurrent");
                myCurrent.innerHTML = " ";
                let ahhurrent= document.getElementById("wordscurrentplayer");
                ahhurrent.innerHTML = " ";
                mySvg.innerHTML = "<h1>Game Over.</h1><div style='border: 2px solid black; padding: 10px; margin-top: 10px; background-color: #f0f0f0;'><h2>Winner is " + data.theWinner + "</h2></div>";

                $.post("../GameEnd", { winner: data.theWinner }, function(response) {

                    $('#gameEndMessage').html(response);
                });
            }
            else{
                mySvg.innerHTML = data.svgs[index];

                // if(index<data.number-1){
                if(index<data.number-1){
                    setTimeout(displaySvg, 19, data, index+1);

                    if(index==data.number-2){
                        if(data.isWinner == "True"){
                            let wCurrent= document.getElementById("wordscurrentplayer");
                            wCurrent.innerHTML= "<h1>Game Over.</h1> "
                            let myCurrent= document.getElementById("theCurrent");
                            myCurrent.innerHTML= "<br><div style='border: 2px solid black; padding: 10px; margin-top: 10px; background-color: #f0f0f0;'><h2>Winner is " + data.theWinner + "</h2></div>";
                        }
                        else{
                            let myCurrent= document.getElementById("theCurrent");
                            myCurrent.innerHTML = "<h3>" + data.cPlayer + "</h3>";
                            let player1Balls=document.getElementById("play1Locat");
                            player1Balls.innerHTML=data.play1Ball
                            let player2Balls=document.getElementById("play2Locat");
                            player2Balls.innerHTML=data.play2Ball
                            let highBalls=document.getElementById("highBalls");
                            highBalls.innerHTML=data.highNum
                            let lowBalls=document.getElementById("lowBalls");
                            lowBalls.innerHTML=data.lowNum
                        }
                    }
                }
            }
        }
            setTimeout(displaySvg, 19, data, 0);
    }

    $("#myBox").mouseup(
        function(){
            if(myTracker==true){
                myTracker= false
                $.post("../trackValues", {
                    xValue: xVar,
                    yValue: yVar,
                    cueXValue: clickX,
                    cueYValue: clickY
                }, function(data) {

                    // Call scaryDisplay with the received data
                    scaryDisplay(data);
                });
                
            }
        }
    )

}

$(document).ready(onDocumentReady);


