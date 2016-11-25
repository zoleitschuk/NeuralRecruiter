function [Theta1_interest, Theta2_interest, Theta1_skills_match, Theta2_skills_match] = main_NN(X_input, Yi_input, Ysm_input)
	% This file will run a 3-layer categorization neural network.

	% Settup some parameters
	[X, Yi, Ysm] = decode_NN_vars(X_input, Yi_input, Ysm_input);
	input_layer_size  = size(X,2);
	hidden_layer_size = size(X,2);
	num_labels = 5;

	initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
	initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);

	% Unroll parameters
	initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];  


	% ------------------------------------------------------------------------------------------------------
	% Step 3: Feed data into neural network.
	% ------------------------------------------------------------------------------------------------------
	fprintf('\nTraining Neural Network... \n')

	%  After you have completed the assignment, change the MaxIter to a larger
	%  value to see how more training helps.
	options = optimset('MaxIter', 200);

	%  You should also try different values of lambda
	lambda = 4;

	% ********************************************************************************************************
	% Train NN for interests
	% ********************************************************************************************************
	
	% Create "short hand" for the cost function to be minimized
	costFunction_interests = @(p) nnCostFunction(p, ...
									   input_layer_size, ...
									   hidden_layer_size, ...
									   num_labels, X, Yi, lambda);

	% Now, costFunction is a function that takes in only one argument (the
	% neural network parameters)
	[nn_params, cost] = fmincg(costFunction_interests, initial_nn_params, options);

	% Obtain Theta1 and Theta2 back from nn_params
	Theta1_interest = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
					 hidden_layer_size, (input_layer_size + 1));

	Theta2_interest = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
					 num_labels, (hidden_layer_size + 1));
	
	
	% ********************************************************************************************************
	% Train NN for qualifications
	% ********************************************************************************************************
	
	% Create "short hand" for the cost function to be minimized
	costFunction_skills_match = @(p) nnCostFunction(p, ...
									   input_layer_size, ...
									   hidden_layer_size, ...
									   num_labels, X, Ysm, lambda);

	% Now, costFunction is a function that takes in only one argument (the
	% neural network parameters)
	[nn_params, cost] = fmincg(costFunction_skills_match, initial_nn_params, options);

	% Obtain Theta1 and Theta2 back from nn_params
	Theta1_skills_match = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
					 hidden_layer_size, (input_layer_size + 1));

	Theta2_skills_match = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
					 num_labels, (hidden_layer_size + 1));
					 
	% ********************************************************************************************************
	
	% save('Thetas.mat','Theta1_interest', 'Theta2_interest', 'Theta1_skills_match', 'Theta2_skills_match');

end