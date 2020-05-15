

class InformationAnalyzer:
    from PIL import Image, ImageDraw, ImageTk

    def __init__(self):
        self._synapse_values = [[], []]
        self.widthLine = 1

    def update_synapses(self, synapse_values, network_index):
        self._synapse_values[network_index] = synapse_values

    def get_rendered_information(self, canvas_height, canvas_width):
        image = self.Image.new("RGBA", (canvas_width+50, canvas_height+50), (0, 0, 0, 0))
        draw = self.ImageDraw.Draw(image)

        draw.line(((0, 0), (canvas_width, 0)), fill=(0, 0, 255), width=self.widthLine)
        draw.line(((0, 0), (0, canvas_height)), fill=(0, 0, 255), width=self.widthLine)
        draw.line(((canvas_width, canvas_height), (0, canvas_height)), fill=(0, 0, 255),
                  width=self.widthLine)
        draw.line(((canvas_width, canvas_height), (canvas_width, 0)), fill=(0, 0, 255),
                  width=self.widthLine)

        del draw
        image = self.ImageTk.PhotoImage(image)
        return image

