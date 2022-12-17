import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from st_aggrid import AgGrid

st.set_page_config(layout="wide")
st.title("Ultimate Fighting Bets Prediction and Analysis Tool")

st.markdown("""
<style>

.css-9s5bis.edgvbvh3
{
   visibility: hidden;
   
}
.css-1q1n0ol.egzxvld0
{
   visibility : hidden;
   
}

.css-qri22k.egzxvld0
{
   visibility: hidden;

}


</style>



""", unsafe_allow_html=True)






col7,col8 = st.columns([3,4])



#load in data

with col7:
    st.image("Unbenanntes_Projekt.jpg")
    st.subheader("Ultimate Fighting Bets by Alex Srkn")
    st.markdown("**-Tool for Optimizing your UFC Bets**")
    st.markdown("**-Compare 2 Fighters Stats against each other**")
    st.markdown("**-Get Win % for both Fighters based on Combat Score**")
    st.markdown("**-Combat Score combines all Stats of a Fighter**")
    st.markdown("**-Calculate EV using individual Bet Size and Odds**")


df= pd.read_csv('final.csv')
df= df.drop(columns =['Unnamed: 0'])

with col8:
     st.subheader("Fighter Dataset")
     AgGrid(df)


col1,col2 = st.columns([2,3])

#sidebar - weight Selection


#describe data



col1.subheader("Dataset Description")
col1.write(df.describe().T)


#correlation Heatmap
df.corr()
fig = plt.figure(figsize=(10,4))
heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True)
heatmap.set_title('FighterStats', fontdict = {'fontsize':16}, pad =12);

col2.subheader("Correlation Matrix")
with col2:
    st.pyplot(fig)

col420,col690 = st.columns(2)


with col420:
    
    st.markdown("**SLpM** - Significant Strikes Landed per Minute")
    st.markdown("**Str. Acc.** - Significant Striking Accuracy")
    st.markdown("**SApM** - Significant Strikes Absorbed per Minute")
    st.markdown("**Str. Def.** - Significant Strike Defence (the % of opponents strikes that did not land)")
with col690:
    
    st.markdown("**TD Avg.** - Average Takedowns Landed per 15 minutes")
    st.markdown("**TD Acc.** - Takedown Accuracy")
    st.markdown("**TD Def.** - Takedown Defense (the % of opponents TD attempts that did not land)")
    st.markdown("**Sub. Avg.** - Average Submissions Attempted per 15 minutes")







df = df.reset_index()

st.subheader("Choose your Fighters")
options = df['Name'].unique().tolist()
selected_options = st.multiselect('Pick  2 Fighters',options)

filtered_df = df[df['Name'].isin(selected_options)]


st.dataframe(filtered_df)



filtered_df.set_index('Name', inplace =True)
optionStats = filtered_df[['SLpM','SApM','TDAvg','SubAvg']]
optionStats = optionStats.reset_index()
os = optionStats.melt(id_vars=['Name'],value_vars = ['SLpM','SApM','TDAvg','SubAvg'], ignore_index=False)





col3,col4 = st.columns([3,3])


y= alt.Chart(os).mark_bar().encode(
x='value',
y='Name',
color='variable').properties(height=180,width=450)

col3.subheader("**Activity**")
col3.write(y)

##

#plotting scores
optionPercs = filtered_df[['ScoreStrAcc','ScoreStrDef','ScoreTDDef','ScoreTDAcc',
                         'CombatScore']]
optionPercs = optionPercs.reset_index()
op = optionPercs.melt(id_vars=['Name'],value_vars=['ScoreStrAcc','ScoreStrDef',
                                                 'ScoreTDAcc','ScoreTDDef','CombatScore'], ignore_index=False)

z= alt.Chart(op).mark_bar().encode(
x='value',
y='Name',
color='variable').properties(height=180,width=450)

col4.subheader("**Effectivity**")
col4.write(z)



## Win Percentage
st.subheader("Win Percentages for Both Fighters")



if not filtered_df.empty:
   
    
    wi_percentage = filtered_df['CombatScore']
    try:
        tot_percentage = (wi_percentage.iloc[0] + wi_percentage.iloc[1])
    
        col14,col15,col16,col17 = st.columns(4)
        chosenNames = op['Name']
        fighter1Name = chosenNames.iloc[0]
        fighter2Name = chosenNames.iloc[1]
        wi_percentage_fighter1= wi_percentage.iloc[0]/tot_percentage*100
        wi_percentage_fighter2= wi_percentage.iloc[1]/tot_percentage*100
        
    
        col14.markdown( "**Fighter 1 (**" + " " + fighter1Name + " " + " " + "**) Win % is :**")
        col15.write(wi_percentage_fighter1)
        col16.markdown("**Fighter 2 (**" + " " + fighter2Name + " " + " " + "**) Win % is :**")
        col17.write(wi_percentage_fighter2)
    except IndexError:
        st.markdown("**Pick 2 Fighters to Calculate Win Percentage**")

def ev(odds,prob_win,prob_lose,size):
    return prob_win * odds + prob_lose *(-1)*size


# user input for Odds and Win Amount




st.subheader("EV Calculator")

col42,col69 = st.columns(2)

with col42:
    odd1 = st.number_input('Profit Fighter 1')
    betSize1= st.number_input('Bet Size Fighter 1')
    
with col69:    
    odd2 = st.number_input('Profit Fighter 2')
    betSize2= st.number_input('Bet Size Fighter 2')

if not filtered_df.empty:
    
    try:
        ev_prob_fighter1 = wi_percentage_fighter1/100
        ev_prob_fighter2 = wi_percentage_fighter2/100
    
        if odd1>= 1 and odd2>=1 and betSize1>=1 and betSize2>=1:
        
            col20,col21,col22,col23 = st.columns(4)
            
            col20.markdown("**EV for Fighter 1 is:**")
            col21.write(ev(odd1,ev_prob_fighter1,ev_prob_fighter2,betSize1))
            col22.markdown("**EV for Fighter 2 is:**")
            col23.write(ev(odd2,ev_prob_fighter2,ev_prob_fighter1,betSize2))
    except NameError:
        st.markdown("**2 Fighters required**")
    
    



