load('../hw3/problem1/bodyfat_data.mat')
activate=@(x) max(0,x);
activate_derivative=@(x) double(x>0);

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


a1=W1*X_train'+b1;
z1=activate(a1);

a2=W2*z1+b2;
z2=activate(a2);

a3=W3*z2+b3;
d3=2*(a3'-y_train);
d2=(d3*W3).*activate_derivative(a2');
d1=(d2*W2).*activate_derivative(a1');