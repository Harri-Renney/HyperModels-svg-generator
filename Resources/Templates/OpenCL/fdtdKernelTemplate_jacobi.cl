int rem(int x, int y)
{
    return (x % y + y) % y;
}

__kernel
void $insertHeader$
{
	//Rotation Index into model grid//
	int gridSize = get_global_size(0) * get_global_size(1);
    
	$insertRotationIndices$
    
	//Get index for current and neighbouring nodes//
	$insertIndices$
	int t1x0y0Idx = rotation1 + ((get_global_id(1)) * get_global_size(0) + get_global_id(0));
	
	$insertBC$

	do
	{
		normPrev = 0.0;
		normCurrent = 0.0;
		
		t1x0y0 = $insertEq$;
		
		barrier(CLK_GLOBAL_MEM_FENCE);
		
		normCurrent += t1x0y0 * t1x0y0[;
		normPrev += jx0y0 * jx0y0;
		
		if (idxCentre == 1)
		{
			normCurrent = sqrt(normCurrent);
			normPrev = sqrt(normPrev);1
		}
		
		modelGrid[t1x0y0Idx] = t1x0y0;
		
		//Global Synch?
		barrier(CLK_GLOBAL_MEM_FENCE);
		
		jx0y0 = modelGrid[t1x0y0Idx];
		jx0yM1 = modelGrid[t1x0yM1Idx];
		jxM1y0 = modelGrid[t1xM1y0Idx];
		jx1y0 = modelGrid[t1x1y0Idx];
		jx0y1 = modelGrid[t1x0y1Idx];
	
	}while (abs(normPrev - normCurrent) > convergenceThreshold);
	
	if(centreIdx == outputPosition)
	{
		output[idxSample]= t0x0y0;    //@ToDo - Make current timestep centre point auto generated?
	}
	
	if(centreIdx == inputPosition)	//If the position is an excitation...
	{
		t1x0y0 += input[idxSample];	//Input excitation value into point. Then increment to next excitation in next iteration.
	}
	
	modelGrid[t0x0y0Idx] = t1x0y0;
}