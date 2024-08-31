import numpy as np
import matplotlib.pyplot as plt

class OilGasPipelineOptimizer:
    def __init__(self, well_locations, obstacles=None):
        self.well_locations = np.array(well_locations)
        self.num_wells = len(well_locations)
        self.obstacles = obstacles if obstacles is not None else np.zeros((self.num_wells, self.num_wells))
        self.distance_matrix = self.calculate_distance_matrix()

    def calculate_distance_matrix(self):
        D = np.zeros((self.num_wells, self.num_wells))
        for i in range(self.num_wells):
            for j in range(self.num_wells):
                if i != j and self.obstacles[i, j] == 0:
                    D[i, j] = np.linalg.norm(self.well_locations[i] - self.well_locations[j])
                else:
                    D[i, j] = np.inf
        return D

    def find_shortest_path(self):
        path = [0]  # Start with the first well
        unvisited = set(range(1, self.num_wells))
        total_distance = 0

        while unvisited:
            current = path[-1]
            next_well = min(unvisited, key=lambda x: self.distance_matrix[current, x])
            path.append(next_well)
            total_distance += self.distance_matrix[current, next_well]
            unvisited.remove(next_well)

        return path, total_distance

    def plot_path(self, path):
        plt.figure(figsize=(10, 10))
        plt.scatter(self.well_locations[:, 0], self.well_locations[:, 1], c='blue', s=50)
        for i, well in enumerate(self.well_locations):
            plt.annotate(f'Well {i}', (well[0], well[1]))

        path_coords = self.well_locations[path]
        plt.plot(path_coords[:, 0], path_coords[:, 1], c='red', linewidth=2, linestyle='--')

        plt.title("Optimized Oil-Gas Pipeline Path")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.grid(True)
        plt.show()

# Example usage
if __name__ == "__main__":
    # Example well locations
    well_locations = [
        (0, 0), (2, 4), (5, 2), (7, 7), (10, 3),
        (12, 8), (15, 5), (18, 9), (20, 2), (22, 7)
    ]

    # Example obstacles (1 indicates an obstacle between wells)
    obstacles = np.zeros((len(well_locations), len(well_locations)))
    obstacles[1, 3] = obstacles[3, 1] = 1  # Example obstacle between wells 1 and 3

    optimizer = OilGasPipelineOptimizer(well_locations, obstacles)
    best_path, total_distance = optimizer.find_shortest_path()

    print(f"Best path: {best_path}")
    print(f"Total distance: {total_distance:.2f}")

    optimizer.plot_path(best_path)
