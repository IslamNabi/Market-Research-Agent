from typing import List, Dict, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import os
from config import REPORTS_DIR

class Analyzer:
    def __init__(self):
        pass

    def to_dataframe(self, structured: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(structured)
        expected = ['name', 'description', 'sector', 'founded_year', 'website', 'notes']
        for col in expected:
            if col not in df.columns:
                df[col] = None
        return df[expected]

    def basic_stats_and_charts(self, df: pd.DataFrame, slug: str = "report") -> Tuple[Dict, List[str], pd.DataFrame]:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        charts = []
        stats = {}

        # Normalize sector text
        if 'sector' in df.columns:
            df['sector'] = df['sector'].fillna('Unknown').astype(str).str.strip().str.title()
            sector_counts = df['sector'].value_counts()
            if not sector_counts.empty:
                fig, ax = plt.subplots(figsize=(6, 4))
                sector_counts.plot(kind='bar', ax=ax)
                ax.set_title('Startups by Sector')
                plt.tight_layout()
                path = os.path.join(REPORTS_DIR, f"{slug}_sector_distribution.png")
                fig.savefig(path)
                plt.close(fig)
                charts.append(path)
                stats['sector_counts'] = sector_counts.to_dict()

        # Founded year histogram
        if 'founded_year' in df.columns and df['founded_year'].notna().any():
            years = pd.to_numeric(df['founded_year'], errors='coerce').dropna().astype(int)
            if not years.empty:
                bins = min(len(years.unique()), 20)  # Adaptive bin count
                fig, ax = plt.subplots(figsize=(6, 4))
                years.plot(kind='hist', bins=bins, ax=ax)
                ax.set_title('Founded Year Distribution')
                plt.tight_layout()
                path = os.path.join(REPORTS_DIR, f"{slug}_founded_hist.png")
                fig.savefig(path)
                plt.close(fig)
                charts.append(path)
                stats['founded_year_summary'] = years.describe().to_dict()

        # Basic counts
        stats['total_companies'] = len(df)
        stats['unique_sectors'] = df['sector'].nunique() if 'sector' in df.columns else None

        return stats, charts, df
