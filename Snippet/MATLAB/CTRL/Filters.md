## Discretization of Low-Pass Filter
Assume a LPF following as : 
$$ G(s) = \frac{1}{\tau s + 1} $$

It can be represented on continuous-time domain state-space form
$$\begin{cases} \dot{x} = A x + B u \\ y = C x + Du\end{cases}$$
$$\begin{cases}\dot{x} = -(1/\tau)x + 1u \\y=1x+0u\end{cases}$$
$$A=-1/\tau, B = 1, C = 1, D = 0$$

It also can be on discrete-time domain
$$ \begin{cases} x_{k} = (1+AT) x_{k-1}  + B T u_{k-1} \\ y_k =C x_{k-1} + D u_{k-1}\end{cases}$$

Conversion continuous-domain to discrete-domain is..
$$ \begin{aligned}
\dot {x} &= A x + Bu \\ 
\frac{x_k - x_{k-1}}{T} &= A x_{k-1} + B u_{k-1} \\ 
x_T &= (1+AT) x_{k-1} + B T u_{k-1} 
\end{aligned}$$

## Discretization of High-Pass Filter
$$ G(s) = \frac{\tau s}{\tau s + 1} $$
$$\begin{cases}
\dot{x} = -(1/\tau)x + 1u \\
y=-(1/\tau)x+1u
\end{cases}$$
$$A=-1/\tau, B = 1, C = -1/\tau, D = 1$$
$$\begin{cases}
x_k = (1+AT) x_{k-1} + B T u_{k-1} \\ 
y_k = C x_{k-1} + D u_{k-1}
\end{cases} $$

## Discretization of PID Controller 
Assume a PID Controller form : 
$$ u(t) = k_p e(t) +  \int{ k_i e(t) d\tau} + k_d \dot{e}(t)$$
$$ G_c (s)=\frac{U(s)}{E(s)} = k_p + k_i\frac{1}{s} + k_d s$$
$$ G_c (s)=\frac{U(s)}{E(s)} = k_p (1 + \frac{1}{\tau_i s} + \tau_d s )$$