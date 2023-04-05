#
# (c) 2023 Giorgio Gonnella
#
import os
import functools
from tempfile import TemporaryDirectory
import ec_finder

TEST_ENZYME_DAT = """\
ID   1.1.1.1
DE   Alcohol dehydrogenase.
AN   ADH.
AN   AHD2.
CA   An NAD+ oxidoreductase.
CF   Zinc.
CC   -!- A zinc protein. Animal and plant ADH's are classified in
CC       etc etc etc
//
ID   1.1.1.2
DE   D/L-glycerol-3-phsphate dehydrogenase.
AN   GLYCEROL-3-PHOSPHATE DEHYDROGENASE (ACCEPTOR).
AN   GLYCEROPHOSPHATE DEHYDROGENASE.
AN   GPDH.
CA   An NAD(P)+ oxidoreductase.
CC   -!- The enzyme is a complex of three polypeptides of which the
CC       etc etc etc
//
ID   1.1.1.3
DE   2-oxoacid:ferredoxin oxidoreductase.
AN   Oxidoreductase, 2-oxoacid:ferredoxin.
AN   2-ketoacid-ferredoxin oxidoreductase.
CA   An NAD(P)+ oxidoreductase.
CF   Iron-sulfur.
CC   -!- A group of enzymes, formerly listed under EC 1.2.7, catalysing
CC       etc etc etc
//
"""

def test_parse_enzyme_dat():
    with TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "enzyme.dat")
        with open(filename, "w") as f:
            f.write(TEST_ENZYME_DAT)
        index = ec_finder.ec_finder.parse_enzyme_dat(filename)
        assert len(index["main"]) == 3
        assert len(index["alt"]) == 7
        assert "Alcohol dehydrogenase" in index["main"]
        assert "1.1.1.2" in index["main"].values()
        assert "GLYCEROPHOSPHATE DEHYDROGENASE" in index["alt"]
        assert "1.1.1.2" in index["main"].values()

def test_search():
    with TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "enzyme.dat")
        with open(filename, "w") as f:
            f.write(TEST_ENZYME_DAT)
        index = ec_finder.ec_finder.parse_enzyme_dat(filename)
        search = functools.partial(ec_finder.ec_finder.search, index=index)
        # Test exact match with main name
        assert search("Alcohol dehydrogenase") == \
                      "MAIN\t1.1.1.1\tAlcohol dehydrogenase"
        # Test separator argument
        assert search("Alcohol dehydrogenase", separator=';') == \
                      "MAIN;1.1.1.1;Alcohol dehydrogenase"
        # Test exact match with alternative name
        assert search("GLYCEROPHOSPHATE DEHYDROGENASE") == \
                      "ALT\t1.1.1.2\tGLYCEROPHOSPHATE DEHYDROGENASE"
        # Test fuzzy match
        assert search("alcohol dehydrogenase") == \
            "FUZZY:Alcohol dehydrogenase\t1.1.1.1\talcohol dehydrogenase"
        # Test no match
        assert search("alcohol dehydro") == \
            "NOT_FOUND\t\talcohol dehydro"
        # Test min_score argument
        assert search("alcohol dehydro", min_score=20) == \
            "FUZZY:Alcohol dehydrogenase\t1.1.1.1\talcohol dehydro"

