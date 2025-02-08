from pydantic import BaseModel, ConfigDict, Field
from shapely.geometry import Polygon


class PlyShape(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    label: str | None = None
    parent_file: str | None = None
    geom: Polygon
    material_label: str | None = None
    bounding_box_axes: tuple[float, float]


class PickResult(BaseModel):
    cell_label: str | None = None
    end_effector_label: str | None = None
    plyshape: PlyShape
    plyshape_orientation: float = 0.0
    valid: bool = False
    reason: str = "Unknown error"
    end_effector_orientation: float = 0.0
    end_effector_translation_x: float = 0.0
    end_effector_translation_y: float = 0.0
    active_valves: list[str] = Field(default_factory=list)
    zone_index: int = 0
    weight: float = 0.0


class PlyResult(BaseModel):
    picks: list[PickResult] = Field(default_factory=list)
    success_rate: float = 0.0


class Report(BaseModel):
    picks: list[PickResult] = Field(default_factory=list)
    time_estimate: dict[str, float] = Field(default_factory=dict)
    tec_config_label: str | None = None
    ply_results: list[PlyResult] = Field(default_factory=list)
    failed_filenames: list[str] = Field(default_factory=list)
