import numpy as np
try:
    import Waves
    import GeometricOptics
except:
    import WavesAndOptics.Waves as Waves
    import WavesAndOptics.GeometricOptics as GeometricOptics

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        self.TypeMovementSHM = "sin"
        self.TypeMotionSHM = "SHM"
        self.BoundsSHM = np.array([0.0,10.0])
        self.XAxisSHM = np.linspace(self.BoundsSHM[0],self.BoundsSHM[1],50)
        self.ParametersSHM = np.array([1.0,1.0,0.0,1.0,0.0])      #Amplitude, omega, phi, and gamma, omega damped
        self.PhysicalParametersSHM = np.array([1.0,1.0])  #Mass and k of Spring
        self.ParametersSHM[4] = np.sqrt(self.ParametersSHM[1]**2 - (self.ParametersSHM[3]/(2*self.PhysicalParametersSHM[0]))**2)
        self.ShowAllSHM = False

        self.PositionSHM, self.SpeedSHM, self.AccelerationSHM = Waves.SimpleHarmonicMotion(self.XAxisSHM,self.ParametersSHM,self.PhysicalParametersSHM,self.TypeMovementSHM,self.TypeMotionSHM)
        self.KineticSHM, self.PotentialSHM, self.TotaleSHM = Waves.EnergySHM(self.PositionSHM,self.SpeedSHM,self.PhysicalParametersSHM)
        self.CursorSHM = 0

        self.TypeMovement2DWaves = "sin"
        self.TypeMotion2DWaves = "Full"
        self.BoundsT2DWaves = np.array([0.0,10.0])
        self.BoundsX2DWaves = np.array([0.0,10.0])
        self.XAxis2DWaves = np.linspace(self.BoundsX2DWaves[0],self.BoundsX2DWaves[1],100)
        self.TAxis2DWaves = np.linspace(self.BoundsT2DWaves[0],self.BoundsT2DWaves[1],100)
        self.Parameters2DWaves = np.array([1.0,1.0,1.0,0.0])      #Amplitude, k, omega, and phi
        self.PhysicalParameters2DWaves = np.array([1.0,1.0])  #Mass and k of Spring
        self.ShowAll2DWaves = False

        self.Position2DWaves = Waves.Waves2D(self.TAxis2DWaves,self.XAxis2DWaves,self.Parameters2DWaves,self.TypeMovement2DWaves)
        self.CursorT2DWaves = 0
        self.CursorX2DWaves = 0
        self.TimeSlice2DWave = Waves.Waves2DT(
                                                self.XAxis2DWaves,
                                                self.CursorT2DWaves,
                                                self.Parameters2DWaves,
                                                self.TypeMovement2DWaves
                                            )                                                        
        self.PositionSlice2DWave = Waves.Waves2DX(
                                                self.TAxis2DWaves,
                                                self.CursorX2DWaves,
                                                self.Parameters2DWaves,
                                                self.TypeMovement2DWaves
                                            )  
        ###
        self.CurrentNumberInterfacesRefraction = 1
        self.maxNumberInterfacesRefraction = 10
        self.IndicesRefraction = np.ones(self.maxNumberInterfacesRefraction+1)
        self.PointOfIntersectYRefraction = -np.arange(-1.0,self.maxNumberInterfacesRefraction+1)
        self.showReflectionsRefraction = []
        self.showRefractionRefraction = []
        self.showNormalRefraction = []
        self.showIncidentAngleRefraction = []
        self.showReflectedAngleRefraction = []
        self.showRefractedAngleRefraction = []
        for i in range(self.maxNumberInterfacesRefraction):
            self.showReflectionsRefraction.append(False)
            self.showRefractionRefraction.append(True)
            self.showNormalRefraction.append(False)
            self.showIncidentAngleRefraction.append(False)
            self.showReflectedAngleRefraction.append(False)
            self.showRefractedAngleRefraction.append(False)

        self.PointOfIntersectXRefraction = np.ones(self.maxNumberInterfacesRefraction+2)

        self.AnglesRefraction = 10 * np.ones(self.maxNumberInterfacesRefraction+1)
        self.PointOfIntersectXRefraction[1] = 0

        self.PointOfIntersectXRefraction[0] = -(self.PointOfIntersectYRefraction[0] - self.PointOfIntersectYRefraction[1]) * np.tan(self.AnglesRefraction[0])
        for i in range(1,self.AnglesRefraction.shape[0]-1):
            self.AnglesRefraction[i] = GeometricOptics.RefractionLaw(self.IndicesRefraction[i-1],self.AnglesRefraction[i-1],self.IndicesRefraction[i])
            self.PointOfIntersectXRefraction[i+1] = self.PointOfIntersectXRefraction[i] + np.abs((self.PointOfIntersectYRefraction[i+1]-self.PointOfIntersectYRefraction[i])*np.tan(self.AnglesRefraction[i]*np.pi/180))


        ###
        self.MirrorType = "Concave"
        self.FocalLengthMirrors = 1
        self.CurvatureRadiusMirrors = 2 * self.FocalLengthMirrors
        self.ObjectHeightMirrors = 1
        self.ObjectPositionMirrors = 2

        self.ImagePositionMirrors = GeometricOptics.MirrorEquation(self.ObjectPositionMirrors, self.FocalLengthMirrors, "p")
        self.MagnificationMirrors = -self.ImagePositionMirrors/self.ObjectPositionMirrors
        self.ImageHeightMirrors = self.ObjectHeightMirrors * self.MagnificationMirrors

        self.showObjectMirrors = True
        self.showImageMirrors = True
        self.showRaysParallelMirrors = True
        self.showRaysFocusMirrors = True
