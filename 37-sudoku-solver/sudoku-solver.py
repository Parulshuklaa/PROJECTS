class Solution:
    def solveSudoku(self, board):

        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for r in range(9):
            for c in range(9):
                if board[r][c] != ".":
                    val = board[r][c]
                    box = (r // 3) * 3 + (c // 3)
                    rows[r].add(val)
                    cols[c].add(val)
                    boxes[box].add(val)

        def helper(r, c):
            if r == 9:
                return True

            if c == 9:
                return helper(r + 1, 0)

            if board[r][c] != ".":
                return helper(r, c + 1)

            box = (r // 3) * 3 + (c // 3)

            for num in "123456789":
                if num not in rows[r] and num not in cols[c] and num not in boxes[box]:

                    board[r][c] = num
                    rows[r].add(num)
                    cols[c].add(num)
                    boxes[box].add(num)

                    if helper(r, c + 1):
                        return True

                    board[r][c] = "."
                    rows[r].remove(num)
                    cols[c].remove(num)
                    boxes[box].remove(num)

            return False

        helper(0, 0)