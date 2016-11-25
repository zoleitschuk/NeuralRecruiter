function [p, p_contin] = predict(Theta1_in, Theta2_in, X_in)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

[X, Theta1, Theta2] = decode_prediction_vars(X_in, Theta1_in, Theta2_in);

% Useful values
m = size(X, 1);
num_labels = size(Theta2, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

h1 = sigmoid([ones(m, 1) X] * Theta1');
h2 = sigmoid([ones(m, 1) h1] * Theta2');
[dummy, p] = max(h2, [], 2);

p_contin = p + sum(h2 .* (([1 2 3 4 5] .- p) / 2), 2)

% =========================================================================


end
