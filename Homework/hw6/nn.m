load('../hw3/problem1/bodyfat_data.mat')
activate=@(x) max(0,x);
activate_derivative=@(x) double(x>0);

forward=@(X,W1,W2,W3,b1,b2,b3)...
    W3*activate(W2*activate(W1*X'+b1)+b2)+b3;

gamma=1e-7;

rng(0)
N=150;
X_train=X(1:N,:);
y_train=y(1:N);

b1=zeros(64,1);
b2=zeros(16,1);
b3=zeros(1,1);
W1=randn([size(b1,1),size(X_train,2)]);
W2=randn([size(b2,1),size(b1,1)]);
W3=randn([size(b3,1),size(b2,1)]);

loss=1;
d3=0;

%% Train %%
for i=1:100000
    %% forward %%
    a1=W1*X_train'+b1;
    z1=activate(a1);
    
    a2=W2*z1+b2;
    z2=activate(a2);
    
    a3=W3*z2+b3;
    
    %% back %%
    if abs(loss-sum(d3.^2)/size(X_train,1))<gamma
        break
    else
        loss=sum(d3.^2)/size(X_train,1);
    end
    
    d3=2*(a3'-y_train);
    d2=(d3*W3).*activate_derivative(a2');
    d1=(d2*W2).*activate_derivative(a1');
    
    W3=W3-gamma*(d3'*z2')/N;
    W2=W2-gamma*(d2'*z1')/N;
    W1=W1-gamma*(d1'*X_train)/N;
    b3=b3-gamma*mean(d3,1)';
    b2=b2-gamma*mean(d2,1)';
    b1=b1-gamma*mean(d1,1)';
end

%% Test %%
result=forward(X,W1,W2,W3,b1,b2,b3)';
error=result-y;
sum(error(1:N).^2)/N                    % training MSE
sum(error(N+1:end).^2)/(size(X,1)-N)    % test MSE
