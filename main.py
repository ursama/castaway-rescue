import sys
import random
import itertools
from types import NoneType
import numpy as np
import cv2 as cv

MAP_FILE = "cape_map.png"

SA1_CORNERS = (261, 303, 328, 372)  # "SA" stands for search area
SA2_CORNERS = (331, 325, 400, 395)
SA3_CORNERS = (291, 396, 364, 470)


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

        self.actual_area = 2
        self.actual_castaway = [357, 352]

        self.sa1 = self.img[SA1_CORNERS[1] : SA1_CORNERS[3],
                            SA1_CORNERS[0] : SA1_CORNERS[2]]

        self.sa2 = self.img[SA2_CORNERS[1] : SA2_CORNERS[3],
                            SA2_CORNERS[0] : SA2_CORNERS[2]]

        self.sa3 = self.img[SA3_CORNERS[1] : SA3_CORNERS[3],
                            SA3_CORNERS[0] : SA3_CORNERS[2]]

        self.prob1 = 0.2
        self.prob2 = 0.5
        self.prob3 = 0.3

        self.searchprob1 = 0.5
        self.searchprob2 = 0.5
        self.searchprob3 = 0.5

    def draw_map(self, last_known):  # mogę tu kiedyś dodać wymóg typu
        """
        Shows the map of the region with a scale, last known castaway's position and the search areas
        :param last_known:
        :return:
        """

        # Draws a scale
        cv.line(self.img, (716, 655), (845, 655), (0, 0, 0), 2)
        cv.putText(self.img, '0', (689, 626), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, '50', (832, 626), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, 'nautical miles', (733, 663), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        # Draws search areas
        cv.rectangle(self.img, (SA1_CORNERS[1], SA1_CORNERS[3]), (SA1_CORNERS[0], SA1_CORNERS[2]), (0, 0, 0), 1)
        cv.putText(self.img, '1', (251, 279), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.rectangle(self.img, (SA2_CORNERS[1], SA2_CORNERS[3]), (SA2_CORNERS[0], SA2_CORNERS[2]), (0, 0, 0), 1)
        cv.putText(self.img, '2', (393, 296), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.rectangle(self.img, (SA3_CORNERS[1], SA3_CORNERS[3]), (SA3_CORNERS[0], SA3_CORNERS[2]), (0, 0, 0), 1)
        cv.putText(self.img, '3', (370, 446), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))


if __name__ == "__main__":
    game = Search("new_game")
    game.draw_map((285, 344))
