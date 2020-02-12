function r = eval_input(t, x, p)
    % EVAL_INPUT - Returns the input vector at any given time.
    %
    % Syntax: r = eval_input(t, x)
    %
    % Inputs:
    %   t - A scalar value of time, size 1x1.
    %   x - State vector at time t, size mx1 were m is the number of states.
    %   p - Constant parameter vector for the input function, size px1 were 
    %       p is the number of parameters.
    % Outputs:
    %   r - Input vector at time t, size ox1 where o is the number of
    %       inputs.

     % unpack the state variables
    theta = x(1);
    omega = x(2);
    
    % unpack the constant parameter
    Tm_max = p(1);       % Maximum Torque of the main motor
    
%     commandStr = 'python excavation_force.py';
%     [status, commandOut] = system(commandStr);
%     if status==0
%         force = str2num(commandOut);
%     end
    
%     force_x = force(1);
%     force_y = force(2);
    force_x = 0;
    force_y = 0;
    
    if omega >= 0
        torque = Tm_max;
    else
        torque = -Tm_max;
    end
    
    r = [force_x; force_y; torque];
end

