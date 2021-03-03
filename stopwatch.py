from datetime import datetime
from modules.paint_it.paint_it import PaintIt


class Stopwatch(object):
    """
    Context manager that allows for measuring and displaying time with
    consistent indentations.
    """
    # count indentation common for all MeasureTimeClasses to make
    # displaying logs from multiple sources consistent
    global_indent = 0
    initial_time = datetime.now()

    def __init__(self, measurement_name, name=None, skip_start=False,
                 output=None, verbose=True):
        """
        C-tor that registers initial time.
        :param measurement_name: name of this logging device
        :param output: object that will store the output
        :param verbose: should logs be printed on stdio
        """
        self.indent = 0
        self.measur_name = measurement_name
        self.output = output
        self.verbose = verbose
        self.name = []
        self.color = []
        self.start = []
        self.skip_current_start = False
        if name or skip_start:
            self.__call__(name, skip_start)

    def log(self, message, color='unchanged'):
        """
        Prints simple log message which starts with the timestamp,
        respecting global and local indents.
        :param message: message to be displayed
        :param color: message color
        """
        message = f"{'> ' * self.indent}# {self.measur_name}: {message}"
        self.__output(message, color)

    def __call__(self, name='unknown', skip_start=False, color='unchanged'):
        """
        Allows adding a title to context-manager measurements.
        :param name: name of current measurement
        """
        self.skip_current_start = skip_start
        self.name.append(name)
        self.color.append(color)
        return self

    def __enter__(self):
        """
        Context manager that allows to measure time of chosen parts of
        code conveniently
        """
        self.start.append(datetime.now())
        if not self.skip_current_start:
            text = f"{'> ' * self.indent}> {self.measur_name}:" \
                   f"{' ' + self.name[-1] if self.name else ''} starting..."
            self.__output(text, color=self.color[-1])
        self.indent += 1
        Stopwatch.global_indent += 1
        return self

    def __exit__(self, type, value, traceback):
        """
        Ends context-manager measurement, logs execution time.
        """
        stop = datetime.now()
        self.indent -= 1
        Stopwatch.global_indent -= 1
        text = f"{'> ' * self.indent}< {self.measur_name}:" \
               f"{' ' + self.name.pop() if self.name else ''} finished in {stop - self.start.pop()}"
        self.__output(text, self.color.pop())

    def __output(self, text, color='unchanged'):
        """
        Formats input text, add timestamp and sends the output to stdio
        and log-saver
        :param text: text to be logged
        """
        text = f'[{datetime.now() - Stopwatch.initial_time}] ' +\
               '- ' * (Stopwatch.global_indent - self.indent) + text
        text = PaintIt(color)(text)
        if self.verbose:
            print(text)
        if self.output:
            self.output.write(text)
