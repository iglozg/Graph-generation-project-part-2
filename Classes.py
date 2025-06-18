# Classes

import random

class Landpatch:
    def __init__(self, patch_id):
        self.patch_id = patch_id
        self.neighbors = []
        self.firefighter_present = False

    def get_neighbors(self):
        return self.neighbors

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Rockpatch(Landpatch):
    def __init__(self, patch_id):
        super().__init__(patch_id)

    def mutate(self, treepatch):
        new_treepatch = Treepatch(self.patch_id, 50)  # Create a new Treepatch with desired stats
        for neighbor in self.neighbors:
            if neighbor != treepatch:
                new_treepatch.add_neighbor(neighbor)  # Copy neighbors except the treepatch
                neighbor.neighbors.remove(self)  # Remove the Rockpatch from its neighbors

        # Replace the Rockpatch with the new Treepatch in all its neighbors' connections
        for neighbor in new_treepatch.neighbors:
            neighbor.neighbors.remove(treepatch)
            neighbor.add_neighbor(new_treepatch)

        return new_treepatch

class Treepatch(Landpatch):
    def __init__(self, patch_id, treestats):
        super().__init__(patch_id)
        self.treestats = treestats

    def get_treestat(self):
        return self.treestats
    
    def updateland(self, action):
    # Update Treepatch dynamics based on action
        if action == 'fire':
            self.treestats -= 20
            if self.treestats <= 0:
                self.mutate(Rockpatch(self.patch_id))
        elif action == 'nofire':
            if self.treestats == 256:
                return self.treestats
            elif (self.treestats <= 246):
                self.treestats += 10
            elif (246<self.treestats<256):
                self.treestats = 256

    def mutate(self, rockpatch):
        new_rockpatch = Rockpatch(self.patch_id)  # Create a new Rockpatch with the same ID

        # Copy neighbors except the rockpatch
        for neighbor in self.neighbors:
            if neighbor != rockpatch:
                new_rockpatch.add_neighbor(neighbor)
                neighbor.neighbors.remove(self)  # Remove Treepatch from its neighbors

        # Replace the Treepatch with the new Rockpatch in all its neighbors' connections
        for neighbor in new_rockpatch.neighbors:
            neighbor.neighbors.remove(self)
            neighbor.add_neighbor(new_rockpatch)

        return new_rockpatch

class Firefighter:
    def __init__(self, firefighter_id, skill_level, current_patch):
        self.firefighter_id = firefighter_id
        self.skill_level = skill_level
        self.current_patch = current_patch
        self.busy = False

    def move(self, target_patch):
    # Move the firefighter to the target patch
        if not self.busy:
            self.current_patch.firefighter_present = False
            self.current_patch = target_patch
            self.current_patch.firefighter_present = True

    def extinguish_fire(self, patch):
    # Extinguish fire in the given patch
        for neighbor in patch.get_neighbors():
            if isinstance(neighbor, Treepatch) and neighbor.treestats < 0:
                neighbor.updateland('firefighter')
        self.busy = False

    def is_busy(self):
        return self.busy






