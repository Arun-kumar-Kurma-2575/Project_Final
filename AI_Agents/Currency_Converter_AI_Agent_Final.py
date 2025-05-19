import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType
import streamlit as st
import time
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Retrieve the key
api_key = os.getenv("GOOGLE_API_KEY")

# Access the URL stored in the .env file
exchange_api_url = os.getenv("EXCHANGE_API_URL")

# Streamlit app setup
st.set_page_config(page_title="Currency Converter AI", layout="centered")
st.title("💱 AI Agent for Currency Conversion")


currency_dict = {
    'United Arab Emirates (UAE Dirham)': 'AED',
    'Afghanistan (Afghan Afghani)': 'AFN',
    'Albania (Albanian Lek)': 'ALL',
    'Armenia (Armenian Dram)': 'AMD',
    'Netherlands Antilles (Netherlands Antillian Guilder)': 'ANG',
    'Angola (Angolan Kwanza)': 'AOA',
    'Argentina (Argentine Peso)': 'ARS',
    'Australia (Australian Dollar)': 'AUD',
    'Aruba (Aruban Florin)': 'AWG',
    'Azerbaijan (Azerbaijani Manat)': 'AZN',
    'Bosnia and Herzegovina (Bosnia and Herzegovina Mark)': 'BAM',
    'Barbados (Barbados Dollar)': 'BBD',
    'Bangladesh (Bangladeshi Taka)': 'BDT',
    'Bulgaria (Bulgarian Lev)': 'BGN',
    'Bahrain (Bahraini Dinar)': 'BHD',
    'Burundi (Burundian Franc)': 'BIF',
    'Bermuda (Bermudian Dollar)': 'BMD',
    'Brunei (Brunei Dollar)': 'BND',
    'Bolivia (Bolivian Boliviano)': 'BOB',
    'Brazil (Brazilian Real)': 'BRL',
    'Bahamas (Bahamian Dollar)': 'BSD',
    'Bhutan (Bhutanese Ngultrum)': 'BTN',
    'Botswana (Botswana Pula)': 'BWP',
    'Belarus (Belarusian Ruble)': 'BYN',
    'Belize (Belize Dollar)': 'BZD',
    'Canada (Canadian Dollar)': 'CAD',
    'Democratic Republic of the Congo (Congolese Franc)': 'CDF',
    'Switzerland (Swiss Franc)': 'CHF',
    'Chile (Chilean Peso)': 'CLP',
    'China (Chinese Renminbi)': 'CNY',
    'Colombia (Colombian Peso)': 'COP',
    'Costa Rica (Costa Rican Colon)': 'CRC',
    'Cuba (Cuban Peso)': 'CUP',
    'Cape Verde (Cape Verdean Escudo)': 'CVE',
    'Czech Republic (Czech Koruna)': 'CZK',
    'Djibouti (Djiboutian Franc)': 'DJF',
    'Denmark (Danish Krone)': 'DKK',
    'Dominican Republic (Dominican Peso)': 'DOP',
    'Algeria (Algerian Dinar)': 'DZD',
    'Egypt (Egyptian Pound)': 'EGP',
    'Eritrea (Eritrean Nakfa)': 'ERN',
    'Ethiopia (Ethiopian Birr)': 'ETB',
    'European Union (Euro)': 'EUR',
    'Fiji (Fiji Dollar)': 'FJD',
    'Falkland Islands (Falkland Islands Pound)': 'FKP',
    'Faroe Islands (Faroese Króna)': 'FOK',
    'United Kingdom (Pound Sterling)': 'GBP',
    'Georgia (Georgian Lari)': 'GEL',
    'Guernsey (Guernsey Pound)': 'GGP',
    'Ghana (Ghanaian Cedi)': 'GHS',
    'Gibraltar (Gibraltar Pound)': 'GIP',
    'The Gambia (Gambian Dalasi)': 'GMD',
    'Guinea (Guinean Franc)': 'GNF',
    'Guatemala (Guatemalan Quetzal)': 'GTQ',
    'Guyana (Guyanese Dollar)': 'GYD',
    'Hong Kong (Hong Kong Dollar)': 'HKD',
    'Honduras (Honduran Lempira)': 'HNL',
    'Croatia (Croatian Kuna)': 'HRK',
    'Haiti (Haitian Gourde)': 'HTG',
    'Hungary (Hungarian Forint)': 'HUF',
    'Indonesia (Indonesian Rupiah)': 'IDR',
    'Israel (Israeli New Shekel)': 'ILS',
    'Isle of Man (Manx Pound)': 'IMP',
    'India (Indian Rupee)': 'INR',
    'Iraq (Iraqi Dinar)': 'IQD',
    'Iran (Iranian Rial)': 'IRR',
    'Iceland (Icelandic Króna)': 'ISK',
    'Jersey (Jersey Pound)': 'JEP',
    'Jamaica (Jamaican Dollar)': 'JMD',
    'Jordan (Jordanian Dinar)': 'JOD',
    'Japan (Japanese Yen)': 'JPY',
    'Kenya (Kenyan Shilling)': 'KES',
    'Kyrgyzstan (Kyrgyzstani Som)': 'KGS',
    'Cambodia (Cambodian Riel)': 'KHR',
    'Kiribati (Kiribati Dollar)': 'KID',
    'Comoros (Comorian Franc)': 'KMF',
    'South Korea (South Korean Won)': 'KRW',
    'Kuwait (Kuwaiti Dinar)': 'KWD',
    'Cayman Islands (Cayman Islands Dollar)': 'KYD',
    'Kazakhstan (Kazakhstani Tenge)': 'KZT',
    'Laos (Lao Kip)': 'LAK',
    'Lebanon (Lebanese Pound)': 'LBP',
    'Sri Lanka (Sri Lanka Rupee)': 'LKR',
    'Liberia (Liberian Dollar)': 'LRD',
    'Lesotho (Lesotho Loti)': 'LSL',
    'Libya (Libyan Dinar)': 'LYD',
    'Morocco (Moroccan Dirham)': 'MAD',
    'Moldova (Moldovan Leu)': 'MDL',
    'Madagascar (Malagasy Ariary)': 'MGA',
    'North Macedonia (Macedonian Denar)': 'MKD',
    'Myanmar (Burmese Kyat)': 'MMK',
    'Mongolia (Mongolian Tögrög)': 'MNT',
    'Macau (Macanese Pataca)': 'MOP',
    'Mauritania (Mauritanian Ouguiya)': 'MRU',
    'Mauritius (Mauritian Rupee)': 'MUR',
    'Maldives (Maldivian Rufiyaa)': 'MVR',
    'Malawi (Malawian Kwacha)': 'MWK',
    'Mexico (Mexican Peso)': 'MXN',
    'Malaysia (Malaysian Ringgit)': 'MYR',
    'Mozambique (Mozambican Metical)': 'MZN',
    'Namibia (Namibian Dollar)': 'NAD',
    'Nigeria (Nigerian Naira)': 'NGN',
    'Nicaragua (Nicaraguan Córdoba)': 'NIO',
    'Norway (Norwegian Krone)': 'NOK',
    'Nepal (Nepalese Rupee)': 'NPR',
    'New Zealand (New Zealand Dollar)': 'NZD',
    'Oman (Omani Rial)': 'OMR',
    'Panama (Panamanian Balboa)': 'PAB',
    'Peru (Peruvian Sol)': 'PEN',
    'Papua New Guinea (Papua New Guinean Kina)': 'PGK',
    'Philippines (Philippine Peso)': 'PHP',
    'Pakistan (Pakistani Rupee)': 'PKR',
    'Poland (Polish Złoty)': 'PLN',
    'Paraguay (Paraguayan Guaraní)': 'PYG',
    'Qatar (Qatari Riyal)': 'QAR',
    'Romania (Romanian Leu)': 'RON',
    'Serbia (Serbian Dinar)': 'RSD',
    'Russia (Russian Ruble)': 'RUB',
    'Rwanda (Rwandan Franc)': 'RWF',
    'Saudi Arabia (Saudi Riyal)': 'SAR',
    'Solomon Islands (Solomon Islands Dollar)': 'SBD',
    'Seychelles (Seychellois Rupee)': 'SCR',
    'Sudan (Sudanese Pound)': 'SDG',
    'Sweden (Swedish Krona)': 'SEK',
    'Singapore (Singapore Dollar)': 'SGD',
    'Saint Helena (Saint Helena Pound)': 'SHP',
    'Sierra Leone (Sierra Leonean Leone)': 'SLE',
    'Somalia (Somali Shilling)': 'SOS',
    'Suriname (Surinamese Dollar)': 'SRD',
    'South Sudan (South Sudanese Pound)': 'SSP',
    'São Tomé and Príncipe (São Tomé and Príncipe Dobra)': 'STN',
    'Syria (Syrian Pound)': 'SYP',
    'Eswatini (Eswatini Lilangeni)': 'SZL',
    'Thailand (Thai Baht)': 'THB',
    'Tajikistan (Tajikistani Somoni)': 'TJS',
    'Turkmenistan (Turkmenistan Manat)': 'TMT',
    'Tunisia (Tunisian Dinar)': 'TND',
    'Tonga (Tongan Paʻanga)': 'TOP',
    'Turkey (Turkish Lira)': 'TRY',
    'Trinidad and Tobago (Trinidad and Tobago Dollar)': 'TTD',
    'Tuvalu (Tuvaluan Dollar)': 'TVD',
    'Taiwan (New Taiwan Dollar)': 'TWD',
    'Tanzania (Tanzanian Shilling)': 'TZS',
    'Ukraine (Ukrainian Hryvnia)': 'UAH',
    'Uganda (Ugandan Shilling)': 'UGX',
    'United States (United States Dollar)': 'USD',
    'Uruguay (Uruguayan Peso)': 'UYU',
    "Uzbekistan (Uzbekistani So'm)": 'UZS',
    'Venezuela (Venezuelan Bolívar Soberano)': 'VES',
    'Vietnam (Vietnamese Đồng)': 'VND',
    'Vanuatu (Vanuatu Vatu)': 'VUV',
    'Samoa (Samoan Tālā)': 'WST',
    'CEMAC (Central African CFA Franc)': 'XAF',
    'Organisation of Eastern Caribbean States (East Caribbean Dollar)': 'XCD',
    'International Monetary Fund (Special Drawing Rights)': 'XDR',
    'CFA (West African CFA franc)': 'XOF',
    'Collectivités d\'Outre-Mer (CFP Franc)': 'XPF',
    'Yemen (Yemeni Rial)': 'YER',
    'South Africa (South African Rand)': 'ZAR',
    'Zambia (Zambian Kwacha)': 'ZMW',
    'Zimbabwe (Zimbabwean Dollar)': 'ZWL'
}

currency_list=['Afghanistan (Afghan Afghani)',
 'Albania (Albanian Lek)',
 'Algeria (Algerian Dinar)',
 'Angola (Angolan Kwanza)',
 'Argentina (Argentine Peso)',
 'Armenia (Armenian Dram)',
 'Aruba (Aruban Florin)',
 'Australia (Australian Dollar)',
 'Azerbaijan (Azerbaijani Manat)',
 'Bahamas (Bahamian Dollar)',
 'Bahrain (Bahraini Dinar)',
 'Bangladesh (Bangladeshi Taka)',
 'Barbados (Barbados Dollar)',
 'Belarus (Belarusian Ruble)',
 'Belize (Belize Dollar)',
 'Bermuda (Bermudian Dollar)',
 'Bhutan (Bhutanese Ngultrum)',
 'Bolivia (Bolivian Boliviano)',
 'Bosnia and Herzegovina (Bosnia and Herzegovina Mark)',
 'Botswana (Botswana Pula)',
 'Brazil (Brazilian Real)',
 'Brunei (Brunei Dollar)',
 'Bulgaria (Bulgarian Lev)',
 'Burundi (Burundian Franc)',
 'CEMAC (Central African CFA Franc)',
 'CFA (West African CFA franc)',
 'Cambodia (Cambodian Riel)',
 'Canada (Canadian Dollar)',
 'Cape Verde (Cape Verdean Escudo)',
 'Cayman Islands (Cayman Islands Dollar)',
 'Chile (Chilean Peso)',
 'China (Chinese Renminbi)',
 "Collectivités d'Outre-Mer (CFP Franc)",
 'Colombia (Colombian Peso)',
 'Comoros (Comorian Franc)',
 'Costa Rica (Costa Rican Colon)',
 'Croatia (Croatian Kuna)',
 'Cuba (Cuban Peso)',
 'Czech Republic (Czech Koruna)',
 'Democratic Republic of the Congo (Congolese Franc)',
 'Denmark (Danish Krone)',
 'Djibouti (Djiboutian Franc)',
 'Dominican Republic (Dominican Peso)',
 'Egypt (Egyptian Pound)',
 'Eritrea (Eritrean Nakfa)',
 'Eswatini (Eswatini Lilangeni)',
 'Ethiopia (Ethiopian Birr)',
 'European Union (Euro)',
 'Falkland Islands (Falkland Islands Pound)',
 'Faroe Islands (Faroese Króna)',
 'Fiji (Fiji Dollar)',
 'Georgia (Georgian Lari)',
 'Ghana (Ghanaian Cedi)',
 'Gibraltar (Gibraltar Pound)',
 'Guatemala (Guatemalan Quetzal)',
 'Guernsey (Guernsey Pound)',
 'Guinea (Guinean Franc)',
 'Guyana (Guyanese Dollar)',
 'Haiti (Haitian Gourde)',
 'Honduras (Honduran Lempira)',
 'Hong Kong (Hong Kong Dollar)',
 'Hungary (Hungarian Forint)',
 'Iceland (Icelandic Króna)',
 'India (Indian Rupee)',
 'Indonesia (Indonesian Rupiah)',
 'International Monetary Fund (Special Drawing Rights)',
 'Iran (Iranian Rial)',
 'Iraq (Iraqi Dinar)',
 'Isle of Man (Manx Pound)',
 'Israel (Israeli New Shekel)',
 'Jamaica (Jamaican Dollar)',
 'Japan (Japanese Yen)',
 'Jersey (Jersey Pound)',
 'Jordan (Jordanian Dinar)',
 'Kazakhstan (Kazakhstani Tenge)',
 'Kenya (Kenyan Shilling)',
 'Kiribati (Kiribati Dollar)',
 'Kuwait (Kuwaiti Dinar)',
 'Kyrgyzstan (Kyrgyzstani Som)',
 'Laos (Lao Kip)',
 'Lebanon (Lebanese Pound)',
 'Lesotho (Lesotho Loti)',
 'Liberia (Liberian Dollar)',
 'Libya (Libyan Dinar)',
 'Macau (Macanese Pataca)',
 'Madagascar (Malagasy Ariary)',
 'Malawi (Malawian Kwacha)',
 'Malaysia (Malaysian Ringgit)',
 'Maldives (Maldivian Rufiyaa)',
 'Mauritania (Mauritanian Ouguiya)',
 'Mauritius (Mauritian Rupee)',
 'Mexico (Mexican Peso)',
 'Moldova (Moldovan Leu)',
 'Mongolia (Mongolian Tögrög)',
 'Morocco (Moroccan Dirham)',
 'Mozambique (Mozambican Metical)',
 'Myanmar (Burmese Kyat)',
 'Namibia (Namibian Dollar)',
 'Nepal (Nepalese Rupee)',
 'Netherlands Antilles (Netherlands Antillian Guilder)',
 'New Zealand (New Zealand Dollar)',
 'Nicaragua (Nicaraguan Córdoba)',
 'Nigeria (Nigerian Naira)',
 'North Macedonia (Macedonian Denar)',
 'Norway (Norwegian Krone)',
 'Oman (Omani Rial)',
 'Organisation of Eastern Caribbean States (East Caribbean Dollar)',
 'Pakistan (Pakistani Rupee)',
 'Panama (Panamanian Balboa)',
 'Papua New Guinea (Papua New Guinean Kina)',
 'Paraguay (Paraguayan Guaraní)',
 'Peru (Peruvian Sol)',
 'Philippines (Philippine Peso)',
 'Poland (Polish Złoty)',
 'Qatar (Qatari Riyal)',
 'Romania (Romanian Leu)',
 'Russia (Russian Ruble)',
 'Rwanda (Rwandan Franc)',
 'Saint Helena (Saint Helena Pound)',
 'Samoa (Samoan Tālā)',
 'Saudi Arabia (Saudi Riyal)',
 'Serbia (Serbian Dinar)',
 'Seychelles (Seychellois Rupee)',
 'Sierra Leone (Sierra Leonean Leone)',
 'Singapore (Singapore Dollar)',
 'Solomon Islands (Solomon Islands Dollar)',
 'Somalia (Somali Shilling)',
 'South Africa (South African Rand)',
 'South Korea (South Korean Won)',
 'South Sudan (South Sudanese Pound)',
 'Sri Lanka (Sri Lanka Rupee)',
 'Sudan (Sudanese Pound)',
 'Suriname (Surinamese Dollar)',
 'Sweden (Swedish Krona)',
 'Switzerland (Swiss Franc)',
 'Syria (Syrian Pound)',
 'São Tomé and Príncipe (São Tomé and Príncipe Dobra)',
 'Taiwan (New Taiwan Dollar)',
 'Tajikistan (Tajikistani Somoni)',
 'Tanzania (Tanzanian Shilling)',
 'Thailand (Thai Baht)',
 'The Gambia (Gambian Dalasi)',
 'Tonga (Tongan Paʻanga)',
 'Trinidad and Tobago (Trinidad and Tobago Dollar)',
 'Tunisia (Tunisian Dinar)',
 'Turkey (Turkish Lira)',
 'Turkmenistan (Turkmenistan Manat)',
 'Tuvalu (Tuvaluan Dollar)',
 'Uganda (Ugandan Shilling)',
 'Ukraine (Ukrainian Hryvnia)',
 'United Arab Emirates (UAE Dirham)',
 'United Kingdom (Pound Sterling)',
 'United States (United States Dollar)',
 'Uruguay (Uruguayan Peso)',
 "Uzbekistan (Uzbekistani So'm)",
 'Vanuatu (Vanuatu Vatu)',
 'Venezuela (Venezuelan Bolívar Soberano)',
 'Vietnam (Vietnamese Đồng)',
 'Yemen (Yemeni Rial)',
 'Zambia (Zambian Kwacha)',
 'Zimbabwe (Zimbabwean Dollar)']

# we need to take a llms
llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash',
                     api_key=api_key)


# we need to consider a tool
@tool
def  get_conversion_factor(base_currency: str, target_currency: str,base_amount: float) -> str:
  """
  Get the converted amount from a base currency to a target currency.
    Inputs: base_currency (e.g., 'INR'), target_currency (e.g., 'USD'), and base_amount (e.g., 100).
    Returns the total converted amount with date info.
  """
  url = f'{exchange_api_url}pair/{base_currency}/{target_currency}'

  response = requests.get(url)
  data = response.json()
  total_amount=data['conversion_rate']*base_amount
  date=data['time_last_update_utc']
  date=date[:-15]
  time_1=time.ctime()
  time_2=time_1[-14:-5]

  return f"{base_amount} {base_currency} = {total_amount:.3f} {target_currency} (as of {time_2} {date})"



# Initialize the Agent
agent_executor = initialize_agent(
    tools=[get_conversion_factor],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    #verbose=True  # shows internal thinking
)


# Input layout
col1, col2 = st.columns(2)

with col1:
    base_currency_option = st.selectbox("From", options=currency_list)
    base_amount = st.number_input("Amount", min_value=0.0, step=1.0)

with col2:
    target_currency_option = st.selectbox("To", options=currency_list)


base_currency = currency_dict[base_currency_option]
target_currency = currency_dict[target_currency_option]

# Query
user_query = f"What is the value of {base_amount} {base_currency} in {target_currency}?"

# Result
if st.button("🔁 Convert"):
    response = agent_executor.invoke({"input": user_query})
    st.markdown(f"<h3 style='text-align: center; font-size: 20px;'>{response['output']}</h3>", unsafe_allow_html=True)
    
