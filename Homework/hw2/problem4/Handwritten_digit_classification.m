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

