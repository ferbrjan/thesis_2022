clear;
close all;

% load pts
pts_orig = pcread('HL2COLMAP_mesh.ply');
X = pts_orig.Location;

% compose R
vec = [4.47689-4.44789; -1.20351-0.350422; 2.55937-3.1937]; %Points from meshlab
vec = vec / norm(vec);
new_vec = [0; 0; 1];

v = cross(vec, new_vec);
v = v / norm(v);
th = acos(vec' * new_vec);
Q = cos(th)*eye(3) + (1-cos(th))*v*v' + sin(th)*xx(v,[]);

X = X - mean(X);
X = (Q * X')';
pts_new = pointCloud(X, 'Color', pts_orig.Color);

% show
figure();
pcshow(pts_new);
xlabel('x'); 
ylabel('y');
zlabel('z');

% save pts
% pcwrite(pts_new, 'HL2COLMAP_mesh_rotated.ply');


% read COLMAP
[cameras, images, points3D] = read_model(fullfile(pwd,'Colmap_sparse')); %path change needed while not working on IMPACT 

% update extrinsics
new_images = images;
c_images = images.values();
len = length(images);
for i = 1:len
    img = c_images{i};
    C = - img.R' * img.t;
    Cp = Q * C;
    Rp = img.R * Q';
    tp = - Rp * Cp;
    
    img.R = Rp;
    img.t = tp; 
    new_images(img.image_id) = img;
end

% update colmap points
new_points3D = points3D;
c_points3D = points3D.values();
len = length(points3D);

for i = 1:len
    pt = c_points3D{i};
    
    pt.X = Q * pt.X;
    new_points3D(pt.point3D_id) = pt;
end

% save colmap model
saveColmap( fullfile(pwd,'Colmap_sparse_rotated'), cameras, new_images, new_points3D );




