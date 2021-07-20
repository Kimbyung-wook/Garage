function y = view_atti(in)
time = in(1);
CB2N = reshape(in(2:10),3,3);
y = 1;
persistent prev_time_for_view;
if isempty(prev_time_for_view)
    prev_time_for_view = time;
end
if time == 0.0
    prev_time_for_view = 0.0;
end
dT = 0.1;
if (time < prev_time_for_view + dT)
    return;
else
    prev_time_for_view = time;
end

figure(2);
image_scaler = 5.0;

t = linspace(0,2*pi,16);
diameter = 0.100;
arm_len = 0.330/2; 
lims = diameter*1.5 + arm_len;
arms{1} = (arm_len*[cosd(45) sind(45) 0]);
arms{2} = (arm_len*[cosd(-45) sind(-45) 0]);
arms{3} = (arm_len*[cosd(-135) sind(-135) 0]);
arms{4} = (arm_len*[cosd(135) sind(135) 0]);
Circle_big{1} = CB2N*(diameter*[cos(t') sin(t') zeros(size(t))']+arms{1})';
Circle_big{2} = CB2N*(diameter*[cos(t') sin(t') zeros(size(t))']+arms{2})';
Circle_big{3} = CB2N*(diameter*[cos(t') sin(t') zeros(size(t))']+arms{3})';
Circle_big{4} = CB2N*(diameter*[cos(t') sin(t') zeros(size(t))']+arms{4})';
trans_arms{1} = CB2N*arms{1}';
trans_arms{2} = CB2N*arms{2}';
trans_arms{3} = CB2N*arms{3}';
trans_arms{4} = CB2N*arms{4}';

fill3(  Circle_big{1}(2,:), Circle_big{1}(1,:), -Circle_big{1}(3,:),'r',...
        Circle_big{2}(2,:), Circle_big{2}(1,:), -Circle_big{2}(3,:),'r',...
        Circle_big{3}(2,:), Circle_big{3}(1,:), -Circle_big{3}(3,:),'k',...
        Circle_big{4}(2,:), Circle_big{4}(1,:), -Circle_big{4}(3,:),'k'...
        ); hold on; grid on;
plot3(  [0 trans_arms{1}(2)],[0 trans_arms{1}(1)],-[0 trans_arms{1}(3)],'r',...
        [0 trans_arms{2}(2)],[0 trans_arms{2}(1)],-[0 trans_arms{2}(3)],'r',...
        [0 trans_arms{3}(2)],[0 trans_arms{3}(1)],-[0 trans_arms{3}(3)],'k',...
        [0 trans_arms{4}(2)],[0 trans_arms{4}(1)],-[0 trans_arms{4}(3)],'k','LineWidth',2);
hold off;
xlim([-lims lims]); ylim([-lims lims]); zlim([-lims lims]);
grid on;
view(30,30);
title_str = sprintf('Attitude of model @ %.1f s',time);
title(title_str);
xlabel('x'); ylabel('y');
drawnow;