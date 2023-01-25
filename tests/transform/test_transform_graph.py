from musiclang.transform import TransformGraph



def test_multioutput():
    g = TransformGraph(inputs=['A', 'B', 'C'], outputs=('D', 'E'))
    g[('D', 'E')] = (('A', 'B'), (lambda a, b: (a + b, b)))
    res = g(1, 2, 3)
    assert res == (3, 2)



def test_singleoutput():
    g = TransformGraph(inputs=['A', 'B', 'C'], outputs='D')
    g[('D', 'E')] = (('A', 'B'), (lambda a, b: (a + b, b)))
    res = g(1, 2, 3)
    assert res == 3