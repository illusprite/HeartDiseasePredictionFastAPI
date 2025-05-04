import numpy as np
from pydantic import BaseModel

from PatientInput import PatientInput
from PatientFeatures import PatientFeatures


class PatientDataProcessor:
    def __init__(self):
        pass

    # Деление возраста на категории
    def age_category(self, age) -> int:
        if age <= 35:
            return 0
        elif age <= 40:
            return 1
        elif age <= 45:
            return 2
        elif age <= 50:
            return 3
        elif age <= 55:
            return 4
        elif age <= 60:
            return 5
        else:
            return 6

    # Расчёт индекса массы тела
    def mass_idx(self, weight, height) -> float:
        mass_idx = weight / (height / 100) ** 2
        return mass_idx

    # Деление индекса масы тела на категории
    def mass_idx_category(self, mass_idx) -> int:
        if mass_idx < 16:
            return 0
        elif mass_idx < 18.5:
            return 1
        elif mass_idx < 25:
            return 2
        elif mass_idx < 30:
            return 3
        elif mass_idx < 35:
            return 4
        else:
            return 5

    # Расчёт пульсового давления
    def pulse_pressure(self, ap_hi, ap_lo) -> int:
        pulse_pressure = ap_hi - ap_lo
        return pulse_pressure

    # Расчёт среднего артериального давления
    def avrg_ap(self, ap_hi, ap_lo) -> float:
        avrg_ap = np.round((2 * ap_lo + ap_hi) / 3, 1)
        return avrg_ap

    # Расчёт доп показателя возраст на индекс массы тела
    def age_bmi(self, age, mass_idx) -> float:
        age_bmi = age * mass_idx
        return age_bmi

    # функция, определяющая степень артериальной гиепртензии по систалическому давлению
    def ag_st(self, ap_hi) -> int:
        if ap_hi < 140:
            return 0
        elif 140 <= ap_hi < 160:
            return 1
        elif 160 <= ap_hi < 180:
            return 2
        elif ap_hi >= 180:
            return 3
        else:
            return 4

    def get_features(self, data: PatientInput) -> PatientFeatures:
        gender = data.gender
        age = data.age
        age_category = self.age_category(age)
        mass_idx = self.mass_idx(data.weight, data.height)
        mass_idx_category = self.mass_idx_category(self.mass_idx(data.weight, data.height))
        pulse_pressure = self.pulse_pressure(data.ap_hi, data.ap_lo)
        ag_st = self.ag_st(data.ap_hi)
        avrg_ap = self.avrg_ap(data.ap_hi, data.ap_lo)
        cholesterol = data.cholesterol
        gluc = data.gluc
        smoke = data.smoke
        alco = data.alco
        active = data.active
        age_bmi = self.age_bmi(age, mass_idx)

        patient_features = PatientFeatures(
            gender=gender,
            age=age,
            age_category=age_category,
            mass_idx=mass_idx,
            mass_idx_category=mass_idx_category,
            pulse_pressure=pulse_pressure,
            ag_st=ag_st,
            avrg_ap=avrg_ap,
            cholesterol=cholesterol,
            gluc=gluc,
            smoke=smoke,
            alco=alco,
            active=active,
            age_bmi=age_bmi
        )
        return patient_features
