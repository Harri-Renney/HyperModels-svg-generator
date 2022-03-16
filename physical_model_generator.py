from flask import Flask, render_template, redirect, url_for,request, jsonify
from flask import make_response
app = Flask(__name__)

import sys
import re
from enum import Enum

from pyparsing import *

from PhysicalModelParser import *
from PhysicalModelGenerator import *

@app.route("/")
def home():
  return "hi"
@app.route('/index', methods=['GET', 'POST'])
def index():
  response = jsonify({'some': 'noob'})
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route('/parse', methods=['GET', 'POST'])
def parse():

  #strEquation = "2 * T(0)(0,0) + ((deltaT*Delta*) * (((c*c) * ((T(0)(1,0) - 2 * T(0)(0,0) + T(0)(-1,0)) / (deltaX*deltaX))) - ((2*omegaOne) * ((T(0)(0,0) - T(-1)(0,0)) / deltaT) + ((2*omegaTwo) * ((1/deltaT) * (((T(0)(1,0) - 2 * T(0)(0,0) + T(0)(-1,0)) - (T(-1)(1,0) - 2 * T(-1)(0,0) + T(-1)(-1,0))) / (deltaX*deltaX))))))) - T(-1)(0,0)"

  strEquation = request.form['mydata']
  print(strEquation)

  #Define grammar
  grammar = defineGrammar()
  
  #Parse equation and create AST from it.
  parsedAST = parseStr(strEquation, grammar)
  print(strEquation, "->", parsedAST.dump())

  #Prepare AST target API generation.
  parsedAST[0].targetAPI = TargetAPI.OpenCL
  #print(parsedAST[0].targetAPI)
  
  #Prepare AST target scheme generation.
  parsedAST[0].targetScheme = TargetScheme.Explicit
  #print(parsedAST[0].targetScheme)
  
  #Run AST generation based on targetted API and scheme.
  #parsedAST[0].generateKernel()
  #if parsedAST[0].targetAPI == TargetAPI.OpenCL:
  #    generateKernelCL(parsedAST[0])
  #if parsedAST[0].targetAPI == TargetAPI.Vulkan:
  #    generateKernelGLSL(parsedAST[0])

  temp = generateKernelCL(parsedAST)
  print(temp)
  response = jsonify({'name': temp})
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route('/login', methods=['GET', 'POST'])
def login():
  message = None
  if request.method == 'POST':
    datafromjs = request.form['mydata']
    result = "return this"
    resp = make_response('{"response": '+result+'}')
    resp.headers['Content-Type'] = "application/json"
    return resp
    return render_template('login.html', message='')

if __name__ == "__main__":
  app.run(debug = True)

