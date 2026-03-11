import streamlit as st
from reia.crew import Reia
import usaddress


def parse_address(address: str):
    parsed, _ = usaddress.tag(address)

    return {
        "street": " ".join(
            filter(
                None,
                [
                    parsed.get("AddressNumber"),
                    parsed.get("StreetNamePreDirectional"),
                    parsed.get("StreetName"),
                    parsed.get("StreetNamePostType"),
                ],
            )
        ),
        "city": parsed.get("PlaceName"),
        "state": parsed.get("StateName"),
        "zip": parsed.get("ZipCode"),
    }


st.title("REIA Property Intelligence")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_input = st.chat_input("Enter an address")

if user_input:

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        inputs = parse_address(user_input)
    except:
        response = "❌ Could not parse the address."
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Running agent..."):
            result = Reia().crew().kickoff(inputs=inputs)

        data = result.pydantic

        response = f"""
### Business
{data.confirmed_business_name}
{data.business_type}

### NAICS
{data.primary_naics_code}  
{data.primary_naics_title}

### Notes
{data.notes}
"""
# ### Property
# Owner: {data.owner_name}  
# Sqft: {data.building_sqft}  
# Year Built: {data.year_built}

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})