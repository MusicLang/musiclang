class FakeModel:

    def predict(self, start="Time Signature: 4/4\nm0", bar_number_start=0, seed=None, **config):
        text = """Time Signature: 4/4
                m0 C: I b3 V7
                m1 IV b3 V7
                m2 I
        """

        text = '\n'.join([c.lstrip() for c in text.split('\n')])
        return text


model = FakeModel()

from musiclang import Score
from musiclang.predict import AutoComposer

expected_annotation = """Time Signature: 4/4
mx C: I b3 V7
mx IV b3 V7
mx C: I b3 V7
mx IV b3 V7
mx I
mx C: I b3 V7"""

expected_text = """
(I % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(V['7'] % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(IV % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(V['7'] % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(I % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(V['7'] % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(IV % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(V['7'] % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(I % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w)+
(I % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(V['7'] % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)
"""
def test_auto_composer():
    orch4 = """
    """

    orchestras = [orch4]
    parts = [2, 4]
    tonalities = ['d', 'a']
    form = [0, 1]
    form_orchestra = [0, 0]
    signature = (4, 4)
    ###################

    composer = AutoComposer(model, parts, tonalities, form, form_orchestra, orchestras, signature=signature, continuation=False)
    score, annotation = composer.compose()
    expected_score = Score.from_str(expected_text)
    assert annotation == expected_annotation
    assert score == expected_score
