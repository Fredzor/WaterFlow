import math

class WaterTank():
    
    
    def __init__(self, name, diameter, height_floor, height_tank, height_water):
        self.name = name
        self.visited = False
        self.diameter = diameter
        self.height_floor = height_floor # height in m from normal-zero
        self.height_water = height_water  # height of water in m from height_floor
        self.height_water_total = height_water + height_floor # height of water from normal-zero
        self.height_tank = height_tank # height of the tank from height_floor (maximum fill-height)
        self.connections = [] # list of pipes, which are connected to the tank
        

    def append_connection(self, connected_tank, diameter, length, heightTank1, heightTank2, k):
        Pipe(self, connected_tank, diameter, length, heightTank1, heightTank2, k)


class Pipe():
    
    
    def __init__(self, tank1, tank2, diameter, length, heightTank1, heightTank2, k ):
        self.k = k
        self.diameter = diameter
        self.length = length
        self.tank1 = tank1
        self.tank2 = tank2
        self.heightTank1 = heightTank1
        self.heightTank2 = heightTank2
        self.resistances = []
        self.visited = False
        tank1.connections.append(self)
        tank2.connections.append(self)
    
        
    def append_resistance(self, resistance_coefficient):
        self.resistances.append(resistance_coefficient)
        
    
    def waterFlowCalculation(self, height1, height2):
            
            g = 0.81
            density = 1
            viscosity = 1
            
            if self.k < 0.3:
                # flow calculation for smooth pipes
                rohrrauigkeitsbeiwert_annahme = 0.02
                resistances_sum = sum(self.resistances)
                while True:
                    u = (height1 - height2) * 2 * g / (1 + resistances_sum + rohrrauigkeitsbeiwert_annahme * self.diameter / self.length)
                    reynolds = density * abs(u) * self.diameter / viscosity
                    rohrrauigkeitsbeiwert = 0.3164 / (reynolds **  0.25)
                    if 0.99 < rohrrauigkeitsbeiwert_annahme / rohrrauigkeitsbeiwert < 1.01:
                        break
                    rohrrauigkeitsbeiwert_annahme = rohrrauigkeitsbeiwert
            elif self.k >= 0.3:
                # flow calculation for rough pipes
                rohrrauigkeitsbeiwert = (1 / (-2 * math.log10(self.k / (3.71 * self.diameter))))**2
                u = ((height1 - height2) * 2 * g / (1 + resistances_sum + rohrrauigkeitsbeiwert / self.diameter * self.length)) **2
                    
            volumetricFlow = u * self.diameter
            return volumetricFlow
    
        
    def pipeFlowCalculation(self):
  
        # determine which tank has a higher water-height (from which water could flow to the other tank)
        if self.tank1.height_water_total > self.tank2.height_water_total and self.tank1.height_water > self.heightTank1:
            counter_height = max(self.tank2.height_water_total, self.heightTank2)
            volumetricFlow = self.waterFlowCalculation( self.tank1.height_water_total, counter_height)
            
        elif self.tank1.height_water_total < self.tank2.height_water_total and self.tank2.height_water > self.heightTank2:
            counter_height = max(self.tank1.height_water_total, self.heightTank1)
            volumetricFlow = self. waterFlowCalculation( counter_height, self.tank2.height_water_total)
            
        else:
            volumetricFlow = 0
            
        def newHeight(tank, volumetricFlow):
            tank.height_water = tank.height_water + volumetricFlow / tank.diameter
            
        self.tank1.water_height = newHeight(self.tank1, - volumetricFlow)
        self.tank2.water_height = newHeight(self.tank2, volumetricFlow)
        
        self.visited = True
         

class Process():
    
    
    def __init__(self, WaterTanks, fluid = 'H2O'):
        self.WaterTanks = WaterTanks
        self.fluid = fluid
        if self.fluid == 'H2O':
            self.density = 1
            self.viscosity = 1
    
        
    def append_tank(self, WaterTank):
        self.WaterTanks.append(WaterTank)
     
        
    def find_subtrees(self):
        
        for tank in self.WaterTanks:
            tank.visited = False
        
        # num of subtrees
        numSubTrees = 0
        # list with all subtrees
        subTreeList = []
        
        def traverse(tank):
            # sub-function to traverse all tanks which are connected to 'tank' and set visited for each visited to 'True'
            tank.visited = True
            subTree.append(tank)
            for pipe in tank.connections:
                for tank2 in [pipe.tank1, pipe.tank2]:
                    if tank2 != tank and tank2.visited == False:
                        traverse(tank2)
            
        for tank in self.WaterTanks:
            if tank.visited == False:
                # found a non-visited tank and traverse all connected tanks. append them to the 'subTree'
                subTree = []
                numSubTrees += 1
                traverse(tank)
                subTreeList.append(subTree)
        return numSubTrees, subTreeList
    
    
    def modelWaterFlow(self, t_start, t_end, resolution):
        
 
        deltaTime = (t_end - t_start) / resolution
        
        numSubtrees, listSubtrees = self.find_subtrees()
        
        for t in range(t_start, t_end , resolution):
            
            for subtree in listSubtrees:
                
                for tank in subtree:
                    
                    for pipe in tank.connections:
                        
                        if pipe.visited == False:
                            pipe.pipeFlowCalculation()
                            
            
            # resetten the visited-status of each pipe
            for subtree in listSubtrees:
                
                for tank in subtree:
                    print(tank.name, tank.height_water)
                    
                    for pipe in tank.connections:
                        
                        pipe.visited = False
                            
        
            
                        
                        
# concept in order to not calculate the same flow twice (when moving from one or the other direction)
# herefore we need to keept track of whether or not we habe yet calculated a flow
# this can be done by a list of lists in which we have True / False for each connection. 
# After habinf calculated a flow/connection we set the value to True
# everythinf must be set back to False after a calculation for a time has been done
                        
            
            
            
            
 
tank1 = WaterTank(name = 'tank1', diameter = 10, height_floor = 5, height_tank = 5, height_water= 4)  
tank2 = WaterTank(name = 'tank2', diameter = 10, height_floor = 5, height_tank = 5, height_water= 5)  
tank3 = WaterTank(name = 'tank3', diameter = 10, height_floor = 5, height_tank = 5, height_water= 5)  
tank4 = WaterTank(name = 'tank4', diameter = 10, height_floor = 5, height_tank = 5, height_water= 5)  

tank1.append_connection(connected_tank= tank2,
                        diameter = 0.01,
                        length = 100,
                        heightTank1= 2,
                        heightTank2 = 3,
                        k = 0.2
                        )
    
proc = Process([tank1, tank2, tank3, tank4])

proc.modelWaterFlow(10,100,10)

nums, llist = proc.find_subtrees()
print(nums, llist)
                
                
# Speicherung von Wasser bei dicken und langen Rohren
# Einfluss der Länge einer Leitung auf die Fließgeschwindigkeit (Zeitverzug analog zu dem zuvor erwähnten Punkt)
# Rohrleitungen, welche mehrere Tanks miteinander verbinden (3 und mehr)   
# berechnung wasserflow bei nur zum teil benetzter Fläche des kanals
# berechnung freier fluss von einem beckenteil zum anderen (wenn ein Becken als meherere Einzelbecken abgebildet wird)
# speichern der Ergebnisse in arrays für alle Ströme und Füllstände etc. 