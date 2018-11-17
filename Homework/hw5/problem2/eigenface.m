load yalefaces % loads the 3-d array yalefaces

X=double(reshape(yalefaces,...
    [size(yalefaces,1)*size(yalefaces,2),size(yalefaces,3)]));

mu=mean(X,2);
U=X-mu*ones(1,size(X,2));
S=U*U'/size(X,2);
[V,D]=eig(S);
semilogy(diag(D))

set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,...
    'PaperPosition',[0 0 screenposition(3:4)],...
    'PaperSize',[screenposition(3:4)]);
print -dpdf -painters hw5p2a -r300
close all

[~,permutation]=sort(diag(D),'descend');
D=D(permutation,permutation);
V=V(:,permutation);

d=diag(D);
for k=1:size(d,1)
    if sum(d(1:k))/sum(d)>0.95
        k1=k
        break
    end
end
for k=1:size(d,1)
    if sum(d(1:k))/sum(d)>0.99
        k2=k
        break
    end
end

colormap(gray)
subplot(4,5,1)
imagesc(reshape(mu,...
        [size(yalefaces,1),size(yalefaces,2)]))
title('mean')
for i=1:19
    subplot(4,5,i+1)
    imagesc(reshape(V(:,i),...
        [size(yalefaces,1),size(yalefaces,2)]))
    title(strcat(num2ordinal(i),' evec'))
end

set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,...
    'PaperPosition',[0 0 screenposition(3:4)],...
    'PaperSize',[screenposition(3:4)]);
print -dpdf -painters hw5p2b -r300
close all