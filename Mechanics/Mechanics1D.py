import numpy as np
from scipy import special
import math
try:
    import Constants
except:
    import sys
    import os
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    import Constants

def NewPosition(Pos, Vel, Acc, deltaTime):
    """Computes a new position using equations of motion"""
    NewPos = Pos + Vel*deltaTime + 1/2*Acc*deltaTime**2
    return NewPos

def NewVelocity(Vel, Acc, delaTime):
    """Computes a new velocity using equations of motion"""
    NewVel = Vel + Acc * delaTime
    return NewVel

def FindTime(Pos, Vel, Acc):
    """Finds the time to be at a certain position. Only returns the highest time"""
    time = (-Vel-(Vel**2-2*Acc*Pos)**(1/2))/(Acc)
    return time

def MechanicsTrajectory1D(Position:np.ndarray, Velocity:np.ndarray, Acceleration:np.ndarray, timeScale:np.ndarray, toggleGround:bool):
    """Computes the trajectory of a particle with given initial parameters"""
    NewPositions = np.zeros([timeScale.shape[0],Position.shape[0]])
    NewVelocities = np.zeros([timeScale.shape[0],Position.shape[0]])
    endValue = NewPositions.shape[0]
    ContactTime = timeScale[-1]
    for i in range(NewPositions.shape[0]):
        for j in range(NewPositions.shape[1]):
            NewPositions[i,j] = NewPosition(Position[j],Vel=Velocity[j],Acc=Acceleration[j],deltaTime=timeScale[i])
    if toggleGround:
        firstOccurence = -1
        for i in range(NewPositions.shape[0]):
            if NewPositions[i,1] < 0:
                if firstOccurence == -1:
                    firstOccurence = i-1
                ContactTime = FindTime(Pos=Position[1],Vel=Velocity[1],Acc=Acceleration[1])
                NewPositions[i:,1] = NewPosition(Position[1],Vel=Velocity[1],Acc=Acceleration[1],deltaTime=ContactTime)
                NewPositions[i:,0] = NewPosition(Position[0],Vel=Velocity[0],Acc=Acceleration[0],deltaTime=ContactTime)
                endValue = firstOccurence+1
                break
    for i in range(NewPositions.shape[0]):
        if i < endValue:
            NewVelocities[i,0] = NewVelocity(Vel = Velocity[0], Acc = Acceleration[0], delaTime= timeScale[i])
            NewVelocities[i,1] = NewVelocity(Vel = Velocity[1], Acc = Acceleration[1], delaTime= timeScale[i])
        else:
            NewVelocities[i:,0] = NewVelocity(Vel = Velocity[0], Acc = Acceleration[0], delaTime= ContactTime)
            NewVelocities[i:,1] = NewVelocity(Vel = Velocity[1], Acc = Acceleration[1], delaTime= ContactTime)
            break
    return NewPositions, NewVelocities, endValue

def GravitationalForce(mass1, mass2, distance1, distance2):
    """Computes the gravitational force between two objects"""
    normDistanceSquared = ((distance1[0]-distance2[0])**2+(distance1[1]-distance2[1])**2)
    Fg = -Constants.G * mass1 * mass2/(normDistanceSquared)
    return Fg/normDistanceSquared**(1/2)*(distance1 - distance2)

def ManyBodiesGravitationalEvolution(mass,timeScale,initialPos,initialVel,massFixed,collision:bool=False, radii=[0,0]):
    """Computes the evolution of a dynamic system with many masses"""
    Positions = np.zeros((timeScale.shape[0],mass.shape[0],2))
    Velocities = np.zeros((timeScale.shape[0],mass.shape[0],2))
    Accelerations = np.zeros((timeScale.shape[0],mass.shape[0],2))
    endValue = timeScale.shape[0]

    for i in range(timeScale.shape[0]):
        if i == 0:
            for j in range(mass.shape[0]):
                Velocities[0,j,:] = initialVel[j,:]
                Positions[0,j,:] = initialPos[j,:]
        else:
            for j in range(mass.shape[0]):
                if not massFixed[j]:
                    TotalForce = np.zeros(2)
                    for k in range(mass.shape[0]):
                        if j != k:
                            #distanceTmp = ((Positions[i,j,0]-Positions[i,k,0])**2+(Positions[i,j,1]-Positions[i,k,1])**2)**(1/2)
                            TotalForce += GravitationalForce(mass1=mass[j],mass2=mass[k],distance1=Positions[i-1,j,:],distance2=Positions[i-1,k,:])
                    deltaTime = timeScale[i] - timeScale[i-1]
                    Accelerations[i,j,:] = TotalForce/mass[j]
                    Velocities[i,j,:] = Velocities[i-1,j,:] + deltaTime * Accelerations[i,j,:]
                    Positions[i,j,:] = Positions[i-1,j,:] + deltaTime * Velocities[i-1,j,:] + 0.5 * deltaTime**2 * Accelerations[i,j,:]
                else:
                    Accelerations[i,j,:] = [0,0]
                    Velocities[i,j,:] = [0,0]
                    Positions[i,j,:] = Positions[i-1,j,:]
        if collision:
            for j in range(mass.shape[0]):
                for k in range(mass.shape[0]):
                    distanceTmp = ((Positions[i,j,0]-Positions[i,k,0])**2+(Positions[i,j,1]-Positions[i,k,1])**2)**(1/2)
                    if distanceTmp <= radii[j] + radii[k] and j != k:
                        print(distanceTmp,radii[j],radii[k])
                        endValue = i
                        Positions[i:,:,:] = Positions[i,:,:]
                        Velocities[i:,:,:] = Velocities[i,:,:]
                        Accelerations[i:,:,:] = Accelerations[i,:,:]
                        return Positions,Velocities,Accelerations,endValue
    return Positions,Velocities,Accelerations,endValue