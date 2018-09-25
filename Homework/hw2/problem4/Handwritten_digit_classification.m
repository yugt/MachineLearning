load mnist_49_3000
[d,n] = size(x);
i = 1; % index of image to be visualized
imagesc(reshape(x(:,i),[sqrt(d),sqrt(d)])')