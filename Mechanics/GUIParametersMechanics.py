import numpy as np
try:
    import Mechanics1D
except:
    import Mechanics.Mechanics1D as Mechanics1D

try:
    import Constants
except:
    import sys
    import os

    # getting the name of the directory
    # where the this file is present.
    current = os.path.dirname(os.path.realpath(__file__))
    
    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)
    
    # adding the parent directory to 
    # the sys.path.
    sys.path.append(parent)
    
    # now we can import the module in the parent
    # directory.
    import Constants

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        self.mass1D = 1
        self.timeScale1D = np.linspace(0,100,5000)
        self.initialPosition1D = np.array([0,0])
        self.initialVelocity1D = np.array([3,3])
        self.initialAcceleration1D = np.array([0,-Constants.g])

        self.toggleGround1D = True
        self.toggleDynamic1DTrajectory = False
        self.toggleStatic1DTrajectory = True
        self.dynamicSpeed1DTrajectory = 100

        self.trajectory1D, self.Velocitiestrajectory1D, self.trajectory1DEndValue = Mechanics1D.MechanicsTrajectory1D(self.initialPosition1D,self.initialVelocity1D,self.initialAcceleration1D,
                                                              timeScale=self.timeScale1D, toggleGround= self.toggleGround1D)

        self.toggleDynamic2DTrajectory = False
        self.toggleStatic2DTrajectory = True
        self.toggleObjectPositions2DTrajectory = False
        self.toggleAbsValues2DTrajectory = False
        self.dynamicSpeed2DTrajectory = 100
        self.step2DTrajectory = 25

        self.toggleCollision2DTrajectory = False
        self.finalTime2DTrajectory = 3600 * 24 * 365.24
        self.numberSteps2DTrajectory = 4
        self.timeScale2DTrajectory = np.linspace(0,self.finalTime2DTrajectory,int(10**self.numberSteps2DTrajectory))
        self.massesFix2DTrajectory = np.array([False,False])

        self.massFactor2DTrajectory = np.array(["EarthMass","SolarMass"])
        self.mass2DTrajectory = np.array([1.0,1.0])

        self.radiusFactor2DTrajectory = np.array(["EarthRadius","SolarRadius"])
        self.radius2DTrajectory = np.array([1,1])

        self.factorInitialPosition2DTrajectory = np.array(["AstronomicalUnit","AstronomicalUnit"])
        self.initialPosition2DTrajectory = np.array([[1.0,0.0],[0.0,0.0]])
        self.factorInitialVelocity2DTrajectory = np.array(["EarthLinearSpeed","EarthLinearSpeed"])
        self.initialVelocity2DTrajectory = np.array([[0.0,1.0],[0.0,0.0]])

        self.PositionsTrajectory2D, self.VelocitiesTrajectory2D, self.AccelerationsTrajectory2D, self.trajectory2DEndValue = Mechanics1D.ManyBodiesGravitationalEvolution(
            mass = self.mass2DTrajectory*Constants.getConstants(self.massFactor2DTrajectory), timeScale= self.timeScale2DTrajectory, 
            initialPos= self.initialPosition2DTrajectory*Constants.getConstants(self.factorInitialPosition2DTrajectory),
            initialVel=self.initialVelocity2DTrajectory*Constants.getConstants(self.factorInitialVelocity2DTrajectory), 
            massFixed=self.massesFix2DTrajectory,
            collision=self.toggleCollision2DTrajectory,
            radii = self.radius2DTrajectory*Constants.getConstants(self.radiusFactor2DTrajectory)
        )

        self.toggleDynamic3BodyProblem = True
        self.toggleStatic3BodyProblem = True
        self.toggleObjectPositions3BodyProblem = True
        self.toggleAbsValues3BodyProblem = False
        self.dynamicSpeed3BodyProblem = 100        
        self.step3BodyProblem = 25

        self.toggleCollision3BodyProblem = False
        self.finalTime3BodyProblem = 3600 * 24 * 365.24
        self.numberSteps3BodyProblem = 4
        self.timeScale3BodyProblem = np.linspace(0,self.finalTime3BodyProblem,int(10**self.numberSteps3BodyProblem))
        self.numberOfMass3BodyProblem = 3
        self.massesFix3BodyProblem = np.ones(self.numberOfMass3BodyProblem,dtype = int)*0

        self.massFactor3BodyProblem = np.ones(self.numberOfMass3BodyProblem,dtype = object) * "SolarMass"
        self.mass3BodyProblem = np.ones(self.numberOfMass3BodyProblem)

        self.radiusFactor3BodyProblem = np.ones(self.numberOfMass3BodyProblem,dtype = object) * "SolarRadius"
        self.radius3BodyProblem = np.ones(self.numberOfMass3BodyProblem)

        self.factorInitialPosition3BodyProblem = np.ones((self.numberOfMass3BodyProblem,1),dtype = object) * "AstronomicalUnit"
        self.initialPosition3BodyProblem = np.ones((self.numberOfMass3BodyProblem,2))
        self.factorInitialVelocity3BodyProblem = np.ones((self.numberOfMass3BodyProblem,1),dtype = object)*"EarthLinearSpeed"
        self.initialVelocity3BodyProblem = np.ones((self.numberOfMass3BodyProblem,2))
        for i in range(self.numberOfMass3BodyProblem):
            self.mass3BodyProblem[-i-1] *= (i+1)
            self.initialPosition3BodyProblem[i,0] *= i**1
            self.initialPosition3BodyProblem[i,1] *= i**1
            self.initialVelocity3BodyProblem[i-0*int(self.numberOfMass3BodyProblem/2),:] = i
            self.initialVelocity3BodyProblem[i-0*int(self.numberOfMass3BodyProblem/2),1] = 0
        self.initialPosition3BodyProblem[:,0] *= -1
    
        self.PositionsTrajectory3BodyProblem, self.VelocitiesTrajectory3BodyProblem, self.AccelerationsTrajectory3BodyProblem, self.trajectory3BodyProblemEndValue = Mechanics1D.ManyBodiesGravitationalEvolution(
            mass = self.mass3BodyProblem*Constants.getConstants(self.massFactor3BodyProblem), timeScale= self.timeScale3BodyProblem, 
            initialPos= self.initialPosition3BodyProblem*Constants.getConstants(self.factorInitialPosition3BodyProblem),
            initialVel=self.initialVelocity3BodyProblem*Constants.getConstants(self.factorInitialVelocity3BodyProblem), 
            massFixed=self.massesFix3BodyProblem,
            collision=self.toggleCollision3BodyProblem,
            radii = self.radius3BodyProblem*Constants.getConstants(self.radiusFactor3BodyProblem)
        )
