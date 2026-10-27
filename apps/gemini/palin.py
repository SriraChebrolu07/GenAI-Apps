import streamlit as st

st.title("Palindrome checker")

a=st.text_input("enter a word or number")
if st.button("check"):
    a=a.lower().strip()
    if a == a[::-1]:
        st.success("palindrome")
    else:
        st.success("not a palindrome")