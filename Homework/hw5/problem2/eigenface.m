load yalefaces % loads the 3-d array yalefaces
for i=1:size(yalefaces,3)
x = double(yalefaces(:,:,i));
imagesc(x);
colormap(gray)
drawnow
% pause(.1)
end