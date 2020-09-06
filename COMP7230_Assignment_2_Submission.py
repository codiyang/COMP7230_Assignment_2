"""
COMP7230 - 2020 Assignment 2 code skeleton.

TODO: Replace this with your student id
Student ID: u1043456

This assignment assesses some of the topics we have covered more recently
in the course. There is a reduced emphasis on actual coding and a greater emphasis on understanding, using and
modifying existing code in order to solve a particular problem.

You are given a (more-or-less) working piece of software, that simulates a pandemic outbreak in Australia. The
pandemic could be anything from the current COVID-19 outbreak to a zombie apocalypse. A similar approach could be used to
model memes spreading out across the internet, news spreading over Twitter or animals spreading in a new habitat.

This software is much more complex than what you are expected to be able to create on your own.
However it is a good example of the type of thing you might be able to find on the Internet and use
to solve a problem. As such, your tasks are to refactor and modify the software, to improve the documentation and
add logging functionality. Finally, you are asked to use the software to answer two questions about where to target a
response to the pandemic.

The assignment will be marked out of 40 and is worth 40% of your final grade for COMP7230.

For a full specification of your tasks for this assignment please see the Assignment Specification file on Wattle.

The assignment is structured as follows:

    Part 1 consists of Questions 1 and 2 and requires you to refactor part of the City class, add in
    logging functionality and improve the documentation and code quality of the City class.
    It is worth twenty (20) marks.

    Part 2 consists of Questions 3 and it asks you to extend the functionality of the
    TreatmentCentre class by completing the move method.
    It is worth four (6) marks.

    Part 3 consists of Questions 4 and 5 and asks you to use (and modify) the software
    in order to answer some questions. It is worth a total of ten (10) marks.
    Please be aware that these are a challenging questions and make sure you have
    solved parts 1 and 2 before spending too much time here.

Part 1 contains six (6) marks which are allocated to improving the code quality in the City class (included in the 20).
There will also be four (4) additional marks allocated to code quality for your answers to Parts 2 and 3,
which includes such aspects as:

    Appropriate commenting
    Variable naming
    Efficiency of computation
    Code structure and organisation

In addition to this file COMP7230_Assignment_2_Submission.py, we have also provided
some unit tests in COMP7230_Assignment_2_Submission_Tests.py which
will help you to test your work. Please note that these tests are there to assist you,
but passing the tests is NOT a guarantee that your solution is correct.

The assignment must be entirely your own work. Copying other students or sharing
solutions is a breach of the ANU Academic Honesty Policy and will be dealt with
accordingly. We reserve the right to ask any student to explain their code, and further
action may be taken if they are unable to do so.

The Assignment is due at 11:59pm, Sunday 6 September 2020.

Submission will be done through the link in Wattle . To submit your assignment, please upload your modified version
of COMP7230_Assignment_2_Submission.py (this file) ONLY. No work you undertake in other files will be marked.

Please don't forget to include your UID at the top of the file.

Once marks are released, you will have two weeks in which to question your mark.
After this period has elapsed, your mark will be considered final and no further
changes will be made.

If you ask for a re-mark, your assignment will be re-marked entirely, and your mark
may go UP or DOWN as a result.

The city data was obtained by merging information from: http://www.tageo.com/index-e-as-cities-AU.htm
with data from https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population
and individual Wikipedia pages for the cities.
The map was obtained from: https://www.google.com.au/maps
"""

import matplotlib.pyplot as plt
import imageio as im
import matplotlib.animation as animation
import sys
import datetime
import os
from matplotlib import gridspec

########################################################################################################################
#                               Simulation settings
########################################################################################################################
"""
    There are six different simulations that are 'built in' to the assignment (you can create others if you wish).
    They essentially change the parameters and initial setup (such as where the outbreak starts).
    You can change the simulation being run by changing the SIMULATION_NUMBER constant.
    0: the default - this is the default simulation settings, and also the settings used for the unit-testing.
    1 - 3: Other simulations you can explore, or use to check your answers to Parts 1 and 2
    4: is the simulation you should use to answer question 4
    5: is the simulation you should use to answer question 5
    Once you choose the simulation number, all the other parameters will be set accordingly.
"""
########################################################################################################################
#                           Change this to run a different simulation
SIMULATION_NUMBER = 0  # An integer from 0 to 5 corresponding to the particular simulation we are running
########################################################################################################################

# Create a logging directory if there isn't one there already.
if not os.path.exists(os.path.join(os.getcwd(), "logs")):
    os.mkdir(os.path.join(os.getcwd(),  "logs"))

########################################################################################################################
#                           Write to this log file for Question 2
LOG_FILE = open(os.path.join(os.getcwd(), "logs", "COMP7230_Assignment_2_Log_{}.txt".format(
    str(datetime.datetime.now()).replace(":", "_"))), mode="w")
LOG_FILE.write("=========================== Pandemic Simulation " + str(SIMULATION_NUMBER) + " ===========================\n")
########################################################################################################################


#  Map coordinates
MAP_LEFT = 112.2
MAP_RIGHT = 154.3
MAP_TOP = -10.3
MAP_BOTTOM = -40.2

# These parameters will be set by choosing the simulation number. They are all constant for a particular simulation.
STOPPING_CONDITIONS = 0  # An integer 0 - run to completion, otherwise an integer > 0 to describe the number of turns.
TREATMENT_MOVEMENT = False  # A boolean: False means the treatment centres are stationary, True means they move.
TREATMENT_LIMIT = 0  # The maximum number of infected a treatment unit can deal with.
MORTALITY_RATE = 1.0  # The proportion of infected people who die (float between 0 and 1.0).
INFECTION_RATE = 4.0  # The spreading factor. The number of new cases per infected per step (float >= 0).
MOVEMENT_PROPORTION = 0.1  # The proportion of infected who move cities each step (float between 0 and 1).
AVERAGE_DURATION = 4.0  # The average number of turns to recover or die, (float > 0).


########################################################################################################################
#                               City Class - Parts 1 and 2 of the Assignment
########################################################################################################################

# Note that for Question 2 - you should write to the file opened as LOG_FILE above

class City(object):
    """ Basic class for modelling a population centre. """

    def __init__(self, lat, long, name, population):

        self.name = name
        self.lat = lat
        self.long = long
        self.infected = 0
        self.incoming_infected = 0
        self.survivors = 0
        self.cured = 0
        self.dead = 0
        self.initial_population = population
        self.healthy_population = population
        self.neighbours = set()  # These are other instances of the city class.


        self.has_been_infected = False


    def __hash__(self):
        return hash(self.name)

    def __ne__(self, other):
        return self.name != other.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def remove_neighbour(self, neighbour):
        self.neighbours.remove(neighbour)

    def start_of_turn(self):
        # Needs to happen here
        if self.infected == 0 and self.incoming_infected > 0 and not self.has_been_infected:
            LOG_FILE.write("The pandemic reached {} for the first time in turn number {}.\n".format(self.name, engine.turn_number))
            self.has_been_infected = True

        self.infected += self.incoming_infected
        self.incoming_infected = 0

    def run_turn(self, turn_number):

        # Each turn:
        # A proportion of infected cases move to a neighbouring city
        # Then a proportion of infected cases either die or recover
        # Each remaining infected case contacts other people based on infection rate.
        # - if the contact is a survivor or has been cured, nothing happens.
        # - if the contact a healthy person, they get the disease.

        # Two other rules to stop the simulation running forever, or going very slowly.
        # The minimum number of infected cases that either die or recover is 5 (or all cases if less than 5 infected).
        # If there are less than 10 infected people and no healthy people in the city, set the number of infected to 0.

        # TODO: Question 1
        # TODO: Refactor this into several small methods. You can use the ones below or create your own.
        # TODO: You should call those methods from here instead, and the unit-test should still pass.

        self.move_infected()
        self.change_in_infected_numbers()
        self.spread_infection()
        self.infection_free()

    def move_infected(self):

        num_moving = int(self.infected * MOVEMENT_PROPORTION)
        num_per_neighbour = num_moving // len(self.neighbours)

        for nbr in self.neighbours:
            nbr.incoming_infected += num_per_neighbour
            self.infected -= num_per_neighbour

    def change_in_infected_numbers(self):

        if self.infected > 5:
            num_resolved = max(int(self.infected // AVERAGE_DURATION), 5)
        elif self.infected > 0:
            num_resolved = self.infected
        else:
            num_resolved = 0
        num_die = int(num_resolved * MORTALITY_RATE)

        self.infected -= num_resolved
        self.survivors += (num_resolved - num_die)
        self.dead += num_die

    def spread_infection(self):

        if self.healthy_population + self.survivors + self.cured > 0:

            r = self.healthy_population / (self.healthy_population + self.survivors + self.cured)

            hc = int(r * self.infected * INFECTION_RATE)

            if self.healthy_population < hc:
                self.infected += self.healthy_population
                self.healthy_population = 0

                if SIMULATION_NUMBER == 0:
                    LOG_FILE.write("Everyone in {} was infected and died in turn number {}\n".format(self.name, engine.turn_number))
                elif SIMULATION_NUMBER >= 0:
                    LOG_FILE.write("Everyone in {} was infected in turn number {}\n".format(self.name, engine.turn_number))

            elif self.infected > 0:
                self.healthy_population -= hc
                self.infected += hc


    def infection_free(self):
        """Added this function to define when is a city considered as infection free"""

        if self.infected < 10 and self.healthy_population == 0:
            self.dead += int(self.infected * MORTALITY_RATE)
            self.survivors += (self.infected - int(self.infected * MORTALITY_RATE))
            self.infected = 0
            LOG_FILE.write("The city {} became infection free in turn number {}; total death {}, total survivors {}.\n".
                           format(self.name, engine.turn_number, self.dead, self.survivors))


########################################################################################################################
#                               Treatment Centre Class - Part 2
########################################################################################################################
class TreatmentCentre(object):
    """ Class for a treatment for the pandemic (Could be a cure for a virus, soldiers for a zombie apocalypse, etc."""

    def __init__(self, treatment_id, city):
        """
        :param treatment_id: The id of the TreatmentCentre
        :param city: The city where it is located (instance of the City class).
        """

        self.treatment = treatment_id
        self.treatment_remaining = TREATMENT_LIMIT
        self.city = city

    def move(self):
        """ Moves the treatment centre.
        Looks at neighbouring cities of the current city to find the one with the most
        infected cases and moves there. Should stay where it is if the current city has the most.
        """

        # TODO: Question 3
        # TODO: Implement this function.
        pass

    def run_turn(self, turn_number):
        """ Runs the turn for the treatment unit.
        If movement is on, tries to move.
        Then treats any infected people in the city.
        """

        if TREATMENT_MOVEMENT:
            self.move()

        if self.city.infected <= self.treatment_remaining:
            self.treatment_remaining -= self.city.infected
            self.city.cured += self.city.infected
            self.city.infected = 0
        else:
            self.city.cured += self.treatment_remaining
            self.city.infected -= self.treatment_remaining
            self.treatment_remaining = 0


########################################################################################################################
#                               Engine Class
########################################################################################################################
class Engine(object):
    """ Class to actually run the simulation. """

    def __init__(self, cities, treatments):

        self.turn_number = 0
        self.cities = cities
        self.treatments = treatments

        # Attributes for collecting simulation statistics.
        self.healthy_population = []
        self.infected = []
        self.survivors = []
        self.deaths = []
        self.cured = []

    def run_turn(self):
        """ Advances the simulation by a single turn."""

        self.turn_number += 1

        # Run the start of turn in each city.
        for city in self.cities.values():
            city.start_of_turn()

        # Run the actual turn in each city.
        for city in self.cities.values():
            city.run_turn(self.turn_number)

        # Run the turn for each treatment centre
        for treatment in self.treatments.values():
            treatment.run_turn(self.turn_number)

        # Gather the statistics
        self.infected.append(sum([city.infected for city in self.cities.values()]))
        self.healthy_population.append(sum([city.healthy_population for city in self.cities.values()]))
        self.survivors.append(sum([city.survivors for city in self.cities.values()]))
        self.deaths.append(sum([city.dead for city in self.cities.values()]))
        self.cured.append(sum([city.cured for city in self.cities.values()]))


########################################################################################################################
#                               Other functions
########################################################################################################################
def convert_lat_long(lat, long):
    """ Converts a latitude and longitude pair into an x, y pair of map-coordinates.
    :param lat: the latitude value.
    :param long: the longitude value.
    :return an (x, y) tuple of coordinates, where x and y are floats between 0.0 and 1.0.
    """

    x_diff = MAP_RIGHT - MAP_LEFT
    y_diff = MAP_TOP - MAP_BOTTOM

    return (long - MAP_LEFT) / x_diff, (lat - MAP_BOTTOM) / y_diff


def get_city_data(file_name):
    """ Reads in city and connection data from the specified file.
    Format of the file is:
    lat,long,name,population
    ### - break point between the two sections.
    city_1,city_2
    """

    input_file = open(file_name, mode="r")

    # Get the cities first
    cities = dict()
    for line in input_file:
        # Check for the end of the city information
        if line[0:3] == "###":
            break
        line = line.strip().split(",")

        lat = float(line[0])
        long = float(line[1])
        name = line[2]
        population = int(line[3])
        cities[name] = City(lat, long, name, population)

    # Now read in the connections
    for line in input_file:
        city_1, city_2 = line.strip().split(",")
        cities[city_1].add_neighbour(cities[city_2])
        cities[city_2].add_neighbour(cities[city_1])

    return cities


def get_initial_parameters(scenario_number):
    """
    Gets the initial parameters and treatment options for the given scenario.
    :param scenario_number: The scenario being run.
    :return: a tuple of (stopping, treatment move, treat lim, mortality, infection rt, movement prop, average dur).
    """

    #       Stop    TrtMo   TRtL    MoR     InR     MoP     AvgDur
    scenario_dict = {
        0: (0,      False,  0,      1.0,    4.0,    0.1,    4.0),
        1: (150,    False,  0,      0.1,    0.4,    0.25,   3.0),
        2: (150,    True,   150000, 0.1,    0.4,    0.25,   3.0),
        3: (0,      True,   150000, 0.25,   1.5,    0.1,    4.0),
        4: (20,     False,  0,      0.3,    1.0,    0.05,   4.0),
        5: (0,      False,  1000,   0.05,   0.7,    0.1,    3.0)
    }

    if scenario_number not in scenario_dict:
        scenario_number = 0

    return scenario_dict[scenario_number]


def set_initial_state(scenario_number, engine):
    """
    Sets the initial infection cases and treatment centres.
    The initial infection cases are added using the 'incoming_infected' attribute.
    Modifies the state of cities and treatment centres in the engine directly.
    :param scenario_number: The scenario being run.
    :param engine: the engine running the simulation.
    :return: None
    """

    state_dict = {
        0: (tuple(), (("Alice Springs", 1000),)),
        1: (tuple(), (("Rockhampton", 1000), ("Brisbane", 10000), ("Gold Coast", 1000))),
        2: (("Sydney", "Melbourne", "Adelaide"), (("Rockhampton", 1000), ("Brisbane", 10000), ("Gold Coast", 1000))),
        3: (("Sydney", "Perth", "Melbourne"), (("Canberra", 5000), ("Cairns", 5000))),
        4: (tuple(), (("Rockhampton", 1000), ("Brisbane", 10000), ("Gold Coast", 1000))),
        5: (("Sydney", "Perth", "Melbourne"), (("Canberra", 5000), ("Cairns", 5000)))
    }
    if scenario_number not in state_dict:
        scenario_number = 0

    for index, city in enumerate(state_dict[scenario_number][0]):
        engine.treatments[index] = TreatmentCentre(index, engine.cities[city])

    for city, cases in state_dict[scenario_number][1]:
        engine.cities[city].incoming_infected = cases


def animate_map(data, engine, map_image, sp1, sp2, sp3, sp4):

    if not engine:
        return

    # Check for termination conditions here.
    if (engine.infected and engine.infected[-1] == 0) or (STOPPING_CONDITIONS and
                                                          engine.turn_number >= STOPPING_CONDITIONS):
        get_input = input("The simulation has ended; press 'Enter' to finish.")

        LOG_FILE.write("=========================== End of Log ===========================\n")
        LOG_FILE.close()
        sys.exit()

    # Advance the simulation by 1 turn
    engine.run_turn()

    # Display the map and statistics
    height, width = len(map_image), len(map_image[0])

    sp1.clear()
    sp1.set_axis_off()
    sp1.imshow(map_image)
    sp1.set_title("Pandemic Simulation - {} turns".format(engine.turn_number))

    # Plot the cities
    for city in engine.cities.values():
        x, y = convert_lat_long(city.lat, city.long)
        if city.infected > 0.1 * city.initial_population:
            color = "red"
        elif city.infected > 0.01 * city.initial_population:
            color = "orange"
        elif city.infected > 0:
            color = "yellow"
        elif city.healthy_population == 0 and city.survivors == 0 and city.cured == 0:
            color = "black"
        else:
            color = "blue"

        sp1.plot(x * width, (1 - y) * height, "o", markersize=10.0, color=color)
        if city.initial_population > 150000:
            sp1.text(x * width + 12, (1 - y) * height + 12, s=city.name)

        # Uncomment the following four lines if you wish to see the connections on the map during simulation.
        #for nbr in city.neighbours:
        #    if nbr < city:
        #        nx, ny = convert_lat_long(nbr.lat, nbr.long)
        #        sp1.plot((x * width, nx * width), ((1 - y) * height, (1 - ny) * height), color="black")

    # Plot the line graphs
    sp2.clear()
    sp2.plot(range(1, engine.turn_number + 1), engine.healthy_population, color="blue", label="Healthy")
    sp2.plot(range(1, engine.turn_number + 1), engine.infected, color="red", label="Infected")
    sp2.set_xlim([1, engine.turn_number + 15])
    sp2.legend(loc="right")
    sp2.set_xlabel("Turns")
    sp2.set_ylabel("People")
    sp2.set_title("Simulation Statistics")
    if (max(engine.healthy_population) > 10 * max(engine.infected) or
            max(engine.healthy_population) * 10 < max(engine.infected)):
        sp2.set_yscale("log")

    sp3.clear()
    sp3.plot(range(1, engine.turn_number + 1), engine.survivors, color="green", label="Survivors")
    sp3.plot(range(1, engine.turn_number + 1), engine.deaths, color="black", label="Deaths")
    sp3.set_xlim([1, engine.turn_number + 15])
    sp3.legend(loc="right")
    sp3.set_xlabel("Turns")
    sp3.set_ylabel("People")
    if (max(engine.survivors) > 10 * max(engine.deaths) or
            max(engine.survivors) * 10 < max(engine.deaths)):
        sp3.set_yscale("log")

    sp4.clear()
    sp4.plot(range(1, engine.turn_number + 1), engine.cured, color="purple", label="Cured")
    sp4.set_xlim([1, engine.turn_number + 15])
    sp4.legend(loc="right")
    sp4.set_xlabel("Turns")
    sp4.set_ylabel("People")

########################################################################################################################
#                               Main Function - Part 4
########################################################################################################################
if __name__ == "__main__":

    # Set the scenario parameters
    STOPPING_CONDITIONS, TREATMENT_MOVEMENT, TREATMENT_LIMIT, MORTALITY_RATE, \
        INFECTION_RATE, MOVEMENT_PROPORTION, AVERAGE_DURATION = get_initial_parameters(SIMULATION_NUMBER)

    # Get the city data and population
    cities = get_city_data("final_city_data.csv")
    treatments = dict()

    # Create the engine that will run the simulation
    engine = Engine(cities, treatments)

    # Setup initial infected cases and treatment centres
    set_initial_state(SIMULATION_NUMBER, engine)

    ####################################################################################################################
    #                               Answer to Q4 goes here
    ####################################################################################################################
    if SIMULATION_NUMBER == 4:
        for i in range(20):
            engine.run_turn()
            print("Ran turn{}".format(engine.turn_number))

    ####################################################################################################################
    #                               Answer to Q5 goes here
    ####################################################################################################################
    if SIMULATION_NUMBER == 5:
        pass

    ####################################################################################################################

    # Get the map and fade it for better viewing.
    aus_map = im.imread("Aus_Map.PNG")
    aus_map[:,:,3] = (aus_map[:,:,3] * 0.6)

    # Setup the plot layout
    fig = plt.figure(figsize=[10, 13])
    sps1, sps2, sps3, sps4 = gridspec.GridSpec(4, 1, height_ratios=(10, 1, 1, 1))

    sp1 = plt.subplot(sps1)
    sp2 = plt.subplot(sps2)
    sp3 = plt.subplot(sps3)
    sp4 = plt.subplot(sps4)

    # Produce the animation and run the simulation.
    display = animation.FuncAnimation(fig, animate_map, interval=100, repeat=False,
                                      fargs=(engine, aus_map, sp1, sp2, sp3, sp4),
                                      frames=None)
    plt.show()
