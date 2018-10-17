load('nuclear.mat')

% rng(0);
% w=[0.5;0.5]; b=0;
% J=zeros(20*size(x,2),1);
% p=randperm(size(x,2));
% for j=1:200
%     u=zeros(size(w,1)+1,1);
%     for i=1:size(x,2)
%         u=u+subgradient_hinge(w,b,x,y,p(i));
%         b=b-u(1)*100/j;
%         w=w-u(2:end)*100/j;
%         J((j-1)*size(x,2)+i)=objectiveJ(w,b,x,y);
%     end
% 
% end

scatter(x(1,y==-1),x(2,y==-1),'d')
hold on
scatter(x(1,y==1),x(2,y==1))

x1=0:0.02:8;
x2=(-b-w(1)*x1)/w(2);
plot(x1,x2,'g')

set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,...
    'PaperPosition',[0 0 screenposition(3:4)],...
    'PaperSize',[screenposition(3:4)]);
print -dpdf -painters hw3p4c1
hold off
semilogy(J)
xlabel('iteration')
ylabel('objective function')
print -dpdf -painters hw3p4c2

function[J]=objectiveJ(w,b,x,y)
hinge_loss=@(y,t) max(0,1-y.*t);
J=sum(hinge_loss(y,w'*x+b))/size(y,2);
J=J+0.001*(w'*w)/2;
end

function[ui]= subgradient_hinge(w,b,x,y,i)
ui=zeros(size(w,1)+1,1);
ui(1)=(sign(w'*x(:,i)+b-y(i))-y(i))/(2*size(y,2));
ui(2:end)=x(:,i)*ui(1)+0.001*w/size(y,2);
end