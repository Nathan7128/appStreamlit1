import numpy as np
import pandas as pd
import streamlit as st

from faker import Faker

# fonction qui génère des données de membres de l'entreprise
@st.cache_data
def get_profile_dataset(number_of_items: int = 20, seed: int = 0) -> pd.DataFrame :
    new_data = []
    faker = Faker()
    np.random.seed(seed)
    Faker.seed(seed)
    for i in range(number_of_items) :
        profile = faker.profile()
        new_data.append(
            {'name' : profile["name"], 
                        'daily_activity' : np.random.rand(25), 
                        "activity" : np.random.randint(2, 90, size = 12)
            }
        )
    profile_df = pd.DataFrame(new_data)
    return profile_df

# st.dataframe(get_profile_dataset())

column_configuration = {
    "name" : st.column_config.TextColumn(
        "Name", help = "The name of the user", max_chars = 100, width = "medium"
    ),
    "activity" : st.column_config.LineChartColumn(
        "Activity(1 year)",
        help = "The user's activity over the last 1 year",
        width = "large",
        y_min = 0,
        y_max = 100
    ),
    "daily_activity" : st.column_config.BarChartColumn(
        "Activity (daily)",
        help = "The user's activity in the last 25 days",
        width = "medium",
        y_min = 0,
        y_max = 1
    )
}

st.header("All members")

df = get_profile_dataset()
event = st.dataframe(
    df,
    column_config=column_configuration,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="multi-row"
)

st.header("Selected members")

people = event.selection.rows
filtered_df = df.iloc[people]
st.dataframe(
    filtered_df,
    column_config=column_configuration,
    use_container_width=True
)