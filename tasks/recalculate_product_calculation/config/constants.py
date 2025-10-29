from dataclasses import dataclass


ID_FOT = 1048
ID_FABRIC = 149
ID_ECONOMY = 1074

@dataclass(frozen=True)
class SPProductID:
    armchair: int = 165
    bed: int = 189
    chair: int = 150
    melochevka: int = 162
    msp: int = 172
    nightstand: int = 188
    pouf: int = 167
    sofa: int = 158
    table: int = 186


@dataclass(frozen=True)
class SPCalculationID:
    armchair: int = 191
    bed: int = 190
    chair: int = 171
    melochevka: int = 177
    msp: int = 145
    nightstand: int = 170
    pouf: int = 148
    sofa: int = 151
    table: int = 132
