	$onCentre$

	int centreIdx = (get_global_id(1)) * get_global_size(0) + get_global_id(0);
	if(boundaryGrid[centreIdx] > 0.01)
	{
		$onBoundary$
	}
	else
	{
		$offBoundary$
	}