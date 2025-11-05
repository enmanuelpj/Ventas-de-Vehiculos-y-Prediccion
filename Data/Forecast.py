import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_excel(
    r"C:\Users\fliap\OneDrive\Desktop\RK Power\Ventas_M.xlsx",
    sheet_name="Ventas",
    parse_dates=["FechaVenta"]
)

df['Año'] = df['FechaVenta'].dt.year
df['Mes'] = df['FechaVenta'].dt.month
df['Día'] = df['FechaVenta'].dt.day
df['DiaSemana'] = df['FechaVenta'].dt.dayofweek
df['Trimestre'] = df['FechaVenta'].dt.quarter

X = df[['Año', 'Mes', 'Día', 'DiaSemana', 'Trimestre',
        'CodigoMarca', 'ModeloAuto', 'ColorAuto', 'TipoAuto']].copy()
y = df['PrecioUSD']

X['FechaVentaOriginal'] = df['FechaVenta']

X_encoded = pd.get_dummies(X.drop(columns=['FechaVentaOriginal']), drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

fechas_test = X.loc[X_test.index, 'FechaVentaOriginal']
model = RandomForestRegressor(n_estimators=100, random_state=42) #Poniendo la cantidad de arboles, que serian 100
model.fit(X_train, y_train)

#Hubiera sido bueno entonces oslo ponderar los meses y no toda la data para el modelo

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

#print("MAE entrenamiento:", mean_absolute_error(y_train, y_train_pred))
#print("MAE prueba:", mean_absolute_error(y_test, y_test_pred))
#print("RMSE entrenamiento:", mean_squared_error(y_train, y_train_pred, squared=False))
#print("RMSE prueba:", mean_squared_error(y_test, y_test_pred, squared=False))

df_pred_test = X_test.copy()
df_pred_test['FechaVenta'] = fechas_test.values
df_pred_test['Forecast_VentasUSD'] = y_test_pred
df_pred_test.to_csv("forecast_test.csv", index=False)

ultima_fecha = df['FechaVenta'].max()
fechas_futuras = pd.date_range(start=ultima_fecha + pd.Timedelta(days=1),
                               end=f"{ultima_fecha.year}-12-31", freq='D')

#Se crea el dataset futuro
df_futuro = pd.DataFrame({'FechaVenta': fechas_futuras})

df_futuro['Año'] = df_futuro['FechaVenta'].dt.year
df_futuro['Mes'] = df_futuro['FechaVenta'].dt.month
df_futuro['Día'] = df_futuro['FechaVenta'].dt.day
df_futuro['DiaSemana'] = df_futuro['FechaVenta'].dt.dayofweek
df_futuro['Trimestre'] = df_futuro['FechaVenta'].dt.quarter

#Poner todas las combinaciones de los autos
combos = df[['CodigoMarca','ModeloAuto','ColorAuto','TipoAuto']].drop_duplicates()
df_futuro = df_futuro.merge(combos, how='cross')

df_futuro_encoded = pd.get_dummies(df_futuro.drop(columns=['FechaVenta']), drop_first=True)

for col in X_train.columns:
    if col not in df_futuro_encoded.columns:
        df_futuro_encoded[col] = 0
df_futuro_encoded = df_futuro_encoded[X_train.columns]

y_futuro_pred = model.predict(df_futuro_encoded)
df_futuro['Forecast_VentasUSD'] = y_futuro_pred

df_futuro.to_csv("forecast_futuro.csv", index=False)