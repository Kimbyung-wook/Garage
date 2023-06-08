%%
x_minmax = [-200.0, 200.0];
y_minmax = [-200.0, 200.0];
points = 15;
spd = 10.0;
Rd = 100.0;
gamma = 0.2;
 
[X, Y] = meshgrid(linspace(x_minmax(1),x_minmax(2),points), linspace(y_minmax(1),y_minmax(2),points));
R = sqrt(X.^2 + Y.^2);
[m, n] = size(X);
U = zeros(m, n);
V = zeros(m, n);
for i = 1 : m
    for j = 1 : n
        u_rn = [0,0,1];
        u_rt = [X(i,j), Y(i,j), 0];
        u_rt = u_rt / max(1.0, sqrt(dot(u_rt,u_rt)));
        rn = 0;
        rt = R(i,j);
 
        alpha = (1/spd)*sqrt(power(rn,2)+power(rt-Rd,2)+power(Rd*gamma,2));
        dVf = rn*u_rn + (rt - Rd)*u_rt;
        Contraction = dVf / alpha;
        Circular = gamma * rt * cross(u_rn, u_rt) / alpha;
        h = -Contraction + Circular;
        U(i,j) = h(1);
        V(i,j) = h(2);
    end
end
 
 
figure(1);
quiver(X,Y,U,V, 0.5);
grid on;
%%
x_minmax = [-500.0, 500.0];
y_minmax = [-500.0, 500.0];
points = 17;
spd = 10.0;
Rd = 200.0;
gamma = 0.2;
f = 1.0;
a = Rd / 20;
b = Rd * (f-1);
 
[X, Y] = meshgrid(linspace(x_minmax(1),x_minmax(2),points), linspace(y_minmax(1),y_minmax(2),points));
R = sqrt(X.^2 + Y.^2);
[m, n] = size(X);
U = zeros(m, n);
V = zeros(m, n);
for i = 1 : m
    for j = 1 : n
        u_rn = [0,0,1];
        u_rt = [X(i,j), Y(i,j), 0];
        u_rt = u_rt / max(1.0, sqrt(dot(u_rt,u_rt)));
%         u = u_rt(1); u_rt(1) = (power(abs(u)+a,2)+a*(b-a))/power(abs(u)+a,2);
        rn = 0;
        rt = R(i,j);
 
        alpha = (1/spd)*sqrt(power(rn,2)+power(rt-Rd,2)+power(Rd*gamma,2));
        dVf = rn*u_rn + (rt - Rd)*u_rt;
        Contraction = dVf / alpha;
        Circular = gamma * rt * cross(u_rn, u_rt) / alpha;
        h = -Contraction + Circular;
        u = h(1);
%         U(i,j) = (power(abs(u)+a,2)+a*(b-a))/power(abs(u)+a,2);
        U(i,j) = u * (abs(u) + b)/(abs(u) + a);
        U(i,j) = h(1);
        V(i,j) = h(2);
    end
end
 
 
figure(1);
quiver(X,Y,U,V, 1.0);
xlim([x_minmax(1), x_minmax(2)]);
ylim([y_minmax(1), y_minmax(2)]);
grid on;
