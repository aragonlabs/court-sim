import mesa

#from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
#from mesa.visualization.modules import TextElement
from mesa.visualization.ModularVisualization import ModularServer
#from mesa.visualization.TextVisualization import TextData
#from mesa.visualization.TextVisualization import TextVisualization

from court.model import CourtModel

chart1 = ChartModule([
    {"Label": "successful", "Color": "#7bb36e"},{"Label": "failed", "Color": "#c66657"},{"Label": "total", "Color": "#56bfdf"}],
    data_collector_name='datacollector',
    canvas_height=300, canvas_width=300
)


chart2 = ChartModule([
    {"Label": "Gini", "Color": "#56bfdf"}],
    data_collector_name='datacollector',
    canvas_height=300, canvas_width=300
)

server = ModularServer(
    CourtModel,
    [chart1,chart2],
    name="CourtModel",
    model_params={
        "juror_count": UserSettableParameter('slider', "Number of juros", 20, 10, 100, 1,
                               description="Choose how many Juror agents to include in the model"),
        "token_count": UserSettableParameter('slider', "Number of tokens", 40, 10, 400, 1,
                                   description="Choose how many tokens in supply, tokens are split evenly among jurors at initialization."),
        "belief_deviation": UserSettableParameter('slider', "Belief Devation", 0.25, 0.01, 1, 0.01,
                                   description="Standard deviation used for sampling belief from a normal distribution around the models true value"),
        "penalty_pct": UserSettableParameter('slider', "Dispensation Percentage", 0.1, 0.01, 1, 0.01,
                                           description="Percentage of activated tokens which are redistributed from incoherent jurors to coherent")

    })
server.port = 8521
server.launch()
