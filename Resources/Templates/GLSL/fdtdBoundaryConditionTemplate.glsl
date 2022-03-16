$varsBoundary$

	$onCentre$

	int centreIdx = gl_GlobalInvocationID.y * gridWidth + gl_GlobalInvocationID.x;
	if(boundaryGrid[centreIdx] > 0.01)
	{
		$onBoundary$
	}
	else
	{
		$offBoundary$
	}