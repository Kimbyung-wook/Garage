%% LPF
tau = 10.0;
sysc = tf([1],[tau 1]);
[A, B, C, D]  = tf2ss([1],[tau 1]);
ssc = ss(A,B,C,D)
ssd = c2d(ssc,1/40)
step(sysc); grid on;
%% HPF
tau = 10.0;
sysc = tf([tau 0],[tau 1]);
[A, B, C, D]  = tf2ss([tau 0],[tau 1]);
ssc = ss(A,B,C,D)
ssd = c2d(ssc,1/40)

%%
figure(1);
step(ssc); hold on;
step(ssd); hold off; grid on;
