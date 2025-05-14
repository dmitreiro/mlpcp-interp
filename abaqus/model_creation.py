# -*- coding: mbcs -*-
# Do not delete the following import lines
#abaqus cae noGUI=Cruciform.py
#This is the 3D Cruciform NM100 Mesh
os.system('Abaqus job=Job-1.inp user=UMMDp_FLC.f interactive ask_delete=OFF')
from abaqus import *
from abaqusConstants import *
# from odbAccess import *
from pyD import new
from array import array

import __main__
import glob
import os
import csv
import time
import  sys
import numpy as np
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

# Define path for data
current_dir = os.getcwd()
MYCSVDIR = os.path.join(current_dir, 'data', 'regular_mesh')
MYCSVDIR = os.path.normpath(MYCSVDIR)

overwrite=True

#  ----------------------------------------------------------------------------------------------------------------  #
# -----------------------------------  Define the Extrusion Part and Partition  -----------------------------------  #
#  ----------------------------------------------------------------------------------------------------------------  #

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(30.0, 0.0))
s.HorizontalConstraint(entity=g[2], addUndoState=False)
s.Line(point1=(30.0, 0.0), point2=(30.0, 15.0))
s.VerticalConstraint(entity=g[3], addUndoState=False)
s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
s.Line(point1=(0.0, 0.0), point2=(0.0, 30.0))
s.VerticalConstraint(entity=g[4], addUndoState=False)
s.PerpendicularConstraint(entity1=g[2], entity2=g[4], addUndoState=False)
s.Line(point1=(0.0, 30.0), point2=(15.0, 30.0))
s.HorizontalConstraint(entity=g[5], addUndoState=False)
s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
s.FixedConstraint(entity=v[0])
s.EqualLengthConstraint(entity1=g[2], entity2=g[4])
s.EqualLengthConstraint(entity1=g[3], entity2=g[5])
s.CircleByCenterPerimeter(center=(15.0, 15.0), point1=(22.5, 23.75))
s.Line(point1=(15.0, 30.0), point2=(15.0, 26.5244305715896))
s.VerticalConstraint(entity=g[7], addUndoState=False)
s.PerpendicularConstraint(entity1=g[5], entity2=g[7], addUndoState=False)
s.CoincidentConstraint(entity1=v[7], entity2=g[6], addUndoState=False)
s.Line(point1=(30.0, 15.0), point2=(26.5244305715896, 15.0))
s.HorizontalConstraint(entity=g[8], addUndoState=False)
s.PerpendicularConstraint(entity1=g[3], entity2=g[8], addUndoState=False)
s.CoincidentConstraint(entity1=v[8], entity2=g[6], addUndoState=False)
s.autoTrimCurve(curve1=g[6], point1=(19.2347831726074, 25.6309909820557))
s.autoTrimCurve(curve1=g[9], point1=(24.0811347961426, 21.9118900299072))
s.FixedConstraint(entity=v[11])
s.RadialDimension(curve=g[10], textPoint=(3.96877670288086, 3.67629909515381), 
    radius=7.0)
s.FilletByRadius(radius=2.5, curve1=g[7], nearPoint1=(14.8730659484863, 
    23.1115970611572), curve2=g[10], nearPoint2=(13.4191551208496, 
    21.7919178009033))
s.FilletByRadius(radius=2.5, curve1=g[8], nearPoint1=(22.9907035827637, 
    14.9535703659058), curve2=g[10], nearPoint2=(22.1425971984863, 
    13.7538595199585))
s.ObliqueDimension(vertex1=v[3], vertex2=v[4], textPoint=(8.93628692626953, 
    38.5878562927246), value=15.0)
s.dragEntity(entity=v[14], points=((12.5, 24.1651513899117), (12.5, 23.75), (
    13.75, 26.25), (13.75, 27.5)))
s.dragEntity(entity=v[4], points=((15.0, 30.0), (15.0, 30.0), (16.25, 30.0), (
    13.75, 30.0), (11.25, 28.75)))
s.undo()
s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(14.1344108581543, 
    -7.11508655548096), value=30.0)
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s, depth=0.5)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['Part-1']
f, e, d1 = p.faces, p.edges, p.datums
t = p.MakeSketchTransform(sketchPlane=f[9], sketchUpEdge=e[19], 
    sketchPlaneSide=SIDE1, origin=(12.169049, 12.169049, 0.5))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=84.85, gridSpacing=2.12, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
s1.rectangle(point1=(-12.169049, -12.169049), point2=(-2.11879614980537, 
    -2.11879678680635))
s1.CoincidentConstraint(entity1=v[13], entity2=g[5], addUndoState=False)
s1.EqualDistanceConstraint(entity1=v[3], entity2=v[5], midpoint=v[13], 
    addUndoState=False)
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
pickedFaces = f.getSequenceFromMask(mask=('[#200 ]', ), )
e1, d2 = p.edges, p.datums
p.PartitionFaceBySketch(sketchUpEdge=e1[19], faces=pickedFaces, sketch=s1)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)

#  ----------------------------------------------------------------------------------------------------------------  #
# -------------------------------------------  Define the Material  -----------------------------------------------  #
#  ----------------------------------------------------------------------------------------------------------------  #

mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Depvar(n=7)
mdb.models['Model-1'].materials['Material-1'].UserOutputVariables(n=6)
mdb.models['Model-1'].materials['Material-1'].UserMaterial(
mechanicalConstants=())
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
    material='Material-1', thickness=None)                                                                                                                                                                            #Section Homogeneous Solid
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='Set-1')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)                                                                                                                                                                                               #Section Assignment
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(cells=cells)
orientation=None
mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(region=region, 
    orientationType=SYSTEM, axis=AXIS_3, localCsys=orientation, 
    fieldName='', additionalRotationType=ROTATION_ANGLE, 
    additionalRotationField='', angle=0.0, stackDirection=STACK_3)                                                                                                                         #Alfa Defining for Rotation of Field
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=ON)                                                                                                                                                             #Assembly Instance
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', 
    maxNumInc=100000, initialInc=0.1, minInc=1e-20, nlgeom=ON)                                                                                                                               #Step 1 Define | nlgeo ON | increment
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'CDISP', 'CF', 'CSTRESS', 'LE', 'PE', 'PEEQ', 'PEMAG', 'RF', 'S', 'TF', 
    'U','SDV','UVARM', 'COORD'), numIntervals=20)                                                                                                                                                            #Field Output Defining SDV UVARM LE TF 20 FRAMES
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#100 ]', ), )

#  ----------------------------------------------------------------------------------------------------------------  #
# -----------------------------------------  Boundary Conditions Defining  ----------------------------------------  #
#  ----------------------------------------------------------------------------------------------------------------  #

region = a.Set(faces=faces1, name='Set-1')                                                                                                                                                                       #U1 Belongs on Set-2 Wich is x direction
mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Step-1', 
    region=region, u1=2.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)                                                                                                                                                                                                                                 #U1 = 2 mm
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#4 ]', ), )
region = a.Set(faces=faces1, name='Set-2')                                                                                                                                                                       #U2 Belongs on Set-2 Wich is y direction
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', 
    region=region, u1=0.0, u2=2.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)                                                                                                                                                                                                                                 #U2 = 2 mm
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#400 ]', ), )
region = a.Set(faces=faces1, name='Set-3')                                                                                                                                                                       #Set-3 is the X Symetry BC (left)
mdb.models['Model-1'].XsymmBC(name='BC-3', createStepName='Step-1', 
    region=region, localCsys=None)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#200 ]', ), )
region = a.Set(faces=faces1, name='Set-4')                                                                                                                                                                       #Set-4 is the Y Symetry BC (down)
mdb.models['Model-1'].YsymmBC(name='BC-4', createStepName='Step-1', 
    region=region, localCsys=None)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1000 ]', ), )
region = a.Set(faces=faces1, name='Set-5')                                                                                                                                                                       #Set-5 is the Z Symetry BC (behind)
mdb.models['Model-1'].ZsymmBC(name='BC-5', createStepName='Step-1', 
    region=region, localCsys=None)
    
#  ----------------------------------------------------------------------------------------------------------------  #
# -----------------------------------------------  Mesh Defining  -------------------------------------------------  #
#  ----------------------------------------------------------------------------------------------------------------  #

session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
    bcs=OFF, predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.setMeshControls(regions=pickedRegions, algorithm=MEDIAL_AXIS)
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=ENHANCED, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)

#  ----------------------------------------------------------------------------------------------------------------  #
# ------------------------------------------------  Job 1  ---------------------------------------------------------  #
#  ----------------------------------------------------------------------------------------------------------------  #

mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)