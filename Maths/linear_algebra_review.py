"""
This file is about linear algebra review coded from lecture_01_linear_algebra_optimization_review.pdf
Original Author: Trung-Ng
Date: 01/11/2019
"""

import numpy as np

# 1. Matrix and Vector
print('\n------------------ SECTION 1 --------------------')
matrix1 = np.array([[1, 2, 3], [4, 5, 6]])
print('Matrix form: {}'.format(matrix1))
print('Matrix shape: {}'.format(matrix1.shape))

vec1 = np.array([149, 92, 313])
print('Vector form: {}'.format(vec1))
print('Vector shape: {}'.format(vec1.shape))

# 2. Matrix calculation
print('\n------------------ SECTION 2 --------------------')
sample_matrix_1 = np.array([[23, 402], [69, 221], [118, 0]])
sample_matrix_2 = np.array([[2], [1]])
sample_matrix_3 = np.ones(sample_matrix_1.shape)

print('Addition: {}'.format(np.add(sample_matrix_1, sample_matrix_3)))
print('Subtraction: {}'.format(sample_matrix_1 - sample_matrix_3))
print('Element-wise multiplication: {}'.format(sample_matrix_1 * sample_matrix_3))
print('Matrix mul: {}'.format(sample_matrix_1.dot(sample_matrix_2)))

# 3. Matrix DET
print('\n------------------ SECTION 3 --------------------')
mat =  np.array([[23, 402], [69, 221]])
print("Matrix determinant: {}".format(np.linalg.det(mat)))

# 4. Inverse
print('\n------------------ SECTION 4 --------------------')
mat = np.array([[1, 3], [2, 7]])
print("Inverse: {}".format(np.linalg.inv(mat)))

# 5. Eigenvalues and eigenvectors
print('\n------------------ SECTION 5 --------------------')
diag_mat = np.diag(((1, 2, 3)))
w, v = np.linalg.eig(diag_mat)
print("Eigenvalues - Eigenvectors: {} - {}".format(w, v))