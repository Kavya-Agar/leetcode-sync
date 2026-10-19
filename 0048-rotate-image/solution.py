class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        for m in range(len(matrix)):
            for n in range(m, len(matrix[m])):
                temp = matrix[n][m]
                matrix[n][m] = matrix[m][n]
                matrix[m][n] = temp
            matrix[m] = matrix[m][::-1]
        
        
