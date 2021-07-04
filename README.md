# CardinalBSplineCoefficients
Sometimes you just need the coefficient matrix of an arbitrary order Cardinal B-Spline curve,

These can be hard to find, but you can find a paper detailing how to calculate them efficiently here:
https://www.sciencedirect.com/science/article/pii/S0893965910002284

I needed the matrix for an order 13 cardinal spline for a recreational mathematics project I was working on one weekend, 
so I went to the trouble of implementing the whole algorithm described in the paper.  

It seems like the type of thing that should only really be typed up once, so I'm posting it here for anyone to use.  
Hopefully it helps someone focus on unsolved problems instead of fretting about reimplementing the solution to this one.
