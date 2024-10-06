class Boat:
    # Boat class, represents all ships within the game

    def __init__(self, coor:tuple[int], b_type:int, facing:str):
        """
        IN : tuple[int], int, str
        OUT : Boat
        Create a new boat object
        """
        self.coor = coor
        self.type = b_type
        self.facing = facing
        self.dead = 0
	
    def checkHealth(self, grid:list[list[int]])->int:
        """
        IN : list[list[int]]
        OUT : int
        Check the health of the boat.
        0 : fine
        1 : hit at least once
        2 : sunk
        """

        v=0
        h=1
        if self.facing=="v":
            v=1
            h=0
        
        #Get the length from the type
        b_length=self.type if self.type>2 else self.type+1
        
        #Counting the number of hits
        totalHit=0
        for i in range(b_length):
            if grid[self.coor[1]+i*v][self.coor[0]+i*h]==-1:
                totalHit+=1
        
        #Output
        if totalHit==0:
            return 0
        elif totalHit==b_length:
            self.dead=1
            return 2
        else:
            return 1

    def get_coor(self):
        """
        IN : None
        OUT : tuple[int]
        Give the coordinates of the upper eft tile of the boat
        """
        return self.coor
		
    def getFacing(self):
        """
        IN : None
        OUT : str
        Give the facing of the boat (v or h)
        """
        return self.facing

    def get_b_type(self):
        """
        IN : None
        OUT : int
        Give the type of the boat
        """
        return self.type

    def getDeath(self):
        """
        IN : None
        OUT : int
        0 if the boat is alive, 1 if the boat sunk
        """
        return self.dead
	
    def __str__(self):
        c = "sunk" if self.dead else "afloat"
        return f"Boat : {self.coor}, {self.type}, {self.facing}, {c}"
