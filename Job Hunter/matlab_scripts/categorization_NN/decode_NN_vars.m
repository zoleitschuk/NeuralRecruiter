function [X, Yi, Ys] = decode_NN_vars(X_initial, Yi_initial, Ys_initial)
	
	% X_initial is currently in cell format. This needs to be decoded into a matrix
	% of size m x n.
	m = size(X_initial, 2);
	X = [];
	
	for i=1:m
		X = [X; X_initial{1,i}];
	end
	
	% Convert X from type int32 into double for functions to work.
	X = double(X);
	
	% Both Y variables need to be transposed as the NN calcs. require them to be m x 1,
	% not the current 1 x m.
	
	Yi = Yi_initial';
	Ys = Ys_initial';
	