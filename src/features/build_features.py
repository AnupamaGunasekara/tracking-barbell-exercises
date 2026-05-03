import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DataTransformation import LowPassFilter, PrincipalComponentAnalysis
from TemporalAbstraction import NumericalAbstraction
from sklearn.preprocessing import StandardScaler
from FrequencyAbstraction import FourierTransformation
from sklearn.cluster import KMeans

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
df_temporal = df_squred.copy()
NumericalAbstraction = NumericalAbstraction()
predictor_columns = predictor_columns + ["acc_r", "gyro_r"]
ws = int(1000/200)

df_temporol_list = []
for s in df_temporal["set"].unique():
    subset = df_temporal[df_temporal["set"]==s].copy()
    for col in predictor_columns:
        subset = NumericalAbstraction.abstract_numerical(subset, [col], ws,"mean")
        subset = NumericalAbstraction.abstract_numerical(subset, [col], ws,"std")
    df_temporol_list.append(subset)  # Moved outside the col loop
        
df_temporal = pd.concat(df_temporol_list)

subset[["acc_y","acc_y_temp_mean_ws_5","acc_y_temp_std_ws_5"]].plot()
subset[["gyro_y","gyro_y_temp_mean_ws_5","gyro_y_temp_std_ws_5"]].plot()
    

# --------------------------------------------------------------
# Frequency features
# --------------------------------------------------------------
df_frequency = df_temporal.copy().reset_index()
FreqAbs = FourierTransformation()

fs = int(1000/200)
ws = int(2800/200)

df_frequency = FreqAbs.abstract_frequency(df_frequency, ["acc_y"], ws,fs)

subset = df_frequency[df_frequency["set"]==15]
subset[["acc_y"]].plot()

df_frequency_list = []
for s in df_frequency["set"].unique():
    print(f"Applying frequency abstraction to set {s}")
    subset = df_frequency[df_frequency["set"]==s].reset_index(drop=True).copy()
    subset = FreqAbs.abstract_frequency(subset,predictor_columns, ws, fs)
    df_frequency_list.append(subset)
    
df_frequency = pd.concat(df_frequency_list).set_index("epoch (ms)", drop=True)
# --------------------------------------------------------------
# Dealing with overlapping windows
# --------------------------------------------------------------
df_frequency =df_frequency.dropna()
df_frequency = df_frequency.iloc[::2]

# --------------------------------------------------------------
# Clustering
# --------------------------------------------------------------
df_cluster = df_frequency.copy()
cluster_columns = ["acc_x", "acc_y", "acc_z"]
k_values = range(2, 10)
inertias = []
for k in k_values:
    subset = df_cluster[cluster_columns]
    kmeans = KMeans(n_clusters=k,n_init=20, random_state=0)
    cluster_labels = kmeans.fit_predict(subset)
    inertias.append(kmeans.inertia_)
    
plt.figure(figsize=(10, 10))
plt.plot(k_values, inertias)
plt.xlabel("number of clusters")
plt.ylabel("sum of squared distances")
plt.title("Elbow method for determining optimal number of clusters")
plt.show()

kmeans = KMeans(n_clusters=5, n_init=20, random_state=0)
subset = df_cluster[cluster_columns]
df_cluster["cluster"] = kmeans.fit_predict(subset)

#plotting clusters  
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(projection='3d')
for c in df_cluster["cluster"].unique():
    cluster_data = df_cluster[df_cluster["cluster"] == c]
    ax.scatter(cluster_data["acc_x"], cluster_data["acc_y"], cluster_data["acc_z"], label=f"Cluster {c}")
ax.set_xlabel("acc_x")
ax.set_ylabel("acc_y")
ax.set_zlabel("acc_z")
ax.set_title("3D Scatter Plot of Clusters")
ax.legend()
plt.show()

#plotting clusters with labels
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(projection='3d')
for l in df_cluster["label"].unique():
    subset = df_cluster[df_cluster["label"] == l] 
    ax.scatter(subset["acc_x"], subset["acc_y"], subset["acc_z"], label=f"Label {l}")
ax.set_xlabel("acc_x")
ax.set_ylabel("acc_y")
ax.set_zlabel("acc_z")
ax.set_title("3D Scatter Plot of Clusters with Labels")
ax.legend()
plt.show()  


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
df_cluster.to_pickle("../../data/interim/03_data_features.pkl")