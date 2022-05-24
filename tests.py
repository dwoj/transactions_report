from helpers import convert_to_pln, make_card_info


def test_make_card_info():
    assert make_card_info("John", "Doe", 1324568643212345) == "John Doe 1324********2345", "Should be: John Doe 1324********2345"

def test_convert_to_pln():
    assert convert_to_pln("GBP", 1000, "2021-05-14T18:32:26Z") == 5208, "Should be: 5208"

if __name__ == "__main__":
    test_make_card_info()
    # test_convert_to_pln()
    print("Everything passed")