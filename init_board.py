A = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 2, 2, 2, 3, 4],
    [4, 5, 5, 6, 6, 7]
]

# A = [
#     [1, 2, 2, 2, 3, 4],
#     [4, 5, 5, 6, 6, 7],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0]
# ]

S = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

# 1: A[0]

CS = 0

for i in range(len(A)):
    for j in range(len(A[0])):
        val = (2 ** (3*(6*i+j)))*A[i][j]
        S[i][j] = val
        CS += val

for i in range(len(S)):
    print(S[i])

print(CS)


# def create_cumulative_sum_array(A):
#     S = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]

#     for j in reversed(range(len(A))):
#         for i in reversed(range(len(A[0]))):
#             S[len(A)-1-j][len(A[0])-1-i] = 2**(6*j + i) * A[j][i]

#     return S

# S = create_cumulative_sum_array(A)

# for row in S:
#     print(row)
