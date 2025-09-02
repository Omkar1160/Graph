import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Step 1: Load CSV file ---
file_path = r"C:\Users\LENOVO60\Desktop\mock_scores_upsc.csv"  # Update this path if needed
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# --- Step 2: Rename "Name of the candidate" column if needed ---
if 'Name of the candidate' in df.columns:
    df.rename(columns={'Name of the candidate': 'Name'}, inplace=True)

# --- Step 3: Detect number of mocks dynamically ---
num_mocks = max(
    int(col.split()[1])
    for col in df.columns
    if col.startswith("Mock") and any(x in col for x in ["Math", "GAT", "Total"])
)

# --- Step 4: Rename mock columns consistently ---
for i in range(1, num_mocks + 1):
    df.rename(columns={
        f"Mock {i} Math": f"Mock{i}_Math",
        f"Mock {i} GAT": f"Mock{i}_GAT",
        f"Mock {i} Total": f"Mock{i}_Total"
    }, inplace=True)

# --- Step 5: Convert score columns to numeric ---
for i in range(1, num_mocks + 1):
    for part in ['Math', 'GAT', 'Total']:
        col = f"Mock{i}_{part}"
        if col in df.columns:  # only process if column exists
            df[col] = pd.to_numeric(df[col], errors='coerce')

df.fillna(0, inplace=True)

# --- Step 6: Output folder ---
output_folder = r"C:\Users\LENOVO60\Documents\Graph\student_graphs"
os.makedirs(output_folder, exist_ok=True)

# --- Step 7: Plot graphs for each student ---
for idx, row in df.iterrows():
    name = str(row['Name']).replace(" ", "_").replace("/", "_") if 'Name' in df.columns else f"Student{idx}"
    roll_no = str(row.get('Roll No', idx))  # fallback to index if Roll No missing
    section = str(row.get('Section', 'Unknown'))  # Section column (default Unknown)

    math_scores = [row.get(f"Mock{i}_Math", 0) for i in range(1, num_mocks + 1)]
    gat_scores = [row.get(f"Mock{i}_GAT", 0) for i in range(1, num_mocks + 1)]
    total_scores = [row.get(f"Mock{i}_Total", 0) for i in range(1, num_mocks + 1)]
    mock_labels = [f"Mock {i}" for i in range(1, num_mocks + 1)]

    fig, ax = plt.subplots(figsize=(10, 6))

    # --- Shaded Areas ---
    ax.axhspan(0, 75, facecolor='red', alpha=0.15, zorder=0)       # Low Math
    ax.axhspan(75, 150, facecolor='green', alpha=0.15, zorder=0)   # Good Math
    ax.axhspan(150, 225, facecolor='red', alpha=0.15, zorder=0)    # Low GAT
    ax.axhspan(225, 350, facecolor='green', alpha=0.15, zorder=0)  # Good GAT

    # --- Shaded Area Labels ---
    ax.text(num_mocks - 2, 35, "Low (Math)", color='red', fontsize=9,
            va='center', ha='right', fontweight='bold')
    ax.text(num_mocks - 2, 112, "Good (Math)", color='green', fontsize=9,
            va='center', ha='right', fontweight='bold')
    ax.text(num_mocks - 2, 187, "Low (GAT)", color='red', fontsize=9,
            va='center', ha='right', fontweight='bold')
    ax.text(num_mocks - 2, 287, "Good (GAT)", color='green', fontsize=9,
            va='center', ha='right', fontweight='bold')

    # --- Plot Scores ---
    for scores, label, color in zip(
        [math_scores, gat_scores, total_scores],
        ['Math', 'GAT', 'Total'],
        ['blue', 'orange', 'green']
    ):
        ax.plot(mock_labels, scores, marker='o', label=label, color=color, zorder=2)
        for i, score in enumerate(scores):
            ax.text(i, score + 5, str(int(score)), ha='center',
                    va='bottom', fontsize=8, color=color, zorder=3)

    # --- Graph Aesthetics ---
    ax.set_title(f"Section: {section} | {row.get('Name', f'Student {idx}')} (Roll No: {roll_no})")
    ax.set_xlabel("Mock Test")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 500)
    ax.set_yticks(range(0, 550, 25))
    ax.grid(True, zorder=1)
    ax.legend(loc='upper left')
    fig.tight_layout()

    # --- Watermark (Roll No + Section) ---
    fig.text(
        0.5, 0.5, f"Roll No: {roll_no} | Section: {section}",
        fontsize=35, color='gray',
        ha='center', va='center',
        alpha=0.15, rotation=30
    )

    # --- Save and Close ---
    fig.savefig(os.path.join(output_folder, f"{name}_{roll_no}.png"))  # Save in Documents\student_graph
    plt.close(fig)

print("✅ All student graphs saved in C:\\Users\\LENOVO60\\Documents\\student_graph with Section (title + watermark only), Name, Roll No, shaded zones, and point annotations.")
