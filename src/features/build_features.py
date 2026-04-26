import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DataTransformation import LowPassFilter, PrincipalComponentAnalysis
from TemporalAbstraction import NumericalAbstraction
from sklearn.preprocessing import StandardScaler

# Scale data before PCA





# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle("../../data/interim/02_data_outliers_removed.pkl")
predictor_columns = list(df.columns[:6])
df.info()

plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (20, 5)
plt.rcParams["figure.dpi"] = 100 
plt.rcParams["lines.linewidth"] = 2   
# --------------------------------------------------------------
# Dealing with missing values (imputation)
# --------------------------------------------------------------
for col in predictor_columns:
    df[col] = df[col].interpolate()
    
df.info()

# --------------------------------------------------------------
# Calculating set duration
# --------------------------------------------------------------
df[df["set"]==25]["acc_y"].plot()
df[df["set"]==50]["acc_y"].plot()

duration = df[df["set"]==1].index[-1] - df[df["set"]==1].index[0]
duration.seconds

for s in df["set"].unique():
    duration = df[df["set"]==s].index[-1] - df[df["set"]==s].index[0]
    df.loc[df["set"]==s, "duration"] = duration.seconds
    
duration_df = df.groupby(["category"])["duration"].mean()

duration_df.iloc[0]/ 5
duration_df.iloc[1]/ 10
    
# --------------------------------------------------------------
# Butterworth lowpass filter
# --------------------------------------------------------------
df_lowpass = df.copy()
Lowpass = LowPassFilter()
samplig_frequency = 1000/200
cutoff_frequency = 1.2

df_lowpass = Lowpass.low_pass_filter(df_lowpass, "acc_y", sampling_frequency=samplig_frequency, cutoff_frequency=cutoff_frequency, order=5)

subset = df_lowpass[df_lowpass["set"]==45]
print(subset["label"].iloc[0])

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
ax [0].plot (subset ["acc_y"].reset_index(drop=True), label="raw data")
ax [1].plot (subset ["acc_y_lowpass"].reset_index(drop=True), label="butterworth filter")
ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)

for col in predictor_columns:
    df_lowpass = Lowpass.low_pass_filter(df_lowpass, col, samplig_frequency,cutoff_frequency,order=5)
    df_lowpass[col]= df_lowpass[col + "_lowpass"]
    del df_lowpass[col + "_lowpass"]

# --------------------------------------------------------------
# Principal component analysis PCA
# --------------------------------------------------------------
df_pca = df_lowpass.copy()


PCA = PrincipalComponentAnalysis()
pca_values = PCA.determine_pc_explained_variance(df_pca, predictor_columns)

plt.figure(figsize=(10, 10))
plt.plot(range(1, len(predictor_columns) + 1), pca_values)
plt.xlabel("number of principal components")
plt.ylabel("explained variance")
plt.title("Explained variance by number of principal components")
plt.show()

df_pca = PCA.apply_pca(df_pca, predictor_columns,3)
# After applying PCA
df_pca["pca_1"] = df_pca["pca_1"] * -1
df_pca["pca_2"] = df_pca["pca_2"] * -1
df_pca["pca_3"] = df_pca["pca_3"] * -1

subsets = df_pca[df_pca["set"] == 35]
subsets[["pca_1", "pca_2", "pca_3"]].plot()

# --------------------------------------------------------------
# Sum of squares attributes
# --------------------------------------------------------------
df_squred = df_pca.copy()
acc_r = df_squred["acc_x"]**2 + df_squred["acc_y"]**2 + df_squred["acc_z"]**2
gyro_r = df_squred["gyro_x"]**2 + df_squred["gyro_y"]**2 + df_squred["gyro_z"]**2
df_squred["acc_r"] = np.sqrt(acc_r)
df_squred["gyro_r"] = np.sqrt(gyro_r)

df_squred[df_squred["set"]==14][["acc_r","gyro_r"]].plot(subplots=True, )


# --------------------------------------------------------------
# Temporal abstraction
# --------------------------------------------------------------


# --------------------------------------------------------------
# Frequency features
# --------------------------------------------------------------


# --------------------------------------------------------------
# Dealing with overlapping windows
# --------------------------------------------------------------


# --------------------------------------------------------------
# Clustering
# --------------------------------------------------------------


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------