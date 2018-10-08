%% Experiment constants (Global)
% experiment size
n=500;
alpha=0.1;
b=4;

% covariance
sigma_0=1;
rho_0=0.5;
nu=.5:.5:1.5;
Kv=@(v,x) 2^(2-v)*pi*x^v*besselk(v,x)/(gamma(v));

% covariance matrix
covariance=sigma_0^2*eye(n)/2 * 10; % BUGGY
for i=1:n
    for j=i+1:n
        covariance(i,j)=sigma_0^2*Kv(nu(1),(j-i)/(n*rho_0));
    end
end
covariance=covariance'+covariance;

%% Generate Gaussian Process
% rng default
t=randi([floor(alpha*n),floor((1-alpha)*n)],1,1);
xi=sign((1:n)-t);
xi(xi==0)=1;
X=mvnrnd(xi*b/2,covariance);
plot(X)