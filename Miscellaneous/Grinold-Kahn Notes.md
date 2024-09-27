# Grinold-Kahn Notes

For asset returns $r_{it}\ :\ i\in[1,N], t\in\mathbb{Z}^+$, define the matrix $G_N(\rho)$ as the covariance matrix of returns where all pairwise correlations are equal. i.e.

$$
\mathbb{V}[r_{it},r_{jt}]=\sigma_{i}\sigma_{j}\rho \Leftrightarrow V=SG_N(\rho)S\ \mathrm{where}\ G_N(\rho)=\begin{pmatrix}
1&\rho&\cdots&\rho\\
\rho&1&\cdots&\rho\\
\vdots&&\ddots&\vdots\\
\rho&\rho&\cdots&1
\end{pmatrix}\ \mathrm{and}
\ S_t=\begin{pmatrix}
\sigma_1&0&\cdots&0\\
0&\sigma_2&\cdots&0\\
\vdots&&\ddots&\vdots\\
0&0&\cdots&\sigma_N
\end{pmatrix}.
$$

As a symmetric positive definite matrix, $G_N(\rho)$, may always be diagonalized by a similarity transformation. The eigenvalues are:

1. one eigenvalue of $1+(N-1)\rho$; and,
2. $N-1$ eigenvalues of magnitude $1-\rho$.

and the associated eigenvectors are:

1. one eigenvector of all ones: $(1\,1\dots 1)^T=\mathbf{1}_N$ where $\mathbf{1}_N$ is the unit-vector of dimension $N$; and,
2. $N-1$ vectors of the form: $(1\,-1\,0 \dots 0)^T$, $(1,0\,-1\,0 \dots 0)^T$ through $(1\,0 \dots 0\,-1)^T$.
