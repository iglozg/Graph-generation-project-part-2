#Unittesting
import unittest

target = __import__("Classes")
tree = target.Treepatch
tree_stat = tree(1, 200)

class TestTreepatch(unittest.TestCase):
    """This class contains unit tests for the TreePatch class.
    Test the 'updateland' method with the 'fire' action.
    Test the 'updateland' method with the 'nofire' action.
    """
    def test_updateland_fire(self):
        action = "fire"
        tree.updateland(tree_stat, action)
        self.assertEqual(tree_stat.get_treestat(), 180)
    def test_updateland_nofire(self):
        action = "nofire"
        tree.updateland(tree_stat, action)
        self.assertEqual(tree_stat.get_treestat(), 190)

if __name__ == "__main__":
    unittest.main()