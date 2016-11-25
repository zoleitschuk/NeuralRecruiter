function [X, Theta1, Theta2] = decode_prediction_vars(X_initial, Theta1_initial, Theta2_initial)
	
	% X_initial is currently in cell format. This needs to be decoded into a matrix
	% of size m x n.
	m = size(X_initial, 2);
	X = [];
	
	for i=1:m
		X = [X; X_initial{1,i}];
	end
	
	% Convert X from type int32 into double for functions to work.
	X = double(X);
	
	% Both Theta variables are in the correct form to function with predict.m
	
	Theta1 = Theta1_initial;
	Theta2 = Theta2_initial;
	