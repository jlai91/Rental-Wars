#==============================================================================
# Model class
# Used in CSS 458 A Spring 2024 Final Project - Rental Wars
#
# Team Digital Directors
# May 2024
#==============================================================================
# Class Hierarchy: Model(Top)

# Temp TODO: 
# High-Priority: 
#   complete sim_step()
#   brainstorm random events and add to event()
# Low-Priority: 
#   create data storage variables for values of note that are lost by end of simulation (needs further discussion)
#   

#- Imports of packages and modules:
import numpy as N
import random
import matplotlib.pyplot as plt
from .building import Building
from .city import City
from .landowner import Landowner
from .unit import Unit
from . import visualize as V

#========================== USER ADJUSTABLE (begin) ==========================
city_size = 20                                                              # City Size
num_landowners = 20                                                         # Initial number of Land Owners
num_months = 240                                                            # Number of months the simulation will run
num_money_min = 50000                                                       # Minimum amount of money a Landowner initializes with
num_money_max = 500000                                                      # Maximum amount of money a Landowner initializes with
num_patience_min = 3                                                        # Minimum amount of months a Landowner is willing to wait to start a project
num_patience_max = 12                                                       # Maximum amount of months a Landowner is willing to wait to start a project
owner_type = ["Pass", "Agg", "Mod", "P-Mod", "A-Mod"]                       # Choices of Landowner Disposition/Preference/Type
prob_residential = [0.6, 0.7, 0.8, 0.9, 1.0]                                # Likeliness of a grid unit being a residential building when initialized
num_poi = 20                                                                # Initial number of Points of Interest in the City

#=========================== USER ADJUSTABLE (end) ===========================

class Model:
    def __init__(self, prob_res):
        """Model Initialization Function
        
        Initializes City Class, Landowner List, and Simulation Step Count. 
        Initialized Model is then step-progressed until intended month is reached.
        """
        self.month = 0                                                      # Initialize Month Count
        self.step = 0                                                       # Initialize Step Phase Count
        self.city = City(city_size, prob_res, num_poi)                      # Initialize City using Size, residential probability, and PoI number adjustables
        self.landowners = []                                                # Initialize Landowner List
        for _ in range(num_landowners):                                     # Populate Landowner List using:
            money = random.randint(num_money_min, num_money_max)            # Random int between min and max money adjustable for initial starting funds
            patience = random.randint(num_patience_min,num_patience_max)    # Random int between min and max patience adjustable for patience in months
            type = random.choice(owner_type)                                # Random choice of owner_type to establish Landowner disposition
            self.landowners.append(Landowner(money, patience, type))

    def run_sim(self, steps):
        """Simulation Run Function
        
        Steps model until target month is reached. Triggers random event every 60 months (5 years).
        """
        while (self.month!=steps):
            self.sim_step()
            if (self.month>0 and self.month%60==0):
                self.event()

    def sim_step(self):
        """Simulation Step Function
        
        Checks step phase of model and updates city/landowners accordingly:
        
        0 - Buildings: Update Vacancies, -> 1
        1 - Landowners: Collect Rent, -> 2
        2 - Buildings: Update Rent based on Owner type -> 3
        3 - Landowners: Update/Begin Decisions/Projects -> 4
        4 - City: Remove Retired Landowners -> 0
        """
        # update building ages and statuses
        for row in self.city.grid:
            for building in row:
                if building:
                    building.age += 1
                    # additional logic for updating status, collecting rent, etc

        # Landowner actions
        for landowner in self.landowners:
            # example of a decison a landowner can make change or add more 
            if landowner.money > 50000:
                for x in range(self.city.size):
                    for y in range(self.city.size):
                        building = self.city.get_building(x, y)
                        if building and building.owner is None:
                            landowner.acquire_building(building)
    
    def event(self,i=random.randint(0,2)):
        """Event Function
        
        Holds an event that occurs in the simulation at random. Function details are held in this function and called by index

        (Events are expected to be random, but for testing purposes or targeted examination may be arbitrarily constant) 
        """
        temp = None

# initialize the model
model = Model(prob_residential[0]) # temporarily setting residential probability to 60%, may consider running multiple models of varying probabilities down the road

# run the simulation
model.run_sim(num_months)