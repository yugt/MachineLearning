close all
rng(0);
n = 200; % sample size
K = 2; % number of lines
e=[.7 .3]; % mixing weights
w=[-2 1]; % slopes of lines
b=[.5 -.5]; % offsets of lines
v=[.2 .1]; % variances

x=zeros(n,1);
y=zeros(n,1);

for i=1:n
    x(i) = rand;
    if rand < e(1)
        y(i) = w(1)*x(i) + b(1) + randn*sqrt(v(1));
    else
        y(i) = w(2)*x(i) + b(2) + randn*sqrt(v(2));
    end
end
plot(x,y,'bo')
hold on
t=0:0.01:1;
plot(t,w(1)*t+b(1),'k')
plot(t,w(2)*t+b(2),'k')