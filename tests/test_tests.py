@given(st.integers(), st.integers())
def test_ints_are_commutative(x, y):
    assert x + y == y + x
