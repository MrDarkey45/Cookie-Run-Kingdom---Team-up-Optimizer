import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 5)

def load_data(filepath):
    """
    Load the cookie data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file
    
    Returns:
        pd.DataFrame: Loaded data
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully! Shape: {df.shape}")
        print(f"\nColumns: {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_visualizations(df):
    """
    Create three visualizations: pie chart for rarity, 
    bar graphs for role and position.
    
    Args:
        df (pd.DataFrame): Cookie data
    """
    # Create a figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. PIE CHART - Cookie Rarity
    if 'cookie_rarity' in df.columns:
        rarity_counts = df['cookie_rarity'].value_counts()
        
        # Define custom colors for the pie chart
        colors = plt.cm.Set3(range(len(rarity_counts)))
        
        # Create explode array to pull out small slices slightly
        explode = [0.05 if count < rarity_counts.sum() * 0.02 else 0 
                   for count in rarity_counts.values]
        
        wedges, texts, autotexts = axes[0].pie(
            rarity_counts.values, 
            labels=rarity_counts.index, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=explode,
            pctdistance=0.85,
            labeldistance=1.15,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
        )
        
        # Improve text readability
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(8)
        
        axes[0].set_title('Cookie Rarity Distribution', fontsize=14, fontweight='bold')
    else:
        axes[0].text(0.5, 0.5, 'cookie_rarity column not found', 
                     ha='center', va='center')
        axes[0].set_title('Cookie Rarity Distribution', fontsize=14, fontweight='bold')
    
    # 2. BAR GRAPH - Cookie Role
    if 'cookie_role' in df.columns:
        role_counts = df['cookie_role'].value_counts()
        
        axes[1].bar(range(len(role_counts)), 
                    role_counts.values, 
                    color='steelblue',
                    edgecolor='black',
                    linewidth=0.7)
        axes[1].set_xticks(range(len(role_counts)))
        axes[1].set_xticklabels(role_counts.index, rotation=45, ha='right')
        axes[1].set_ylabel('Count', fontsize=11)
        axes[1].set_title('Cookie Role Distribution', fontsize=14, fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)
        
        # Add value labels on top of bars
        for i, v in enumerate(role_counts.values):
            axes[1].text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')
    else:
        axes[1].text(0.5, 0.5, 'cookie_role column not found', 
                     ha='center', va='center', transform=axes[1].transAxes)
        axes[1].set_title('Cookie Role Distribution', fontsize=14, fontweight='bold')
    
    # 3. BAR GRAPH - Cookie Position
    if 'cookie_position' in df.columns:
        position_counts = df['cookie_position'].value_counts()
        
        axes[2].bar(range(len(position_counts)), 
                    position_counts.values, 
                    color='coral',
                    edgecolor='black',
                    linewidth=0.7)
        axes[2].set_xticks(range(len(position_counts)))
        axes[2].set_xticklabels(position_counts.index, rotation=45, ha='right')
        axes[2].set_ylabel('Count', fontsize=11)
        axes[2].set_title('Cookie Position Distribution', fontsize=14, fontweight='bold')
        axes[2].grid(axis='y', alpha=0.3)
        
        # Add value labels on top of bars
        for i, v in enumerate(position_counts.values):
            axes[2].text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')
    else:
        axes[2].text(0.5, 0.5, 'cookie_position column not found', 
                     ha='center', va='center', transform=axes[2].transAxes)
        axes[2].set_title('Cookie Position Distribution', fontsize=14, fontweight='bold')
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('cookie_analysis.png', dpi=300, bbox_inches='tight')
    print("\nVisualizations saved as 'cookie_analysis.png'")
    
    # Display the plots
    plt.show()

def print_summary_statistics(df):
    """
    Print summary statistics for the cookie data.
    
    Args:
        df (pd.DataFrame): Cookie data
    """
    print("\n" + "="*50)
    print("SUMMARY STATISTICS")
    print("="*50)
    
    if 'cookie_rarity' in df.columns:
        print("\nCookie Rarity Counts:")
        print(df['cookie_rarity'].value_counts())
    
    if 'cookie_role' in df.columns:
        print("\nCookie Role Counts:")
        print(df['cookie_role'].value_counts())
    
    if 'cookie_position' in df.columns:
        print("\nCookie Position Counts:")
        print(df['cookie_position'].value_counts())
    
    print("\n" + "="*50)

def main():
    """
    Main function to orchestrate the data analysis workflow.
    """
    # Specify your file path here
    filepath = 'crk-cookies.csv'  # Change this to your actual file path
    
    print("Cookie Data Analysis Program")
    print("="*50)
    
    # Load the data
    df = load_data(filepath)
    
    if df is not None:
        # Print summary statistics
        print_summary_statistics(df)
        
        # Create visualizations
        print("\nCreating visualizations...")
        create_visualizations(df)
        
        print("\nAnalysis complete!")
    else:
        print("\nAnalysis failed due to data loading error.")

if __name__ == "__main__":
    main()