import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_df = df[df["set"] == 1]
plt.plot(set_df["acc_y"])

plt.plot(set_df["acc_y"].reset_index(drop=True))

# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
for lable in df["label"].unique():
    subset = df[df["label"] == lable]
    plt.plot(subset["acc_y"].reset_index(drop=True), label=lable)
    plt.legend()
    plt.show()
    
for lable in df["label"].unique():
    subset = df[df["label"] == lable]
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=lable)
    plt.legend()
    plt.show()

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20, 5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
category_df = df.query("label =='squat'").query("participant == 'A'").reset_index()
fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set_title("Comparison of medium vs. heavy squat sets")
ax.set_xlabel("samples")
ax.set_ylabel("acc_y")
plt.legend()

# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------
participant_df = df.query("label =='bench'").sort_values("participant").reset_index()
fig, ax = plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot()
ax.set_title("Comparison of bench sets across participants")
ax.set_xlabel("samples")
ax.set_ylabel("acc_y")
plt.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
lable = "squat"
paritipant = "A"
all_axis_df = df.query("label == @lable").query("participant == @paritipant").reset_index()

fig, ax = plt.subplots()
all_axis_df.groupby(["category"])[["acc_x", "acc_y", "acc_z"]].plot(ax=ax)
ax.set_title("Comparison of medium vs. heavy squat sets across all axes")
ax.set_xlabel("samples")
ax.set_ylabel("acceleration")
plt.legend()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
lable = df["label"].unique()
participants = df["participant"].unique()

for label in lable:
    for participant in participants:
        all_axis_df = df.query("label == @label").query("participant == @participant").reset_index()
        if len(all_axis_df) > 0:
            
            fig, ax = plt.subplots()
            all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
            plt.title(f"Comparison of {label} sets across {participant}")
            plt.xlabel("samples")
            plt.ylabel("acc_y")
            plt.legend()
            plt.show()
            
for label in lable:
    for participant in participants:
        all_axis_df = df.query("label == @label").query("participant == @participant").reset_index()
        if len(all_axis_df) > 0:
            
            fig, ax = plt.subplots()
            all_axis_df[["gyro_x","gyro_y","gyro_z"]].plot(ax=ax)
            plt.title(f"Comparison of {label} sets across {participant}")
            plt.xlabel("samples")
            plt.ylabel("gyro_y")
            plt.legend()
            plt.show()
# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
    lable = "row"
    paritipant = "A"
    combined_plot_df = df.query("label == @lable").query("participant == @paritipant").reset_index(drop =True)

    fig, ax = plt.subplots(nrows=2, sharex=True,figsize=(20,10))
    combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
    combined_plot_df[["gyro_x", "gyro_y", "gyro_z"]].plot(ax=ax[1])
    ax[0].set_title(f"Comparison of {lable} sets across {paritipant} - Accelerometer")
    ax[1].set_title(f"Comparison of {lable} sets across {paritipant} - Gyroscope")
    ax[1].set_xlabel("samples")
    ax[0].set_ylabel("acceleration")
    ax[1].set_ylabel("angular velocity")
    ax[0].legend(loc = "upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True, ncol=3)
    ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True, ncol=3)
    plt.show()


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------

lable = df["label"].unique()
participants = df["participant"].unique()

for label in lable:
    for participant in participants:
        combined_plot_df = df.query("label == @label").query("participant == @participant").reset_index()
        if len(combined_plot_df) > 0:
            fig, ax = plt.subplots(nrows=2, sharex=True,figsize=(20,10))
            combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
            combined_plot_df[["gyro_x", "gyro_y", "gyro_z"]].plot(ax=ax[1])
            ax[0].set_title(f"Comparison of {label} sets across {participant} - Accelerometer")
            ax[1].set_title(f"Comparison of {label} sets across {participant} - Gyroscope")
            ax[1].set_xlabel("samples")
            ax[0].set_ylabel("acceleration")
            ax[1].set_ylabel("angular velocity")
            ax[0].legend(loc = "upper center", bbox_to_anchor=(0.5, 1.2), fancybox=True, shadow=True, ncol=3)
            ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.2), fancybox=True, shadow=True, ncol=3)
            plt.savefig(f"../../reports/figures/{label.title()}_({participant}).png")
            plt.show()