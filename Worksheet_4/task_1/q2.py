import numpy as np
import time
import matplotlib.pyplot as plt

def divide_matrix(matrix):
    """Splits a given matrix into quadrants"""
    mid = matrix.shape[0] // 2
    return matrix[:mid, :mid], matrix[:mid, mid:], matrix[mid:, :mid], matrix[mid:, mid:]

def strassen_matrix_mult(A, B):
    """Performs Strassen’s matrix multiplication recursively"""
    n = A.shape[0]
    
    # Base case: If matrix size is 1x1, perform direct multiplication
    if n == 1:
        return A * B
    
    # Divide matrices into quadrants
    A11, A12, A21, A22 = divide_matrix(A)
    B11, B12, B21, B22 = divide_matrix(B)

    # Compute the 7 products (Strassen’s formula)
    M1 = strassen_matrix_mult(A11 + A22, B11 + B22)
    M2 = strassen_matrix_mult(A21 + A22, B11)
    M3 = strassen_matrix_mult(A11, B12 - B22)
    M4 = strassen_matrix_mult(A22, B21 - B11)
    M5 = strassen_matrix_mult(A11 + A12, B22)
    M6 = strassen_matrix_mult(A21 - A11, B11 + B12)
    M7 = strassen_matrix_mult(A12 - A22, B21 + B22)

    # Compute the result quadrants
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Combine quadrants into final matrix
    return np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))

def pad_to_power_of_two(matrix):
    """Pads a matrix to the next power of 2 size"""
    n, m = matrix.shape
    next_power_of_two = 1 << (max(n, m) - 1).bit_length()
    padded_matrix = np.zeros((next_power_of_two, next_power_of_two), dtype=matrix.dtype)
    padded_matrix[:n, :m] = matrix
    return padded_matrix

def matrix_multiply_strassen(A, B):
    """Handles padding and calls Strassen’s algorithm"""
    n = A.shape[0]
    A = pad_to_power_of_two(A)
    B = pad_to_power_of_two(B)
    return strassen_matrix_mult(A, B)[:n, :n]

# Testing performance
sizes = [2, 4, 8, 16, 32, 64]
times_strassen = []

for size in sizes:
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    start = time.time()
    matrix_multiply_strassen(A, B)
    end = time.time()
    times_strassen.append(end - start)

# Plot execution time
plt.plot(sizes, times_strassen, label="Strassen’s Algorithm")
plt.xlabel("Matrix Size (n)")
plt.ylabel("Time (seconds)")
plt.title("Performance of Strassen’s Algorithm")
plt.legend()
plt.show()

# Theoretical complexity curve
theoretical_times = [n**2.81 for n in sizes]

# Log-log plot comparison
plt.loglog(sizes, times_strassen, label="Strassen’s Experimental", marker="o")
plt.loglog(sizes, theoretical_times, label="O(n².81) Theoretical", linestyle="dashed")
plt.xlabel("Matrix Size (n)")
plt.ylabel("Time (log scale)")
plt.title("Strassen’s Algorithm: Experimental vs Theoretical Complexity")
plt.legend()
plt.show()


