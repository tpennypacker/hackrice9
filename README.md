# hackrice9
Circuit Design/Build Tool

Inspiration
The intermediate steps between schematic design and board production are too time-consuming and tedious. After designing the schematic in a program such as LTSpice, you need to find usable packages for each component, place each component on the board, route the pin connections using bloated software, send the design files to a PCB manufacturer, wait a few weeks for the board to arrive, and then solder all of the components. Our software automates all of those intermediate steps, so you can skip from schematic design directly to functional prototype.

What it does
Our software takes just a circuit schematic as an input. It parses the schematic, and finds packages for each component, automatically lays the components out on the board, and automatically routes the traces using our custom algorithms. It displays the final board as an image, uses a camera and a neural network to find the physical board on the table, and projects the virtual board onto the physical board to be a template for soldering.

How we built it
Nikil has the most experience working with industry tools such as LTSpice, so he designed the test circuit and wrote the parser. Trevor used Python to determine the positions of the components and the traces, and OpenCV to construct and display the image. Paul and Alan used Tensorflow to detect the physical board from a webcam, and matrix algebra and projective transformations to morph the virtual board onto the physical board.

Challenges we ran into
It is physically impossible for the camera and the projector to be in the same exact location, forcing us to do some math to map the projector output onto the camera view. Auto routing also turned out to be an extremely complex problem, but we were able to come up with some algorithms to accomplish most of what we hoped to do.

Accomplishments that we're proud of
The whole project.

What we learned
Don't order essential components online during a hurricane.

What's next for Circuit 2.0
More advanced automation, faster computer vision, and integration into school curriculum.
