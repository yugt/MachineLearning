load('../../hw3/problem1/bodyfat_data.mat')

n=150;
X_train=X(1:n,:);
y_train=y(1:n);
X_test=X(n+1:end,:);
y_test=y(n+1:end);

[m,d]=size(X_test);

sigma=15;
lambda=0.003;
K=exp(-dist2(X_train,X_train)/(2*sigma^2));
K_tilde=K-K*ones(n)/n-ones(n)*K/n+ones(n)*K*ones(n)/n^2;
K_prime=exp(-dist2(X_test,X_train)/(2*sigma^2));


%% With offset
disp('with offset')
J=eye(n)-ones(n)/n;
y_tilde=J*y_train;

Core=J*((K_tilde+n*lambda*eye(n))\y_tilde);

y_predict_train=K*Core+ones(n,n)*(y_train-K*Core)/n;
y_predict_test=K_prime*Core+ones(m,n)*(y_train-K*Core)/n;
offset=ones(1,n)*(y_train-K*Core)/n

error=y_train-y_predict_train;
mse_train=error'*error/n

error=y_test-y_predict_test;
mse_test=error'*error/m


% Core=J*((K_tilde+n*lambda*eye(n))\J);
% y_predict=K_prime*Core*y_train...
%     +ones(m,n)*(eye(n)-K*Core)*y_train/n;

% Core=J*(eye(n)-(n*lambda*eye(n)+K_tilde)\K_tilde)*J;
% y_predict=K_prime*Core*y_train/(n*lambda)...
%     +ones(m,n)*(eye(n)-K*Core/(n*lambda))*y_train/n;

%% Without offset
disp('without offset')
y_predict_train=K*((K+n*lambda*eye(n))\y_train);
y_predict_test=K_prime*((K+n*lambda*eye(n))\y_train);

error=y_train-y_predict_train;
mse_train=error'*error/n

error=y_test-y_predict_test;
mse_test=error'*error/m