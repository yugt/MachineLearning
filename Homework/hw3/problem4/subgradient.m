load('nuclear.mat')

loss_hinge=@(y,t)max(0,1-y.*t);

% loss_hinge([0,1,2],[3,4,5])

rng(0)
x=[ones(1,size(x,2));x];
x=x';
y=y';
lambda=0.001;
theta=zeros(1,size(x,2));

J=zeros(1000,1);
for j=1:1000
    u=lambda*theta-y'*x/2;
    theta=theta-u*100/j;
    J(j)=sum(loss_hinge(y,x*theta'))/size(y,1)+lambda*(vecnorm(theta(2:end))^2)/2;
end
plot(J)
