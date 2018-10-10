close all;clc;
n = 200;
rng(0); % seed random number generator
x = rand(n,1);
z = zeros(n,1); k = n*0.4; rp = randperm(n); ...
outlier_subset = rp(1:k); z(outlier_subset)=1; % outliers
y = (1-z).*(10*x + 5 + randn(n,1)) + z.*(20 - 20*x + 10*randn(n,1));
% plot data and true line
scatter(x,y,'b')
hold on
t = 0:0.01:1;
plot(t,10*t+5,'k')


% add your code for ordinary least squares below
X=[ones(size(x)) x];
w=X\y;
w_ols=w(2);
b_ols=w(1);
plot(t, w_ols*t + b_ols, 'g--');


% add your code for the robust regression MM algorithm below
rho_prime=@(r) r./sqrt(1+r.^2);
theta=[0;0];
for i=1:100
    r=y-X*theta;
    C=diag(rho_prime(r)./r);
    theta_new=wls(X,y,C);
    if(vecnorm(theta_new-theta)<1e-5)
        disp('converge')
        disp(i)
        break
    else
        theta=theta_new;
    end
end
b_rob=theta(1);
w_rob=theta(2);

plot(t, w_rob*t + b_rob, 'r:');
legend('data','true line','least squares','robust')

set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,...
    'PaperPosition',[0 0 screenposition(3:4)],...
    'PaperSize',[screenposition(3:4)]);
print -dpdf -painters hw3p2 -r300

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [theta] = wls(X,y,c)
% a helper function to solve weighted least squares
theta=(X'*c*X)\(X'*c*y);
end
