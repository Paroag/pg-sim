def set_to_tuple(s):
    return tuple(sorted(list(s)))


if __name__ == "__main__":
    assert set_to_tuple({"Water", "Grass"}) == ("Grass", "Water")
