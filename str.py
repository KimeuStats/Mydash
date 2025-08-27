import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.set_page_config(page_title="Pokémon Dashboard", layout="wide")

st.title("📊 Pokémon Dashboard")
st.markdown("Explore and analyze Pokémon stats in an interactive way!")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\User\Downloads\pokemon.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Pokémon")

# Use correct column names
types = df['type_1'].unique().tolist()
selected_type = st.sidebar.multiselect("Select Type", types, default=types)

# Your dataset might not have 'Legendary', so we add a check
if 'legendary' in df.columns:
    legendary_filter = st.sidebar.selectbox("Legendary Only?", ["All", "Yes", "No"])
else:
    legendary_filter = "All"  # skip filter if column missing

# Apply filters
filtered_df = df[df['type_1'].isin(selected_type)]
if legendary_filter == "Yes" and 'legendary' in df.columns:
    filtered_df = filtered_df[filtered_df['legendary'] == True]
elif legendary_filter == "No" and 'legendary' in df.columns:
    filtered_df = filtered_df[filtered_df['legendary'] == False]

# Show dataset preview
st.subheader("📋 Pokémon Data")
st.dataframe(filtered_df, use_container_width=True)

# Summary stats
st.subheader("📈 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Pokémon", len(filtered_df))
col2.metric("Average Attack", round(filtered_df["attack"].mean(), 1))
col3.metric("Average Defense", round(filtered_df["defense"].mean(), 1))

# Visualizations
st.subheader("📊 Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Distribution of Pokémon Types")
    plt.figure(figsize=(6,4))
    sns.countplot(y="type_1", data=filtered_df, order=filtered_df["type_1"].value_counts().index)
    plt.title("Pokémon Type Distribution")
    st.pyplot(plt)

with col2:
    st.markdown("### Attack vs Defense")
    plt.figure(figsize=(6,4))
    sns.scatterplot(x="attack", y="defense", hue="type_1", data=filtered_df, palette="Set2")
    plt.title("Attack vs Defense")
    st.pyplot(plt)

# Extra: Correlation Heatmap
st.subheader("🔗 Correlation Heatmap")
plt.figure(figsize=(10,6))
sns.heatmap(filtered_df[["hp","attack","defense","speed","special-attack","special-defense"]].corr(), annot=True, cmap="coolwarm")
st.pyplot(plt)
