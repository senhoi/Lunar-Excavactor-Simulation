function xdot = eval_rhs(t, x, w, p)
    % EVAL_RHS - Returns the time derivative of the states, i.e.
    % evaluates the right hand side of the explicit ordinary differential
    % equations.
    %
    % Syntax: xdot = eval_rhs(t, x, w, p)
    %
    % Inputs:
    %   t - Scalar value of time, size 1x1.
    %   x - State vector at time t, size mx1 where m is the number of
    %       states.
    %   w - Anonymous function, w(t, x), that returns the input vector
    %       at time t, size ox1 were o is the number of inputs.
    %   p - Constant parameter vector, size px1 were p is the number of
    %       parameters.
    % Outputs:
    %   xdot - Time derivative of the states at time t, size mx1.

    % unpack the state variables
    theta = x(1);
    omega = x(2);
    
    % unpack the constant parameter
    m = p(1);       % Mass of excavation arm
    l = p(2);       % Length of excavation arm
    e = p(3);       % Distance between axis and CoM
    g = p(4);       % Gravity

    % calculate the input vi
    r = w(t, x);
    
    Tx = r(1);
    Ty = r(2);
    Tm = r(3);

    % calculate the state derivatives_
    dot_theta = omega;
    dot_omega = ((m*g*e+Ty)*cos(theta)-Tx*sin(theta)+Tm)/((1/12+e^2)*m*l);

    % pack the state derivatives into an mx1 vector (same order as states)
    xdot = [dot_theta; dot_omega];

end

