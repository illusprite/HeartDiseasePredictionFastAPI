class RecomendationsProcessor:
    def __init__(self):
        pass

    def conclusion(self, features, probability) -> list:
        risk_factors = self.risk_factor(**features)
        if probability > 0.5:
            conclusion = [
                "Пожалуйста пройдите медицинское обследование! Так же обратите внимание на нижеперечисленные факторы риска сердечно-сосудистых заболеваний:"
            ]
            conclusion += risk_factors
        else:
            if risk_factors:
                conclusion = [
                    "Всё хорошо! Риск наличия сердечно-сосудистых заболеваний невысокий! Однако обратите внимание на следующие аспекты:"
                ]
                conclusion += risk_factors
            else:
                conclusion = [
                    "Всё хорошо! Риск наличия сердечно-сосудистых заболеваний невысокий!"
                ]

        return conclusion

    # функция, возвращающая факторы риска ССЗ
    @staticmethod
    def risk_factor(**kwargs):
        factors = []
        if kwargs['cholesterol'] > 1:
            factors += ["Высокий уровень холестерина!"]
        if kwargs['ap_hi'] > 130:
            factors += ["Повышенное систалическое давление!"]
        if kwargs['ap_lo'] > 90:
            factors += ["Повышенное диастолическое давление!"]
        if kwargs['mass_idx'] > 30:
            factors += ["Избыточная масса тела!"]
        if kwargs['gluc'] > 2:
            factors += ["Уровень глюкозы высок!"]
        if kwargs['active'] == 0:
            factors += ["Вы ведете физически малоактивный образ жизни!"]
        return factors
