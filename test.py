import numpy as np

# TEST 1
# x = np.zeros((3, 3))
# print(x)
# x[0, :] = -1
# print(x)
# print(x[0][0])
# print(x[0, 0])
# x = x.reshape(-1)
# print((x == 0))
# print((x == 0).astype(np.uint8))


# TEST2
# column_count = 3
# player = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
# player[0][2] = 45
# actions = 9
# for action in range(actions):
#     # action = int(action)
#     row = action//column_count
#     column = action % column_count
#     print(f"{player[row][column]}")

# TEST3
# x = np.arange(9)
# print(x)
# print(x.shape)
# print(x.size)
x = np.arange(9).reshape((3, 3))
x = x.reshape(-1)
print((x == 0))
print((x == 0).astype(np.uint8))
print(x)
# print(x.shape)
# print(x.size)
# print(np.diag(x))
# print(np.diag(x, k=1))
# print(np.diag(x, k=2))
# print(np.diag(x, k=-1))
# print(np.diag(x, k=-2))
# print(np.diag(np.diag(x)))
# print(np.flip(x))
# print(np.flip(x, axis=0))
