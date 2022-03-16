#version 450
#extension GL_ARB_separate_shader_objects : enable

$insertHeader$

int rem(int x, int y)
{
    return (x % y + y) % y;
}

void main() 
{
	$insertRotationIndices$
	
	//Get index for current and neighbouring nodes//
	$insertIndices$
	int t1x0y0Idx = rotation1 + (((gl_GlobalInvocationID.y) * gridWidth + gl_GlobalInvocationID.x);
	
	float t1x0y0;
	$insertBC$
	
	//Calculate the next pressure value//
	t1x0y0 = $insertEq$;

	if(centreIdx == outputPosition)	//If the position is an excitation...
	{
		outputPayload[idxSample] = modelGrid[t0x0y0];
	}
	if(centreIdx == inputPosition)	//If the position is an excitation...
	{
		t1x0y0 += input[idxSample];	//Input excitation value into point. Then increment to next excitation in next iteration.
	}

	modelGrid[t1x0y0Idx] = t1x0y0;

	//TODO - Decide if indicies increased on GPu or CPU side. I think GPU side better. NEED TO ADD GENERATION OF CORRECT NUMBER ROTATIONS AND BUFFER SIZE.
	//if(centreIdx == 0)  //One thread handling control variables.
	//{
	//	idxRotate = ((++idxRotate) % 3);
	//	idxSample = ((++idxSample) % 128);
	//}
}