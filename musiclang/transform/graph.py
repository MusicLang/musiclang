
class TransformGraph:
    """
    Store a directed graph of musical transformations.
    Can be called to returns outputs, Usually returns a single node which is a score

    Basically an implementation of a directed graph, nothing specific to musiclang

    Parameters :
    -----------

    - inputs nodes : (MusicLangWrite | Transform | Filter | Pipeline)*
    - transform nodes : Transform | Filter | Pipeline
    - Nodes can be : ``Score``, ``Melodies``, ``ConcatPipeline``, ``TransformPipeline``, ``ScoreMerger`` or any function with appropriate inputs/outputs

    Examples
    --------
    >>> from musiclang.library import *
    >>> from musiclang.transform.score_merger import ConcatScores
    >>> score1 =  (I % I.M)(s0, s2, s4)
    >>> score2 =  (II % I.M)(s0, s2, s4)
    >>> score3 =  (III % I.M)(s0, s2, s4)
    >>> g = TransformGraph(inputs=['A', 'B', 'C'], outputs='D')
    >>> g.add(output="D", inputs=['A', 'B', 'C'], transfo=ConcatScores())
    >>> g.add('D', ('A', 'B', 'C'), ConcatScores())
    >>> g['D'] = (('A', 'B', 'C'), ConcatScores())
    >>> g(score1, score2, score3)
    (I % I.M)(s0, s2, s4) + (II % I.M)(s0, s2, s4) + (III % I.M)(s0, s2, s4)

    You can add multioutputs transforms :

    >>> g = TransformGraph(inputs=['A', 'B', 'C'], outputs=('D', 'E'))
    >>> g[('D', 'E')] = (('A', 'B'), (lambda a, b : a+b, b)

    """

    def __init__(self, inputs, outputs, nodes=None):
        self.inputs = inputs
        self.names = set()
        self.compute_order = []
        self.names = self.names.union(inputs)
        self.outputs = tuple(outputs) if isinstance(outputs, (list, tuple)) else outputs
        self.nodes = {}
        if nodes is not None:
            self.add_many(nodes)


    @property
    def _multioutput(self):
        return isinstance(self.outputs, (list, tuple))

    def copy(self):
        new_graph = TransformGraph(self.inputs, self.outputs, nodes=dict(self.nodes))
        return new_graph

    def add_many(self, args):
        for arg in args:
            self.add(*arg)

    def __setitem__(self, outputs, value):
        self.add(outputs, value[0], value[1])

    def add(self, outputs, inputs, transfo):
        """
        Add a node in the graph
        Parameters
        ----------
        outputs: tuple or str
        inputs: tuple or list
        transfo : function
                  Function that will take the inputs and returns the outputs

        """
        outputs = tuple(outputs) if isinstance(outputs, (list, tuple)) else outputs
        self.nodes[outputs] = (inputs, transfo)
        if not self.names.issuperset(inputs):
            raise Exception(f'Unexisting inputs {set(inputs) - self.names}.'
                            f' You must define all inputs before defining the node (Only direct acyclic graphs)')
        if isinstance(outputs, tuple):
            for output in outputs:
                self.names.add(output)
        else:
            self.names.add(outputs)
        self.compute_order.append(outputs)

    def _get_compute_graph(self, *args, **parameters):
        if not self.names.issuperset(self.outputs):
            missing_outputs = set(self.outputs) - self.names
            raise Exception(f'Some outputs : "{missing_outputs}" are not defined ')
        compute_graph = {self.inputs[idx]: arg for idx, arg in enumerate(args)}
        kwargs_compute_graph = {key: val for key, val in parameters.items() if key in self.inputs}
        compute_graph = {**kwargs_compute_graph, **compute_graph}
        for outputs in self.compute_order:
            input_names, transfo = self.nodes[outputs]
            inputs = [compute_graph[i] for i in input_names]
            result = transfo(*inputs)
            if isinstance(outputs, (list, tuple)):
                for r, output in zip(result, outputs):
                    compute_graph[output] = r
            else:
                compute_graph[outputs] = result

        return compute_graph

    def __call__(self, *args, **parameters):
        compute_graph = self._get_compute_graph(*args, **parameters)

        if self._multioutput:
            res = tuple([compute_graph[output] for output in self.outputs])
            return res
        else:
            return compute_graph[self.outputs]

