EXPECTED_RESULT_BASE = [
    [
        "file",
        "ply",
        "cell",
        "ee",
        "area",
        "perimeter",
        "compactness",
        "num_holes",
        "holes_perimeter",
        "holes_area",
        "material",
        "ply_phi",
        "valid",
        "reason",
        "zone",
        "weight",
        "ee_x",
        "ee_y",
        "ee_phi",
        "num_cups",
        "active_cups",
    ],
    [
        "report1.dxf",
        "TestPly1",
        "TestCell1",
        "TestEE1",
        90441.02883364339,
        1758.8307976017325,
        36.73899186484136,
        0,
        0,
        0,
        "TestMat1",
        2.5,
        True,
        "Success",
        4,
        0.4,
        2.0,
        3.0,
        0.0,
        3,
        "a*b*d",
    ],
    [
        "report1.dxf",
        "TestPly2",
        "TestCell1",
        "TestEE1",
        90441.02883364339,
        1758.8307976017325,
        36.73899186484136,
        0,
        0,
        0,
        "TestMat2",
        3.0,
        False,
        "Failure - Sagging",
        4,
        0.2,
        0.0,
        0.0,
        45.0,
        3,
        "a*b*e",
    ],
    [
        "report1.dxf",
        "TestPly3",
        "TestCell1",
        "TestEE1",
        90441.02883364339,
        1758.8307976017325,
        36.73899186484136,
        0,
        0,
        0,
        "TestMat1",
        3.5,
        False,
        "Failure - Unable to pick",
        4,
        0.7,
        20.0,
        30.0,
        0.0,
        3,
        "a*b*d",
    ],
    [
        "report2.dxf",
        "TestPly4",
        "TestCell1",
        "TestEE1",
        55165.049671121145,
        1152.8281000268635,
        52.16086321615416,
        0,
        0,
        0,
        "TestMat2",
        0.0,
        True,
        "Success",
        6,
        0.1,
        42.0,
        43.0,
        -45.0,
        3,
        "a*b*d",
    ],
    [
        "report2.dxf",
        "TestPly5",
        "TestCell1",
        "TestEE1",
        55165.049671121145,
        1152.8281000268635,
        52.16086321615416,
        0,
        0,
        0,
        "TestMat1",
        45.0,
        False,
        "Failure - Sagging",
        6,
        0.25,
        0.0,
        0.0,
        90.0,
        3,
        "a*c*g",
    ],
]

EXPECTED_RESULT_ATTENTION_PLIES = data = [
    ["file", "ply", "cell", "ee", "success_rate"],
    ["report2.dxf", "TestPly4", "TestCell1", "TestEE1", 50],
    ["report1.dxf", "TestPly1", "TestCell1", "TestEE1", 33],
]

EXPECTED_RESULT_UNPROCESSED_PLIES = [["filename"], ["report2.dxf"]]
