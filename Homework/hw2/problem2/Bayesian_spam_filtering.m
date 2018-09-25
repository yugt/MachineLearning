clc;
z = dlmread('spambase.data',',');

%% initialize the random number generator
rng(0);
% random permutation of indices
rp = randperm(size(z,1));
% shuffle the rows of a
z = z(rp,:);
x = z(:,1:end-1);
y = z(:,end);

%% Partition %%
partition = 2000;
x_train = x(1:partition,:);
x_test = x(partition+1:end,:);
y_train = y(1:partition);
y_test = y(partition+1:end);

%% Training %%
x_train = binary_quantize(x_train);

pi_k=zeros(2,1);
P=zeros(2,size(x_train,2),2);
% P(z_l, (j), k)

for k=0:1
    pi_k(k+1)=nnz(y_train==k)/size(y_train,1);
    for l=1:2
        P(l,:,k+1)=sum(x_train(y_train==k,:)==l,1)/nnz(y_train==k);
    end
end

%% Testing %%
x_test = binary_quantize(x_test);

f=zeros(size(x_test,1),2);

for i=1:size(f,1)
    for k=1:2
        f(i,k)=pi_k(k)*...
        prod(P(1,x_test(i,:)==1,k))*prod(P(2,x_test(i,:)==2,k));
    end
end
predict=f(:,1)<f(:,2);

%% Evaluate test error %%
% Naive Bayes Classifier test error
disp('Bayes Classifier test error')
disp(nnz(y_test-predict)/size(y_test,1))
% Majority predictor
disp('Majority predictor')
disp(nnz(y_test)/size(y_test,1))


%% functions %%
function[output] = binary_quantize(x)
    output=x;
    class1=(x<=median(x));
    class2=(x>median(x));
    output(class1)=1;
    output(class2)=2;
end
