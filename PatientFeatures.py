from pydantic import BaseModel


class PatientFeatures(BaseModel):
    gender: int
    age: int
    age_category: int
    mass_idx: float
    mass_idx_category: int
    pulse_pressure: int
    ag_st: int
    avrg_ap: float
    cholesterol: int
    gluc: int
    smoke: int
    alco: int
    active: int
    age_bmi: float
