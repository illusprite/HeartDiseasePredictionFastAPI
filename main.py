from fastapi import FastAPI
import joblib

from RecommendationsProcessor import RecomendationsProcessor
from PatientInput import PatientInput
from PredictionResponse import PredictionResponse
from PatientDataProcessor import PatientDataProcessor

#uvicorn main:app --reload
# Загружаем обученную модель
model = joblib.load(r"./model_prediction1.pcl")

# Создаём FastAPI-приложение
app = FastAPI()

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PatientInput):
    processor = PatientDataProcessor()
    features = processor.get_features(data)
    rec_processor = RecomendationsProcessor()

    features_dict = vars(features)
    features_list = list(features_dict.values())

    features_dict2 = features_dict.copy()
    features_dict2.update({
        'ap_hi': data.ap_hi,
        'ap_lo': data.ap_lo
    })

    prediction = model.predict([features_list])[0]
    probability = model.predict_proba([features_list])[0][1]
    conclusion = rec_processor.conclusion(features_dict2, probability)

    return PredictionResponse(prediction=int(prediction), probability=str(round(probability*100)) + '%', conclusion=conclusion)




# dannye = {
#   "age": 50,
#   "gender": 2,
#   "height": 168,
#   "weight": 62,
#   "ap_hi": 110,
#   "ap_lo": 80,
#   "cholesterol": 1,
#   "gluc": 1,
#   "smoke": 0,
#   "alco": 0,
#   "active": 1
# }

# Эндпоинт предсказания
# @app.post("/predict")
# def predict(data: PatientData):
#     input_data = np.array([[data.age, data.gender, data.mass_idx, data.avrg_ap,
#                             data.cholesterol, data.gluc, data.smoke,
#                             data.alco, data.active]])
#
#     prediction = model.predict(input_data)[0]
#     probability = model.predict_proba(input_data)[0].tolist()
#
#     return {
#         "prediction": int(prediction),
#         "probability": probability
#     }





# # функция подгостовки введенных данных для предсказания модели
# def preprocess():
#     global age, gend, height, weight, ap_hi, ap_lo, chol, gluc, smoke, alco, active
#     height_cm = height * 100
#     mass_idx = weight / (height**2)
#     years = age // 365
#     avrg_ap = np.round((2 * ap_lo + ap_hi) / 3, 1)
#     aphi_chol_gluc = (avrg_ap + years) * (chol + gluc)
#     ag_st = ag_step(ap_hi)
#     ssz_risk = years + avrg_ap + (aphi_chol_gluc // 10)
#     gender = (1 if gend == 'Female' else 2)
#     return [age, gender, height_cm, weight, ap_hi, ap_lo, chol, gluc, smoke, alco, active,
#             mass_idx, years, avrg_ap, aphi_chol_gluc, ag_st, ssz_risk]
#
# # функция, возвращающая факторы риска ССЗ
# def risk_factor(**kwargs):
#     factors = ''
#     if kwargs['chol'] > 1:
#         factors += 'Уровень холестерина высокий!\n\n'
#     if kwargs['ap_hi'] > 130:
#         factors += 'Повышенное систалическое давление!\n\n'
#     if kwargs['ap_lo'] > 90:
#         factors += 'Повышенное диастолическое давление!\n\n'
#     if (kwargs['weight'] // kwargs['height']**2) > 30:
#         factors += 'Избыточная масса тела!\n\n'
#     if kwargs['gluc'] > 2:
#         factors += 'Уровень глюкозы высок!\n\n'
#     if kwargs['active'] == 0:
#         factors += 'Вы ведете физически малоактивный образ жизни!\n\n'
#     return factors

# Интерфейс Streamlit

#st.write("Вы согласны с обработкой персональных данных")
#active = st.checkbox('Да', key='active')

# st.title("Прогнозирование риска сердечно-сосудистых заболеваний")
# st.subheader('Введите данныe:')
# age = st.selectbox('Ваш возраст, лет:', [*range(1, 120)], index=21, key='age')
# height = st.slider('Ваш рост, м', 0.5, 2.5, 1.75)
# weight = st.slider('Ваш вес, кг:', 40, 200, 80)
# # средняя колонка
# ap_hi = st.selectbox('Верхнее (систолическое) давление, мм рт.ст:',
#                        [*range(40, 271)], index=80, key='ap_hi')
# ap_lo = st.selectbox('Нижнее (диастолическое) давление, мм рт.ст:',
#                        [*range(20, 161)], index=60, key='ap_lo')
# chol = st.selectbox('Ваш уровень холестерина:', [1, 2, 3], key='cholesteerol')
# gluc = st.selectbox('Ваш уровень глюкозы', [1, 2, 3], key='glucose')
# # правая колонка
# st.write('Вы курите?')
# smoke = st.checkbox('Да', key='smoke')
# st.write('Вы употребляете алкоголь?')
# alco = st.checkbox('Да', key='alco')
# st.write('Вы ведёте физически активный образ жизни?')
# active = st.checkbox('Да', key='active')
# gend = st.radio('Ваш пол', ('Муж.', 'Жен.'), index=0, key='gender')
#
# # загружаем модель и
# # вызываем функцию подготовки данных перед отправкой в модель
# ###model = load()
# data = preprocess()
# predict = model.predict_proba(np.array(data).reshape((1,-1)))[:, 1]
# # вывод информации и результатов для пользователя
# st.text('Ваша вероятность наличия сердечно-сосудистых заболеваний:')
# st.write(int(predict * 100), '%')
# # вывод рекомендаций
# if predict > 0.5:
#     st.write('Пожалуйста пройдите медицинское обследование! Так же обратите внимание на нижеперечисленные факторы риска сердечно-сосудистых заболеваний:')
#     risk_f = risk_factor(chol=chol, ap_hi=ap_hi, ap_lo=ap_lo, height=height, weight=weight, gluc=gluc, active=active)
#     st.write(risk_f)
# else:
#     st.write('Всё хорошо! Риск наличия сердечно-сосудистых заболеваний не высок!')