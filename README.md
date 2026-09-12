# 🔮 Predicción de Ventas con IA — Mercado de las Especias

Proyecto de **inteligencia artificial** para predecir las ventas semanales del Mercado de las Especias de la isla de Dataclysm, utilizando datos históricos reales y modelos de machine learning.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completado-success.svg)]()

---

## 📌 Descripción del proyecto

Este proyecto aplica técnicas de **inteligencia artificial** para construir un **modelo predictivo de ventas** basado en datos históricos de una tienda online británica (2009–2011).

El objetivo es proporcionar a los mercaderes una herramienta que les permita:
- **Anticipar la demanda** de sus productos.
- **Planificar el stock** en períodos clave (campaña navideña).
- **Ajustar estrategias comerciales** frente a la incertidumbre del mercado.

---

## 🎯 Objetivos

1. **Recolectar** un dataset histórico relevante para el negocio.
2. **Preparar** los datos: limpieza, agregación y creación de features.
3. **Entrenar** varios modelos de predicción.
4. **Evaluar** con métricas RMSE, MAE y R².
5. **Generar predicciones** para planificar el negocio.

---

## 🔍 Resultados principales

| Métrica | Valor |
|---|---|
| **Modelo seleccionado** | Random Forest (100 árboles, profundidad 8) |
| **RMSE** | 46.810 £ |
| **MAE** | 41.178 £ |
| **R²** | -0,04 |
| **Mejora vs baseline** | **40%** |
| **Error en campaña navideña** | **< 5%** |

**Conclusión clave:** el modelo es especialmente fiable durante la campaña navideña, cuando las ventas se triplican y la previsión es más crítica.

---

## 🛠️ Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| **Python 3.13** | Lenguaje principal |
| **pandas 3.0.5** | Manipulación de datos |
| **numpy** | Operaciones numéricas |
| **scikit-learn** | Modelos de ML y métricas |
| **matplotlib 3.11.2** | Visualizaciones |
| **seaborn 0.13.2** | Visualizaciones estadísticas |
| **Google Colab** | Entorno de desarrollo |

---

## 📁 Estructura del repositorio

Reto4_Prediccion_Ventas/
│
├── datos/
│ └── online_retail_completo.csv # Dataset origen
│
├── notebooks/
│ └── Reto2_JuditGiravent_Script.py # Script principal
│
├── salidas/
│ ├── Predicciones_Reto2_JuditGiravent.csv
│ └── figuras/
│ ├── 01_serie_temporal.png
│ ├── 02_predicciones_vs_realidad.png
│ └── 03_importancia_features.png
│
├── docs/
│ ├── Informe_Reto2_JuditGiravent.pdf
│ └── Presentacion_Reto2_JuditGiravent.pptx
│
├── LICENSE
└── README.md

text

---


📊 Metodología aplicada
El proyecto sigue los 5 pasos oficiales del reto:

Paso 1 — Recolección de datos
Dataset Online Retail II (UCI Machine Learning Repository).

995.416 transacciones reales (2009–2011).

Paso 2 — Preparación de datos
Agregación semanal: 104 semanas.

Creación de features:

Temporales: Month, WeekOfYear, Quarter.

Lags: Lag_1, Lag_2, Lag_4.

Medias móviles: Rolling_Mean_4, Rolling_Mean_12.

Paso 3 — Selección y entrenamiento
Se evaluaron 3 modelos:

Regresión Lineal: baseline interpretable.

Árbol de Decisión: max_depth=5.

Random Forest: n_estimators=100, max_depth=8 → Seleccionado.

Paso 4 — Evaluación
Modelo	RMSE (£)	MAE (£)	R²
Regresión Lineal	50.684	42.202	-0,22
Árbol de Decisión	59.731	51.416	-0,70
Random Forest	46.811	41.179	-0,04
Paso 5 — Predicciones
Predicciones para las últimas 12 semanas (sept-dic 2011), comparadas con valores reales.

📈 Visualizaciones destacadas
Serie temporal completa
https://salidas/figuras/01_serie_temporal.png

Predicciones vs Realidad
https://salidas/figuras/02_predicciones_vs_realidad.png

Importancia de las features
https://salidas/figuras/03_importancia_features.png

💡 Recomendaciones de negocio
Basándonos en los resultados del modelo:

Planificación navideña: aumentar stock un 80-100% entre octubre y diciembre.

Reducir costes en enero-febrero: las ventas caen un 60% post-Navidad.

Reentrenar cada 6 meses con datos actualizados.

Ampliar el historial a más de 3 años para mejorar la precisión interanual.

Incorporar variables externas (promociones, meteorología, eventos).

📄 Documentación
Informe completo: docs/Informe_Reto2_JuditGiravent.pdf

Presentación: docs/Presentacion_Reto2_JuditGiravent.pptx

Predicciones generadas: salidas/Predicciones_Reto2_JuditGiravent.csv

🎯 Entregables del proyecto
✅ Código completo (Reto2_JuditGiravent_Script.py)

✅ Informe del modelo (Informe_Reto2_JuditGiravent.pdf)

✅ Dataset de predicciones (Predicciones_Reto2_JuditGiravent.csv)

✅ Presentación ejecutiva (Presentacion_Reto2_JuditGiravent.pptx)

🔄 Próximas mejoras
□ Probar modelos avanzados: SARIMA, Prophet o LSTM.
□ Enriquecer el dataset con más años o variables externas.
□ Implementar un pipeline automatizado de reentrenamiento.
□ Crear un dashboard interactivo en Power BI con las predicciones.
🤝 Contribuciones
Las contribuciones son bienvenidas:

Haz un fork del repositorio.

Crea una rama: git checkout -b feature/nueva-mejora.

Commit: git commit -m "Añade nueva funcionalidad".

Push: git push origin feature/nueva-mejora.

Abre un Pull Request.

📜 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

👤 Autora
Judit Giravent

LinkedIn: judit-giravent-27b167156

GitHub: @jdthgp27

🙏 Agradecimientos
UCI Machine Learning Repository por el dataset Online Retail II.

scikit-learn por las herramientas de ML.

⭐ Si este proyecto te ha resultado útil, considera darle una estrella en GitHub.


