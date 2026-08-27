class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        
        # rows: 
        # if x < 0 -> above the matrix
        # and
        # x > len(image) -> below the matrix 

        # columns: 
        # if y < 0 -> far too left 
        # y > len(image) -> too right 

        start_color = image[sr][sc]

        if start_color == color : 
            return image 

        def flood_fill(x,y): 
            if x < 0 or x >= len(image) :
                return 

            if y < 0 or y >= len(image[0]): 
                return 

            if image[x][y] != start_color: 
                return 

            image[x][y] = color 

            flood_fill(x-1, y)  # up
            flood_fill(x+1, y)  # down
            flood_fill(x,y-1)   # left 
            flood_fill(x, y+1)  # right 

        flood_fill(sr, sc)

        return image 




