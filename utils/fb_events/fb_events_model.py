from pycaret.classification import * 
import pandas as pd
from utils import paths

def predict_noise(month, day, hour, temperature, distance, attendance, rain_density, rain_amount):
    
    model_50 = load_model(paths.path_fb_model_50)
    model_25 = load_model(paths.path_fb_model_25)
    model_01 = load_model(paths.path_fb_model_01)
    model_005 = load_model(paths.path_fb_model_005)

    test = pd.DataFrame([
        {"day_of_week": day, 
         "Hour": hour, 
         'month': month, 
         'Event.location': 5, 
         'Distance': distance, 
         'attendance':attendance, 
         'LC_RAININ': rain_density, 
         'LC_TEMP_QCL3': temperature, 
         'LC_DAILYRAIN': rain_amount},
    ]).astype({
        "day_of_week": "category",
        "Hour": "category",
        "month": "category",
    })

    result_50 = predict_model(model_50, data = test)
    result_25 = predict_model(model_25, data = test)
    result_01 = predict_model(model_01, data = test)
    result_005 = predict_model(model_005, data = test)

    results = [result_50.prediction_label[0], result_25.prediction_label[0], result_01.prediction_label[0], result_005.prediction_label[0]]

    return results