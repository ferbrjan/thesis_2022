clear;
close all;

% read COLMAP
[cameras, images, points3D] = read_model('E:/ferbrjan/Datagen_input_testing/Colmap_sparse');%path change needed while not working on IMPACT 

% load hololens poses
fid = fopen('HoloLens2/2021-10-06-082512/2021-10-06-082512_pv.txt');
tline = fgetl(fid);
pp = cellfun(@(a) str2num(a),split(tline,','));    
tline = fgetl(fid);

% load images from colmap with coresponding directory and write down their centres
len = length(images);
C_colmap = {}; %centres from colmap
PV2_name = {}; %timestamps of frames that are in colmap
for i = 1:len
    if isKey(images,i) == 1
        if startsWith(images(i).name,"HL_PV/HL2") == 1
            C_colmap{end+1} = -images(i).R' * images(i).t; %IDK ABOUT INV!!!!!!
            PV2_name{end+1} = images(i).name;
            PV2_name{end} = erase(PV2_name{end},".png");
            PV2_name{end} = str2num(erase(PV2_name{end},"HL_PV/HL2_PV_"));
        end
    end
end
C_colmap = cell2mat(C_colmap);

% load centres from hololens2
C = {};
while ischar(tline)
    line_num = cellfun(@(a) str2num(a),split(tline,','));
    if ismember(line_num(1),[PV2_name{:}]) == 1 %Only append centres of frames that are in colmap database
        P = reshape(line_num(4:end),4,4)';
        P = inv(P);
        R = P(1:3,1:3);
        t = P(1:3,4);
        C{end+1} = - R' * t;
    end

    % read next
    tline = fgetl(fid);
end
fclose(fid);
C_hololens = cell2mat(C);



% show
figure();
plot3(C_colmap(1,:),C_colmap(2,:),C_colmap(3,:),"r.");hold on;
plot3(C_hololens(1,:),C_hololens(2,:),C_hololens(3,:),"b.");

% read mesh/pts
mesh_pts = pcread("hololens_mesh.ply");


% transoform mesh  --- TODO (this is just copy-pasted documentation)
[d,Z,transform] = procrustes(C_colmap',C_hololens');
Z_points = transform.b*mesh_pts.Location*transform.T + repmat(transform.c(1,:),size(mesh_pts.Location,1),1); %přičít ke každýmu řádku 
 
Z=Z';
Z_points = Z_points';

plot3(Z(1,:),Z(2,:),Z(3,:),"go");
plot3(Z_points(1,:),Z_points(2,:),Z_points(3,:),"b.");axis equal;
mesh_pts.Location = Z_points';
new_mesh_pts = pointCloud(Z_points',"Color", mesh_pts.Color); 
figure();
pcshow(mesh_pts);hold on;
pcshow(new_mesh_pts);
pcwrite(new_mesh_pts,"new_mesh2.ply");
plot3(C_hololens(1,:),C_hololens(2,:),C_hololens(3,:),"b.");
