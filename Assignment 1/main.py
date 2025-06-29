from typing import *
from dataclasses import dataclass
import unittest
import math

calpoly_email_addresses = ["bdaly01@calpoly.edu"]

#This GlobeRect class contains four parameters for the lower latitude, upper latitude, eastern longitude, and western longitude
#each parameter is a float and they represent the four corners of the box that is the globe rectanglue area
@dataclass(frozen=True)
class GlobeRect:
    lower_latitude: float
    upper_latitude: float
    eastern_longetude: float
    western_longetude: float


    #this function tells whether the lower, and upper latitudes, and the eastern and western longitudes are valid
    #the upper and lower latitudes are valid if they are between 90 and -90 (inclusive)
    #the easter and western longetudes are valid if they are between 0 and 360
    #this function also returns false and flashes error message if numbers inputted incorrectly
    def isvalid(self):
        low = self.lower_latitude
        high = self.upper_latitude
        east = self.eastern_longetude
        west = self.western_longetude

        if low < -90:
            print(f"{low} is not a valid number (below -90)!")
            return False
        elif high > 90:
            print(f"{high} is not a valid number (above 90)!")
            return False
        elif west < 0:
            print(f"{west} is not a valid number (below 0)!")
            return False
        elif east > 360:
            print(f"{east} is not a valid number (above 360)!")
            return False
        elif (high < low) or (east < west):
            print("Coordinates inputted in wrong order!")
            return False
        return True

    #This function finds the distance between the upper and lower latitudes, and western and eastern longitudes
    #It first subtracts the upper from lower to find the distance then multiplies the difference in
    #latitudes (height) times the base which would be the longitudes
    #it returns a float of the area
    def area(self):
        lat1 = self.lower_latitude
        lat2 = self.upper_latitude
        long1 = self.western_longetude
        long2 = self.eastern_longetude
        area = abs(lat2 - lat1) / abs(long2 - long1)
        return area


#this class represents the region within the globerect
#it contains a globerect class and two objects (both strings) for name and terrain
#the only options for inputting to terrain are mountains, ocean, forest and other
@dataclass(frozen=True)
class Region:
    area: 'GlobeRect'
    name: str
    terrain: str

#this function validates whether the use inputted terrain is one of the valid options
#if the use inputs anything other than ocean, mountains, forest, or other, it returns false
#there are only strings utilized in this function
    def isvalidregion(self):
        valid_terrains = ['mountains', 'ocean', 'forest', 'other']
        terrain = self.terrain
        if terrain not in valid_terrains:
            return False
        else:
            return True

#this class describes the condition of the region within the globerectangle
#it has four objects (a region class, an int representing the year, an int representing population, and a float representing
#rate of ghg, tons of CO2 per year
@dataclass(frozen=True)
class RegionCondition:
    region: 'Region'
    year: int
    population: int  #(num of ppl)
    rate: float  #rate of ghg, tons of CO2 per year

    #This function computes the tons of CO2- equivalent emitted per person living in the region per year
    #it Utilizes the rate float variable and divides that py the population float
    def emissions_per_capita(self):   #computes the tons of CO2-equivalent emitted per person living in the region per year
        rate = self.rate
        population = self.population
        if population < 0:
            print("Population cannot be negative!")
            return False
        return (rate/population)

#this function calculates the emissions per square kilometer
#It divides the tons of carbondioxide from the area
    def emissions_per_square_km(self):
        tonsCO2 = self.rate
        area = self.region.area.area()
        if tonsCO2 < area:
            print("Tons of CO2 cannot be negative!")
            return False
        return (tonsCO2/area)

#globe rect (bottom, top, east, west)
#Here I created four region conditions of Toronto, NYC, Hawaii, and Cal Poly
#The region conditions take in a region class and the regions take in a globe rectangle class

globerecttoronto = GlobeRect(43.85, 43.89, 280.89, 280.38)
regiontoronto = Region(globerecttoronto, 'Toronto', 'other')
regionconditiontoronto = RegionCondition(regiontoronto, 2023, 6372000, 14000000)

globerecthawaii = GlobeRect(17.5, 23.63, 209.33, 196.83)
regionhawaii = Region(globerecthawaii, 'Hawaii', 'ocean')
regionconditionhawaii = RegionCondition(regionhawaii, 2023, 1440196, 15380000)

globerectcalpoly = GlobeRect(35.29, 35.49, 239.33, 239.23)
regioncalpoly = Region(globerectcalpoly, 'Cal Poly', 'mountains')
regionconditioncalpoly = RegionCondition(regioncalpoly, 2023, 22440, 48000)

globerectnyc = GlobeRect(285.51, 285.64, 41.01,  40.55)
regionnyc = Region(globerectnyc, 'New York City', 'other')
regionconditionnyc = RegionCondition(regionnyc, 2023, 18937000, 92000000)

#Here I created a list of the different region conditions
#this is a representation of the four region conditions that I constructed above
example_region_conditions = [
    regionconditionnyc,
    regionconditiontoronto,
    regionconditionhawaii,
    regionconditioncalpoly
]

#initial max value
#iterate through region condidions
#keep track of area and population
#find area/population
#keep track of region name
#Return region w largest num associated
#this function takes in the example regions conditions list and returns the densest region
def densest(RegionConditions):
    maximum = 0
    name = ''
    for i in RegionConditions:
        pop = i.population
        area = i.region.area.area()
        pplsqm = (pop/area)   #amount of people per square kilometer
        if pplsqm > maximum:
            maximum = pplsqm
            name = i.region.name
    return name

#Trace Table for densest function
#Iteration     Max                   Name        RegionCondition      Population        Area         PplSqm
# 0           67007846          New York City       NYC                18937000         0.2826         67007846
# 1           81243000          Toronto             Toronto             6372000         0.07843        81243000
# 2           81243000          Toronto             Hawaii              1440196         0.4904         2936778
# 3           81243000          Toronto             Cal Poly            22440           0.02           112000
# return Toronto

#This function accepts a Region Condition and a number of years and returns a new Regioncondition that
#estimates the condition of the region after a specified number of years
#then this function returns a new Regioncondition class with the altered year, population, and rate
def project_condition(condition, years):
    year = condition.year + years
    newregion = condition #create new regioncondition
    if newregion == 'ocean':
        growthrate =  0.0001  #growth rate is 0.0001
    elif newregion == 'forest':
        growthrate =  -0.00001  #growth rate is -0.00001
    elif newregion == 'mountain':
        growthrate =  0.0005  #growth rate is 0.0005
    else:
        growthrate =  0.00003  #growth rate is 0.00003

    pop = newregion.population
    rate = newregion.rate
    for i in range(years):  #accumulates given growthrate over number of years
        pop *= (growthrate + 1)
        rate *= (growthrate + 1)

    newregion = RegionCondition(condition.region, year, pop, rate)

    return newregion




# put all test cases in the "Tests" class.
class Tests(unittest.TestCase):
    def test_example_1(self):
        self.assertEqual(14,14)

#negative test case for negative number
    def test_globe_rect(self):
        obj = GlobeRect(-1, 2, 3, -4)
        result = obj.isvalid()
        expected = False
        self.assertEqual(result, expected)

#negative test case, coordinates in wrong order
    def test_globe_rect1(self):
        obj = GlobeRect(1, 2, 3, 4)
        result = obj.isvalid()
        expected = False
        self.assertEqual(result, expected)

    # negative test case, greater than 360
    def test_globe_rect3(self):
        obj = GlobeRect(1, 2, 361, 4)
        result = obj.isvalid()
        expected = False
        self.assertEqual(result, expected)
    #Positive Test Case
    def test_globe_rectarea(self):
        obj = GlobeRect(10, 11, 14, 4)
        result = obj.isvalid()
        expected = True
        self.assertEqual(result, expected)

# Positive Test Case
    def test_globe_rectarea1(self):
        obj = GlobeRect(10, 11, 14, 4)
        result = obj.area()
        expected = 0.1
        self.assertEqual(result, expected)

    # Positive Test Case
    def test_globe_rectarea1(self):
        obj = GlobeRect(10, 11, 14, 4)
        result = obj.area()
        expected = 0.1
        self.assertEqual(result, expected)

#negative Test Case for negative numbers

    def test_globe_rectarea1(self):
        obj = GlobeRect(10, -11, 14, 44)
        result = obj.area()
        expected = 0.7
        self.assertEqual(result, expected)


# Positive Test Case
    def test_isvalid_region(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 'ocean')
        result = obj.isvalidregion()
        expected = True
        self.assertEqual(result, expected)

# Negative Test Case with int
    def test_isvalid_region(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 2)
        result = obj.isvalidregion()
        expected = False
        self.assertEqual(result, expected)

   #negative test case with float

    def test_isvalid_region(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 83759.90)
        result = obj.isvalidregion()
        expected = False
        self.assertEqual(result, expected)

#positive test case
    def test_emissions_sqcap(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 83759.90)
        obj2 = RegionCondition(obj, 2023, 200, 12)
        result = obj2.emissions_per_capita()
        expected = 0.06
        self.assertEqual(result, expected)

        # positive test case
    def test_emissions_sqcap2(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 83759.90)
        obj2 = RegionCondition(obj, 2023, 4567, 67)
        result = obj2.emissions_per_capita()
        expected = 0.014670462010072258
        self.assertEqual(result, expected)

    # positive test case with negative
    def test_emissions_sqcap3(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 83759.90)
        obj2 = RegionCondition(obj, 2023, 5678, -4567)
        result = obj2.emissions_per_capita()
        expected = -0.8043325114476928
        self.assertEqual(result, expected)

#negative test case with negative population

    def test_emissions_sqcap4(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 83759.90)
        obj2 = RegionCondition(obj, 2023, -5678, -4567)
        result = obj2.emissions_per_capita()
        expected = False
        self.assertEqual(result, expected)

#negative test case with negative tons of co2

    def test_emissions_sqkm(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 83759.90)
        obj2 = RegionCondition(obj, 2023, -5678, -4567)
        result = obj2.emissions_per_square_km()
        expected = False
        self.assertEqual(result, expected)


#positive test case
    def test_emissions_sqkm1(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 83759.90)
        obj2 = RegionCondition(obj, 2023, 58, 567)
        result = obj2.emissions_per_square_km()
        expected = 225.51136363636365
        self.assertEqual(result, expected)


#positive test case
    def test_emissions_sqkm2(self):
        obj = Region(GlobeRect(10, 98, 34, 69), 'toronto', 83759.90)
        obj2 = RegionCondition(obj, 2023, 58, 13)
        result = obj2.emissions_per_square_km()
        expected = 5.170454545454546
        self.assertEqual(result, expected)


#positive test case
    def test_densest(self):
        result = densest(example_region_conditions)
        expected = 'Toronto'
        self.assertEqual(result, expected)

    def test_project_condition(self):
        result = project_condition(regionconditionnyc, 6)
        expected = RegionCondition(region=Region(area=GlobeRect(lower_latitude=285.51,
                                             upper_latitude=285.64,
                                             eastern_longetude=41.01,
                                             western_longetude=40.55),
                                            name='New York City',
                                            terrain='other'),
                                            year=2029,
                                            population=18940408.915659726,
                                            rate=92016561.24204968)
        self.assertEqual(result, expected)
#positive test for calpoly
    def test_project_condition3(self):
        result = project_condition(regionconditioncalpoly, 6)
        expected = RegionCondition(region=Region(area=GlobeRect(lower_latitude=35.29,
                                             upper_latitude=35.49,
                                             eastern_longetude=239.33,
                                             western_longetude=239.23),
                                            name='Cal Poly',
                                            terrain='mountains'),
                                            year=2029,
                                            population=22444.03950295212,
                                            rate=48008.64064802591)
        self.assertEqual(result, expected)

#positive test for toronto
    def test_project_condition2(self):
        result = project_condition(regionconditiontoronto, 6)
        expected = RegionCondition(region=Region(area=GlobeRect(lower_latitude=43.85,
                                             upper_latitude=43.89,
                                             eastern_longetude=280.89,
                                             western_longetude=280.38),
                                             name='Toronto',
                                             terrain='other'),
                                             year=2029,
                                             population=6373147.046025441,
                                             rate=14002520.189007558)
        self.assertEqual(result, expected)
#positive test for hawaii
    def test_project_condition2(self):
        result = project_condition(regionconditionhawaii, 6)
        expected = RegionCondition(region=Region(area=GlobeRect(lower_latitude=17.5,
                                             upper_latitude=23.63,
                                             eastern_longetude=209.33,
                                             western_longetude=196.83),
                                             name='Hawaii',
                                             terrain='ocean'),
                                             year=2029,
                                             population=1440455.2547234236,
                                             rate=15382768.607638305)

        self.assertEqual(result, expected)

if (__name__ == '__main__'):
    unittest.main()


