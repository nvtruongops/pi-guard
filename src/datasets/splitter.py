import pandas as pd
from typing import Tuple
from sklearn.model_selection import GroupShuffleSplit

class DatasetSplitter:
    """Group-aware dataset partitioner to prevent data leakage between paraphrased templates."""

    @staticmethod
    def split_group_aware(
        df: pd.DataFrame,
        group_col: str = "cluster_id",
        test_size: float = 0.15,
        val_size: float = 0.15,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Splits a dataframe into train, val, and test partitions based on clusters."""
        if group_col not in df.columns:
            # Fallback if no cluster_id exists: use exact text hash or raw index
            df[group_col] = df.index
            
        gss_test = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
        train_val_idx, test_idx = next(gss_test.split(df, groups=df[group_col]))
        
        train_val_df = df.iloc[train_val_idx].reset_index(drop=True)
        test_df = df.iloc[test_idx].reset_index(drop=True)
        
        adjusted_val_size = val_size / (1.0 - test_size)
        gss_val = GroupShuffleSplit(n_splits=1, test_size=adjusted_val_size, random_state=random_state)
        train_idx, val_idx = next(gss_val.split(train_val_df, groups=train_val_df[group_col]))
        
        train_df = train_val_df.iloc[train_idx].reset_index(drop=True)
        val_df = train_val_df.iloc[val_idx].reset_index(drop=True)
        
        return train_df, val_df, test_df
