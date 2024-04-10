import phylib;
import os;
import sqlite3;
import math

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS= phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH=phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH=phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE=phylib.PHYLIB_SIM_RATE;
VEL_EPSILON=phylib.PHYLIB_VEL_EPSILON;
DRAG=phylib.PHYLIB_DRAG;
MAX_TIME=phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS= phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL=0.01

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];


myNumArray = list(range(1, 16))

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0)
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall

    def svg(self):
        cx = self.obj.still_ball.pos.x
        cy = self.obj.still_ball.pos.y
        r = BALL_RADIUS
        fill = BALL_COLOURS[self.obj.still_ball.number]
        number = self.obj.still_ball.number
        if(self.obj.still_ball.number ==0 ):
            return """<line id="myLine" x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:black;stroke-width:14"/> <circle onmousedown="sillyClick(event)" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (cx, cy,cx, cy, cx, cy, r, fill)
        
        if number > 8:
            return """<circle cx="%d" cy="%d" r="%d" fill="%s" />
            <circle cx="%d" cy="%d" r="%d" fill="white" />
            <text x="%d" y="%d" fill="black" font-size="23" text-anchor="middle" alignment-baseline="middle">%s</text>\n""" % (
            cx, cy, r, fill,
            cx, cy, r * 0.55, cx, cy + 5, number)
        else:
            return """<circle cx="%d" cy="%d" r="%d" fill="%s" />
            <circle cx="%d" cy="%d" r="%d" fill="white" />
            <text x="%d" y="%d" fill="black" font-size="23" text-anchor="middle" alignment-baseline="middle">%s</text>\n""" % (
            cx, cy, r, fill,
            cx, cy, r * 0.55, cx, cy + 5, number)
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0);
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    def svg(self):

        cx= self.obj.rolling_ball.pos.x
        cy= self.obj.rolling_ball.pos.y
        r = BALL_RADIUS
        fill = BALL_COLOURS[self.obj.rolling_ball.number]
        number = str(self.obj.rolling_ball.number)
        if(self.obj.rolling_ball.number ==0 ):
            return '<circle onmouseDown= "sillyClick(event)" cx="%d" cy="%d" r="%d" fill="%s" />\n' % (cx, cy, r, fill)
    
        return """<circle cx="%d" cy="%d" r="%d" fill="%s" />
            <circle cx="%d" cy="%d" r="%d" fill="white" />
            <text x="%d" y="%d" fill="black" font-size="23" text-anchor="middle" alignment-baseline="middle">%s</text>\n""" % (
            cx, cy, r, fill,
            cx, cy, r * 0.55, cx, cy + 5, number)
        

class Hole( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__(self,pos):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0);
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = Hole;


    def svg(self):
        cx= self.obj.hole.pos.x
        cy=self.obj.hole.pos.y
        r = HOLE_RADIUS
        return '<circle cx="%d" cy="%d" r="%d" fill="black" />\n' % (cx, cy, r)

class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. 
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y)
      
        # this converts the phylib_object into a  class
        self.__class__ = HCushion

    def svg(self):
        yHold = self.obj.hcushion.y
        if(yHold==0):
            yHold = -25
        
        elif(yHold==TABLE_LENGTH):
            yHold = 2700

        return '<rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n' % (yHold)


class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. 
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0)
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;

    def svg(self):
        xHold = self.obj.vcushion.x
        if(xHold==0):
            xHold = -25
        
        elif(xHold==TABLE_WIDTH):
            xHold = 1350
        
        return '<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n' % (xHold)

    # add an svg method here


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg id ="insideSvg" width="700" height="1375"  style= "width:350; height:687.5" viewBox="-25 -25 1400 2750 "
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""
    FOOTER = """</svg>\n"""

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def cueBall(self):
        for theObj in self:
            if theObj is not None:
                if(theObj.type == phylib.PHYLIB_STILL_BALL): 
                    if(theObj.obj.still_ball.number==0):
                        return theObj
        return None
        
    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,Coordinate(0,0),Coordinate(0,0),Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,Coordinate( ball.obj.still_ball.pos.x,ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg(self):
        svgString = self.HEADER
        #print(svgString)

        for obj in self:
            if obj is not None:
                svgString += obj.svg()
        svgString+= self.FOOTER
        return svgString
    
    def findCue (self):
        cueBall=None
        for tobj in self:
            if(tobj is not None):
                if(tobj.type == phylib.PHYLIB_STILL_BALL):
                    if(tobj.obj.still_ball.number==0):
                        cueBall=tobj
        return cueBall

    def findEight(self):
        eightBall=None
        for tobj in self:
            if(tobj is not None):
                if(tobj.type == phylib.PHYLIB_STILL_BALL):
                    if(tobj.obj.still_ball.number==8):
                        eightBall=tobj
        return eightBall

    def countLow(self):
        numHigh=0
        for tobj in self:
            if(tobj is not None):
                if(tobj.type == phylib.PHYLIB_STILL_BALL or tobj.type == phylib.PHYLIB_STILL_BALL):
                    if(tobj.obj.still_ball.number>0 and tobj.obj.still_ball.number<8):
                        numHigh+=1
            
        return numHigh

    def countHigh(self):
        numLow=0
        for tobj in self:
            if(tobj is not None):
                if(tobj.type == phylib.PHYLIB_STILL_BALL or tobj.type == phylib.PHYLIB_STILL_BALL):
                    if(tobj.obj.still_ball.number>8 and tobj.obj.still_ball.number<16):
                        numLow+=1
            
        return numLow

class Database:

    def __init__(self, reset=False):
        if reset==True and os.path.exists( 'phylib.db' ):
            os.remove( 'phylib.db' )
        self.conn = sqlite3.connect( 'phylib.db' )
        self.cur=self.conn.cursor()
        # self.createDB()

    def __del__(self):
        self.close()
    def createDB( self ):

        #Makes all tables
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Ball (
                BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                BALLNO INTEGER NOT NULL,
                XPOS FLOAT NOT NULL,
                YPOS FLOAT NOT NULL,
                XVEL FLOAT NOT NULL,
                YVEL FLOAT NOT NULL
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS TTable (
                TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIME FLOAT NOT NULL
            )
        ''')


        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS BallTable(
                BALLID INTEGER NOT NULL,
                TABLEID INTEGER NOT NULL,
                FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Shot(
                SHOTID INTEGER PRIMARY KEY AUTOINCREMENT, 
                PLAYERID INTEGER NOT NULL,
                GAMEID INTEGER NOT NULL,
                FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)

            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS TableShot(
                TABLEID INTEGER NOT NULL,
                SHOTID INTEGER NOT NULL,
                FOREIGN KEY (TABLEID) REFERENCES BallTable(TABLEID),
                FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Game(
                GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMENAME VARCHAR(64) NOT NULL 
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Player(
                PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMEID INTEGER NOT NULL,
                PLAYERNAME VARCHAR(64) NOT NULL,
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            )
        ''') 
        self.cur.close()
        self.conn.commit()


    def readTable( self, tableID ):
        #self.conn = sqlite3.connect('phylib.db')
        self.cur = self.conn.cursor()

        tableID+=1
        #print("ID is the folowing {}". format(tableID))
        self.cur.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
        FROM Ball
        JOIN BallTable ON Ball.BALLID = BallTable.BALLID
        WHERE BallTable.TABLEID = ?
        """, (tableID,))

        BTData = self.cur.fetchall()

        if BTData==None or not BTData:
            return None
        # print("Iii get here")
        # print(BTData)

        myTable=Table()
        # print("Iii table here")

        for ballData in BTData:

            # print("I get here")
            ballNo = ballData[1]
            xPos = ballData[2]
            yPos = ballData[3]
            xVel = ballData[4]
            yVel = ballData[5]

            pos=Coordinate(xPos,yPos)
            vel=Coordinate(xVel,yVel)

            if(xVel==0 and yVel==0):
                sb=StillBall(ballNo,pos)
                myTable+=sb

            else:
                #calc acc 
                rb_ax = 0
                rb_ay = 0
                theSpeed=math.sqrt((xVel * xVel) + (yVel * yVel))
                if(theSpeed>VEL_EPSILON):
                    rb_ax= -1 * xVel / theSpeed *DRAG
                    rb_ay= -1 * yVel / theSpeed *DRAG
                    
                acc=Coordinate(rb_ax, rb_ay)
                rb = RollingBall(ballNo, pos, vel, acc)
                myTable+=rb

            self.cur.execute("""SELECT TTable.TIME FROM TTable WHERE TTable.TABLEID== ?""", (tableID,))
            myTable.time = self.cur.fetchone()[0]
        self.cur.close()
        # self.conn.commit()
        return myTable

    def writeTable(self, table ):
        #self.conn = sqlite3.connect('phylib.db')
        self.cur = self.conn.cursor()

        #insert ball into table
        for theObj in table:
            if theObj is not None:
                if(theObj.type == phylib.PHYLIB_STILL_BALL): 
                    #getvalues
                    ballNum=theObj.obj.still_ball.number
                    ballPosx=theObj.obj.still_ball.pos.x
                    ballPosy=theObj.obj.still_ball.pos.y
                    self.cur.execute("INSERT INTO Ball(BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, 0, 0)", (ballNum, ballPosx, ballPosy))

                elif(theObj.type == phylib.PHYLIB_ROLLING_BALL):
                    #getvalues
                    ballNum=theObj.obj.rolling_ball.number
                    ballPosx=theObj.obj.rolling_ball.pos.x
                    ballPosy=theObj.obj.rolling_ball.pos.y
                    ballVelx=theObj.obj.rolling_ball.vel.x
                    ballVely=theObj.obj.rolling_ball.vel.y

                    self.cur.execute("INSERT INTO Ball(BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)", (ballNum, ballPosx, ballPosy, ballVelx, ballVely))

        #more stuff
        self.cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))

        self.cur.execute("SELECT MAX(TABLEID) FROM BallTable")
        myTableId = self.cur.fetchone()[0]
        if(myTableId==None):
            myTableId=1
        else:
            myTableId+=1
       # print(" I get here and table id is {}".format(myTableId))

        for theObj in table:
            if theObj is not None:
                if(theObj.type == phylib.PHYLIB_STILL_BALL or theObj.type == phylib.PHYLIB_ROLLING_BALL):
                    self.cur.execute("SELECT MAX(BALLID) FROM BallTable")
                    ballId = self.cur.fetchone()[0]
                    if(ballId==None):
                        ballId=1
                    else:
                        ballId+=1
                    #print(" I get here and Ball id is {}".format(ballId))
                    self.cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ballId, myTableId))
                    ballId+=1

        self.cur.close()
        # self.conn.commit()
        return myTableId-1
    
    def close(self):
        self.conn.commit()
        self.conn.close()
    
    def getFirstSunkBallNumber(self):
        self.cur=self.conn.cursor()
        self.cur.execute("SELECT MAX(TABLEID) FROM BallTable")
        maxTabId = self.cur.fetchone()[0]
        self.cur.execute("""
        SELECT BALLID
        FROM BallTable
        WHERE TABLEID = ?
    """, (maxTabId,))
    
        ball_ids = self.cur.fetchall()

        ball_numbers = []
        for ball_id in ball_ids:
            self.cur.execute("SELECT BALLNO FROM Ball WHERE BALLID = ?", ball_id)
            ball_number = self.cur.fetchone()[0]
            ball_numbers.append(ball_number)

        myNumArray = list(range(1, 16))

        # Find the first ball number in myNumArray that is not in ball_numbers
        first_sunk_ball = None
        for ball_number in myNumArray:
            if ball_number not in ball_numbers:
                first_sunk_ball = ball_number
                break

        # print("First sunk ball:", first_sunk_ball)
        self.cur.close()
        return first_sunk_ball
    
    def getGame(self, gameID):
            # self.conn = sqlite3.connect('phylib.db')
            self.cur = self.conn.cursor()

            self.cur.execute("""SELECT Player1.PLAYERNAME, Player2.PLAYERNAME, Game.GAMENAME FROM Game
            JOIN Player AS Player1 ON Game.GAMEID = Player1.GAMEID
            JOIN Player AS Player2 ON Game.GAMEID = Player2.GAMEID
            WHERE Game.GAMEID= ?
            """, (gameID,))         
            gameInfo=self.cur.fetchone()
            return gameInfo
    
    def setUp(self):
        table=Table()
        pos = Coordinate( 
        TABLE_WIDTH / 2.0,
        TABLE_WIDTH / 2.0,
    )

        sb = StillBall(1, pos)
        table += sb

        # Ball 2
        pos = Coordinate(
            TABLE_WIDTH / 2.0 + 34,
            TABLE_WIDTH / 2.0 - 55,
        )
        ball_2 = StillBall(2, pos)
        table += ball_2

        # Ball 3
        pos = Coordinate(
            TABLE_WIDTH / 2.0 - 34,
            TABLE_WIDTH / 2.0 - 55,
        )
        ball_3 = StillBall(15, pos)
        table += ball_3

        # Ball 4
        pos = Coordinate(
            TABLE_WIDTH / 2.0 + 68,
            TABLE_WIDTH / 2.0 - 110,
        )
        ball_4 = StillBall(14, pos)
        table += ball_4

        # Ball 5
        pos = Coordinate(
            TABLE_WIDTH / 2.0,
            TABLE_WIDTH / 2.0 - 110,
        )
        ball_5 = StillBall(8, pos)
        table += ball_5

        # Ball 6
        pos = Coordinate(
            TABLE_WIDTH / 2.0 - 68,
            TABLE_WIDTH / 2.0 - 110,
        )
        ball_6 = StillBall(4, pos)
        table += ball_6

        # Ball 7
        pos = Coordinate(
            TABLE_WIDTH / 2.0 + 102,
            TABLE_WIDTH / 2.0 - 165,
        )
        ball_7 = StillBall(6, pos)
        table += ball_7

        # Ball 8
        pos = Coordinate(
            TABLE_WIDTH / 2.0 - 34,
            TABLE_WIDTH / 2.0 - 165,
        )
        ball_8 = StillBall(5, pos)
        table += ball_8

        # Ball 9
        pos = Coordinate(
            TABLE_WIDTH / 2.0 + 34,
            TABLE_WIDTH / 2.0 - 165,
        )
        ball_9 = StillBall(12, pos)
        table += ball_9

        # Ball 10
        pos = Coordinate(
            TABLE_WIDTH / 2.0 - 102,
            TABLE_WIDTH / 2.0 - 165,
        )
        ball_10 = StillBall(13, pos)
        table += ball_10

        # Ball 11
        pos = Coordinate(
            TABLE_WIDTH / 2.0 + 136,
            TABLE_WIDTH / 2.0 - 220,
        )
        ball_11 = StillBall(11, pos)
        table += ball_11

        # Ball 12
        pos = Coordinate(
            TABLE_WIDTH / 2.0 + 68,
            TABLE_WIDTH / 2.0 - 220,
        )
        ball_12 = StillBall(7, pos)
        table += ball_12

        # Ball 13
        pos = Coordinate(
            TABLE_WIDTH / 2.0,
            TABLE_WIDTH / 2.0 - 220,
        )
        ball_13 = StillBall(10, pos)
        table += ball_13

        # Ball 14
        pos = Coordinate(
            TABLE_WIDTH / 2.0 - 68,
            TABLE_WIDTH / 2.0 - 220,
        )
        ball_14 = StillBall(3, pos)
        table += ball_14

        # Ball 15
        pos = Coordinate(
            TABLE_WIDTH / 2.0 - 136,
            TABLE_WIDTH / 2.0 - 220,
        )
        ball_15 = StillBall(9, pos)
        table += ball_15

        # Cue ball also still
        pos = Coordinate(TABLE_WIDTH / 2.0, TABLE_LENGTH - TABLE_WIDTH / 2.0)
        sb = StillBall(0, pos)
        table += sb

        db = Database(reset=True)
        db.createDB()
        db.writeTable(table)

    def setGame(self, gameName, player1Name, player2Name):
            
            self.conn = sqlite3.connect('phylib.db')
            self.cur = self.conn.cursor()

            self.cur.execute("INSERT INTO Game(GAMENAME) VALUES (?)", (gameName,))
            gameID = self.cur.lastrowid
            # print(gameID)
            self.cur.execute("INSERT INTO Player(GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
            self.cur.execute("INSERT INTO Player(GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))

            self.cur.close()
            # self.conn.commit()


    def newShot(self, playerName):
        #writes shot details
        self.conn = sqlite3.connect('phylib.db')
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT GAMEID FROM Player WHERE PLAYERNAME = ?", (playerName,))
        theGameID = self.cur.fetchone()
        # print("gameId is {}".format(theGameID))

        self.cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?", (playerName,))
        playerID = self.cur.fetchone()

        if(playerID is None):
            raise ValueError("Player '{}' not found in the database.".format(playerName))
        #     print("hi")

        self.cur.execute("INSERT INTO Shot(PLAYERID, GAMEID) VALUES (?, ?)", (playerID[0], theGameID[0]))
        shotID = self.cur.lastrowid
        # print("shot id is{}".format(shotID))
        self.cur.close()
        # self.conn.commit()
        return shotID
    
    def writeTableShot(self, tableId, shotId):
        #function i created to write using self
        self.cur = self.conn.cursor()
        self.cur.execute("INSERT INTO TableShot(TABLEID, SHOTID) VALUES (?, ?)", (tableId, shotId))
        # self.conn.commit()
        self.cur.close()
    
    def getMaxId(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT MAX(TABLEID) FROM BallTable")
        newestId = self.cur.fetchone()[0]
        # self.conn.commit()
        self.cur.close()
        return newestId

    def getThePlayer(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT MAX(SHOTID) FROM Shot")
        last_shot_id = self.cur.fetchone()[0]
        self.cur.execute("""
            SELECT Player.PLAYERNAME 
            FROM Player 
                INNER JOIN Shot ON Player.PLAYERID = Shot.PLAYERID 
                WHERE Shot.SHOTID = ?
            """, (last_shot_id,))
        last_shot_player = self.cur.fetchone()
        self.cur.close()
        self.cur.close()
        if(last_shot_player is not None):
            return last_shot_player[0]
        else:
            return None

class Game: 
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            gameID=int(gameID)+1
            # print("id is:")
            # print(gameID)

            gameInfo=Database().getGame(gameID)
            if(gameInfo is not None):
                self.player1Name = gameInfo[0]
                self.player2Name = gameInfo[1]
                self.gameName = gameInfo[2]

        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:

            Database().setGame(gameName, player1Name, player2Name)

        else:
            raise TypeError("Invalid combination of arguments provided to the constructor")

    def shoot( self, gameName, playerName, table, xvel, yvel ):

        # print("table passed in: ")
        # print(table)
        arrayCounter=0
        tableArray=[]
        myDatabase=Database()
        shotID=myDatabase.newShot(playerName)
        cueBall=table.findCue()
        if(cueBall is not None):
            holdNum=cueBall.obj.still_ball.number
            holdxVal=cueBall.obj.still_ball.pos.x
            holdyVal=cueBall.obj.still_ball.pos.y

        else:
            print("Error finding cueball :(")
            return

        #changes type and resets vals
        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.number = holdNum
        cueBall.obj.rolling_ball.pos.x = holdxVal
        cueBall.obj.rolling_ball.pos.y = holdyVal

        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel

        rb_ax = 0
        rb_ay = 0
        theSpeed=math.sqrt((xvel *xvel) + (yvel *yvel))
        if(theSpeed>VEL_EPSILON):
            rb_ax= -1 * xvel / theSpeed *DRAG
            rb_ay= -1 * yvel / theSpeed *DRAG
                
        cueBall.obj.rolling_ball.acc.x = rb_ax
        cueBall.obj.rolling_ball.acc.y = rb_ay

        while table:
            preSeg=table
            anotherTable=table
            preTime= table.time
            table = table.segment()
            if(table is not None):
                postTime=table.time
                segLength=postTime-preTime
                frameInteger= math.floor(segLength/FRAME_INTERVAL)
                for x in range (frameInteger):
                    frameTime= x * FRAME_INTERVAL
                    anotherTable=preSeg.roll(frameTime)
                    anotherTable.time=preTime+frameTime
                    tableArray.append(anotherTable.svg())
                    arrayCounter+=1
                    # tableID=myDatabase.writeTable(anotherTable)
                    # myDatabase.writeTableShot(tableID, shotID)
            else:
                myCueBall=anotherTable.findCue()
                if(myCueBall is None):
                    pos = Coordinate(TABLE_WIDTH/2.0,
                                TABLE_LENGTH - TABLE_WIDTH/2.0 )
                    sb  = StillBall(0, pos)
                    anotherTable+=sb
                # print(anotherTable)
                tableArray.append(anotherTable.svg()) 
                tableID=myDatabase.writeTable(anotherTable)
                myDatabase.writeTableShot(tableID, shotID)


        return tableArray

