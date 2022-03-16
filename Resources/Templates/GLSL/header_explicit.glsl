layout (constant_id = 1) const uint WORKGROUP_X = 256;
layout (constant_id = 2) const uint WORKGROUP_Y = 1;
layout (constant_id = 3) const int gridWidth = 64;
layout (constant_id = 4) const int gridHeight = 64;
layout (constant_id = 5) const int gridSize = 4096;
layout (constant_id = 6) const int inputPosition = 64;
layout (constant_id = 7) const int outputPosition = 256;

$insertCoeffs$

layout (local_size_x_id = 1, local_size_y_id = 2) in;

layout(binding = 1) buffer pressureBuffer
{
   float modelGrid[$numTimesteps$*WIDTH*HEIGHT];
};

layout(binding = 2) buffer boundaryBuffer
{
   float boundaryGrid[];
};
layout(binding = 3) buffer outputBuffer
{
	float output[];
};
layout(binding = 4) buffer excitationBuffer
{
	float input[];
};
layout(binding = 5) buffer deviceLocalBuffer
{
	int idxRotate;
	int idxSample;
};