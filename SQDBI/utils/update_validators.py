from cassiopeia import Patch
from pygsheets import Worksheet
from typing import Optional

def update_validator_patches(sh: Worksheet, latest_patch: Optional[Patch], region: Optional[str] = 'NA') -> None:
    if latest_patch is None:
        latest_patch = Patch.latest(region)
    patch = [f"{latest_patch.major}.{int(latest_patch.minor) - i}" for i in range(3)]
    sh.worksheet('title', 'validators').update_values('C2', list(map(list, zip(patch))))