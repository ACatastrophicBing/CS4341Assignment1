#!/usr/bin/env python

import math
from priority_queue import PriorityQueue
import numpy as np


class PathPlanner:


    def __init__(self):
        """
        Class constructor
        """



    @staticmethod
    def grid_to_index(mapdata, x, y):
        """
        Returns the index corresponding to the given (x,y) coordinates in the occupancy grid.
        :param x [int] The cell X coordinate.
        :param y [int] The cell Y coordinate.
        :return  [int] The index.
        """

        ### REQUIRED CREDIT
        return y * mapdata.info.width + x

    @staticmethod
    def index_to_grid(mapdata, i):
        """
        Returns the index corresponding to the given (x,y) coordinates in the occupancy grid.
        :param x [int] The cell X coordinate.
        :param y [int] The cell Y coordinate.
        :return  [int] The index.
        """
        x = i%mapdata.info.width
        y = int(math.floor(i/mapdata.info.width))
        ### REQUIRED CREDIT
        return (x,y)


    @staticmethod
    def euclidean_distance(x1, y1, x2, y2):
        """
        Calculates the Euclidean distance between two points.
        :param x1 [int or float] X coordinate of first point.
        :param y1 [int or float] Y coordinate of first point.
        :param x2 [int or float] X coordinate of second point.
        :param y2 [int or float] Y coordinate of second point.
        :return   [float]        The distance.
        """

        ### REQUIRED CREDIT
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)



    @staticmethod
    def grid_to_world(mapdata, x, y):
        """
        Transforms a cell coordinate in the occupancy grid into a world coordinate.
        :param mapdata [OccupancyGrid] The map information.
        :param x       [int]           The cell X coordinate.
        :param y       [int]           The cell Y coordinate.
        :return        [Point]         The position in the world.
        """

        ### REQUIRED CREDIT
        resolution = mapdata.info.resolution
        origin_x = mapdata.info.origin.position.x
        origin_y = mapdata.info.origin.position.y
        world_x = (x+0.5)*resolution + origin_x
        world_y = (y+0.5)*resolution + origin_y
        wc = Point()
        wc.x = world_x
        wc.y = world_y
        return wc



    @staticmethod
    def world_to_grid(mapdata, wp):
        """
        Transforms a world coordinate into a cell coordinate in the occupancy grid.
        :param mapdata [OccupancyGrid] The map information.
        :param wp      [Point]         The world coordinate.
        :return        [(int,int)]     The cell position as a tuple.
        """

        ### REQUIRED CREDIT
        resolution = mapdata.info.resolution
        origin_x = mapdata.info.origin.position.x
        origin_y = mapdata.info.origin.position.y
        grid_x = int((wp.x - origin_x)/resolution)
        grid_y = int((wp.y - origin_y)/resolution)
        return (grid_x, grid_y)



    @staticmethod
    def path_to_poses(mapdata, path):
        """
        Converts the given path into a list of PoseStamped.
        :param mapdata [OccupancyGrid] The map information.
        :param  path   [[(int,int)]]   The path as a list of tuples (cell coordinates).
        :return        [[PoseStamped]] The path as a list of PoseStamped (world coordinates).
        """

        ### REQUIRED CREDIT
        poseS = []
        counter = 0
        for cell in path:
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.header.stamp = rospy.Time.now()
            point = PathPlanner.grid_to_world(mapdata, cell[0], cell[1])
            pose.pose.position = point

            Rot = 0
            if cell != path[-1]:
                nextCell = path[counter + 1]
                deltaX = nextCell[0] - cell[0]
                deltaY = nextCell[1] - cell[1]
                Rot = math.atan2(deltaY, deltaX)

            quaterninon = quaternion_from_euler(0, 0, Rot)
            pose.pose.orientation.x = quaterninon[0]
            pose.pose.orientation.y = quaterninon[1]
            pose.pose.orientation.z = quaterninon[2]
            pose.pose.orientation.w = quaterninon[3]

            counter += 1
            poseS.append(pose)
        # print(poseS)
        return poseS



    @staticmethod
    def is_cell_walkable(mapdata, x, y):
        """
        A cell is walkable if all of these conditions are true:
        1. It is within the boundaries of the grid;
        2. It is free (not unknown, not occupied by an obstacle)
        :param mapdata [OccupancyGrid] The map information.
        :param x       [int]           The X coordinate in the grid.
        :param y       [int]           The Y coordinate in the grid.
        :return        [boolean]       True if the cell is walkable, False otherwise
        """

        ### REQUIRED CREDIT
        width = mapdata.info.width
        height = mapdata.info.height
        #print(x,y,width,height)
        #print(len(mapdata.data))
        #print(PathPlanner.grid_to_index(mapdata, x, y))
        if x >= width or x < 0 or y >= height or y < 0:
            return False
        if mapdata.data[PathPlanner.grid_to_index(mapdata, x, y)] > 50:
            return False
        return True



    @staticmethod
    def neighbors_of_4(mapdata, x, y):
        """
        Returns the walkable 4-neighbors cells of (x,y) in the occupancy grid.
        :param mapdata [OccupancyGrid] The map information.
        :param x       [int]           The X coordinate in the grid.
        :param y       [int]           The Y coordinate in the grid.
        :return        [[(int,int)]]   A list of walkable 4-neighbors.
        """

        ### REQUIRED CREDIT
        neighbors = []

        addx = [1, -1, 0, 0]
        addy = [0, 0, 1, -1]
        for i in range(len(addx)):
            if PathPlanner.is_cell_walkable(mapdata, x + addx[i], y + addy[i]):
                neighbors.append((x + addx[i], y + addy[i]))

        return neighbors



    @staticmethod
    def neighbors_of_8(mapdata, x, y):
        """
        Returns the walkable 8-neighbors cells of (x,y) in the occupancy grid.
        :param mapdata [OccupancyGrid] The map information.
        :param x       [int]           The X coordinate in the grid.
        :param y       [int]           The Y coordinate in the grid.
        :return        [[(int,int)]]   A list of walkable 8-neighbors.
        """

        ### REQUIRED CREDIT
        neighbors = []

        addx = [1, -1, 0, 0, 1, 1, -1, -1]
        addy = [0, 0, 1, -1, 1, -1, -1, 1]
        for i in range(len(addx)):
            try:
               neighbors.append((x + addx[i], y + addy[i]))
               break
            except Exception as err:
                print("Not a valid index!")
        return neighbors


    def a_star(self, mapdata, start, goal):
        """The start and goal are a tuple in grid format, mapdata is a matrix of size x,y"""
        ### REQUIRED CREDIT
        print("Executing A* from (%d,%d) to (%d,%d)" % (start[0], start[1], goal[0], goal[1]))
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        came_from[goal] = None

        # Create the frontiers
        frontierStuff = frontier.get_queue()
        frontierCells = []
        for priorityTuple in frontierStuff:
            gridTuple = priorityTuple[1]
            # print(gridTuple)
            frontierCells.append(gridTuple[0], gridTuple[1])


        #expanded cells to show pathed frontiers
        expandedCells = []


        #Go through graph until frontier is empty
        while not frontier.empty():
            current = frontier.get()

            # update the frontiers visited just to let us see visually if we want
            expandedCells.append(current[0], current[1])

            # If we have reached the goal, leave
            if current == goal:
                break

            #Add viable children to frontier
            for next in PathPlanner.neighbors_of_8(mapdata, current[0], current[1]):
                new_cost = 0 # cost_so_far[current] + PathPlanner.euclidean_distance(current[0], current[1], next[0], next[1])
                cell_cost = mapdata[current[0]][current[1]] # Cost of the next cell
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + PathPlanner.euclidean_distance(current[0], current[1], goal[0], goal[1])
                    frontier.put(next, priority)

                    # update frontier message
                    frontierStuff = frontier.get_queue()
                    frontierCells = []
                    for priorityTuple in frontierStuff:
                        gridTuple = priorityTuple[1]
                        frontierCells.append(gridTuple[0], gridTuple[1])

                    #add parent to came_from table
                    came_from[next] = current

        # Return the path found
        path = []
        current = goal
        if came_from[goal] != None:
            while came_from[current] != None:
                path.append(current)
                current = came_from[current]
            path.append(start)
        else:
            return path

        #reverse path to make it so the first element is the start
        path = path[::-1]
        print("A* completed")
        #print(path)
        return path


    def plan_path(self, mapdata):
        """
        Plans a path between the start and goal locations in the requested.
        Internally uses A* to plan the optimal path.
        :param req
        """
        ## Request the map
        ## In case of error, return an empty path
        ## Execute A*
        start = np.where(mapdata == 'S')
        goal = np.where(mapdata == 'G')
        path  = self.a_star(mapdata, start, goal)
        ## Return a Path message
        return path



if __name__ == '__main__':
    PathPlanner().run()