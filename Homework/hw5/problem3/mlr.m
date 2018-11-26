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

e=[.5 .5];
w=[1 -1];
b=[0 0];
v=repmat(var(y),1,2);

% x: n*d;  w: d*K
phi=@(y,x,w,b,v)...
normpdf(y*ones(size(y,2),K),x*w+b,...
    ones(n,size(v,1))*sqrt(v));

% \frac{\sum_{l=1}^n \gamma_{lk}^{(j)}x_l}
% {\sum_{l=1}^n \gamma_{lk}^{(j)}}
tilde=@(g,z)repmat(z,[1 K])-...
repmat((sum(g.*(z*ones(size(z,2),K)),1)./sum(g,1)),[n 1]);

Q=zeros(n,1);
Q(1)=-Inf;
for i=1:size(Q,1)
% E-step
gamma=e.*phi(y,x,w,b,v);
gamma=gamma./sum(gamma,2);

% check stop criteria
Q(i+1)=sum(sum(gamma.*log(e.*phi(y,x,w,b,v))));
if Q(i+1)-Q(i)<1e-4
    break
end

% M-step
e=sum(gamma,1)/n;
x_tilde=tilde(gamma,x);
y_tilde=tilde(gamma,y);
w=sum(gamma.*y_tilde.*x_tilde,1)./...
sum(gamma.*x_tilde.*x_tilde,1);
b=sum(gamma.*(y-x*w),1)./sum(gamma,1);
v=sum(gamma.*(y-(x*w+b)).^2,1)./sum(gamma,1);
end

% plot
plot(t,w(1)*t+b(1),'.')
plot(t,w(2)*t+b(2),'.')

set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,...
    'PaperPosition',[0 0 screenposition(3:4)],...
    'PaperSize',[screenposition(3:4)]);
print -dpdf -painters hw5p3a -r300

clf
plot(Q(1:i));
xlabel('iteration');
ylabel('log-likelihood')

set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,...
    'PaperPosition',[0 0 screenposition(3:4)],...
    'PaperSize',[screenposition(3:4)]);
print -dpdf -painters hw5p3b -r300
close all