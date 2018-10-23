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
K_tilde=K-K*ones(n)-ones*K+ones(n)*K*ones(n);
K_prime=exp(-dist2(X_test,X_train)/(2*sigma^2));

J=eye(n)-ones(n)/n;


Core=J*(eye(n)-(n*lambda*eye(n)+K_tilde)\K_tilde)*J;
y_predict=K_prime*Core*y_train/(n*lambda)...
    +ones(m,n)*(eye(n)-K*Core/(n*lambda))*y_train/n;