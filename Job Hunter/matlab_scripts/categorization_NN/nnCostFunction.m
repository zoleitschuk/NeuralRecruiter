function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);
         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));


% Add bias column to X and compute a2 = sigmoid(X*Theta1')
bias = ones(m, 1);
a1 = [bias X];
a2 = sigmoid(a1*Theta1');
% size(a2)

% Add bias column to a1 and compute a3 = sigmoid(a1*Theta2')
a2 = [bias a2];
a3 = sigmoid(a2*Theta2');

% In a 2 layer neural network h = a3
h = a3;
% size(h)

% y is currently a 5000 by 1 vector containing numbers 1 to 10.
% Recode y so that it is a 5000 by 10 matrix containing boolean values for each index.
% This is done by creating a 5000 by 10 matrix containing the column index values
% in each row, and then performing a boolean comparison between y and the created matrix.
temp_index = ones(m,num_labels);

for i=1:num_labels
 temp_index(:,i) = i;
endfor

y_new = (temp_index==y);
% size(y_new)
% y_new(1:15)

% Calculate cost function.
% Calculate cost for each label. result will be a num_labels*1 matix
% Calculate total cost. Sum across all labels
J_cost_term = sum((((-y_new.*log(h))-(1-y_new).*log(1-h))/m)*ones(num_labels,1));

% Calculate the regularizattion term for the cost function for a 3 layer NN.
Theta1_reg = Theta1;
Theta1_reg(:,1) = [];
Theta2_reg = Theta2;
Theta2_reg(:,1) = [];

layer1_reg = sum((Theta1_reg .^ 2)*ones(input_layer_size,1));
layer2_reg = sum((Theta2_reg .^ 2)*ones(hidden_layer_size,1));

J_reg_term = (lambda/(2*m))*(layer1_reg + layer2_reg);

% Cost is combined cost term plus regularization term
J = J_cost_term + J_reg_term;

% Backpropagation.
delta_3 = h-y_new;

% size(delta_3)
% size(delta_3 * Theta2)
% size(sigmoidGradient(a1*Theta1'))

z_2 = a1*Theta1';
z_2 = [bias z_2];

delta_2 = delta_3 * Theta2 .* sigmoidGradient(z_2);
delta_2(:,1) = [];
% size(delta_2)

% size(a1)
Theta1_grad_term = (Theta1_grad + delta_2' * a1)/m;

Theta2_grad_term = (Theta2_grad + delta_3' * a2)/m;

% Apply regularization to the gradients.
Theta1_reg_term = (lambda/m) * Theta1;
Theta1_reg_term(:,1) = 0;

Theta2_reg_term = (lambda/m) * Theta2;
Theta2_reg_term(:,1) = 0;

% Add gradient terms and regularization terms together.
Theta1_grad = Theta1_grad_term + Theta1_reg_term;
Theta2_grad = Theta2_grad_term + Theta2_reg_term;

% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];


end
