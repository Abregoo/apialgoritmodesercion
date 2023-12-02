from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import gdown
import copy
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import openpyxl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.config["CORS_ALLOWED_ORIGINS"] = "*"
app.config["CORS_ALLOW_METHODS"] = ["GET","POST", "PUT", "DELETE"]
app.config["CORS_HEADERS"] = ["Content-Type"]
#, "POST", "PUT", "DELETE"

@app.route("/")
def Home():
    return "Hola mundo"

def traininData():
    #Descarga de data a amnbiente local
    idArchivo = '1dH4FCim7UpnKv3q1AhVQcw3O3tyH8_cE'
    urlArchivo = f"https://drive.google.com/uc?id={idArchivo}"
    output_data = 'DataSetTraining.xlsx'

    gdown.download(urlArchivo, output_data, quiet=False)
    
    dataset = pd.read_excel(output_data)
    #jsondata = dataset.to_json(orient='split')
    data = copy.deepcopy(dataset.iloc[:, :-2])
    
    # SEPARACION DE VARIABLES DEPENDIENTES E INDEPENDIENTES:
    X = data.iloc[:,1:].values
    y = dataset.iloc[:,-1].values
    
    
    X_Train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    
    regressor = LinearRegression()
    regressor.fit(X_Train, y_train)
    
    y_predict = regressor.predict(X_test)

    np.set_printoptions(precision=2)
    
    return regressor
    
@app.route("/predict/", methods=["POST"])
def deserializar_parametro():
    try:
        json_data = request.get_json()
        
        # Verifica si el campo 'idDependenciaEconomica' está presente en la solicitud
        if 'idDependenciaEconomica' not in json_data:
            return jsonify({"error": "Campo 'idDependenciaEconomica' faltante en la solicitud"}, 400)
        
        values_list = list(json_data.values())
        
        regressor = LinearRegression()
    
        regressor = traininData()
        
        ndarray = np.array(values_list)
      
    
        prediction = regressor.predict([ndarray])

        if float(prediction[0]) > 1:
            prediction = 1

        print(float(prediction[0]))
        
    
        acurracy = {
            "probability": str(prediction[0])
        }

        print(acurracy)
        

        return jsonify(acurracy)
    except Exception as e:
        return jsonify({"error": "Ocurrió un error al deserializar los datos"}, 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
    
    


    