def multiply_matrices(A, B):
    result = []

    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            value = 0
            for k in range(len(B)):
                value += A[i][k] * B[k][j]
            row.append(value)
        result.append(row)

    return result
