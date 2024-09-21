# /api/app.py
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Ruta de ejemplo para obtener la lista de asistencia desde un archivo Excel
@app.route('/attendance', methods=['GET'])
def get_attendance():
    # Leer el archivo Excel desde la carpeta /data
    df = pd.read_excel('data/asistencia_semanal_G11-P1.xlsx')
    # Convertir los datos del archivo Excel en una lista de diccionarios
    attendance_data = df.to_dict(orient='records')
    return jsonify(attendance_data)

if __name__ == "__main__":
    app.run(debug=True)
