clc
clear all
close all

% set the constant of rhs and package them into a vector
m = 200;        % Mass of excavation arm
l = 6;          % Length of excavation arm
e = 0.5;        % Distance between axis and CoM
g = 9.81;       % Gravity
Tm_max = 10;    % Maximum Torque of the main motor

p = [m, l, e, g];

% set the time resolution for the simulation
ts = linspace(0, 300, 3000);

% set the constant of the pothole input
p_w = [Tm_max];

% set eval_rhs as an anonymous function
f_input_anon = @(t, x) eval_input(t, x, p_w);

% set eval_rhs as an anonymous function
f_rhs_anon = @(t, x) eval_rhs(t, x, f_input_anon, p);

% test eval_rhs
x_0 = [pi/2; 0];
xdot = eval_rhs(0.0, x_0, f_input_anon, p);
disp('eval_rhs executed sucessfully.')

% call function ode45
[ts, xs] = ode45(f_rhs_anon, ts, x_0);

subplot(2,1,1)
plot(ts, xs(:, 1), 'LineWidth', 1)
title('Theta', 'Fontsize', 12, 'Fontweight', 'bold')
xlabel('time [s]', 'Fontsize', 12) 
ylabel('theta [m]', 'Fontsize', 12)

subplot(2,1,2)
plot(ts, xs(:, 2), 'LineWidth', 1)
title('Omega', 'Fontsize', 12, 'Fontweight', 'bold')
xlabel('time [s]', 'Fontsize', 12) 
ylabel('omega [rad/s]', 'Fontsize', 12)