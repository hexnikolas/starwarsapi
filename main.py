import requests
from datetime import datetime
import shutil
import matplotlib
import matplotlib.pyplot as plt
import random
import sys
import os
from itertools import cycle, islice

matplotlib.use('Qt5Agg')


# function to search for the star wars character name
def search(arguments):
    # check if the sys.argv has at least 3 arguments
    if len(arguments) < 3:
        print('not enough arguments to search for, exiting')
        sys.exit()

    # initialization of the output message
    message = ['']

    # check if cached folder exists and create it
    if not os.path.isdir('cached_requests'):
        os.mkdir('cached_requests')

    # check if the request has been made before
    if os.path.isfile(f"cached_requests/{' '.join(sys.argv)}"):
        # if it has, print the cached output
        with open(f"cached_requests/{' '.join(sys.argv)}", 'r') as f:
            print(f.read())
    else:
        # if not, make the request

        # character name to search
        name = arguments[2]

        # world argument
        world = False
        if '--world' in arguments:
            world = True

        # request the api
        response = requests.get(f"https://www.swapi.tech/api/people/?name={name}")

        # if the response is good, get the needed data
        if response.status_code == 200:
            response_data = response.json()
            # print(response_data)
            if response_data['result']:
                for character in response_data['result']:
                    message.append(f"Name: {character['properties']['name']}")
                    message.append(f"Height: {character['properties']['height']}")
                    message.append(f"Mass: {character['properties']['mass']}")
                    message.append(f"Birth Year: {character['properties']['birth_year']}")
                    message.append('')

                    # if world is needed, another request to the world url is made
                    if world:
                        planet_response = requests.get(character['properties']['homeworld'])

                        # check if the request was successful
                        if planet_response.status_code == 200:

                            # get the data
                            planet_response_data = planet_response.json()
                            if planet_response_data['result']:
                                message.append('Homewolrd')
                                message.append('---------')
                                message.append(f"Name: {planet_response_data['result']['properties']['name']}")
                                message.append(
                                    f"Population: {planet_response_data['result']['properties']['population']}")
                                message.append('')
                                try:
                                    day_period = round(
                                        int(planet_response_data['result']['properties']['rotation_period']) / 24, 2)
                                except ValueError:
                                    day_period = 'unknown'
                                try:
                                    orbital_period = round(
                                        int(planet_response_data['result']['properties']['orbital_period']) / 365, 2)
                                except ValueError:
                                    orbital_period = 'unknown'
                                message.append(
                                    f"On {planet_response_data['result']['properties']['name']}, 1 year on earth is {orbital_period} years and 1 day {day_period} days")
                                message.append('')

            else:
                # name not found
                message.append('The force is not strong within you')

            # print the message that has been gathered throughout the execution
            print('\n'.join(message))
            message.append('')

            # add timestamp to message
            message.append(f'cached: {datetime.now()}')

            # save message to cache
            with open(f"cached_requests/{' '.join(sys.argv)}", "w") as fp:
                fp.write('\n'.join(message))


# function to delete cached requests
def clean_cache():
    try:
        shutil.rmtree('cached_requests')
    except FileNotFoundError:
        pass
    print('removed cache')


# function to visualize the results
def visualize():
    try:
        # every file in the directory is a cached request
        points = os.listdir('cached_requests')
    except FileNotFoundError:
        print('no cached requests')
        sys.exit()

    # text to place over points
    annotations = [' '.join(x.split()[2:]) for x in points]

    # mouseover text
    results = []
    for file in points:
        with open(f'cached_requests/{file}', 'r') as f:
            results.append(f.read())

    amount = len(points)

    # create a scatter chart and the axis
    # we want as many points as the cached requests

    # x coordinates evenly spaced
    x = range(amount)

    # y coordinates randomized
    yaxis = [0.7, 0.1, 0.4, 1]
    random.shuffle(yaxis)

    # repeat the shuffled yaxis list, to fill in all the points needed
    y = list(islice(cycle(yaxis), amount))

    fig, ax = plt.subplots()

    # set x axis limits
    ax.set_xlim(-1, amount + 1)

    # set y axis limits
    ax.set_ylim(-0.2, 1.5)

    scatter = plt.scatter(
        x=x,
        y=y,
        s=200,
        picker=True
    )

    # create annotation object
    annotation = ax.annotate(
        text='',
        xy=(0, 0),
        xytext=(15, 15),  # distance from x, y
        textcoords='offset points',
        bbox={'boxstyle': 'round', 'fc': 'w', 'alpha': 1, 'pad': 2}
    )
    annotation.set_visible(False)

    # put the text over each point
    for i, xy in enumerate(zip(x, y)):
        plt.annotate(f"{annotations[i]}", xy, xytext=(-5, 10), textcoords='offset points')

    # implement the mouseover action
    def motion_hover(event):
        annotation_visbility = annotation.get_visible()
        if event.inaxes == ax:
            is_contained, annotation_index = scatter.contains(event)
            if is_contained:
                data_point_location = scatter.get_offsets()[annotation_index['ind'][0]]
                annotation.xy = data_point_location

                text_label = results[int(data_point_location[0])]
                annotation.set_text(text_label)

                annotation.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if annotation_visbility:
                    annotation.set_visible(False)
                    fig.canvas.draw_idle()

    # implement the click action
    def onpick(event):
        ind = event.ind
        print(results[ind[0]])

    fig.canvas.mpl_connect('motion_notify_event', motion_hover)
    fig.canvas.mpl_connect('pick_event', onpick)

    plt.show()


if __name__ == "__main__":

    if 'search' in sys.argv:
        search(sys.argv)
    elif 'cache' in sys.argv:
        clean_cache()
    elif 'visual' in sys.argv:
        visualize()
    else:
        print('wrong command, nothing to do')
