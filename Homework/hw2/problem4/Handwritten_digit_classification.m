load mnist_49_3000
[d,n] = size(x);
i = 1; % index of image to be visualized
imagesc(reshape(x(:,i),[sqrt(d),sqrt(d)])')

%% Partition %%
partition = 2000;
x_train = x(:,1:partition);
x_test = x(:,partition+1:end);
y_train = y(1:partition);
y_test = y(partition+1:end);

x_train = [ones(1,size(x_train,2));x_train];
y_train(y_train<0)=0;

%% Newton-Raphson iteration %%
w=zeros(size(x_train,1),1);
lambda=10;
for i=1:500
    gradient = 2*lambda*w+x_train*(y_train-sigmoid(x_train, -w))';
    p=sigmoid(x_train,w);
    W=diag(p.*(1-p));
    hessian=2*lambda*size(x_train,1)*eye(size(w,1))+x_train*W*x_train';
    w_new=w-hessian\gradient;
    if vecnorm(w_new-w)/vecnorm(w)<0.001
        w=w_new;
        disp('converge with objective function')
        J=(y_train-1).*log(sigmoid(x_train,-w))-...
            y_train.*log(sigmoid(x_train,w));
        disp(sum(J)+lambda*(w'*w))
        break;
    else
        w=w_new;
    end
end

%% Testing %%
predict=sigmoid([ones(1,size(x_test,2));x_test],-w);
compare=ones(size(predict));
compare(predict<0.5)=-1;
disp('test error')
disp(1-nnz(y_test==compare)/size(y_test,2))

error_list = find(y_test~=compare);
[~,index]=maxk(abs(predict(error_list)-0.5),20);
error_list_top = error_list(index);
label=[4,9];
for i=1:length(error_list_top)
    subplot(4,5,i)
    imagesc(reshape(x(:,error_list_top(i)),[sqrt(d),sqrt(d)])')
    title(strcat(num2str(label((y(error_list_top(i))+3)/2)),...
        '  #',num2str(error_list_top(i))))
end
set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,...
    'PaperPosition',[0 0 screenposition(3:4)],...
    'PaperSize',[screenposition(3:4)]);
print -dpdf -painters hw2p4b


function[output] = sigmoid(x, theta)
output = 1./ (1+exp(-theta'*x));
end
