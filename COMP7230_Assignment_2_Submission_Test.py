import unittest
from COMP7230_Assignment_2_Submission import *


def create_test_network():
    """ Needed to setup a small network for testing purposes.
    :return - A dictionary of City objects "A", "B", "C", "D".
    """

    # Create the cities
    A = City(0, 0, "A", 10000)
    B = City(0, 1, "B", 10000)
    C = City(1, 0, "C", 5000)
    D = City(1, 1, "D", 5000)

    # Add the connections between them
    A.add_neighbour(B)
    B.add_neighbour(A)
    A.add_neighbour(C)
    C.add_neighbour(A)
    B.add_neighbour(C)
    C.add_neighbour(B)
    A.add_neighbour(D)
    D.add_neighbour(A)

    # Seed in some initial infected cases
    C.infected = 200

    city_dict = {"A": A, "B": B, "C": C, "D": D}

    return city_dict


class SubmissionTest(unittest.TestCase):

    def test_city_run_turn(self):

        # Create a test network
        cities = create_test_network()

        # Run the turn on C to see what happens
        cities["C"].run_turn(1)

        # Check the result is what we expect.
        self.assertEqual(cities["B"].incoming_infected, 10)
        self.assertEqual(cities["C"].incoming_infected, 0)
        self.assertEqual(cities["C"].dead, 45)
        self.assertEqual(cities["C"].survivors, 0)
        self.assertEqual(cities["C"].infected, 675)

        # Run a turn on B to check
        cities["B"].start_of_turn()

        self.assertEqual(cities["B"].infected, 10)

        cities["B"].run_turn(2)

        self.assertEqual(cities["C"].incoming_infected, 0)
        self.assertEqual(cities["B"].dead, 5)
        self.assertEqual(cities["B"].infected, 25)

if __name__ == "__main__":
    unittest.main()