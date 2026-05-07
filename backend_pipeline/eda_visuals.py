import matplotlib.pyplot as plt
import os

def generate_eda_plots(df, return_fig=False):
    """
    Generates three academic-grade plots to analyze the fraud dataset.
    
    Inputs: 
        df: Cleaned Pandas DataFrame
        return_fig: Boolean. If True, returns the figure (for Streamlit). 
                    If False, saves to disk (for Flask).
    """
    # Create a figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # 1. Bar Chart: Severe Class Imbalance
    class_counts = df['Class'].value_counts()
    
    normal_count = class_counts.get(0, 0)
    fraud_count = class_counts.get(1, 0)
    
    axes[0].bar(['Normal (0)', 'Fraud (1)'], [normal_count, fraud_count], color=['blue', 'red'])
    axes[0].set_title('Transaction Class Imbalance')
    axes[0].set_ylabel('Number of Transactions')
    
    # 2. Histogram: Transaction Amounts Distribution
    normal_amounts = df[df['Class'] == 0]['Amount']
    fraud_amounts = df[df['Class'] == 1]['Amount']
    
    axes[1].hist(normal_amounts, bins=50, alpha=0.5, label='Normal', color='blue', range=(-1, 5))
    axes[1].hist(fraud_amounts, bins=50, alpha=0.5, label='Fraud', color='red', range=(-1, 5))
    axes[1].set_title('Distribution of Transaction Amounts (Scaled)')
    axes[1].set_xlabel('Scaled Amount')
    axes[1].set_ylabel('Frequency')
    axes[1].legend()
    
    # 3. Scatter Plot: Time vs Occurrence of Fraud
    axes[2].scatter(df[df['Class'] == 0]['Time'], df[df['Class'] == 0]['Amount'], 
                    alpha=0.3, label='Normal', color='blue', s=1)
    axes[2].scatter(df[df['Class'] == 1]['Time'], df[df['Class'] == 1]['Amount'], 
                    alpha=0.9, label='Fraud', color='red', s=10)
    axes[2].set_title('Scaled Time vs. Scaled Amount by Class')
    axes[2].set_xlabel('Scaled Time')
    axes[2].set_ylabel('Scaled Amount')
    axes[2].legend()
    
    # Adjust layout for better presentation
    plt.tight_layout()
    
    # --- The Dual-Purpose Routing Logic ---
    if return_fig:
        # If Streamlit calls this, hand the figure object directly to the web app
        return fig
    else:
        # If the backend pipeline calls this, save it as a PNG for Flask
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app_portfolio', 'static', 'img'))
        os.makedirs(img_dir, exist_ok=True)
        
        save_path = os.path.join(img_dir, 'dashboard_charts.png')
        plt.savefig(save_path, bbox_inches='tight')
        print(f"Charts successfully saved to {save_path}")
        
        # Close the plot to prevent the script from freezing!
        plt.close(fig)