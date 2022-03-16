import re

from enum import Enum

from PhysicalModelParser import *  

def generateKernelCL(AST):
    if(isImplicit(AST[0])):
        AST[0].targetScheme =  TargetScheme.Jacobi
        
    if(AST[0].targetScheme == TargetScheme.Explicit):
    
        #Open file to write kernel to.
        with open("Resources/Templates/OpenCL/fdtdKernelTemplate_explicit.cl", 'r') as file:
            strKernelTemplate = file.read()
        kernelFile = open("kernelFile.cl",'w')
        
        #Generate header.
        strHeader = generateHeaderCL(AST)
        strKernelTemplate = re.sub("\$insertHeader\$", strHeader, strKernelTemplate)
        
        #Generate rotation indices.
        strRotationIndices = generateRotationIndicesCL(AST)
        strKernelTemplate = re.sub("\$insertRotationIndices\$", strRotationIndices, strKernelTemplate)
        
        #Generate and insert indices.
        strTimestepIndices = generateIndicesCL(AST)
        strKernelTemplate = re.sub("\$insertIndices\$", strTimestepIndices, strKernelTemplate)

        #Generate and insert variables.
        strTimestepVariables = generateVariablesCL(AST)
        strKernelTemplate = re.sub("\$insertVars\$", strTimestepVariables, strKernelTemplate)
        
        #Generate boundary Condition. @ToDo - Currently a clamped edge Dirichlet condition. Need to enable way of controlling type of BC.
        strBoundaryCondition = generateBoundaryConditionCL(AST)
        strKernelTemplate = re.sub("\$insertBC\$", strBoundaryCondition, strKernelTemplate)
        
        #Generate and insert difference equation#
        strEquation = generateEquation(AST)
        strKernelTemplate = re.sub("\$insertEq\$", strEquation, strKernelTemplate)
        
        #Print generated OpenCL kernel to console.
        return strKernelTemplate
        
        #Write generated OpenCL kernel to file.
        #fileGeneratedKernel = open("kernelFile.cl",'w')
        #kernelFile.write(strKernelTemplate)
    
    if(AST[0].targetScheme == TargetScheme.Jacobi):
        #Open file to write kernel to.
        with open("Resources/Templates/OpenCL/fdtdKernelTemplate_jacobi.cl", 'r') as file:
            strKernelTemplate = file.read()
        kernelFile = open("kernelFile.cl",'w')
        
        #Generate header.
        strHeader = generateHeaderCL(AST)
        strKernelTemplate = re.sub("\$insertHeader\$", strHeader, strKernelTemplate)
        
        #Generate rotation indices.
        strRotationIndices = generateRotationIndicesCL(AST)
        strKernelTemplate = re.sub("\$insertRotationIndices\$", strRotationIndices, strKernelTemplate)
        
        #Generate and insert indices.
        strTimestepIndices = generateIndicesCL(AST)
        strKernelTemplate = re.sub("\$insertIndices\$", strTimestepIndices, strKernelTemplate)

        #Generate and insert variables.
        strTimestepVariables = generateVariablesCL(AST)
        strKernelTemplate = re.sub("\$insertVars\$", strTimestepVariables, strKernelTemplate)
        
        #Generate boundary Condition. @ToDo - Currently a clamped edge Dirichlet condition. Need to enable way of controlling type of BC.
        strBoundaryCondition = generateBoundaryConditionCL(AST)
        strKernelTemplate = re.sub("\$insertBC\$", strBoundaryCondition, strKernelTemplate)
        
        #Generate and insert difference equation#
        strEquation = generateEquationJacobi(AST[0])
        strKernelTemplate = re.sub("\$insertEq\$", strEquation, strKernelTemplate)
        
         #Print generated OpenCL kernel to console.
        #print(strKernelTemplate)
        return strKernelTemplate
        
        #Write generated OpenCL kernel to file.
        #fileGeneratedKernel = open("kernelFile.cl",'w')
        #kernelFile.write(strKernelTemplate)
        
    if(AST.targetScheme == TargetScheme.CrankNikolson):
        pass

def generateHeaderCL(AST):
    retStrHeader = ""
    
    #Generate header for OpenCL implementation.
    if(AST[0].targetScheme == TargetScheme.Explicit):
        strHeaderTemplate = "$insertName$(__global int* idGrid, __global float* modelGrid, __global float* boundaryGrid, int idxRotate, int idxSample, __global float* input, __global float* output, int inputPosition, int outputPosition$insertParams$)"
        retStrHeader = re.sub("\$insertName\$", "fdtdKernel", strHeaderTemplate)   #@ToDo - Add way to generate kernel name here.

        lstCoeffs = []
        strCoeffs = ""
        for eq in AST:
            coefficients = eq.value.find(Variable)
            setCoefficients = set(coefficients)
            for coeff in setCoefficients:
                lstCoeffs.append(str(coeff))

        lstCoeffs = list(dict.fromkeys(lstCoeffs))
        for i in lstCoeffs:
            strCoeffs += ", float " + i
            
        retStrHeader = re.sub("\$insertParams\$", strCoeffs, retStrHeader)
        
    if(AST[0].targetScheme == TargetScheme.Jacobi):
        strHeaderTemplate = "$insertName$(__global float* modelGrid, __global float* boundaryGrid, int idxRotate, int idxSample, __global float* input, __global float* output, int inputPosition, int outputPosition, float convergenceThreshold, float normPrev, float normCurrent$insertParams$)"
        retStrHeader = re.sub("\$insertName\$", "fdtdKernel", strHeaderTemplate)   #@ToDo - Add way to generate kernel name here.
        
        lstCoeffs = []
        strCoeffs = ""
        for eq in AST:
            coefficients = eq.value.find(Variable)
            setCoefficients = set(coefficients)
            for coeff in setCoefficients:
                lstCoeffs.append(str(coeff))

        lstCoeffs = list(dict.fromkeys(lstCoeffs))
        for i in lstCoeffs:
            strCoeffs += ", float " + i
        
        retStrHeader = re.sub("\$insertParams\$", strCoeffs, retStrHeader)
        
    if(AST[0].targetScheme == TargetScheme.CrankNikolson):
        pass
            
    return retStrHeader
    
def generateRotationIndicesCL(AST):       
    strRotation = "int $insertName$ = gridSize * rem(idxRotate+$timestep$, $totalTimesteps$);\n\t"
    strRotationIndices = ""
    
    #Get unique timesteps from all equations.
    maxTimesteps = 0
    for eq in AST:
        if eq.targetScheme == TargetScheme.Explicit:
            if maxTimesteps < eq.numTimesteps()+1:
                maxTimesteps = eq.numTimesteps()+1
        else:
            if maxTimesteps < eq.numTimesteps():
                maxTimesteps = eq.numTimesteps()
    for eq in AST:
        timesteps = eq.value.find(Timestep)
    
        for t in timesteps:
            strTempRotation = re.sub("\$insertName\$", t.getRotationIndex(), strRotation)
            strTempRotation = re.sub("\$timestep\$", str(t.getTimestep()), strTempRotation)
            strTempRotation = re.sub("\$totalTimesteps\$", str(maxTimesteps), strTempRotation)
            
            if strTempRotation not in strRotationIndices:
                strRotationIndices += strTempRotation
                
        #If an explicit scheme, make sure to add the next timestep that is missing. Implicit should capture this anyway.
        if(eq.targetScheme == TargetScheme.Explicit):
            #Add the default next timestep rotation index.
            strTempRotation = re.sub("\$insertName\$", "rotation1", strRotation)
            strTempRotation = re.sub("\$timestep\$", "1", strTempRotation)
            strTempRotation = re.sub("\$totalTimesteps\$", str(maxTimesteps), strTempRotation)
            if strTempRotation not in strRotationIndices:
                    strRotationIndices += strTempRotation

    #Return fully formed set of required timestep indices.
    return strRotationIndices
    
def generateIndicesCL(AST):
    strIndices = ""
    if(AST[0].targetScheme == TargetScheme.Explicit):
        strIndex = "int $indexName$ = $insertRotationIndex$ + ((get_global_id(1)+$xAxis$) * get_global_size(0) + get_global_id(0)+$yAxis$);\n\t"
        
        for eq in AST:
            #Get unique timesteps.      
            timesteps = eq.value.find(Timestep)
            for t in timesteps:
                strTempIndex = re.sub("\$indexName\$", t.getIndex() + "Idx", strIndex)
                strTempIndex = re.sub("\$insertRotationIndex\$", t.getRotationIndex(), strTempIndex)
                strTempIndex = re.sub("\$xAxis\$", str(t.getX()), strTempIndex)
                strTempIndex = re.sub("\$yAxis\$", str(t.getY()), strTempIndex)
                
                if strTempIndex not in strIndices:
                    strIndices += strTempIndex
              
    if(AST[0].targetScheme == TargetScheme.Jacobi):
        strIndex = "int $indexName$ = $insertRotationIndex$ + ((get_global_id(1)+$xAxis$) * get_global_size(0) + get_global_id(0)+$yAxis$);\n\t"
        
        #Get unique timesteps.      
        timesteps = AST.value.find(Timestep)
        for t in timesteps:
            strTempIndex = re.sub("\$indexName\$", t.getIndex() + "Idx", strIndex)
            strTempIndex = re.sub("\$insertRotationIndex\$", t.getRotationIndex(), strTempIndex)
            strTempIndex = re.sub("\$xAxis\$", str(t.getX()), strTempIndex)
            strTempIndex = re.sub("\$yAxis\$", str(t.getY()), strTempIndex)
            
            if strTempIndex not in strIndices:
                strIndices += strTempIndex
            
    #if(AST.targetAPI == TargetAPI.Vulkan):
    #    if(AST.targetScheme == TargetScheme.Explicit):
    #        strIndex = "int $indexName$ = $insertRotationIndex$ + ((gl_GlobalInvocationID.y+$xAxis$) * gridWidth + gl_GlobalInvocationID.x+$yAxis$);\n\t"
    #
    #        for t in timesteps:
    #            strTempIndex = re.sub("\$indexName\$", t.getIndex() + "Idx", strIndex)
    #            strTempIndex = re.sub("\$insertRotationIndex\$", t.getRotationIndex(), strTempIndex)
    #            strTempIndex = re.sub("\$xAxis\$", str(t.getX()), strTempIndex)
    #            strTempIndex = re.sub("\$yAxis\$", str(t.getY()), strTempIndex)
    #            
    #            if strTempIndex not in strIndices:
    #                strIndices += strTempIndex
          
    return strIndices

def generateVariablesCL(AST):
    strVars = ""
    if(AST[0].targetScheme == TargetScheme.Explicit):
        strVar = "float $indexName$;\n\t"
        
        for eq in AST:    
            timesteps = eq.value.find(Timestep)
            for t in timesteps:
                strTempVar = re.sub("\$indexName\$", t.getIndex(), strVar)
                
                if strTempVar not in strVars:
                    strVars += strTempVar
              
    if(AST[0].targetScheme == TargetScheme.Jacobi):
        strVar = "float $indexName$;\n\t"
        
        for eq in AST:    
            timesteps = eq.value.find(Timestep)
            for t in timesteps:
                strTempVar = re.sub("\$indexName\$", t.getIndex(), strVar)
                
                if strTempVar not in strVars:
                    strVars += strTempVar

    return strVars
    
def generateBoundaryConditionCL(AST):
    with open("Resources/Templates/OpenCL/fdtdBoundaryConditionTemplate.cl", 'r') as file:
        strBoundaryConditionTemplate = file.read()
    strVarsBoundary = ""
    strCentre = ""
    strOnBoundary = ""
    strOffBoundary = ""
    
    if(AST[0].targetScheme == TargetScheme.Explicit):
        #Get unique timesteps. 
        for eq in AST:
            #Get unique timesteps.      
            timesteps = eq.value.find(Timestep)
            setTimesteps = set(timesteps)
            for t in setTimesteps:
                strVarsBoundary += "float " + str(t.getIndex()) + ";\n\t"
                if t.getX() == Constant("0") and t.getY() == Constant("0"):
                    strTempIndex = str(t.getIndex()) + " = " + str(t.getGridAccess()) + ";\n\t"
                    if strTempIndex not in strCentre:
                        strCentre += strTempIndex
                else:
                    strTempOnBoundary = str(t.getIndex()) + " = 0;\n\t\t"
                    strTempOffBoundary = str(t.getIndex()) + " = " + str(t.getGridAccess()) + ";\n\t\t"
                    if strTempOnBoundary not in strOnBoundary:
                        strOnBoundary += strTempOnBoundary
                    if strTempOffBoundary not in strOffBoundary:
                        strOffBoundary += strTempOffBoundary
            
        strBoundaryConditionTemplate = re.sub("\$varsBoundary\$", strVarsBoundary, strBoundaryConditionTemplate)
        strBoundaryConditionTemplate = re.sub("\$onCentre\$", strCentre, strBoundaryConditionTemplate)
        strBoundaryConditionTemplate = re.sub("\$onBoundary\$", strOnBoundary, strBoundaryConditionTemplate)
        strBoundaryConditionTemplate = re.sub("\$offBoundary\$", strOffBoundary, strBoundaryConditionTemplate)
    
    if(AST[0].targetScheme == TargetScheme.Jacobi):
        #Get unique timesteps.      
        timesteps = AST.value.find(Timestep)
        setTimesteps = set(timesteps)
        for t in setTimesteps:
            strJacobiIdx = re.sub("t1", "j", t.getIndex())
            strVarsBoundary += "float " + strJacobiIdx + ";\n\t"
            if t.getX() == Constant("0") and t.getY() == Constant("0"):
                strCentre += strJacobiIdx + " = " + str(t.getGridAccess()) + ";\n\t"
            else:
                strOnBoundary += strJacobiIdx + " = 0;\n\t\t"
                strOffBoundary += strJacobiIdx + " = " + str(t.getGridAccess()) + ";\n\t\t"
        
        strBoundaryConditionTemplate = re.sub("\$varsBoundary\$", strVarsBoundary, strBoundaryConditionTemplate)
        strBoundaryConditionTemplate = re.sub("\$onCentre\$", strCentre, strBoundaryConditionTemplate)
        strBoundaryConditionTemplate = re.sub("\$onBoundary\$", strOnBoundary, strBoundaryConditionTemplate)
        strBoundaryConditionTemplate = re.sub("\$offBoundary\$", strOffBoundary, strBoundaryConditionTemplate)
    
    return strBoundaryConditionTemplate

######
#GLSL#
######

def generateKernelGLSL(AST):
    #Open file to write kernel to.
    with open("Resources/Templates/GLSL/fdtdKernelTemplate_explicit.glsl", 'r') as file:
        strKernelTemplate = file.read()
    kernelFile = open("kernelFile.glsl",'w')
    
    #Generate header.
    strHeader = generateHeaderGLSL(AST)
    strKernelTemplate = re.sub("\$insertHeader\$", strHeader, strKernelTemplate)
    
    #Generate rotation indices.
    strRotationIndices = generateRotationIndicesGLSL(AST)
    strKernelTemplate = re.sub("\$insertRotationIndices\$", strRotationIndices, strKernelTemplate)
    
    #Generate and insert indices.
    strTimestepIndices = generateIndicesGLSL(AST)
    strKernelTemplate = re.sub("\$insertIndices\$", strTimestepIndices, strKernelTemplate)
    
    #Generate boundary Condition. @ToDo - Currently a clamped edge Dirichlet condition. Need to enable way of controlling type of BC.
    strBoundaryCondition = generateBoundaryConditionGLSL(AST)
    strKernelTemplate = re.sub("\$insertBC\$", strBoundaryCondition, strKernelTemplate)
    
    #Generate and insert difference equation#
    strEquation = generateEquation(AST)
    strKernelTemplate = re.sub("\$insertEq\$", strEquation, strKernelTemplate)
    
    #Print generated Vulkan kernel to console.
    print(strKernelTemplate)
    
    #Write generated Vulkan kernel to file.
    fileGeneratedKernel = open("kernelFile.glsl",'w')
    kernelFile.write(strKernelTemplate)
    
def generateHeaderGLSL(AST):
    retStrHeader = ""

    if(AST.targetScheme == TargetScheme.Explicit):
        with open("Resources/Templates/GLSL/header_explicit.glsl", 'r') as filelHeader:
            strHeaderTemplate = filelHeader.read()
        retStrHeader = strHeaderTemplate
        
        #Generate number of grids based on number of timesteps.
        numTimesteps = getNumberOfTimesteps(AST)
        retStrHeader = re.sub("\$numTimesteps\$", str(numTimesteps), retStrHeader)
        
        #Add coefficients to the header. Involves the coefficient name and constant_id.
        strCoeffs = ""
        strCoeffsTemplate = "layout (constant_id = $insertNumber$) const float $insertName$ = 0.0;"
        coefficients = AST.value.find(Variable)
        setCoefficients = set(coefficients)
        initialIdConstant = 8               #The initial ID leaves off from the default ID already present.
        idConstant = initialIdConstant
        for coeff in setCoefficients:
            strCoeffsCurrent = re.sub("\$insertName\$", str(coeff), strCoeffsTemplate)
            strCoeffsCurrent = re.sub("\$insertNumber\$", str(idConstant), strCoeffsCurrent)
            strCoeffs += strCoeffsCurrent + "\n"
            idConstant += 1
        
        retStrHeader = re.sub("\$insertCoeffs\$", strCoeffs, retStrHeader)
        
    return retStrHeader
        
def generateRotationIndicesGLSL(AST):       
    strRotation = "int $insertName$ = gridSize * rem(idxRotate+$timestep$, $totalTimesteps$);\n\t"
    strRotationIndices = ""
    
    #Get unique timesteps.      
    timesteps = AST.value.find(Timestep)
    for t in timesteps:
        strTempRotation = re.sub("\$insertName\$", t.getRotationIndex(), strRotation)
        strTempRotation = re.sub("\$timestep\$", str(t.getTimestep()), strTempRotation)
        strTempRotation = re.sub("\$totalTimesteps\$", str(AST.numTimesteps()+1), strTempRotation)
        
        if strTempRotation not in strRotationIndices:
            strRotationIndices += strTempRotation
        
    #Add the default next timestep rotation index.
    strTempRotation = re.sub("\$insertName\$", "rotation1", strRotation)
    strTempRotation = re.sub("\$timestep\$", "1", strTempRotation)
    strTempRotation = re.sub("\$totalTimesteps\$", str(AST.numTimesteps()+1), strTempRotation)
    strRotationIndices += strTempRotation
    
    #Return fully formed set of required timestep indices.
    return strRotationIndices
    
def generateIndicesGLSL(AST):
    strIndices = ""
            
    if(AST.targetScheme == TargetScheme.Explicit):
        strIndex = "int $indexName$ = $insertRotationIndex$ + ((gl_GlobalInvocationID.y+$xAxis$) * gridWidth + gl_GlobalInvocationID.x+$yAxis$);\n\t"

        #Get unique timesteps.      
        timesteps = AST.value.find(Timestep)
        for t in timesteps:
            strTempIndex = re.sub("\$indexName\$", t.getIndex() + "Idx", strIndex)
            strTempIndex = re.sub("\$insertRotationIndex\$", t.getRotationIndex(), strTempIndex)
            strTempIndex = re.sub("\$xAxis\$", str(t.getX()), strTempIndex)
            strTempIndex = re.sub("\$yAxis\$", str(t.getY()), strTempIndex)
            
            if strTempIndex not in strIndices:
                strIndices += strTempIndex
          
    return strIndices
    
def generateBoundaryConditionGLSL(AST):
    with open("Resources/Templates/GLSL/fdtdBoundaryConditionTemplate.glsl", 'r') as file:
        strBoundaryConditionTemplate = file.read()
    strVarsBoundary = ""
    strCentre = ""
    strOnBoundary = ""
    strOffBoundary = ""
    
    #Get unique timesteps.      
    timesteps = AST.value.find(Timestep)
    setTimesteps = set(timesteps)
    for t in setTimesteps:
        strVarsBoundary += "float " + str(t.getIndex()) + ";\n\t"
        if t.getX() == Constant("0") and t.getY() == Constant("0"):
            strCentre += str(t.getIndex()) + " = " + str(t.getGridAccess()) + ";\n\t"
        else:
            strOnBoundary += str(t.getIndex()) + " = 0;\n\t\t"
            strOffBoundary += str(t.getIndex()) + " = " + str(t.getGridAccess()) + ";\n\t\t"
    
    strBoundaryConditionTemplate = re.sub("\$varsBoundary\$", strVarsBoundary, strBoundaryConditionTemplate)
    strBoundaryConditionTemplate = re.sub("\$onCentre\$", strCentre, strBoundaryConditionTemplate)
    strBoundaryConditionTemplate = re.sub("\$onBoundary\$", strOnBoundary, strBoundaryConditionTemplate)
    strBoundaryConditionTemplate = re.sub("\$offBoundary\$", strOffBoundary, strBoundaryConditionTemplate)
    
    return strBoundaryConditionTemplate
    
#Helper functions.
def getNumberOfTimesteps(AST):
    timesteps = AST.value.find(Timestep)
    retNumTimesteps = 1    #Starting at 1, in order to include the the timestep+1 grid required to write to.
    lsTimesteps = []
    for t in timesteps:
        timestep = t.getTimestep()
        if timestep not in lsTimesteps:
            lsTimesteps.append(timestep)
            retNumTimesteps += 1
    
    return retNumTimesteps
    
#Equation uses same syntax between kernels. The order and format of equation may change when kernel specific optimizations explored?
def generateEquation(AST):
    strEq = "if(idGrid[centreIdx] == 0)\n{t1x0y0 = 0.0;}\n"
    for idx, eq in enumerate(AST):
        strEq += "if(idGrid[centreIdx] == " + str(idx+1) + ") {\n\t\t"
        strEq += "t1x0y0 = " + eq.value.__str__() + ";\n}\n\t"
    return strEq

def generateEquationJacobi(AST):
    strEq = AST.value.__str__()
    strNewEq = re.sub("t1", "j", strEq)
    #strNewEq = re.sub("t1", "j", strEq)
    return strNewEq
    
def isImplicit(AST):
    timesteps = AST.value.find(Timestep)
    for t in timesteps:
        if(t.getTimestep().eval() == 1):
            return True
            
    return False