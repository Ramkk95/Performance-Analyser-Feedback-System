import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage ,HumanMessage
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

st.header("Welcome to dashboard")

with st.sidebar:
    st.title("Upload Your file Here")
    file=st.file_uploader("Upload",type=['csv'])
    sub=st.button("Submit")
if sub and file:
    st.session_state.df=pd.read_csv(file)

if 'df' in st.session_state:
    dp=st.session_state.df

    with (st.spinner("Loading file...")):

            roll=st.text_input("Enter your Student ID")
            if roll:
                P=dp['Student_ID']==roll
                ki=dp[P]
                #st.write(ki)
                #kii=pd.Series(ki)
                st.subheader(f"Welcome {ki.iloc[0,1]} :Here is Your result  ")
                subjects=['Polity','History','Geography','Economy','Environment']
                #st.write(ki.iloc[0, 1])
                col1,col2=st.columns(2)
                with col1:
                    st.write("Student Name:",ki.iloc[0,1])
                    st.write('Gender:',ki.iloc[0, 2])
                    st.write('City:',ki.iloc[0, 3])
                    st.write('Attendace %:', ki.iloc[0, 4])
                    st.write('Mock Test Attempted:', ki.iloc[0, 6])



                with col2:

                    st.write('Total Marks :', ki.iloc[0, 12])
                    st.write('Percentage %:', ki.iloc[0, 13])
                    st.write('Grade:', ki.iloc[0, 14])
                    st.write('Avg_Study Hour:', ki.iloc[0, 5])
                    avg_t=dp['Total_Marks'].mean()
                    st.write('Avg Marks of all students:', avg_t)

                Marks = ki[subjects].iloc[0].to_list()


                mark_di={'Subject':subjects,"Marks_subjwctwise":Marks}
                mks=pd.DataFrame(mark_di)
                #st.write(mks)

                fig,ax=plt.subplots(1,2,figsize=(8,3))
                ax[0].bar(subjects,Marks,color='green')
                ax[0].set_xlabel("Subjects")
                ax[0].set_ylabel("Marks")
                ax[0].set_facecolor('red')
                ax[0].grid()
                ax[0].tick_params(axis='x',color='red',rotation=70)
                ax[0].set_title("Subjects vs Marks")
                #st.pyplot(fig)
                avg_P=dp['Polity'].mean()
                avg_H= dp['History'].mean()
                avg_G= dp['Geography'].mean()
                avg_E=dp['Economy'].mean()
                avg_En= dp['Environment'].mean()

                avg_list=[avg_P,avg_H,avg_G,avg_E,avg_En]
                maks={'subj':subjects,"avg_Marks":avg_list}
                new_avg=pd.DataFrame(maks)
                col1,col2 =st.columns(2)
                with col1:
                    st.write(mks)

                with col2:
                    st.write(new_avg)

                #fig,ax=plt.subplots(figsize=(5,3))
                ax[1].bar(subjects,avg_list,color='green')
                ax[1].set_xlabel("Subjects")
                ax[1].set_ylabel("Average Marks")
                ax[1].set_facecolor('yellow')
                ax[1].set_title("Subjects vs Average Marks")
                ax[1].grid()
                ax[1].tick_params(axis='x',color='green',rotation=70)
                st.pyplot(fig)
                st.write(f"Number of student ahead of: {ki["Student_Name"].iloc[0]}")

                num_p=dp['Polity']>ki['Polity'].iloc[0]
                st.write("In Polity",dp[num_p].count().iloc[0])

                num_h=dp['History']>ki['History'].iloc[0]
                #st.write(f"student having more marks than {ki['Student_Name']}")
                st.write("In History",dp[num_h].count().iloc[0])
                #st.write(f"{ki['Student_Name'][0]}")

                num_g=dp['Geography']>ki['Geography'].iloc[0]
                st.write("In Geography",dp[num_g].count().iloc[0])

                num_e=dp['Economy']>ki['Economy'].iloc[0]
                st.write("In Economy",dp[num_e].count().iloc[0])

                num_en=dp['Environment']>ki['Environment'].iloc[0]
                st.write("In Environment",dp[num_en].count().iloc[0])

                pg=dp.groupby('Gender')['Total_Marks'].mean()
                st.write(pg)

                fig,ax=plt.subplots(figsize=(6,4))
                ax.pie(pg,autopct='%1.2f%%',labels=pg.index,radius=1,colors=['yellow','blue'])
                ax.set_title("Total Marks VS  Gender")
                ax.legend(
                    bbox_to_anchor=(0.5, 1.02, 1., .102),
                    loc='right',
                    facecolor='red'
                         )
                ax.set_facecolor('red')
                st.pyplot(fig)
                @st.cache_data
                def analysis(ki):
                    model=init_chat_model("gpt-4.1")


                    messages=[SystemMessage(content="You are a helpful Mentor , and guide them based on their marks performance"),
                              HumanMessage(content=f"""
                                                        student detail :{ki}
                                                        
                                                        average marks of other student in different subject: {new_avg}
                                                        number of student ahead of him in Polity:{dp[num_p].count().iloc[0]}
                                                        number of student ahead of him in History:{dp[num_h].count().iloc[0]},
                                                        number of student ahead of him in Polity:{dp[num_g].count().iloc[0]},
                                                        number of student ahead of him in Polity:{dp[num_e].count().iloc[0]}
                                                        number of student ahead of him in Polity:{dp[num_en].count().iloc[0]}  
                                                        Total students attempeted Test = 100  


                                                        """)]
                    resp=model.invoke(messages)
                    st.write(resp.content)
                analysis(ki)