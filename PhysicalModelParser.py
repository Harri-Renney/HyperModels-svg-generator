import sys
import re
from enum import Enum

from pyparsing import *

class TargetAPI(Enum):
    OpenCL = 1
    OpenGL = 2
    Vulkan = 3
    CUDA   = 4
    
class TargetScheme(Enum):
    Explicit        = 1
    Jacobi          = 2
    CrankNikolson   = 3
    

def operatorOperands(tokenlist):
    "generator to extract operators and operands in pairs"
    it = iter(tokenlist)
    while 1:
        try:
            yield (next(it), next(it))
        except StopIteration:
            break

class NewEq():
    def __init__(self, tokens):
        self.value = tokens[0]
        
    def __str__(self):
        return str(self.value)
       
    def __repr__(self):
        return self.value

    def eval(self):
        return "\n"

class Constant:
    "Class to evaluate a parsed constant or variable"
    vars_ = {}

    def __init__(self, tokens):
        self.value = tokens[0]
        
    def __str__(self):
        return str(self.value)
       
    def __repr__(self):
        return self.value
            
    def __gt__(self, other):
        return float(self.value) > other
        
    def __lt__(self, other):
        return float(self.value) < other
        
    def __hash__(self):
        return hash(self.value)
        
    def __eq__(self, other):
        return self.value == other.value
        
    def eval(self):
        if re.match(r'[0-9].[0-9]', self.value):
            return float(self.value)
        else:
            return int(self.value)
        #if self.value in EvalConstant.vars_:
        #    return EvalConstant.vars_[self.value]
        #else:
        #    return float(self.value)
            
    def find(self, type):
        if(isinstance(self, type)):
            return [self]
        return ""
        
    def get(self):
        return int(self.value)

class Variable():
    def __init__(self, tokens):
        self.__name = tokens[0]
        
    def __str__(self):
        return str(self.__name)
        
    __repr__ = __str__
        
    def __hash__(self):
        return hash(self.__name)
        
    def __eq__(self, other):
        return self.__name == other.__name
        
    def eval(self, dictionary):
        if self.__name not in dictionary:
            raise Exception('Unknown variable: ' + self.__name)
        return dictionary[self.__name]
        
    def find(self, type):
        if(isinstance(self, type)):
            return [self]
        return ""

class Timestep():
    def __init__(self, tokens):
        #Timestep and coordinates#
        self.__timestep = tokens[0][1]
        self.__x = tokens[0][2]
        self.__y = tokens[0][3]
        
        #Index#
        strIndexName = "t"
        t = self.__timestep.get()
        strIndexName += (("M" + str(abs(t))) if t < 0 else str(t))
        x = self.__x.get()
        y = self.__y.get()
        strIndexName += "x"
        strIndexName += (("M" + str(abs(x))) if x < 0 else str(x))
        strIndexName += "y"
        strIndexName += (("M" + str(abs(y))) if y < 0 else str(y))
        self.__index = strIndexName
        
        #GridAccess#
        self.__gridAccess = "modelGrid[" + str(self.__index) + "Idx]"
        
        #Rotation#
        self.__rotationIndex = "rotation" + (("M" + str(abs(t))) if t < 0 else str(t))
        
    def __str__(self):
        #return "modelGrid[t" + str(self.__timestep) + "x" + str(self.__x) + "y" + str(self.__y) + "]"
        #return "modelGrid[" + self.__index + "]"
        return self.__index
        
    __repr__ = __str__
    
    def __hash__(self):
        return hash(self.__timestep)
        
    def __eq__(self, other):
        if(self.__timestep == other.__timestep and self.__x == other.__x and self.__y == other.__y):
            return True
        return False
    
    def eval(self):
        return "modelGrid[t" + self.__timestep + "x" + self.__x + "y" + self.__y + "]"
        
    def find(self, type):
        if(isinstance(self, type)):
            return [self]
        return ""
        
    #Getters#
    def getTimestep(self):
        return self.__timestep
      
    def getX(self):
        return self.__x
        
    def getY(self):
        return self.__y
        
    def getIndex(self):
        return self.__index
        
    def getGridAccess(self):
        return self.__gridAccess
        
    def getRotationIndex(self):
        return self.__rotationIndex

class SignOp:
    "Class to evaluate expressions with a leading + or - sign"

    def __init__(self, tokens):
        self.sign, self.value = tokens[0]
        
    def __str__(self):
        return str(self.sign) + str(self.value)

    def eval(self):
        mult = {"+": 1, "-": -1}[self.sign] #Creates a -1 or +1 to times the number by. Getting the effect expected of - or + a value.
        return mult * self.value.eval()

    def find(self, type):
        if(isinstance(self,type)):
            return [self]
        return self.value.find(type)
        
class BinOp:
    def __init__(self, tokens):
        self.value = tokens[0]
        
    def __str__(self):
        retStr = "("
        #Handle case of power operation.
        if(self.value[1] == '^'):
            retStr += str(self.value[0])
            for _ in range(self.value[2].eval()-1):
                retStr += '*' + str(self.value[0])
        #Handle all other binary operations.
        else:
            for idx, val in enumerate(self.value):
                retStr += str(val)
        retStr += ")"
        return retStr

    def eval(self):
        
        if(self.value[1] == '^'):
            res = self.value[-1].eval()
            for val in self.value[-3::-2]:
                res = val.eval() ** res
            return res
        if(self.value[1] == '*' or self.value[1] == '/'):
            prod = self.value[0].eval()
            for op, val in operatorOperands(self.value[1:]):
                if op == "*":
                    prod *= val.eval()
                if op == "/":
                    prod /= val.eval()
            return prod
        if(self.value[1] == '+' or self.value[1] == '-'):
            sum = self.value[0].eval()
            for op, val in operatorOperands(self.value[1:]):
                if op == "+":
                    sum += val.eval()
                if op == "-":
                    sum -= val.eval()
            return sum
        
    def find(self, type):
        ret = []
        for val in self.value:
            if (isinstance(val, str) is False):
                (ret.extend(val.find(type)) if val.find(type) != "" else "")
        return ret
        
class PhysicalModelAST:        
    def __init__(self, tokens):
        self.value = tokens[0]
        
        self.__targetAPI = TargetAPI.OpenCL
        self.__targetScheme = TargetScheme.Explicit
        
    @property
    def targetAPI(self):
        return self.__targetAPI

    @targetAPI.setter
    def targetAPI(self, aTargetAPI):
        self.__targetAPI = aTargetAPI
        
    @property
    def targetScheme(self):
        return self.__targetScheme

    @targetScheme.setter
    def targetScheme(self, aTargetScheme):
        self.__targetScheme = aTargetScheme

    def __str__(self):
        return self.value.__str__()
        
    __repr__ = __str__
        
    def eval(self):
        return self.value.eval()
           
    def generateKernel(self):
    
        if(self.__targetAPI == TargetAPI.OpenCL):
            if(self.__targetScheme == TargetScheme.Explicit):
            
                #Open file to write kernel to.
                with open("fdtdKernelTemplate_explicit.cl", 'r') as file:
                    strKernelTemplate = file.read()
                kernelFile = open("kernelFile.cl",'w')
                
                #Generate header.
                strHeader = self.generateHeader()
                strKernelTemplate = re.sub("\$insertHeader\$", strHeader, strKernelTemplate)
                
                #Get unique timesteps.      
                self.timesteps = self.value.find(Timestep)
                
                #Generate rotation indices.
                strRotationIndices = self.generateRotationIndices()
                strKernelTemplate = re.sub("\$insertRotationIndices\$", strRotationIndices, strKernelTemplate)
                
                #Generate and insert indices.
                strTimestepIndices = self.generateIndices()
                strKernelTemplate = re.sub("\$insertIndices\$", strTimestepIndices, strKernelTemplate)
                
                #Generate boundary Condition. @ToDo - Currently a clamped edge Dirichlet condition. Need to enable way of controlling type of BC.
                strBoundaryCondition = self.generateBoundaryCondition()
                strKernelTemplate = re.sub("\$insertBC\$", strBoundaryCondition, strKernelTemplate)
                
                #Generate and insert difference equation#
                strEquation = self.generateEquation()
                strKernelTemplate = re.sub("\$insertEq\$", strEquation, strKernelTemplate)
                
                #Print generated OpenCL kernel to console.
                print(strKernelTemplate)
                
                #Write generated OpenCL kernel to file.
                fileGeneratedKernel = open("kernelFile.cl",'w')
                kernelFile.write(strKernelTemplate)
            
        if(self.__targetAPI == TargetAPI.Vulkan):
            if(self.__targetScheme == TargetScheme.Explicit):
            
                #Open file to write kernel to.
                with open("fdtdKernelTemplate_explicit.glsl", 'r') as file:
                    strKernelTemplate = file.read()
                kernelFile = open("kernelFile.glsl",'w')
                
                #Generate header.
                strHeader = self.generateHeader()
                strKernelTemplate = re.sub("\$insertHeader\$", strHeader, strKernelTemplate)
                
                #Get unique timesteps.      
                self.timesteps = self.value.find(Timestep)
                
                #Generate rotation indices.
                strRotationIndices = self.generateRotationIndices()
                strKernelTemplate = re.sub("\$insertRotationIndices\$", strRotationIndices, strKernelTemplate)
                
                #Generate and insert indices.
                strTimestepIndices = self.generateIndices()
                strKernelTemplate = re.sub("\$insertIndices\$", strTimestepIndices, strKernelTemplate)
                
                #Generate and insert difference equation#
                strEquation = self.generateEquation()
                strKernelTemplate = re.sub("\$insertEq\$", strEquation, strKernelTemplate)
                
                #Print generated Vulkan kernel to console.
                print(strKernelTemplate)
                
                #Write generated Vulkan kernel to file.
                fileGeneratedKernel = open("kernelFile.glsl",'w')
                kernelFile.write(strKernelTemplate)
        
    def generateHeader(self):
        retStrHeader = ""
        
        #Generate header for OpenCL implementation.
        if(self.__targetAPI == TargetAPI.OpenCL):
                if(self.__targetScheme == TargetScheme.Explicit):
                    strHeaderTemplate = "$insertName$(__global float* modelGrid, __global float* boundaryGrid, int rotationIndex, int samplesIndex, __global float* input, __global float* output, int inputPosition, int outputPosition$insertParams$)"
                    retStrHeader = re.sub("\$insertName\$", "fdtdKernel", strHeaderTemplate)   #@ToDo - Add way to generate kernel name here.

                    strCoeffs = ""
                    coefficients = self.value.find(Variable)
                    setCoefficients = set(coefficients)
                    for coeff in setCoefficients:
                        strCoeffs += ", float " + str(coeff)
                    
                    retStrHeader = re.sub("\$insertParams\$", strCoeffs, retStrHeader)
            
        #Generate header for Vulkan implementation.
        if(self.__targetAPI == TargetAPI.Vulkan):
            if(self.__targetScheme == TargetScheme.Explicit):
                with open("header_explicit.glsl", 'r') as filelHeader:
                    strHeaderTemplate = filelHeader.read()
                retStrHeader = strHeaderTemplate
                
                #Add coefficients to the header. Involves the coefficient name and constant_id.
                strCoeffs = ""
                strCoeffsTemplate = "layout (constant_id = $insertNumber$) const float $insertName$ = 0.0;"
                coefficients = self.value.find(Variable)
                setCoefficients = set(coefficients)
                idConstant = 10
                for coeff in setCoefficients:
                    strCoeffsCurrent = re.sub("\$insertName\$", str(coeff), strCoeffsTemplate)
                    strCoeffsCurrent = re.sub("\$insertNumber\$", str(idConstant), strCoeffsCurrent)
                    strCoeffs += strCoeffsCurrent + "\n"
                    idConstant += 1
                
                retStrHeader = re.sub("\$insertCoeffs\$", strCoeffs, retStrHeader)
            
        return retStrHeader
        
    def generateRotationIndices(self):
        strRotation = "int $insertName$ = gridSize * rem(rotationIndex+$timestep$, $totalTimesteps$);\n\t"
        strRotationIndices = ""
        for t in self.timesteps:
            strTempRotation = re.sub("\$insertName\$", t.getRotationIndex(), strRotation)
            strTempRotation = re.sub("\$timestep\$", str(t.getTimestep()), strTempRotation)
            strTempRotation = re.sub("\$totalTimesteps\$", str(self.numTimesteps()+1), strTempRotation)
            
            if strTempRotation not in strRotationIndices:
                strRotationIndices += strTempRotation
            
        #Add the default next timestep rotation index.
        strTempRotation = re.sub("\$insertName\$", "rotation1", strRotation)
        strTempRotation = re.sub("\$timestep\$", "1", strTempRotation)
        strTempRotation = re.sub("\$totalTimesteps\$", str(self.numTimesteps()+1), strTempRotation)
        strRotationIndices += strTempRotation
        
        #Return fully formed set of required timestep indices.
        return strRotationIndices
        
    def generateIndices(self):
        strIndex = "int $indexName$ = $insertRotationIndex$ + ((get_global_id(1)+$xAxis$) * get_global_size(0) + get_global_id(0)+$yAxis$);\n\t"
        strIndices = ""
        for t in self.timesteps:
            strTempIndex = re.sub("\$indexName\$", t.getIndex() + "Idx", strIndex)
            strTempIndex = re.sub("\$insertRotationIndex\$", t.getRotationIndex(), strTempIndex)
            strTempIndex = re.sub("\$xAxis\$", str(t.getX()), strTempIndex)
            strTempIndex = re.sub("\$yAxis\$", str(t.getY()), strTempIndex)
            
            if strTempIndex not in strIndices:
                strIndices += strTempIndex
                
        if(self.__targetAPI == TargetAPI.Vulkan):
            if(self.__targetScheme == TargetScheme.Explicit):
                strIndex = "int $indexName$ = $insertRotationIndex$ + ((gl_GlobalInvocationID.y+$xAxis$) * gridWidth + gl_GlobalInvocationID.x+$yAxis$);\n\t"
                strIndices = ""
                for t in self.timesteps:
                    strTempIndex = re.sub("\$indexName\$", t.getIndex() + "Idx", strIndex)
                    strTempIndex = re.sub("\$insertRotationIndex\$", t.getRotationIndex(), strTempIndex)
                    strTempIndex = re.sub("\$xAxis\$", str(t.getX()), strTempIndex)
                    strTempIndex = re.sub("\$yAxis\$", str(t.getY()), strTempIndex)
                    
                    if strTempIndex not in strIndices:
                        strIndices += strTempIndex
                
        
        return strIndices
        
    def generateBoundaryCondition(self):
        with open("fdtdBoundaryConditionTemplate.cl", 'r') as file:
            strBoundaryConditionTemplate = file.read()
        strVarsBoundary = ""
        strCentre = ""
        strOnBoundary = ""
        strOffBoundary = ""
        
        setTimesteps = set(self.timesteps)
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
        
    def generateEquation(self):
        strEq = self.value.__str__()
        return strEq
        
    #Find all objects of a particular 'type'.
    def find(self, type):
        return self.value.find(type)
        
    def numTimesteps(self):
        timestepsReferenced = []
        timesteps = self.value.find(Timestep)
        for t in timesteps:
            timestepsReferenced.append(t.getTimestep())
        
        setTimestepsReferenced = set(timestepsReferenced)
        numTimesteps = len(setTimestepsReferenced)
        
        return numTimesteps
        
    def getUniqueTimesteps(self):
        timestepsReferenced = []
        timesteps = self.value.find(Timestep)
        for t in timesteps:
            timestepsReferenced.append(t.getTimestep())
        
        setTimestepsReferenced = set(timestepsReferenced)
        
        return setTimestepsReferenced

def defineGrammar():
    ParserElement.setDefaultWhitespaceChars(" \t")
    #Numbers - 0.75, 5, 1000.0
    number = pyparsing_common.fnumber
    number.setParseAction(Constant)

    #Coefficients - mu, lambda
    coefficient = Word(alphas)
    coefficient.setParseAction(Variable)

    #Timesteps - T(0)(0,0), T(-1)(0,0), T(0)(2,-1)
    timestep = Group(Literal("T") + Suppress('(') + number + Suppress(')') + Suppress('(') + delimitedList(number) + Suppress(')'))
    timestep.setParseAction(Timestep)

    #Arithmetic - 5 * 5, mu * mu, lambda * (T(0)(0,0) - T(-1)(0,0))
    signop = oneOf("+ -")
    multop = oneOf("* /")
    plusop = oneOf("+ -")
    expop = Literal("^")
    arithmetic = infixNotation(
        timestep | coefficient | number,
        [
            (signop, 1, opAssoc.RIGHT, SignOp),
            (expop, 2, opAssoc.LEFT, BinOp),
            (multop, 2, opAssoc.LEFT, BinOp),
            (plusop, 2, opAssoc.LEFT, BinOp),
        ],
    )
    arithmetic.setParseAction(PhysicalModelAST)

    #Next equation
    newEq = OneOrMore(arithmetic) + Suppress(LineEnd())
                          
    #Collect all rules in grammar.
    grammar = Forward()
    grammar << OneOrMore(newEq)
    grammar.ignore('#' + restOfLine)
    
    return grammar
    
#Takes a string and grammar, parses and generates physical model AST which is returned.
def parseStr(aStr, aGrammar):
    ParserElement.setDefaultWhitespaceChars(" \t")
    parsedAST = OneOrMore(aGrammar).parseString(aStr)
    print(parsedAST)
    return parsedAST