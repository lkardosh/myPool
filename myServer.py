import sys
import cgi
import math
import Physics
import random
import json

from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;

scriptString= """<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
<script src="pool.js"></script>"""

pName1=None
p1HorL="Not yet assigned"
p2HorL="Not yet assigned"
pName2=None
currentPlayer=None
game=None
p1Goals=7
p2Goals=7
joinedName=None
svg_content=None
winName=None

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global pName1, pName2, currentPlayer, game, table, p1Goals, p2Goals, joinedName, myTable, p1HorL, p2HorL
        parsed  = urlparse(self.path)
        if parsed.path in [ '/starter.html']:
            fp = open( '.'+self.path )
            content = fp.read()
            db = Physics.Database(reset=True)
            db.setUp()
            pName1=None
            p1HorL="Not yet assigned"
            p2HorL="Not yet assigned"
            pName2=None
            currentPlayer=None
            game=None
            p1Goals=7
            p2Goals=7
            joinedName=None
            svg_content=None
            self.send_response( 200 )
            self.send_header('Content-type', 'text/html')
            self.send_header( "Content-length", len( content ) )
            self.end_headers()
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close
        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
            fp = open( '.'+self.path, 'rb')
            content = fp.read()
            self.send_response( 200 )
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header( "Content-length", len( content ) )
            self.end_headers()
            self.wfile.write( content )
            fp.close
        elif parsed.path.endswith('pool.js'):
            fp = open( '.'+self.path )
            content = fp.read()
            self.send_response( 200 )
            self.send_header('Content-type', 'text/js')
            self.send_header( "Content-length", len( content ) )
            self.end_headers()
            self.wfile.write( bytes( content, "utf-8" ) )

    def do_POST(self):
        global pName1, pName2, currentPlayer, game, table, p1Goals, p2Goals, joinedName, myTable, p2HorL, p1HorL,winName
        parsed  = urlparse( self.path )
        if parsed.path in [ '/display.html']:
            form = cgi.FieldStorage(fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   )
            if(pName1 is None):
                pName1= form.getvalue('player1Name')
                pName2= form.getvalue('player2Name')
                joinedName= pName1+pName2
                game = Physics.Game( gameName=joinedName, player1Name=pName1, player2Name=pName2);
                currentPlayer = random.choice([pName1, pName2])

            db = Physics.Database()
            maxId=db.getMaxId()
            myTable=db.readTable(maxId-1)
            # print("reads here")
            eightBall=myTable.findEight()

            if(eightBall is None):
                print("AHHHHHH2")
                currentPlayer=db.getThePlayer()
                if(currentPlayer==pName1):
                    currentPlayer=pName2
                elif(currentPlayer==pName2):
                    currentPlayer=pName1

                if(currentPlayer==pName1):
                    # print("thsi one")
                    if(p1HorL=="Low"):
                        if(myTable.countLow()!=0):
                            winVal=pName1
                        else:
                            winVal=pName2
                    elif(p1HorL=="High"):
                        if(myTable.countHigh()!=0):
                            winVal=pName1
                        else:
                            winVal=pName2
                if(currentPlayer==pName2):
                    # print("thheee")
                    if(p2HorL=="Low"):
                        if(myTable.countLow()!=0):
                            winVal=pName2
                        else:
                            winVal=pName1
                    elif(p2HorL=="High"):
                        if(myTable.countHigh()!=0):
                            winVal=pName2
                        else:
                            winVal=pName1
                        
                htmlString = f"""<html><head>{scriptString}<title>Display</title></head>"""
                htmlString += f"""<body style="width:100%;text-align:center; background-color: #F2E8E8">"""
                # htmlString += """<div style="height: 100px;"></div>"""
                htmlString += """<h1>Game Over</h1><br>"""
                htmlString += """<div style="width: 50%; margin: 0 auto; padding: 20px; background-color: #ffffff; border: 2px solid #000000; border-radius: 10px;">"""
                htmlString += f"""<h2>{winVal} wins!!!!</h2>"""
                htmlString += """</div>"""  # Closing the player wins container
                htmlString += """<br><h2><a href='/starter.html'>Start new game</a></h2></body></html>"""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header("Content-length", len(htmlString))
                self.end_headers()
                self.wfile.write(bytes(htmlString, "utf-8"))

            else:
                svg_content=myTable.svg()
                # currentPlayer=db.getThePlayer()
                if(currentPlayer!=None):
                    if(currentPlayer==pName1):
                        currentPlayer=pName2
                    elif(currentPlayer==pName2):
                        currentPlayer=pName1

                # print("html thingys")

                htmlString = f"""<html><head>{scriptString}<title>Display</title></head>"""
                htmlString += f"""<body style="width:100%;text-align:center; background-color: #F2E8E8;"> <div id= "myBox">"""
                htmlString+=f"""Balls left for low numbers: """
                htmlString+= f"""<div id="lowBalls"> {p1Goals} </div>"""
                htmlString+=f"""Balls left for high numbers:"""
                htmlString+= f"""<div id="highBalls"> {p2Goals} </div>"""
                htmlString += f"""<div style="display: flex; justify-content: space-between; align-items: center;">"""
                htmlString += f"""<div style="border: 1px solid black; padding: 5px;"> Player 1: {pName1}<div id="play1Locat">- {p1HorL}</div></div>"""
                htmlString+=f"""<div style="border: 1px solid black; padding: 5px;"> Player 2: {pName2}<div id="play2Locat">- {p2HorL}</div></div>"""
                htmlString += """</div>"""
                htmlString += """<h2 id="wordscurrentplayer"> Current Player: </h2>"""
                htmlString += f"""<h3 id="theCurrent">{currentPlayer}</h3></body></html>"""
                htmlString += f"""<div id="svgContain""> {svg_content} </div>"""
                htmlString+= """</div>"""
                htmlString += """<div style="height: 100px;"></div>"""  
                htmlString+="""<h4 style="text-align:left;"><a href='/starter.html'>End current game and begin new game</a></h4>"""
                htmlString += """</body></html>"""   

    
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header("Content-length", len(htmlString))
                self.end_headers()
                self.wfile.write(bytes(htmlString, "utf-8"))

        elif parsed.path in [ '/trackValues' ]:
            returns = cgi.FieldStorage(fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
            )
            db = Physics.Database()
            maxId=db.getMaxId()
            myTable=db.readTable(maxId-1)
            myCueBall=myTable.findCue()
            # print("here")
            if(myCueBall is None):
                pos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0,
                                Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 )
                sb  = Physics.StillBall(0, pos)
                myTable+=sb
            # print("now here")
            eightBall=myTable.findEight()
            if(eightBall is None):
                ahhNewArray="None"
                myNum=0 
                currentPlayer=None
                pName2=None
                pName1=None
                p1HorL=None
                p2HorL=None
                numHigh=None
                numLow=None
                boolWin="True"
            else:
                xVal= float(returns.getvalue('xValue'))
                yVal= float(returns.getvalue('yValue'))
                cueXVal=float(returns.getvalue('cueXValue'))
                cueYVal=float(returns.getvalue('cueYValue'))
                    # print("cue:", cueXVal, cueYVal)
                    # print("end line: ", xVal, yVal)

                distanceX=cueXVal- xVal 
                distanceY=cueYVal- yVal

                    #velocity
                distanceX =distanceX*10
                if(distanceX >10000):
                        distanceX =10000
                if(distanceX< -10000):
                    distanceX = -10000

                distanceY= distanceY*10
                if(distanceY >10000):
                        distanceY = 10000
                if(distanceY< -10000):
                    distanceY = -10000
                db = Physics.Database()

                    #shoots and gets svg array
                ahhNewArray= game.shoot(joinedName,currentPlayer, myTable, distanceX, distanceY)

                myNewId=db.getMaxId()
                    # print(myNewId)
                mysillyTable=db.readTable(myNewId-1)
                    # print(mysillyTable)
                numHigh=mysillyTable.countHigh()
                numLow=mysillyTable.countLow()
                    #determining low or high
                if(p1HorL=="Not yet assigned"):
                    sunkNum =db.getFirstSunkBallNumber()
                    # print(sunkNum)
                    if(sunkNum is not None):
                            # myPlayer= db.getThePlayer()
                        if(currentPlayer==pName1):
                            if(sunkNum<8):
                                    #print("this")
                                p1HorL="Low"
                                p2HorL="High"
                            else:
                                    #print("thisss")
                                p2HorL="Low"
                                p1HorL="High"
                        elif(currentPlayer==pName2):
                            if(sunkNum<8):
                                    #print("tahis")
                                p2HorL="Low"
                                p1HorL="High"
                            else:
                                    #print("thisamas")
                                p1HorL="Low"
                                p2HorL="High"

                preNewId=db.getMaxId()
                preTab=db.readTable(preNewId-2)
                # print("current table", mysillyTable)
                # print("pre table", preTab)

                if(p1HorL=="Not yet assigned"):
                    if(currentPlayer==pName1):
                        currentPlayer=pName2
                    else:
                        currentPlayer=pName1

                if(currentPlayer==pName1):
                    if(p1HorL=="Low"):
                        # print("hereeeee")
                        newTableCount=mysillyTable.countLow()
                        preTableCount=preTab.countLow()
                        if(newTableCount==preTableCount):
                            currentPlayer=pName2
                            # print("heasre")
                    elif(p1HorL=="High"):
                        # print("hesare")
                        newTableCount=mysillyTable.countHigh()
                        preTableCount=preTab.countHigh()
                        
                        if(newTableCount==preTableCount):
                            currentPlayer=pName2 
                            # print("aahere")
                elif(currentPlayer==pName2):
                    if(p2HorL=="Low"):
                        # print("heare")
                        newTableCount=mysillyTable.countLow()
                        preTableCount=preTab.countLow()
                        if(newTableCount==preTableCount):
                            currentPlayer=pName1 
                            # print("bbhere")
                    elif(p2HorL=="High"):
                        newTableCount=mysillyTable.countHigh()
                        preTableCount=preTab.countHigh()
                        # print("here")
                        if(newTableCount==preTableCount):
                            # print("bhere")
                            currentPlayer=pName1 

                eightBall=mysillyTable.findEight()
                if(eightBall is None):
                    # print("AHHHHHH2")
                    currentPlayer=db.getThePlayer()

                    if(currentPlayer==pName1):
                        if(p1HorL=="Low"):
                            if(mysillyTable.countLow()!=0):
                                winVal=pName2
                            else:
                                winVal=pName1
                        elif(p1HorL=="High"):
                            if(mysillyTable.countHigh()!=0):
                                winVal=pName2
                            else:
                                winVal=pName1
                    if(currentPlayer==pName2):
                        if(p2HorL=="Low"):
                            if(mysillyTable.countLow()!=0):
                                winVal=pName1
                            else:
                                winVal=pName2
                        elif(p2HorL=="High"):
                            if(mysillyTable.countHigh()!=0):
                                winVal=pName1
                            else:
                                winVal=pName2

                    boolWin="True"
                    winName=winVal
                else:
                    boolWin=False
                    winName=None
                #scary json, sends to pool.js

            myNum=len(ahhNewArray)
            myNewArray={"svgs": ahhNewArray, "number": myNum, "cPlayer": currentPlayer,"player2": pName2,"player1": pName1, "play1Ball": p1HorL, "play2Ball": p2HorL, "highNum": numHigh, "lowNum": numLow, "isWinner": boolWin,"theWinner": winName}
            jsonStr = json.dumps(myNewArray)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header("Content-length", len(jsonStr))
            self.end_headers()
            self.wfile.write( bytes( jsonStr, "utf-8" ))
        
        elif parsed.path in [ '/GameEnd' ]:
            returns = cgi.FieldStorage(fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
            )
            winner= returns.getvalue('winner')
            
            html_response = f"""<html><head><title>Game End</title></head><body>"""
            html_response += f"""<h2>{winner} is the winner</h2>"""
            html_response += f"""<br><h2><a href='/starter.html'>Start new game</a></h2></body></html>"""

            # Send the response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(html_response, "utf-8"))

    #part 2
if __name__ == "__main__":
    #port=52097
    try:
        httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), myHandler )
        print( "Server listing in port:", int(sys.argv[1]) )
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" ")
        print("Closing the server. yippee!!!!!!")
