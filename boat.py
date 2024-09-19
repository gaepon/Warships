class Boat:
    def __init__(self, coor:tuple[int], b_type:int, facing:str)->None:
        self.coor = coor
        self.type = b_type
        self.facing = facing
        self.dead = 0
	
    def checkHealth(self, grid):
        v=0
        h=1
        if self.facing=="v":
            v=1
            h=0
        b_length=self.type if self.type>2 else self.type+1
        totalHit=0
        for i in range(b_length):
            if grid[self.coor[1]+i*v][self.coor[0]+i*h]==-1:
                totalHit+=1
        if totalHit==0:
            return 0
        elif totalHit==b_length:
            self.dead=1
            return 2
        else:
            return 1

    def get_coor(self):
        return self.coor
		
    def get_b_type(self):
        return self.type

    def getDeath(self):
        return self.dead
	
    def __str__(self):
        return f"Boat : {self.coor}, {self.type}, {self.facing}"
