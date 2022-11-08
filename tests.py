import unittest
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(num_rows = num_rows, num_cols = num_cols, cell_width = 10, cell_height = 10)

        self.assertEqual(
            len(m1.cells),
            num_cols)

        self.assertEqual(
            len(m1.cells[0]),
            num_rows)

        self.assertEqual(
            m1.cells[0][0].has_top_wall,
            False)

        self.assertEqual(
            m1.cells[-1][-1].has_bottom_wall,
            False)

        for i in m1.cells:
            for j in i:
                self.assertEqual(
                    j.visited,
                    False)

if __name__ == "__main__":
    unittest.main()