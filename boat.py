class Boat:
	def __init__(self, coor:tuple[int], b_type:int, facing:str)->None:
		self.coor = coor
		self.type = b_type
		self.facing = facing
	
	def get_coor(self):
		return self.coor
		
	def get_b_type(self):
		return self.type
	
	def __str__(self):
		return f"Boat : {self.coor}, {self.type}, {self.facing}"
