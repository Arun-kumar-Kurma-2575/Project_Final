import streamlit as st
import pickle

# Set up page configuration
st.set_page_config(page_title="Restaurant Rating Predictor", page_icon="🍔", layout="centered")

# Custom CSS for Background and Styling
st.markdown(
    """
    <style>
        body {
            background-image: url('https://source.unsplash.com/1600x900/?restaurant,food');
            background-size: cover;
            background-position: center;
            color: 
            font-family: Arial, sans-serif;
        }
        .main-title {
            font-size: 42px;
            font-weight: bold;
            color:  #000000;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            text-align: center;
            margin-bottom: 10px;
        }
        .sub-title {
            font-size: 18px;
            color:#000000; 
            text-align: center;
            margin-bottom: 20px;
        }
        .stSelectbox label, .stNumberInput label, .stTextInput label {
            font-size: 18px;
            color:#000000;
        }
        .stButton>button {
            background-color:#ff5733; 
            color: white;
            font-size: 16px;
            padding: 10px 24px;
            border-radius: 12px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #c70039;
            color: #fff;
        }
        .stMultiSelect label {
            color: #000000;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<h1 class="main-title">Restaurant Rating Prediction 🍽️</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Predict the rating of your restaurant based on key attributes!</p>', unsafe_allow_html=True)

# Restaurant Name
name = st.text_input('🏨 Enter the Restaurant Name:')

# Country Code Encoding
country_code_option=['162','30','216','14','37','184','214','1','94','148','215','166','189','191','208']
country_sorted=sorted(['Philippines','Brazil','USA','Canada','Australia','Singapore','UAE','India','Indonesia','New Zealand','UK','Qatar','South Africa','Sri Lanka','Turkey'])
country_code = st.selectbox('🌍 Select the Country:', country_sorted)
country_dict={'Philippines':'162','Brazil':'30','USA':'216','Canada':'37','Australia':'14','Singapore':'184','UAE':'214','India':'1','Indonesia':'94','New Zealand':'148','UK':'215','Qatar':'166','South Africa':'189','Sri Lanka':'191','Turkey':'208'}
code=country_dict[country_code]
country_code_encoded = country_code_option.index(code)

# City Encoding
city_option=['Makati City','Mandaluyong City','Pasay City','Pasig City','Quezon City','San Juan City','Santa Rosa','Tagaytay City','Taguig City','Bras_lia','Rio de Janeiro','So Paulo','Albany','Armidale','Athens','Augusta','Balingup','Beechworth','Boise','Cedar Rapids/Iowa City','Chatham-Kent','Clatskanie','Cochrane','Columbus','Consort','Dalton','Davenport','Des Moines','Dicky Beach','Dubuque','East Ballina','Fernley','Flaxton','Forrest','Gainesville','Hepburn Springs','Huskisson','Inverloch','Lakes Entrance','Lakeview','Lincoln','Lorn','Macedon','Macon','Mayfield','Mc Millan','Middleton Beach','Miller','Monroe','Montville','Ojo Caliente','Orlando','Palm Cove','Paynesville','Penola','Pensacola','Phillip Island','Pocatello','Potrero','Princeton','Rest of Hawaii','Savannah','Singapore','Sioux City','Tampa Bay','Tanunda','Trentham East','Valdosta','Vernonia','Victor Harbor','Vineland Station','Waterloo','Weirton','Winchester Bay','Yorkton','Abu Dhabi','Dubai','Sharjah','Agra','Ahmedabad','Allahabad','Amritsar','Aurangabad','Bangalore','Bhopal','Bhubaneshwar','Chandigarh','Chennai','Coimbatore','Dehradun','Faridabad','Ghaziabad','Goa','Gurgaon','Guwahati','Hyderabad','Indore','Jaipur','Kanpur','Kochi','Kolkata','Lucknow','Ludhiana','Mangalore','Mohali','Mumbai','Mysore','Nagpur','Nashik','New Delhi','Noida','Panchkula','Patna','Puducherry','Pune','Ranchi','Secunderabad','Surat','Vadodara','Varanasi','Vizag','Bandung','Bogor','Jakarta','Tangerang','Auckland','Wellington City','Birmingham','Edinburgh','London','Manchester','Doha','Cape Town','Inner City','Johannesburg','Pretoria','Randburg','Sandton','Colombo','Ankara','stanbul']
cities_dict = {
    'Philippines': ['Makati City','Mandaluyong City','Pasay City','Pasig City','Quezon City','San Juan City','Santa Rosa','Tagaytay City','Taguig City'],
    'Brazil':['Brasília','Rio de Janeiro','São Paulo'],
    'USA':['Albany','Athens','Augusta','Boise','Cedar Rapids/Iowa City','Clatskanie','Columbus','Dalton','Davenport','Des Moines','Dubuque','Fernley','Gainesville','Lakeview','Lincoln','Macon','Miller','Monroe','Ojo Caliente','Orlando','Pensacola','Potrero','Pocatello','Princeton','Rest of Hawaii','Savannah','Sioux City','Tampa Bay','Valdosta','Vernonia','Waterloo','Weirton','Winchester Bay'],
    'Canada':['Chatham-Kent','Cochrane','Consort','Yorkton','Vineland Station'],
    'Australia':['Armidale','Balingup','Beechworth','Dicky Beach','East Ballina','Flaxton','Forrest','Hepburn Springs','Huskisson','Inverloch','Lakes Entrance','Lorn','Mayfield','Macedon','Mc Millan','Middleton Beach','Montville','Palm Cove','Paynesville','Penola','Phillip Island','Tanunda','Trentham East','Victor Harbor'],
    'Singapore':['Singapore'],
    'UAE':['Abu Dhabi','Dubai','Sharjah'],
   'India':['Agra','Ahmedabad','Allahabad','Amritsar','Aurangabad','Bangalore','Bhopal','Bhubaneshwar','Chandigarh','Chennai','Coimbatore','Dehradun','Faridabad','Ghaziabad','Goa','Gurgaon','Guwahati','Hyderabad','Indore','Jaipur','Kanpur','Kochi','Kolkata','Lucknow','Ludhiana','Mangalore','Mohali','Mumbai','Mysore','Nagpur','Nashik','New Delhi','Noida','Panchkula','Patna','Puducherry','Pune','Ranchi','Secunderabad','Surat','Vadodara','Varanasi','Vizag'],
    'Indonesia':['Bandung','Bogor','Jakarta','Tangerang'],
    'New Zealand':['Auckland','Wellington City'],
    'UK':['Birmingham','Edinburgh','London','Manchester'],
    'Qatar':['Doha'],
    'South Africa':['Cape Town','Inner City','Johannesburg','Pretoria','Randburg','Sandton'],
    'Sri Lanka':['Colombo'],
   'Turkey':['Ankara','Istanbul']
}
city_sorted=sorted(cities_dict[country_code])
city = st.selectbox('🏙️ Select the City:', city_sorted)
city_encoded = city_option.index(city)


# Currency Encoding
Currency_option=['Botswana Pula(P)','Brazilian Real(R$)','Dollar($)','Emirati Diram(AED)','Indian Rupees(₹)','Indonesian Rupiah(IDR)','NewZealand($)','Pounds()','Qatari Rial(QR)','Rand(R)','Sri Lankan Rupee(LKR)','Turkish Lira(TL)']
Currency_sorted=sorted(Currency_option)
Currency = st.selectbox('💵 Select The Currency used for Payment:', Currency_sorted)
currency_encoded = Currency_option.index(Currency)


#Price Range
price_range_dict={'3': 0, '4(High)': 1, '2': 2, '1(Low)': 3}
price_range=st.selectbox('💲 Select the Price Range:',['4(High)','3','2','1(Low)'])
price_range_encoded=price_range_dict[price_range]

#Average_Cost_for_two
Average_Cost_for_two=int(st.number_input('💰 Enter the Average cost', value=0))


# Convert Selected Cuisines to Encoded Values (for model input)
cuisine_options = sorted(['Greek','Mithai','Mexican','Mineira','Curry','Moroccan','Filipino','Scottish','Chinese','Juices','Burger','Raw Meats','Indonesian','British','Chettinad','Andhra','Singaporean','Salad','Durban','Asian','Pub Food','Fusion','Iranian','Lebanese','Sandwich','Dim Sum','Arabian','Pizza','African','Australian','Gujarati','Ramen','Irish','Canadian','Continental','Nepalese','Ice Cream','Caribbean','Bakery','Malwani','Bubble Tea','European','Kebab','Cantonese','Spanish','Southwestern','Armenian','Italian','Beverages','Finger Food','Teriyaki','Persian','Southern','Deli','Japanese','Lucknowi','Kiwi','Turkish','Bihari','Modern Australian','Asian Fusion','Sri Lankan','Cuban','Awadhi','Fast Food','South African','Soul Food','Bar Food','Vietnamese','Taiwanese','Drinks Only','Biryani','Latin American','Mediterranean','Hawaiian','Malaysian','International','German','Rajasthani','Oriya','North Indian','Peranakan','Restaurant Cafe','Kerala','D_ner','Mughlai','Cuisine Varies','Izgara','South American','Steak','Seafood','Assamese','Afghani','Bengali','Vegetarian','Cajun','North Eastern','Fish and Chips','New American','Healthy Food','Malay','Hyderabadi','Parsi','Brazilian','B_rek','Peruvian','Gourmet Fast Food','Argentine','Naga','Tea','Pakistani','Grill','Charcoal Grill','Diner','Portuguese','Maharashtrian','Indian','Sushi','Tibetan','Patisserie','Coffee and Tea','Western','Thai','Turkish Pizza','Middle Eastern','Goan','French','Cafe','Belgian','Mangalorean','Breakfast','American','Burmese','Kashmiri','Contemporary','Sunda','Street Food','BBQ','Tapas','South Indian','Modern Indian','World Cuisine','Desserts','Tex-Mex','Korean'])
# Multi-Select for Cuisines
cuisines_selected = st.multiselect("Select the Cuisines Served in the Restaurant:", cuisine_options)
# Convert Selected Cuisines to Encoded Values (for model input)
cuisines_encoded=[1 if cuisine in cuisines_selected else 0 for cuisine in cuisine_options]

# Table Booking
Has_Table_booking = st.radio('📅 Has Table Booking?', ['Yes', 'No'])
table_booking_encoded = 1 if Has_Table_booking == 'Yes' else 0

# Online Delivery
Has_Online_delivery = st.radio('🚀 Has Online Delivery?', ['Yes', 'No'])
online_delivery_encoded = 1 if Has_Online_delivery == 'Yes' else 0



#Rating color
Rating_color_dict = {5:'Dark Green',4:'Green',3:'Yellow',2:'Orange',1:'White',0:'Red'}
Rating_color_option=['Dark Green','Green','Yellow','Orange','White','Red']
# Slider for star rating (0 to 5 stars)
rating = st.slider("Give the rating for Food Quality (0 to 5 stars):", min_value=0, max_value=5, value=0)
st.write(f"Your rating: {'⭐' * rating} ({rating} Stars)")
Rating_color=Rating_color_dict[rating]
Rating_color_encoded=Rating_color_option.index(Rating_color)



# Rating Encoding
rating_text_option = ['Excellent', 'Very Good', 'Good', 'Average','Not rated', 'Poor']
rating_text = st.selectbox('How was your overall experience?', rating_text_option)
rating_text_encoded = rating_text_option.index(rating_text)

#votes
votes=int(st.number_input('📝 Enter the no.of Reviews given:',value=0))





# Prediction Button
if st.button('🔮 Predict Rating'):
    input_data = [
        country_code_encoded, city_encoded, Average_Cost_for_two, currency_encoded,
        table_booking_encoded, online_delivery_encoded, price_range_encoded,
        Rating_color_encoded, rating_text_encoded, votes
    ] + cuisines_encoded
    
    try:
        with open('Restaurant_rating_RF.pkl', 'rb') as file:
            model = pickle.load(file)
        prediction = model.predict([input_data])[0]
        st.success(f"✨ Predicted Rating for **{name}**: **{prediction:.2f}**")
    except FileNotFoundError:
        st.error("🚨 Model file not found. Please check the file path.")
    except Exception as e:
        st.error(f"🚨 Prediction failed: {e}")

# Footer
st.markdown("""
    <hr style="border: 0; height: 1px; background-color: #000000;">
    <div style="text-align: center; font-size: 14px; color: #000000;">
        Created with ❤️ for Foodies | Powered by Arun kumar Kurma🍔
    </div>
    """, unsafe_allow_html=True)

