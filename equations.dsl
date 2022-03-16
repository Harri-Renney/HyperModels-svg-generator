#1 + 2 * (2 + 3) * 1
#(2 - (20*(mu*mu))) * u[0,0,0] + (8*(mu*mu)) * (u[0,0,1] + u[0,0,-1] + u[0,1,0] + u[0,-1,0]) - (2*(mu*mu)) * (u[0,1,1] + u[0,1,-1] + u[0,-1,1] + u[0,-1,-1]) - (mu*mu) * (u[0,0,2] + u[0,0,-2] + u[0,2,0] + u[0,-2,0] - u[-1,0,0])
#(2 - (20*(mu^2))) * T(0)(0,0) + (8*(mu*mu)) * (T(0)(0,1) + T(0)(0,-1) + T(0)(1,0) + T(0)(-1,0)) - (2*(mu^2)) * (T(0)(1,1) + T(0)(1,-1) + T(0)(-1,1) + T(0)(-1,-1)) - (mu^2) * (T(0)(0,2) + T(0)(0,-2) + T(0)(2,0) + T(0)(-2,0)) - T(-1)(0,0)
#(-mu^2) * (T(0)(1,0) + T(0)(-1,0)) + lambda
#2 * T(0)(0,0) - T(-1)(0,0) + (lambda^2) * (T(0)(0,1) + T(0)(0,-1) + T(0)(1,0) + T(0)(-1,0) - 4*T(0)(0,0))
#( 2 * T(0)(0,0) + (mu - 1.0) * T(-1)(0,0) + lambda * (T(0)(0,1) + T(0)(0,-1) + T(0)(1,0) + T(0)(-1,0) - (4*T(0)(0,0))) ) * (1.0 / (mu + 1.0))

#2D Heat Diffusion? - http://geodynamics.usc.edu/~becker/teaching/557/problem_sets/problem_set_fd_2dheat.pdf
#T(0)(0,0) + xHeat * (T(0)(0,1) - 2 * T(0)(0,0) + T(0)(0,-1)) + yHeat * (T(0)(1,0) - 2 * T(0)(0,0) + T(0)(-1,0)) + productionHeat
# The boundary condition can just be Dirichlet/clamped. Setting the boundary to some constant temperature. See article also for how do Neumann condition.

#Implicit Heat Equation
#alpha * deltaT * (((T(1)(1,0) - 2 * T(1)(0,0) + T(1)(-1,0)) / deltaX^2) + ((T(1)(0,1) - 2 * T(1)(0,0) + T(1)(0,-1)) / deltaY^2)) + T(0)(0,0)

#1D String equation with general and and frequency damping
(2 * T(0)(0,0) + ((deltaT*deltaT) * (((c*c) * ((T(0)(1,0) - 2 * T(0)(0,0) + T(0)(-1,0)) / (deltaX*deltaX))) - ((2*omegaOne) * ((T(0)(0,0) - T(-1)(0,0)) / deltaT) + ((2*omegaTwo) * ((1/deltaT) * (((T(0)(1,0) - 2 * T(0)(0,0) + T(0)(-1,0)) - (T(-1)(1,0) - 2 * T(-1)(0,0) + T(-1)(-1,0))) / (deltaX*deltaX))))))) - T(-1)(0,0))
(2 * T(0)(0,0) + ((deltaT^2) * (((c*c) * ((T(0)(1,0) - 2 * T(0)(0,0) + T(0)(-1,0)) / (deltaX^2))) - ((2*omegaOne) * ((T(0)(0,0) - T(-1)(0,0)) / deltaT) + ((2*omegaTwo) * ((1.0/deltaT) * (((T(0)(1,0) - 2 * T(0)(0,0) + T(0)(-1,0)) - (T(-1)(1,0) - 2 * T(-1)(0,0) + T(-1)(-1,0))) / (deltaX^2))))))) - T(-1)(0,0))

#SImple 1D wave equation
(2 * T(0)(0,0) + (stringLambda^2 * (T(0)(1,0) - 2 * T(0)(0,0) + T(0)(-1,0))) - T(-1)(0,0)) * (1.0 / (stringMu + 1.0))

# 1D Acoustic Tube - Webster's Equation
2 * (1 - lambda^2) * T(0)(0,0) - T(0)(-1,0) + ( lambda^2 * 

# 2D plate equation from Silvin's Thesis - This has  frequency-independent and  frequency-dependent damping.
(2 - 20 * mu*mu - 4 * ((2 * sigmaOne * deltaT) / (deltaX*deltaX))) * T(0)(0,0) + ((8 * mu * mu + ((2 * sigmaOne * deltaT) / (deltaX*deltaX))) * (T(0)(1,0) + T(0)(-1,0) + T(0)(0,1) + T(0)(0,-1))) - ((2 * mu * mu) * (T(0)(1,1) + T(0)(-1,1) + T(0)(1,-1) + T(0)(-1,-1))) - ((mu*mu) * (T(0)(2,0) + T(0)(0,2) + T(0)(-2,0) + T(0)(0,-2))) + ((sigmaZero * deltaT - 1 + 4 * ((2 * sigmaOne * deltaT) / (deltaX*deltaX))) * T(-1)(0,0)) - (((2 * sigmaOne * deltaT) / (deltaX*deltaX)) * (T(-1)(1,0) + T(-1)(-1,0) + T(-1)(0,1) + T(-1)(0,-1)))

# 2D Stiff Membrane - Combination of 2D wave and linear plate equations