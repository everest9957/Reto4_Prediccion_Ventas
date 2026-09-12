# ============================================================
# RETO 4 — Aplicación de IA para predicción de ventas
# Autor: Judit Giravent
# Fecha: 2026
# ============================================================
# Descripción:
# Modelo predictivo de ventas semanales para el Mercado de las
# Especias (isla de Dataclysm). Utiliza Random Forest con features
# temporales (lags, medias móviles y estacionalidad).
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (14, 6)


# ============================================================
# PASO 1: RECOLECCIÓN DE DATOS
# ============================================================

print("=" * 60)
print("PASO 1: RECOLECCIÓN DE DATOS")
print("=" * 60)

# Cargar dataset (Online Retail II ya limpio)
df = pd.read_csv('online_retail_completo.csv')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

print(f"Filas: {len(df):,}")
print(f"Rango temporal: {df['InvoiceDate'].min()} → {df['InvoiceDate'].max()}")


# ============================================================
# PASO 2: PREPARACIÓN DE DATOS
# ============================================================

print("\n" + "=" * 60)
print("PASO 2: PREPARACIÓN DE DATOS")
print("=" * 60)

# 2.1 Agregación semanal
df['YearWeek'] = df['InvoiceDate'].dt.to_period('W').astype(str)
ventas = df.groupby('YearWeek').agg({'TotalPrice': 'sum'}).reset_index()
ventas.columns = ['YearWeek', 'Ventas']
ventas['YearWeek_dt'] = pd.to_datetime(ventas['YearWeek'].str[:10])
ventas = ventas.sort_values('YearWeek_dt').reset_index(drop=True)

print(f"Semanas totales: {len(ventas)}")

# 2.2 Creación de features
ventas['Month'] = ventas['YearWeek_dt'].dt.month
ventas['WeekOfYear'] = ventas['YearWeek_dt'].dt.isocalendar().week.astype(int)
ventas['Quarter'] = ventas['YearWeek_dt'].dt.quarter

# Lags (valores pasados)
ventas['Lag_1'] = ventas['Ventas'].shift(1)
ventas['Lag_2'] = ventas['Ventas'].shift(2)
ventas['Lag_4'] = ventas['Ventas'].shift(4)

# Medias móviles
ventas['Rolling_Mean_4'] = ventas['Ventas'].rolling(window=4).mean()
ventas['Rolling_Mean_12'] = ventas['Ventas'].rolling(window=12).mean()

# Limpiar NaN
ventas = ventas.dropna().reset_index(drop=True)
print(f"Semanas útiles tras features: {len(ventas)}")


# ============================================================
# PASO 3: SELECCIÓN Y ENTRENAMIENTO DEL MODELO
# ============================================================

print("\n" + "=" * 60)
print("PASO 3: SELECCIÓN Y ENTRENAMIENTO")
print("=" * 60)

# 3.1 Features y target
features = ['Lag_1', 'Lag_2', 'Lag_4', 'Rolling_Mean_4', 'Rolling_Mean_12',
            'Month', 'WeekOfYear', 'Quarter']
X = ventas[features]
y = ventas['Ventas']

# 3.2 Split temporal (últimas 12 semanas como test)
n_test = 12
X_train, X_test = X.iloc[:-n_test], X.iloc[-n_test:]
y_train, y_test = y.iloc[:-n_test], y.iloc[-n_test:]

print(f"Train: {len(X_train)} semanas | Test: {len(X_test)} semanas")

# 3.3 Entrenar 3 modelos para comparar
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

modelos = {
    'Regresión Lineal': LinearRegression(),
    'Árbol de Decisión': DecisionTreeRegressor(max_depth=5, random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
}

resultados = []
predicciones = {}

for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    resultados.append({
        'Modelo': nombre, 'RMSE': round(rmse, 2),
        'MAE': round(mae, 2), 'R2': round(r2, 4)
    })
    predicciones[nombre] = y_pred

df_resultados = pd.DataFrame(resultados).set_index('Modelo')
print("\n=== COMPARATIVA DE MODELOS ===")
print(df_resultados.to_string())


# ============================================================
# PASO 4: EVALUACIÓN DEL MODELO
# ============================================================

print("\n" + "=" * 60)
print("PASO 4: EVALUACIÓN DEL MODELO FINAL")
print("=" * 60)

# Modelo seleccionado: Random Forest (mejor RMSE y MAE)
modelo_final = modelos['Random Forest']
y_pred_final = predicciones['Random Forest']

rmse_final = np.sqrt(mean_squared_error(y_test, y_pred_final))
mae_final = mean_absolute_error(y_test, y_pred_final)
r2_final = r2_score(y_test, y_pred_final)

print(f"\nMétricas del modelo Random Forest:")
print(f"  RMSE: {rmse_final:,.2f} £")
print(f"  MAE:  {mae_final:,.2f} £")
print(f"  R²:   {r2_final:.4f}")

# Comparar con baselines
media_train = y_train.mean()
pred_media = np.full(n_test, media_train)
rmse_media = np.sqrt(mean_squared_error(y_test, pred_media))

print(f"\nBaseline (media histórica) RMSE: {rmse_media:,.2f} £")
print(f"Mejora del modelo: {(1 - rmse_final/rmse_media) * 100:.1f}%")


# ============================================================
# PASO 5: REALIZACIÓN DE PREDICCIONES
# ============================================================

print("\n" + "=" * 60)
print("PASO 5: GENERACIÓN DE PREDICCIONES")
print("=" * 60)

fechas_test = ventas['YearWeek_dt'].iloc[-n_test:].values

predicciones_df = pd.DataFrame({
    'Fecha': fechas_test,
    'Real': y_test.values,
    'Prediccion': y_pred_final.round(2),
    'Error': (y_test.values - y_pred_final).round(2),
    'Error_Absoluto': np.abs(y_test.values - y_pred_final).round(2),
    'Error_%': (np.abs(y_test.values - y_pred_final) / y_test.values * 100).round(2)
})

print(predicciones_df.to_string(index=False))

# Guardar entregable
predicciones_df.to_csv('Predicciones_Reto2_JuditGiravent.csv', index=False)
print("\n✅ Guardado: Predicciones_Reto2_JuditGiravent.csv")


# ============================================================
# VISUALIZACIONES
# ============================================================

# 1. Serie temporal completa
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(ventas['YearWeek_dt'], ventas['Ventas'], marker='o',
        linewidth=1.5, markersize=4, color='steelblue')
ax.set_title('Ventas semanales (2010–2011)', fontsize=14)
ax.set_xlabel('Semana')
ax.set_ylabel('Ventas (£)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('01_serie_temporal.png', dpi=100, bbox_inches='tight')
plt.close()

# 2. Predicciones vs Realidad
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(fechas_test, y_test.values, marker='o', color='darkgreen',
        label='Real', linewidth=2)
ax.plot(fechas_test, y_pred_final, marker='x', color='red',
        label='Predicción', linestyle='--', linewidth=2)
ax.set_title('Predicciones vs Realidad — Random Forest', fontsize=14)
ax.set_xlabel('Semana')
ax.set_ylabel('Ventas (£)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('02_predicciones_vs_realidad.png', dpi=100, bbox_inches='tight')
plt.close()

# 3. Importancia de features
importancias = pd.DataFrame({
    'Feature': features,
    'Importancia': modelo_final.feature_importances_
}).sort_values('Importancia', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(importancias['Feature'], importancias['Importancia'], color='seagreen')
ax.set_title('Importancia de las features (Random Forest)')
ax.set_xlabel('Importancia relativa')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('03_importancia_features.png', dpi=100, bbox_inches='tight')
plt.close()

print("\n✅ Todas las visualizaciones guardadas")
print("\n" + "=" * 60)
print("RETO COMPLETADO")
print("=" * 60)