import sys
import random
import itertools
from types import NoneType
import numpy as np
import cv2 as cv

MAP_FILE = "cape_map.png"

SA1_CORNERS = (260, 300, 330, 370)  # "SA" stands for search area
SA2_CORNERS = (330, 325, 400, 395)
SA3_CORNERS = (290, 395, 360, 465)


class Search:
    """
    Game simulator of a search for a castaway within 3 search areas
    """

    def __init__(self, name):
        self.name = name
        try:
            self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        except NoneType:
            print("Can't load the file with a map {}.".format(MAP_FILE), file=sys.stderr)
            sys.exit(1)

        self.actual_area = 0
        self.actual_location = []

        # Arrays of search areas for NumPy operations
        self.sa1 = self.img[SA1_CORNERS[1] : SA1_CORNERS[3],
                            SA1_CORNERS[0] : SA1_CORNERS[2]]

        self.sa2 = self.img[SA2_CORNERS[1] : SA2_CORNERS[3],
                            SA2_CORNERS[0] : SA2_CORNERS[2]]

        self.sa3 = self.img[SA3_CORNERS[1] : SA3_CORNERS[3],
                            SA3_CORNERS[0] : SA3_CORNERS[2]]

        # Probability of finding the castaway at a particular search area
        self.prob1 = 0.2
        self.prob2 = 0.5
        self.prob3 = 0.3

        # Probability of an effective search
        self.effectprob1 = 0
        self.effectprob2 = 0
        self.effectprob3 = 0

    def draw_map(self, last_known):  # mogę tu kiedyś dodać wymóg typu
        """
        Shows the map of the region with a scale, last known castaway's position and the search areas
        :param last_known:
        :return:
        """

        # Draws a scale
        cv.line(self.img, (700, 650), (830, 650), (0, 0, 0), 2)
        cv.putText(self.img, '0', (680, 650), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, '50', (840, 650), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, 'nautical miles', (708, 670), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        # Draws search areas
        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1]), (SA1_CORNERS[2], SA1_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '1', (265, 295), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.rectangle(self.img, (SA2_CORNERS[0], SA2_CORNERS[1]), (SA2_CORNERS[2], SA2_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '2', (385, 320), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.rectangle(self.img, (SA3_CORNERS[0], SA3_CORNERS[1]), (SA3_CORNERS[2], SA3_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '3', (365, 460), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        # Draws a "+" symbol on the last known position of the castaway
        cv.putText(self.img, "+", (last_known[0] - 8, last_known[1] + 5), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

        # Draws a legend
        cv.putText(self.img, '+ -> last known location', (648, 25), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, '* -> actual location', (648, 45), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        # Displays the map
        cv.imshow(self.name, self.img)
        cv.moveWindow(self.name, 750, 10)
        cv.waitKey(50000000)

    def gen_actual_location(self, num_search_areas):
        """
        Returns coordinates of the actual castaway's location
        :return x, y:
        """

        # Draws a coordinates within a search area (no matter which one)
        self.actual_location[0] = np.random.choice(self.sa1.shape[1], 1)
        self.actual_location[1] = np.random.choice(self.sa1.shape[0], 1)

        # Draws the actual area of the castaway (2nd being the most possible one)
        self.actual_area = int(random.triangular(1, num_search_areas + 1))

        # Provides the final coordinates according to the whole map
        if self.actual_area == 1:
            x = self.actual_location[0] + SA1_CORNERS[0]
            y = self.actual_location[1] + SA1_CORNERS[1]
        elif self.actual_area == 2:
            x = self.actual_location[0] + SA2_CORNERS[0]
            y = self.actual_location[1] + SA2_CORNERS[1]
        elif self.actual_area == 3:
            x = self.actual_location[0] + SA3_CORNERS[0]
            y = self.actual_location[1] + SA3_CORNERS[1]
        else:
            print("Error with actual location")
            sys.exit(1)



        return x, y

    def calc_search_effectiveness(self):
        """
        Designates a decimal value of search effectiveness for each search area
        (it won't ever be 100% effective because of e.g. bad weather or equipment faults)
        :return:
        """

        self.effectprob1 = random.uniform(0.2, 0.9)
        self.effectprob2 = random.uniform(0.2, 0.9)
        self.effectprob3 = random.uniform(0.2, 0.9)

    def conduct_search(self, area_num, area_array, effectiveness_prob):
        """
        Returns the outcome of the search and the list of searched coordinates
        :return outcome:
        """

        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])

        coords_list = list(itertools.product(local_x_range, local_y_range))
        random.shuffle(coords_list)
        coords_list = coords_list[:int((len(coords_list) * effectiveness_prob))]


if __name__ == "__main__":
    game = Search("new_game")
    game.draw_map((285, 344))
