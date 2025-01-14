from cassiopeia import Patch
from gspread import Worksheet


def update_validator_patches(
    sh: Worksheet, latest_patch: Patch | None, region: str | None = "NA"
) -> None:
    if latest_patch is None:
        latest_patch = Patch.latest(region)
    patch = [f"{latest_patch.major}.{int(latest_patch.minor) - i}" for i in range(3)]
    sh.worksheet("validators").update("C2", list(map(list, zip(patch))))
