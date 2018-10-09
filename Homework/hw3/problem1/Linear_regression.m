load('bodyfat_data.mat')
partition=150;
X_train=X(1:partition,:);
X_test=X(partition+1:end,:);
y_train=y(1:partition);
y_test=y(partition+1:end);


%% Ordinary Least Square
X_train=[ones(size(X_train,1),1) X_train];
X_test=[ones(size(X_test,1),1) X_test];
w_ordinary=X_train\y_train;
disp('ordinary least square training mse')
sum((X_train*w_ordinary-y_train).^2)./size(y_train,1)
disp('ordinary least square testing mse')
sum((X_test*w_ordinary-y_test).^2)./size(y_test,1)


%% Regularized (Ridge) regression
lambda=10;
y_train=y_train-mean(y_train);
X_train=X_train(:,2:end);
X_train=X_train-mean(X_train);
w_ridge=(X_train'*X_train+lambda*partition*...
    eye(size(X_train,2)))\(X_train'*y_train);
X_train=X(1:partition,:);
y_train=y(1:partition);
b_ridge=mean(y_train)-mean(X_train)*w_ridge;
X_test=X(partition+1:end,:);
disp('ridge regression training mse')
sum((X_train*w_ridge+b_ridge-y_train).^2)./size(y_train,1)
disp('ridge regression testing mse')
sum((X_test*w_ridge+b_ridge-y_test).^2)./size(y_test,1)
disp('predict x=[100 100]')
[100 100]*w_ridge+b_ridge